# Simforge API

This is the backend API for Simforge, built with [FastAPI](https://fastapi.tiangolo.com/).  
It serves as the foundation for submitting and managing simulation jobs.

---

## 🚀 Running Locally

### With Poetry or pip
```bash
cd apps/api
uvicorn app.main:app --reload
````

### With Docker (if `Dockerfile` present)

```bash
docker build -t simforge-api .
docker run -p 8000:8000 simforge-api
```

Or use `make dev` if you're running via `docker-compose`.

---

## ✅ Healthcheck

Check if the API is live:

```
GET /health
→ 200 OK: { "ok": true }
```

---

## 📘 API Documentation

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 🎯 Available Endpoints (M0)

### `POST /jobs`

Creates a new job (stub). Example body:

```json
{
  "note": "simulate rogue burst"
}
```

Returns:

```json
{
  "id": "uuid",
  "status": "queued",
  "note": "simulate rogue burst"
}
```

---

### `GET /jobs/{id}`

Retrieves a previously submitted job by UUID.

---

## 🧪 Running Tests

```bash
cd apps/api
pytest -q
```

---

## 🗒️ Notes

* Job data is stored **in-memory** and will reset on restart.
* Root path `/` returns `404` by design (no landing page).
* This structure will be extended in future milestones with DB, worker queue, etc.
