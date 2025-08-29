from fastapi import FastAPI
from pydantic import BaseModel
import os
import redis
from rq import Queue
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Simforge API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HelloReq(BaseModel):
    name: str

@app.get("/health")
def health(): return {"ok": True, "service": "api"}

@app.post("/enqueue/hello")
def enqueue_hello(body: HelloReq):
    r = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
    q = Queue("default", connection=r)
    job = q.enqueue("worker.tasks.hello", body.name)
    return {"job_id": job.get_id()}
