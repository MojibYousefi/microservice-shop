.PHONY: help dev down-dev prod down-prod build logs ps migrate-init migrate-up migrate-down test clean

COMPOSE_DEV = deployments/docker-compose.yml
COMPOSE_PROD = deployments/docker-compose.prod.yml

help: ## Show list of available Make commands
	@echo "======================================================================"
	@echo "MicroShop Microservices Platform - Makefile Commands"
	@echo "======================================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

dev: ## Run development environment in detached mode (Docker Compose)
	docker compose -f $(COMPOSE_DEV) up -d --build

up-dev: dev ## Alias for dev

down-dev: ## Stop and remove development environment containers and networks
	docker compose -f $(COMPOSE_DEV) down

prod: ## Run production environment in detached mode
	docker compose -f $(COMPOSE_PROD) up -d --build

up-prod: prod ## Alias for prod

down-prod: ## Stop and remove production environment containers
	docker compose -f $(COMPOSE_PROD) down

build: ## Build or rebuild service images
	docker compose -f $(COMPOSE_DEV) build

logs: ## View container logs (optional: make logs SERVICE=auth-service)
	docker compose -f $(COMPOSE_DEV) logs -f $(SERVICE)

ps: ## List running containers
	docker compose -f $(COMPOSE_DEV) ps

migrate-init: ## Generate automatic Alembic migration revision
	PYTHONPATH=. uv run alembic revision --autogenerate -m "auto_migration"

migrate-up: ## Apply database migrations to head
	PYTHONPATH=. uv run alembic upgrade head

migrate-down: ## Revert last applied database migration
	PYTHONPATH=. uv run alembic downgrade -1

test: ## Run pytest test suite with uv
	PYTHONPATH=. uv run pytest tests/

clean: ## Remove temporary python artifacts and build caches
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .venv microshop.db
