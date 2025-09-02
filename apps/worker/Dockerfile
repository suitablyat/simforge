ARG SIMC_WEEKLY_TAG=1120-2025-09-02-c9cad05

FROM --platform=linux/amd64 simulationcraftorg/simc:latest AS simc_nightly
FROM --platform=linux/amd64 simulationcraftorg/simc:${SIMC_WEEKLY_TAG} AS simc_weekly
FROM --platform=linux/amd64 simulationcraftorg/simc:latest

RUN apk add --no-cache python3 py3-pip py3-virtualenv ca-certificates libstdc++ libgcc

RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m ensurepip
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN mkdir -p /opt/simc/nightly /opt/simc/weekly \
 && cp -a /app/SimulationCraft/. /opt/simc/nightly/ \
 && ln -sf /opt/simc/nightly/simc /usr/local/bin/simc
COPY --from=simc_weekly /app/SimulationCraft /opt/simc/weekly

WORKDIR /app
COPY apps/worker/requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt
COPY apps/worker/ ./

ENTRYPOINT ["python", "-m", "worker.main"]
