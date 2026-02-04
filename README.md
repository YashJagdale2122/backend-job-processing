# Backend Job Processing System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)
![Architecture](https://img.shields.io/badge/Architecture-Layered-informational)
![Status](https://img.shields.io/badge/Status-Actively%20Maintained-brightgreen)

A production-oriented backend system for **asynchronous job processing**, built with **FastAPI** and **SQLAlchemy**.
Designed to demonstrate **backend system design**, **job lifecycle management**, and **clean architecture patterns** — without unnecessary ML complexity.


## Problem Statement

Modern backend systems often need to process **long-running or asynchronous tasks** such as:

* Video processing
* Email sending
* Data pipelines
* Background computations

Handling these tasks synchronously blocks APIs, reduces throughput, and hurts reliability.


## Solution Overview

This project implements a **job-based backend processing system** where:

* Jobs are created via APIs
* Each job has a well-defined lifecycle
* Jobs can retry on failure
* State transitions are explicit and controlled
* The architecture cleanly separates concerns

The system is intentionally **framework-light** and **queue-agnostic**, making it easy to extend with real workers (Celery, Kafka, RabbitMQ, etc.).


## Architecture

### High-Level Flow

```
Client
  ↓
FastAPI (Routes)
  ↓
Service Layer (Business Logic)
  ↓
Repository Layer (DB Access)
  ↓
Database (Jobs Table)
```

### Core Layers

* **API Layer**

  * Exposes job creation & status APIs
  * No business logic

* **Service Layer**

  * Controls job lifecycle
  * Handles retries and state transitions

* **Repository Layer**

  * Database persistence using SQLAlchemy
  * No business rules

* **Domain Layer**

  * Enums and domain concepts (JobStatus, JobType)

* **Infrastructure Layer**

  * Database models
  * DB initialization
  * (Worker extension-ready)


## Job Lifecycle

Each job moves through controlled states:

```
PENDING → RUNNING → COMPLETED
            ↓
         FAILED
            ↓
         RETRYING → PENDING
```

Supported states:

* `PENDING`
* `RUNNING`
* `COMPLETED`
* `FAILED`
* `RETRYING`

Retry logic is handled at the **service layer**, not the API.


## Key Features

* Clean modular architecture
* Explicit job lifecycle management
* Retry & failure handling
* Database-backed job state
* Idempotent DB initialization
* Easily extendable to real worker queues
* Interview-friendly design (no magic)


## Tech Stack

* **Backend**: FastAPI
* **ORM**: SQLAlchemy
* **Database**: SQLite (Postgres-ready)
* **Language**: Python 3.10+
* **Architecture**: Layered / Domain-driven


## How to Run Locally

### Start the API
```bash
uvicorn app.main:app --reload

Start the Worker (separate terminal)

python -m app.worker.job_worker
```


## API Endpoints

### Create Job

```http
POST /jobs
```

**Request**

```json
{
  "payload": {
    "task": "example",
    "value": 42
  }
}
```

**Response**

```json
{
  "id": "uuid",
  "status": "PENDING",
  "retries": 0,
  "result": null,
  "last_error": null
}
```


### Get Job Status

```http
GET /jobs/{job_id}
```

**Response**

```json
{
  "id": "uuid",
  "status": "COMPLETED",
  "retries": 1,
  "result": {
    "output": "success"
  },
  "last_error": null
}
```


## Testing (Planned / Extendable)

* Unit tests for service layer
* Repository tests with isolated DB
* API contract tests

(Structure is already designed to support this cleanly.)


## Future Improvements

* Multiple worker processes (horizontal scaling)
* Queue integration (Redis / RabbitMQ / Kafka)
* Rate limiting per job type
* Job scheduling & priorities
* Observability (metrics, logs)
* Distributed execution
