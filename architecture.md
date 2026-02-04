# Backend Job Processing System – Architecture

## Overview
This project implements a simple, production-oriented job processing system
using FastAPI, SQLAlchemy, and a database-backed worker.

The goal is to demonstrate:
- Clear backend layering
- Explicit job lifecycle management
- Failure and retry handling
- Platform-style ownership boundaries


## High-Level Components

- **API (FastAPI)**
  - Accepts job creation requests
  - Exposes job status via REST
  - Delegates all logic to service layer

- **Service Layer (JobService)**
  - Single authority for job lifecycle
  - Enforces valid state transitions
  - Handles retries and failures

- **Repository Layer (JobRepository)**
  - Encapsulates database access
  - No business logic

- **Worker**
  - Runs as a separate process
  - Polls database for PENDING jobs
  - Executes jobs and delegates outcomes to service

- **Database**
  - Stores job state and execution metadata
  - Acts as the coordination point between API and worker


## Job Lifecycle

- PENDING
- → RUNNING
- → COMPLETED
- → FAILED
- → RETRYING → PENDING


Rules:
- COMPLETED and FAILED are terminal
- RETRYING is bounded by max_retries
- All transitions are enforced in the service layer


## Retry Strategy

- Retries are immediate and bounded
- No backoff by design (single-process system)
- Retry decision is centralized in JobService
- Backoff or scheduling can be added later without redesign


## Worker Responsibility

- Worker is intentionally dumb
- It never decides lifecycle transitions
- All state changes go through the service layer
