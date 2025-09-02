from fastapi import FastAPI
from .routers import jobs

app = FastAPI(title="Simforge API", version="0.0.1")

@app.get("/health", tags=["meta"])
def health():
    return {"ok": True}

app.include_router(jobs.router)
