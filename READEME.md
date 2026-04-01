# Apprentice

AI-powered study companion. Upload a book, and an AI tutor teaches you everything in it — concept by concept, chapter by chapter.

## Quick Start

### Prerequisites
- Node.js 20+, pnpm
- Python 3.11+
- Docker (for Postgres + Redis)

### 1. Start infrastructure
```bash
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
make infra
```

### 2. Run database migrations
```bash
make migrate
```

### 3. Start dev servers (in separate terminals)
```bash
make dev-backend   # FastAPI on :8000
make dev-frontend  # Next.js on :3000
```

Open http://localhost:3000

## Project Structure

```
├── frontend/          Next.js 15 + Tailwind v4 + shadcn/ui + Framer Motion
├── backend/           Python FastAPI + SQLAlchemy + Alembic
├── docker-compose.yml PostgreSQL (pgvector) + Redis
└── Makefile           Dev commands
```

## Tech Stack

| Layer     | Technology                                    |
|-----------|-----------------------------------------------|
| Frontend  | Next.js 15, Tailwind CSS v4, shadcn/ui, Framer Motion, Zustand |
| Backend   | FastAPI, SQLAlchemy 2.0, Alembic              |
| Database  | PostgreSQL 16 + pgvector                      |
| Queue     | Redis + arq                                   |
| AI        | Claude API (Anthropic)                        |
| Parsing   | PyMuPDF, pdfplumber                           |
