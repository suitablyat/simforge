# Simforge

Monorepo for a Raidbots-like WoW simulation service.

## Apps
- `apps/web` – Next.js + Tailwind
- `apps/api` – FastAPI
- `apps/worker` – Python RQ worker

## Local Development with Docker Compose

**Requirements:** Docker Desktop/Engine + Docker Compose v2

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Start the development environment:

```bash
make dev
# or alternatively:
docker compose up --build
```

3. Verify that services are running:

* Web: [http://localhost:3000](http://localhost:3000)
* API: [http://localhost:8000/healthz](http://localhost:8000/healthz)
* Database: `localhost:5432` (user: `postgres`, password: `postgres`)
* Redis: `localhost:6379`

4. **Hot Reloading**

* Changes in `./api`, `./web`, and `./worker` are reloaded automatically (`uvicorn --reload` / `npm run dev`).
