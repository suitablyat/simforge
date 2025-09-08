Excellent – below is a **fully restructured, cleaned-up version of the `AGENT_REQUIREMENTS.md`** file, written clearly and concisely for someone starting the project from scratch with **no prior context**.

All unnecessary background, comparisons, history, and post-MVP decisions have been removed. This version is **strictly focused on building the MVP**, and assumes the reader is a developer or technical contributor who will implement the system based on this document.

---

# REQUIREMENTS.md

## 1. Overview

This project is a web application that allows users to run **SimulationCraft (SimC)** simulations for World of Warcraft characters and view the results. The application provides a **simple form** to submit a simulation job, runs it in the background, and streams **real-time status updates and logs** to the user.

The application architecture is based on a **frontend–API–worker model**, with Redis for background job processing and PostgreSQL for data storage. All simulations are **anonymous** and there is no monetization or user account system in the MVP.

---

## 2. Features (MVP)

### Required:

* Submit a **Quick Sim** job with SimC input text
* Backend runs the simulation using a pre-installed SimC binary
* User receives **live updates** during job execution via **Server-Sent Events (SSE)**
* On completion, the user can:

  * View the result summary (e.g., DPS)
  * Download result JSON and logs
* All jobs are anonymous and public via an unguessable ID

---

## 3. System Architecture

### 3.1 Components

| Component          | Description                                                                  |
| ------------------ | ---------------------------------------------------------------------------- |
| **Frontend**       | Single Page App (SPA) built with Next.js. Communicates only with the API.    |
| **API Server**     | REST API built with FastAPI. Accepts jobs, streams events, serves artifacts. |
| **Worker**         | Celery-based background job processor that runs SimC jobs.                   |
| **PostgreSQL**     | Stores job metadata and metrics.                                             |
| **Redis**          | Used for task queueing (Celery) and optional event buffering.                |
| **Docker Compose** | Used to run all services locally for development and testing.                |

---

## 4. User Flow

1. User opens the web app and pastes SimC input into a form
2. User selects the SimC channel: `nightly`, `latest`, or `weekly`
3. User submits the job via the API
4. API returns a unique job ID
5. Frontend opens an SSE stream to `/sims/{id}/events`
6. Worker processes the job and emits events (stage changes, logs, errors, final status)
7. After the job completes:

   * User sees DPS summary and can download the result files

---

## 5. SimC Integration

* **SimC Input**: Provided as plain text from the user
* **Binary execution**: The worker runs SimC using the CLI binary mounted at a configurable path
* **Channels**:

  * `nightly`: updated every night
  * `latest`: current build
  * `weekly`: built every Monday at 10:45 PM EST
* **Input handling**:

  * Input is saved to a temp file
  * The SimC binary is executed with that file as input
* **Output**:

  * JSON result is parsed and stored
  * stdout and stderr are captured
* **Failure cases**:

  * Timeouts
  * Invalid input (“Nothing to sim!”)
  * Binary/runtime errors

---

## 6. API Endpoints

| Method | Path                   | Description                         |
| ------ | ---------------------- | ----------------------------------- |
| `GET`  | `/health`              | Health check endpoint               |
| `POST` | `/sims`                | Submit a new simulation job         |
| `GET`  | `/sims/{id}`           | Fetch job status and metadata       |
| `GET`  | `/sims/{id}/artifacts` | List result and log files           |
| `GET`  | `/sims/{id}/log`       | View or download stderr/stdout      |
| `GET`  | `/sims/{id}/events`    | Open an SSE stream for live updates |

---

## 7. Live Event Stream (SSE)

The API provides real-time updates using **Server-Sent Events** via the `/sims/{id}/events` endpoint.

### Format:

Each event contains:

* `event`: event type (string)
* `id`: unique event ID (incrementing per job)
* `data`: JSON payload
* All events include a `trace_id` for logging

### Event Types:

| Event            | Description                                      |
| ---------------- | ------------------------------------------------ |
| `job.accepted`   | Job successfully submitted                       |
| `job.started`    | Worker started the job                           |
| `job.stage`      | Phase marker (e.g., `run_simc`, `parse_results`) |
| `job.progress`   | Optional numeric progress or ETA                 |
| `log.stdout`     | Output from SimC stdout                          |
| `log.stderr`     | Output from SimC stderr                          |
| `artifact.ready` | A new artifact is available                      |
| `job.warning`    | Warning during processing                        |
| `job.error`      | Error occurred during execution                  |
| `job.finished`   | Job is completed (success or failure)            |
| `heartbeat`      | Keep-alive event                                 |

### Behavior:

* Events must be sent in order
* Event stream stays open until job finishes
* After completion, stream remains open for a short time (e.g. 30 minutes) for client reconnect
* Client may reconnect using `Last-Event-ID` header

---

## 8. Database Models

### Table: `sims`

* `id`: UUID (primary key)
* `status`: pending | running | success | failed
* `channel`: nightly | latest | weekly
* `simc_input`: text
* `created_at`, `started_at`, `finished_at`: timestamps
* `trace_id`: string

### Table: `artifacts`

* `id`: UUID
* `sim_id`: foreign key
* `kind`: result\_json | report\_html | stderr | stdout
* `url` or `path`: storage reference
* `size`: in bytes
* `created_at`: timestamp

### Table: `metrics`

* `sim_id`: foreign key
* `wall_time`: seconds
* `iterations`: int
* `dps_mean`, `dps_stddev`: float

---

## 9. Worker (Celery)

* **Queue**: All jobs go through Redis queue
* **Retries**: Up to 2 automatic retries on failure
* **Timeouts**: Each job has a maximum execution time
* **Artifacts**:

  * stdout/stderr are saved to files
  * JSON result is stored and parsed
* **Error Handling**:

  * SimC errors are returned as structured payloads
  * Logs are always available for debugging

---

## 10. Frontend Requirements

* Single Page App using Next.js and TypeScript
* Quick Sim submission form with validation
* Status page that connects to the SSE endpoint and displays:

  * Progress stages
  * Logs (stdout, stderr)
  * Final result summary (e.g. DPS)
* Download links for result and log files
* Fallback polling if SSE fails
* No login or account system

---

## 11. Environment Configuration

All services must be configurable using environment variables:

### Required ENV variables:

* `DATABASE_URL`
* `REDIS_URL`
* `SIMC_CHANNEL`
* `SIMC_BINARY_PATH`
* `NEXT_PUBLIC_API_URL` (for frontend)

---

## 12. Local Development (Docker)

Use Docker Compose to start all services locally:

* PostgreSQL
* Redis
* API
* Worker
* Frontend

Example `make` targets:

* `make dev` — start stack
* `make down` — stop stack
* `make logs` — tail logs
* `make migrate` — apply database migrations

---

## 13. Definition of Done (MVP)

* Job submission via API works
* SSE provides real-time job updates
* SimC job is executed and returns result
* Logs and artifacts are stored and accessible
* Frontend can:
  * Submit jobs
  * Show live progress
  * Display results
* System runs locally with Docker Compose
* No login or monetization features
