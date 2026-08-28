from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.config.config import settings

pwd_context: CryptContext = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security_bearer: HTTPBearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    """
    return str(pwd_context.hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored hash.
    """
    return bool(pwd_context.verify(plain_password, hashed_password))


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user_payload(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer)
) -> Dict[str, Any]:
    """
    Validates JWT credentials with behavior dependent on DEBUG mode:
    - If DEBUG=True: Allows mock dev tokens ('dev-mock-token' / 'dev-admin-token') or dev bypass fallback.
    - If DEBUG=False: Strictly enforces valid JWT bearer token expiration, signature, and claims.
    """
    token = credentials.credentials if credentials else None

    # Handle DEBUG=True dev authentication modes
    if settings.DEBUG:
        if token in ("dev-mock-token", "dev-admin-token", "mock-token"):
            return {
                "sub": "1",
                "user_id": 1,
                "username": "debug_admin",
                "email": "admin@microshop.dev",
                "is_admin": True
            }

    if not token:
        if settings.DEBUG:
            # In DEBUG mode, if no token provided, yield a default dev user
            return {
                "sub": "1",
                "user_id": 1,
                "username": "debug_admin",
                "email": "admin@microshop.dev",
                "is_admin": True
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            if settings.DEBUG:
                return {"sub": "1", "user_id": 1, "username": "debug_admin", "email": "admin@microshop.dev", "is_admin": True}
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload["user_id"] = int(user_id) if str(user_id).isdigit() else user_id
        return payload
    except jwt.PyJWTError as e:
        if settings.DEBUG:
            return {"sub": "1", "user_id": 1, "username": "debug_admin", "email": "admin@microshop.dev", "is_admin": True}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_admin_user_payload(
    payload: Dict[str, Any] = Depends(get_current_user_payload)
) -> Dict[str, Any]:
    """
    Enforces admin privileges on token payload.
    """
    if not payload.get("is_admin", False):
        if not settings.DEBUG:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required."
            )
    return payload
