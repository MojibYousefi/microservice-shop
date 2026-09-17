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

## Running the project

The examples below use `/home/yasin/Desktop/microshop` as the checkout path; replace it with your own absolute path if needed. Run Make commands from the repository root:

```bash
cd /home/yasin/Desktop/microshop
make help
```

Choose **one backend mode** at a time: local Python processes or Docker development. Both use ports 8000, 8001, and 8002, so stop the other mode first.

### 1. Local backend (without Docker)

Requirements: Python 3.11+, `uv`, and GNU Make. SQLite is included through the Python dependencies; a PostgreSQL server is not required for this mode.

```bash
cd /home/yasin/Desktop/microshop
uv sync --locked
```

Create `/home/yasin/Desktop/microshop/.env` if it does not exist, or update the corresponding values in the existing file without replacing unrelated settings:

```dotenv
DEBUG=True
DATABASE_URL=sqlite+aiosqlite:////home/yasin/Desktop/microshop/microshop.db
REDIS_URL=redis://127.0.0.1:6379/0
AUTH_SERVICE_URL=http://127.0.0.1:8001
CATALOGUE_SERVICE_URL=http://127.0.0.1:8002
```

Use the same private `SECRET_KEY` for all services. Do not commit `.env`. The checked-in `.env.example` mixes a local SQLite URL with Docker hostnames, so it must not be used unchanged for local execution. Shell environment variables override `.env`; remove stale exported values when switching modes.

The current auth/catalogue routes do not use Redis. If you work on code using the shared Redis client, run a local Redis instance at the configured address. The Compose Redis container does not publish port 6379 to the host.

Start each service in a **separate terminal**, with the repository root as the working directory:

```bash
# Terminal 1: auth
cd /home/yasin/Desktop/microshop
uv run uvicorn backend.auth_service.main:app --host 127.0.0.1 --port 8001 --reload
```

```bash
# Terminal 2: catalogue
cd /home/yasin/Desktop/microshop
uv run uvicorn backend.catalogue.main:app --host 127.0.0.1 --port 8002 --reload
```

```bash
# Terminal 3: gateway
cd /home/yasin/Desktop/microshop
uv run uvicorn backend.gateway.main:app --host 127.0.0.1 --port 8000 --reload
```

Wait for auth to finish starting before starting catalogue on a fresh SQLite database. Auth and catalogue create missing tables during startup; this does not migrate existing tables. Stop each process with `Ctrl+C`. The Makefile currently has **no target for starting local Python services**; `make dev` starts Docker, not these processes.

### 2. Development with Docker Compose and Make

Requirements: Docker Engine, the Docker Compose v2 plugin (`docker compose`), and GNU Make. Host Python/`uv` is not needed to start this stack.

If switching from local mode, update `/home/yasin/Desktop/microshop/.env` for the Docker network:

```dotenv
DEBUG=True
POSTGRES_USER=micro_user
POSTGRES_PASSWORD=micro_pass
POSTGRES_DB=microshop_db
DATABASE_URL=postgresql+asyncpg://micro_user:micro_pass@postgres:5432/microshop_db
REDIS_URL=redis://redis:6379/0
AUTH_SERVICE_URL=http://auth-service:8001
CATALOGUE_SERVICE_URL=http://catalogue-service:8002
```

These database credentials are for local development only. If you change them, keep `DATABASE_URL` consistent with `POSTGRES_*`; changing environment values does not reset credentials in an existing PostgreSQL volume. Compose reads shell variables and `.env` for interpolation, so do not leave a local SQLite URL or localhost Redis URL active. Inside a container, `localhost` refers to that container, not the host or another service.

```bash
cd /home/yasin/Desktop/microshop
make dev
```

`make dev` builds images and starts the stack **in the foreground**, showing logs. Despite its current help description, it does not use `-d`. To run in the background instead:

```bash
make dev-d
make ps
make logs SERVICE=catalogue-service
```

The stack contains gateway, auth, catalogue, PostgreSQL, and Redis. It does **not** start the React/Vite frontend. The Make targets select `/home/yasin/Desktop/microshop/deployments/docker-compose.yml`; an equivalent foreground command is:

