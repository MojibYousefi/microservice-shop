import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.config.config import settings
from backend.config.database import init_db, get_async_session
from backend.auth_service.models import User, UserCreate, UserRead, UserLogin, Token
from backend.config.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_payload
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Async database initialization
    await init_db()
    yield


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Auth Service",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "auth_service", "debug": settings.DEBUG}


@app.post("/api/v1/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    # Check if username or email already exists asynchronously
    stmt_username = select(User).where(User.username == user_in.username)
    res_username = await db.exec(stmt_username)
    if res_username.first():
        raise HTTPException(status_code=400, detail="Username already registered.")

    stmt_email = select(User).where(User.email == user_in.email)
    res_email = await db.exec(stmt_email)
    if res_email.first():
        raise HTTPException(status_code=400, detail="Email already registered.")

    db_user = User(
        email=user_in.email,
        username=user_in.username,
        password=hash_password(user_in.password),
        full_name=user_in.full_name,
        is_admin=user_in.is_admin
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.post("/api/v1/auth/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(User).where(
        (User.username == credentials.username_or_email) |
        (User.email == credentials.username_or_email)
    )
    res = await db.exec(stmt)
    user = res.first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password."
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account.")

    access_token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin
    })

    return Token(
        access_token=access_token,
        user=UserRead(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_admin=user.is_admin
        )
    )


@app.get("/api/v1/auth/me", response_model=UserRead)
async def get_me(
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_async_session)
):
    user_id = payload.get("user_id")
    if user_id:
        stmt = select(User).where(User.id == user_id)
        res = await db.exec(stmt)
        user = res.first()
        if user:
            return UserRead(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_admin=user.is_admin
            )

    # If user not found in DB but in DEBUG mode, return mock user
    if settings.DEBUG:
        return UserRead(
            id=1,
            email=payload.get("email", "admin@microshop.dev"),
            username=payload.get("username", "debug_admin"),
            full_name="Debug Admin User",
            is_active=True,
            is_admin=True
        )

    raise HTTPException(status_code=404, detail="User not found.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.AUTH_SERVICE_PORT)
