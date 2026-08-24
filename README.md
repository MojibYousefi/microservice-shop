# MicroShop - Asynchronous Microservices Architecture

A production-grade, fully asynchronous microservices platform built with Python, FastAPI, SQLModel, Pydantic, Redis, PostgreSQL/SQLite, `uv`, and Docker.

---

## 🏛️ Architecture Overview

MicroShop consists of an **XHTTP API Gateway** and microservices supported by shared configuration modules:

```text
                           ┌─────────────────────────┐
                           │   XHTTP API Gateway     │
                           └────────────┬────────────┘
                                        │
                                        ▼ (XHTTP Forwarding)
                           ┌─────────────────────────┐
                           │  Auth Microservice      │
                           │  Port: 8001             │
                           └────────────┬────────────┘
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │ PostgreSQL / SQLite DB  │
                           └─────────────────────────┘
                                        ▲
                           ┌────────────┴────────────┐
                           │     Async Redis         │
                           └─────────────────────────┘
```

### Folder Structure
- `backend/config/`: System-wide settings (`config.py`), async database lifecycle (`database.py`), async Redis manager (`redis.py`), JWT security (`security.py`).
- `backend/auth_service/`: User authentication microservice containing app-specific models (`models.py`), endpoints (`main.py`), and Dockerfile.
- `backend/gateway/`: XHTTP reverse proxy router (`main.py`) routing requests inside internal Docker network.

---

## ⚡ Key Technical Features

1. **Fully Asynchronous Architecture**:
   - Asynchronous Database initialization (`init_db`)
   - Asynchronous Database sessions (`AsyncSession`, `async_sessionmaker`)
   - Asynchronous Redis operations (`redis.asyncio`)
   - Asynchronous FastAPI endpoints and Gateway proxying

2. **App-Scoped Models**:
   - Each app maintains its own models (e.g. `backend/auth_service/models.py`).

3. **`uv` Package Management**:
   - Project dependencies managed via `uv` and `pyproject.toml`.

4. **Environment-Driven Configuration**:
   - Supports both PostgreSQL (`postgresql+asyncpg`) for Production and SQLite (`sqlite+aiosqlite`) for local dev.
   - `DEBUG=True` enables mock dev tokens and testing flexibility.
   - `DEBUG=False` enforces strict JWT verification.

---

## 🐳 Docker Commands

### 1. Local Development
```bash
docker compose up --build
```

### 2. Production Deployment
```bash
docker compose -f docker-compose.prod.yml up -d --build
```