```bash
docker compose -f /home/yasin/Desktop/microshop/deployments/docker-compose.yml up --build
```

The development stack currently has **no source bind mounts or automatic reload**. After Python code changes, run `make dev-d` again to rebuild, or rebuild only the changed service:

```bash
docker compose -f /home/yasin/Desktop/microshop/deployments/docker-compose.yml up -d --build catalogue-service
```

Stop and remove development containers/networks with:

```bash
make down-dev
```

Named PostgreSQL/Redis volumes are retained. Do not add `--volumes`/`-v` unless you intentionally want to delete stored data. The development configuration publishes service ports and enables debug authentication; use it only in a trusted development environment, not on a public server.

### Service URLs (local or Docker development)

| Service | Swagger UI | Health check |
| --- | --- | --- |
| Gateway | http://localhost:8000/docs | http://localhost:8000/health |
| Auth | http://localhost:8001/docs | http://localhost:8001/health |
| Catalogue (front and admin) | http://localhost:8002/docs | http://localhost:8002/health |

The gateway forwards `/api/v1/auth` and `/api/v1/catalogue` requests, but its Swagger UI does not aggregate the microservices' schemas. Use each service's own docs for its full API. PostgreSQL and Redis ports are not exposed by the development Compose file.
### Make command reference

| Command | Purpose |
| --- | --- |
| `make help` | List available targets. |
| `make dev` / `make up-dev` | Build and start development containers in the foreground. |
| `make dev-d` | Build and start development containers in the background. |
| `make down-dev` | Remove development containers/networks, retaining volumes. |
| `make build` | Build development images without starting services. |
| `make ps` | Show development containers. |
| `make logs` | Follow all development logs; use `SERVICE=catalogue-service` to select one. |
| `make migrate-up` | Run Alembic upgrade to head on the host using the configured database. |
| `make migrate-init` | Generate a migration for model changes; review it before applying. |
| `make migrate-down` | Downgrade one migration; may remove data. |
| `make test` | Run the Python test suite on the host using `uv`. |
| `make prod` / `make up-prod` | Build and start production Compose in the background. |
| `make down-prod` | Remove production containers/networks, retaining volumes. |
| `make clean` | Delete Python caches, the local virtual environment, and `microshop.db`. **Destructive: not a stop command.** |

Migration and test targets run on the **host**, not inside Docker. A hostname such as `postgres` is not reachable from the host, and the Compose database does not expose a host port. Verify `DATABASE_URL` before running database commands. Do not run `migrate-init` on every startup or blindly apply initial migrations over tables already created by application startup.

For tests without touching the development database, override the URL explicitly:

```bash
cd /home/yasin/Desktop/microshop
DEBUG=True DATABASE_URL='sqlite+aiosqlite:///:memory:' make test
```

### Frontend (separate from either backend mode)

Use a Node.js version supported by Vite 8 (Node 20.19+ or 22.12+). Install and start the frontend from its own directory:

```bash
cd /home/yasin/Desktop/microshop/frontend
npm ci
npm run dev
```

Open the URL printed by Vite (normally http://localhost:5173). There is no Vite API proxy configured currently; backend API requests should target the gateway at http://localhost:8000. The gateway's `/shop` static mount is not a replacement for running the React/Vite development server.

### Production distinction

`make prod` uses `/home/yasin/Desktop/microshop/deployments/docker-compose.prod.yml`, sets `DEBUG=False`, and exposes only gateway port 8000. Direct auth/catalogue docs on ports 8001/8002 are not published in this mode.

Before deployment, configure private `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, and `SECRET_KEY` values; the checked-in defaults are examples, not production credentials. Stop the development stack first to avoid port and Compose-project conflicts. Do not treat `make prod` alone as a complete production hardening/deployment procedure.

```bash
cd /home/yasin/Desktop/microshop
make prod
# Stop the production stack when needed:
make down-prod
```

`make logs` and `make ps` select development Compose. For production logs/status, use the production file explicitly:

```bash
docker compose -f /home/yasin/Desktop/microshop/deployments/docker-compose.prod.yml logs -f
docker compose -f /home/yasin/Desktop/microshop/deployments/docker-compose.prod.yml ps
```
