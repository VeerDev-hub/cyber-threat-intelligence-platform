# Cyber Threat Intelligence Platform

## Overview
This project is a modular SOC-focused platform built with Flask. It ingests security logs, processes them into structured records, computes analytics, and renders a dashboard.

## Current Stack
- Backend: Flask (app factory pattern)
- ORM: SQLAlchemy
- Database: PostgreSQL
- Auth: Flask-Login + Flask-Bcrypt
- Migrations: Flask-Migrate + Alembic
- Dashboard: Jinja templates + Chart.js

## Completed So Far
### 1. Authentication Layer
- User model with `username`, `email`, `password_hash`, `role`, `is_active`
- Registration API
- Unified login route supporting browser form and JSON API payload
- Session-based auth via Flask-Login
- Role guard via decorator (`admin-only` route available)

### 2. Log Ingestion
- Auth-protected ingestion endpoint: `POST /ingest/logs`
- Raw logs persisted to `raw_logs`
- Tracks upload source and user

### 3. ETL / Processing
- Raw logs transformed into `processed_logs`
- Extracted/derived fields:
  - `source_ip`
  - `destination_ip`
  - `destination_port`
  - `attack_type`
  - `severity`
- Raw logs marked as processed after transformation

### 4. Analytics Engine
- Service-layer aggregations:
  - `summary_metrics()`
  - `top_attacker_ips()`
  - `top_target_ports()`
  - `attack_types_distribution()`
- Analytics API routes are protected and return JSON

### 5. Dashboard
- Overview dashboard page
- Severity distribution chart
- Attack type distribution chart

### 6. Database and Migrations
- Users table migration
- Raw and processed logs migration
- PostgreSQL connection configured through `DATABASE_URL`

### 7. Quality and Cleanup
- Duplicate/misplaced route modules removed
- Runtime cache artifacts cleaned
- Dependency list cleaned (`python-dotenv` retained, redundant `dotenv` removed)

## Current Gap Summary
- ML anomaly pipeline not integrated yet
- `processed_logs` missing `anomaly_score` and `risk_level`
- Alerting domain not implemented yet
- API versioning and standardized API error contract were pending
- React SPA and JWT flow not started

## Phase Plan
### Phase 1 (completed)
- Introduce versioned API structure under `/api/v1`
- Route/service split for v1 API handlers
- Request payload validation via schema helpers
- Centralized JSON error handling for API routes
- Standardized v1 response envelope

### Phase 2
- Add ML columns (`anomaly_score`, `risk_level`) + migration
- Refactor ETL for cleaner processing flow

### Phase 3
- Add ML module (`features`, `train`, `inference`, `model loader`)
- Run inference during processing

### Phase 4
- Add alerts table, service, and API

### Phase 5
- Async jobs, observability, and production hardening

### Phase 6
- React SPA + JWT auth integration

## Run
```powershell
.\.venv\Scripts\python run.py
```

## API Baseline
- Existing routes:
  - `/auth/*`
  - `/ingest/*`
  - `/analytics/*`
  - `/dashboard/*`
- New versioned routes:
  - `/api/v1/auth/*`
  - `/api/v1/ingest/*`
  - `/api/v1/analytics/*`

## v1 Response Contract
### Success
```json
{
  "success": true,
  "message": "optional",
  "data": {},
  "meta": {}
}
```

### Error
```json
{
  "success": false,
  "error": {
    "code": "ValidationError",
    "message": "Human-readable message",
    "details": {}
  }
}
```
