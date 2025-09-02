# Simforge

A minimal, modular “Raidbots-like” simulator stack.

This monorepo hosts:
- **API** — FastAPI service (Python 3.11) with PostgreSQL via SQLAlchemy + Alembic
- **Worker** — Celery worker (Python) using Redis
- **Web** — Next.js app for the frontend
- **Infra** — Docker Compose for local development (Postgres + Redis)

> Root path (`/`) intentionally returns **404**. A liveness endpoint is available at **`/health`**.

---

## Table of contents
- [Quick start](#quick-start)
- [Environment variables](#environment-variables)
- [Project structure](#project-structure)
- [API](#api)
  - [Run migrations](#run-migrations)
  - [Healthcheck](#healthcheck)
  - [Smoke tests](#smoke-tests)
- [Web](#web)
- [Worker](#worker)
- [Makefile (optional helpers)](#makefile-optional-helpers)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Quick start

**Prerequisites**
- Docker Desktop / Docker Engine with Docker Compose

**Run**
```bash
# 1) Copy environment file
cp .env.example .env

# 2) Start the full stack (db, redis, api, worker, web)
docker compose up -d --build

# 3) Verify API liveness
curl -s http://localhost:8000/health
````

**Open**

* API docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
* Web app (Next.js dev): [http://localhost:3000](http://localhost:3000)

> The stack starts with hot reload for web and api when using the local bind mounts defined in `docker-compose.yml`.

---

## Environment variables

Set these in `.env` (see `.env.example` for a template):

```env
# API / DB
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/simforge

# Worker / Queue
REDIS_URL=redis://redis:6379/0

# Web
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Notes**

* Use the `postgresql+psycopg://` URL format (SQLAlchemy 2.x, psycopg 3).
* The `db` hostname matches the Compose service name.

---

## Project structure

```
.
├── apps/
│   ├── api/
│   │   ├── app/
│   │   │   ├── api/                 # FastAPI routers
│   │   │   ├── core/                # settings/config
│   │   │   ├── db/                  # SQLAlchemy Base, session, models, Alembic
│   │   │   │   ├── migrations/      # Alembic scripts (env.py, versions/)
│   │   │   │   ├── models/          # SQLAlchemy models (e.g., job.py)
│   │   │   │   ├── base.py
│   │   │   │   └── session.py
│   │   │   └── main.py              # FastAPI app (incl. /health)
│   │   ├── Dockerfile               # API image (prod/dev baseline)
│   │   └── requirements.txt
│   ├── worker/
│   │   └── Dockerfile.dev           # Celery worker image for dev
│   └── web/
│       └── Dockerfile.dev           # Next.js image for dev
├── docker-compose.yml
├── .env.example
└── Makefile
```

---

## API

The API is built with **FastAPI** and uses **PostgreSQL** via **SQLAlchemy**. Database schema is managed by **Alembic** migrations.

### Run migrations

> Always commit your Alembic revisions (the generated files in `app/db/migrations/versions/`). In CI or fresh clones, only `upgrade head` is needed.

Create a migration (autogenerate) and apply it:

```bash
# create new migration from current models
docker compose exec api python -m alembic revision -m "create jobs table" --autogenerate

# apply latest migrations
docker compose exec api python -m alembic upgrade head
```

Useful alternatives:

```bash
# downgrade one step
docker compose exec api python -m alembic downgrade -1

# stamp database to head without applying (rarely needed)
docker compose exec api python -m alembic stamp head
```

### Healthcheck

* Liveness: `GET /health` → `{"status": "ok"}`
* Swagger UI: `GET /docs`
* OpenAPI: `GET /openapi.json`

> The Compose healthcheck pings `http://127.0.0.1:8000/health` **inside** the API container.
> If your base image doesn’t include `wget`, either install it or use the Python-based healthcheck from the Troubleshooting section.

### Smoke tests

Example calls (adjust once you add/expand endpoints):

```bash
# Health
curl -i http://localhost:8000/health

# Example Jobs API (if implemented):
# Create
curl -s -X POST http://localhost:8000/jobs \
  -H 'content-type: application/json' \
  -d '{"note":"hello"}'

# Get by id (replace <uuid>)
curl -s http://localhost:8000/jobs/<uuid>
```

---

## Web

* Next.js dev server runs on port **3000** (Turbopack in dev).
* The app consumes the API using `NEXT_PUBLIC_API_URL` (default `http://localhost:8000` in dev).
* Live reload is enabled via the volume mount in `docker-compose.yml`.

Run in isolation (optional):

```bash
docker compose up -d web
```

---

## Worker

* Celery worker runs against the same codebase and uses Redis (`REDIS_URL`).
* Start automatically with the stack or run standalone:

```bash
docker compose up -d worker
```

---

## Contributing

* Branch naming: `feature/<slug>`, `fix/<slug>`, `chore/<slug>`
* Write PR bodies in **English** and keep them focused:

  * What changed, why, how to test, breaking changes (if any)
* For DB changes:

  * Update models
  * Generate Alembic migration
  * Commit the migration file(s)
  * Include brief run instructions in the PR

