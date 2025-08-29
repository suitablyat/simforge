FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir rq redis pydantic
COPY worker /app/worker
ENV REDIS_URL=redis://redis:6379/0
CMD ["python", "-m", "worker.main"]
