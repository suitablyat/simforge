import os
from rq import Worker, Queue, Connection
from redis import Redis
from .settings import settings
from . import jobs  # noqa: F401 ensures import

listen = ["default", "sims"]

def get_connection():
    return Redis.from_url(settings.redis_url)

def main():
    with Connection(get_connection()):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=True)

if __name__ == "__main__":
    main()
