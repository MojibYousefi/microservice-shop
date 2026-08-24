# MicroShop - Asynchronous Microservices E-Commerce Platform

A production-grade, fully asynchronous microservices e-commerce platform built with Python, FastAPI, SQLModel, Pydantic, Redis, PostgreSQL/SQLite, and Docker.

---

## 🏛️ Architecture Overview

MicroShop consists of 4 decoupled microservices communicates via an asynchronous **XHTTP API Gateway**:

```text
                           ┌─────────────────────────┐
                           │   Frontend / Client     │
                           └────────────┬────────────┘
                                        │
                                        ▼ (HTTP :8000)
                           ┌─────────────────────────┐
                           │   XHTTP API Gateway     │
                           └────┬────────┬────────┬──┘
                                │        │        │
               ┌────────────────┘        │        └────────────────┐
               ▼ (XHTTP Forwarding)      ▼ (XHTTP Forwarding)      ▼ (XHTTP Forwarding)
    ┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
    │  Auth Service      │    │  Product Service   │    │   Order Service    │
    │  Port: 8001        │    │  Port: 8002        │    │   Port: 8003       │
    └──────────┬─────────┘    └──────────┬─────────┘    └──────────┬─────────┘
               │                         │                         │
               └─────────────────────────┼─────────────────────────┘
                                         ▼
                             ┌───────────────────────┐
                             │ PostgreSQL / SQLite   │
                             └───────────────────────┘
                                         ▲
                             ┌───────────┴───────────┐
                             │     Async Redis       │
                             └───────────────────────┘
```

### Microservices Breakdown
1. **API Gateway (`backend/gateway`)**
   - Routes request traffic inside the Docker network.
   - Proxies endpoints (`/api/v1/auth`, `/api/v1/products`, `/api/v1/categories`, `/api/v1/cart`, `/api/v1/orders`).
   - Serves frontend static application.

2. **Auth Service (`backend/auth_service`)**
   - User registration, login, profile management.
   - Generates and verifies JWT tokens.
   - Implements `DEBUG=True` (dev token bypass) and `DEBUG=False` (strict JWT verification) modes.

3. **Product Service (`backend/product_service`)**
   - Manages product catalog and categories.
   - Performs category/product searches and filters.
   - Auto-seeds initial catalog and category data asynchronously on startup if DB is empty.

4. **Order Service (`backend/order_service`)**
   - Shopping cart operations powered by async Redis (`redis.asyncio`).
   - Checkout & Order creation powered by async SQLModel database transactions.
   - Decrements product stock in DB and clears cart in Redis upon checkout.

---

## ⚡ Asynchronous Infrastructure

- **Async Database Engine**: `create_async_engine` using `postgresql+asyncpg` (Production) or `sqlite+aiosqlite` (Local Dev).
- **Async Database Sessions**: `AsyncSession` yielded via `async_sessionmaker`.
- **Async Redis**: `redis.asyncio` client with connection pool.
- **Async Lifecycle & Routing**: Lifespan startup hooks (`lifespan`) for DB tables initialization and Redis shutdown handlers.

---

## 🔒 DEBUG Mode & JWT Behavior

Controlled via environment variable `DEBUG`:

- **`DEBUG=True` (Local / Development)**:
  - Enables mock dev tokens (`dev-mock-token`, `dev-admin-token`).
  - Fallback dev user context when headers are omitted, making API testing seamless.
  - Exposes detailed tracebacks and debug endpoints.

- **`DEBUG=False` (Production)**:
  - Enforces strict JWT verification (expiration, HS256 signature, secret key validation).
  - Production-safe error responses.
  - Requires valid Bearer authorization token for secure endpoints.

---

## 🐳 Docker Deployment Scenarios

### 1. Backend Only
To run all backend microservices, Gateway, PostgreSQL, and Redis:
```bash
docker compose up postgres redis auth-service product-service order-service gateway
```

### 2. Local Development (Backend + Frontend)
To run the full stack locally with PostgreSQL & Redis:
```bash
docker compose up --build
```
Access the application:
- Frontend Shop: `http://localhost:3000`
- API Gateway Health: `http://localhost:8000/health`
- Auth Service: `http://localhost:8001/health`
- Product Service: `http://localhost:8002/health`
- Order Service: `http://localhost:8003/health`

### 3. Production Deployment
To run in production mode with `DEBUG=False` and strict networking:
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

---

## ⚙️ Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `DEBUG` | Toggle debug mode (`True`/`False`) | `True` |
| `DATABASE_URL` | Async DB connection string | `sqlite+aiosqlite:///./microshop.db` |
| `REDIS_URL` | Async Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT Signing key | `super-secret-key-change-in-production` |
| `AUTH_SERVICE_URL` | Internal Auth URL | `http://auth-service:8001` |
| `PRODUCT_SERVICE_URL` | Internal Product URL | `http://product-service:8002` |
| `ORDER_SERVICE_URL` | Internal Order URL | `http://order-service:8003` |
