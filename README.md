# Simforge

Monorepo for a Raidbots-like WoW simulation service.

## Apps
- `apps/web` – Next.js + Tailwind
- `apps/api` – FastAPI
- `apps/worker` – Python RQ worker

## Dev (Docker)
```bash
cd infra/compose
docker compose up --build

