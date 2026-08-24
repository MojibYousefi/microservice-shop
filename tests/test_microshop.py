import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import select
from backend.config.config import settings
from backend.config.database import init_db, async_session_maker
from backend.auth_service.models import User
from backend.auth_service.main import app as auth_app


@pytest.fixture(autouse=True)
async def setup_test_db():
    await init_db()
    yield


@pytest.mark.asyncio
async def test_async_database_init_and_session():
    """
    Verifies asynchronous database initialization and session querying.
    """
    async with async_session_maker() as session:
        stmt = select(User)
        res = await session.exec(stmt)
        users = res.all()
        assert users is not None


@pytest.mark.asyncio
async def test_auth_service_registration_and_login():
    """
    Verifies Auth Service user registration and JWT token creation.
    """
    transport = ASGITransport(app=auth_app)
    uid = str(uuid.uuid4())[:8]
    username = f"user_{uid}"
    email = f"user_{uid}@example.com"

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Register user
        reg_resp = await ac.post("/api/v1/auth/register", json={
            "email": email,
            "username": username,
            "password": "secretpassword123",
            "full_name": "Test User"
        })
        assert reg_resp.status_code == 201
        data = reg_resp.json()
        assert data["email"] == email

        # Login user
        login_resp = await ac.post("/api/v1/auth/login", json={
            "username_or_email": username,
            "password": "secretpassword123"
        })
        assert login_resp.status_code == 200
        token_data = login_resp.json()
        assert "access_token" in token_data


@pytest.mark.asyncio
async def test_debug_mode_jwt_behavior():
    """
    Verifies DEBUG=True dev token bypass vs DEBUG=False strict token verification.
    """
    # 1. Test DEBUG=True
    settings.DEBUG = True
    transport = ASGITransport(app=auth_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/auth/me", headers={"Authorization": "Bearer dev-mock-token"})
        assert resp.status_code == 200
        assert "id" in resp.json() or "username" in resp.json()

    # 2. Test DEBUG=False
    settings.DEBUG = False
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid-token"})
        assert resp.status_code == 401

    # Reset debug mode
    settings.DEBUG = True
