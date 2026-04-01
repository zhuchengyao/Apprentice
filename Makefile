.PHONY: dev dev-frontend dev-backend infra migrate test

# Start all infrastructure (Postgres + Redis)
infra:
	docker compose up -d

# Stop infrastructure
infra-down:
	docker compose down

# Run database migrations
migrate:
	cd backend && python -m alembic upgrade head

# Start backend dev server
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

# Start frontend dev server
dev-frontend:
	cd frontend && pnpm dev

# Start everything (run in separate terminals)
dev:
	@echo "Run in separate terminals:"
	@echo "  make infra"
	@echo "  make dev-backend"
	@echo "  make dev-frontend"

# Run backend tests
test:
	cd backend && python -m pytest -v

# Create a new migration
migration:
	cd backend && python -m alembic revision --autogenerate -m "$(msg)"
