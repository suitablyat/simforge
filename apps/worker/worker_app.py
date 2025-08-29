import os
from celery import Celery

broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
app = Celery("simforge", broker=broker_url, backend=broker_url)

@app.task
def ping():
    return "pong"