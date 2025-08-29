import os
from rq import Worker, Queue
import redis

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
listen = ['default']

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    # Übergib die Connection explizit
    worker = Worker([Queue(name, connection=conn) for name in listen], connection=conn)
    worker.work()

