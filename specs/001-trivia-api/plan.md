# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, Pydantic, SQLAlchemy (ORM), SQLite3, Uvicorn (ASGI server)  
**Storage**: SQLite (persistent file-based database per spec assumptions)  
**Testing**: N/A (manual verification only - per constitution)  
**Target Platform**: Linux server (REST API backend)  
**Project Type**: Single project (API-only backend, no frontend)  
**Performance Goals**: API responses <500ms, handle 100+ concurrent user submissions (per spec)  
**Constraints**: Admin authentication via API key in `.env`, OpenAPI 3.0+ compliant, demo-ready with swagger UI, case-insensitive answer matching, timestamp all attempts in ISO 8601 format  
**Scale/Scope**: Single active trivia session at a time, support multiple concurrent users, persistent score tracking across sessions, leaderboard ranking with tie-breaking by earliest score acquisition

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Code Quality First:**
- [x] Code uses clear, self-documenting names (API follows REST conventions, model names are explicit)
- [x] Complex logic has explanatory comments (case-insensitive matching, tie-breaking algorithm)
- [x] No magic numbers (all constants named: MAX_CONCURRENT, SESSION_ID_LENGTH, etc.)
- [x] Functions follow single responsibility principle (separate endpoints for each action)
- [x] Code duplication eliminated (shared models, reusable service layer)
- [x] Error handling is explicit with user-friendly messages (spec defines all error codes)
- [x] No commented-out code (implementation will enforce this)
- [x] Linting/formatting rules configured (will setup black, flake8 in project)

**II. User Experience Consistency:**
- [x] Visual design system defined (JSON response structure consistent across all endpoints)
- [x] Interaction patterns documented and consistent (all endpoints follow REST conventions)
- [x] User feedback mechanisms identified (immediate correctness feedback, HTTP status codes, error messages)
- [x] Navigation flow is intuitive (clear endpoint purposes, logical grouping by resource)
- [x] Terminology is consistent across UI (question, answer, session, attempt, score defined clearly)
- [x] Responsive design strategy defined (API-only, no client-side concerns in scope)
- [x] Accessibility requirements specified (N/A for API, documented error messages aid programmatic access)

**III. Rapid Development for Live Demos:**
- [x] Feature can be demo'd independently (each endpoint callable via curl or Swagger UI)
- [x] No formal testing infrastructure required (manual verification via API docs acceptable)
- [x] Environment configuration externalized (admin API key in .env, no hardcoded values)
- [x] Mock/demo data prepared and realistic (demo script can populate sessions, attempts, leaderboard)
- [x] Demo scenario scripted (defined in quickstart.md)
- [x] Deployment is single-command or automated (Docker+docker-compose or local uvicorn startup)
- [x] Dependencies are minimal and stable (FastAPI, SQLAlchemy, Pydantic are production-ready)
- [x] Quickstart guide will be updated (Phase 1 deliverable)

**IV. OpenAPI-First API Design:**
- [x] FastAPI framework selected for Python backends (REQUIRED per constitution)
- [x] All endpoints have OpenAPI operationId, summary, description (spec provides all details)
- [x] Request/response schemas defined with Pydantic models (will create models for each endpoint)
- [x] Example values included in schema definitions (spec shows JSON examples)
- [x] Error responses documented with proper HTTP status codes (spec lists all error cases)
- [x] OpenAPI spec accessible at /openapi.json (FastAPI auto-generates)
- [x] Interactive API docs (Swagger UI) available (FastAPI auto-generates at /docs)
- [x] Complex parameters documented with constraints (leaderboard pagination, session scope, etc.)

**Constitution Status**: ✅ **PASS - All gates satisfied. Ready for Phase 0.**

## Project Structure

### Documentation (this feature)

```text
specs/001-trivia-api/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (none needed - no unknowns)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (setup and demo instructions)
├── contracts/           # Phase 1 output (OpenAPI contracts)
│   └── openapi.yaml     # Complete OpenAPI 3.0 specification
└── checklists/
    └── requirements.md  # Tracking checklist
```

### Source Code (repository root)

```text
trivia_api/                    # Main Python package
├── __init__.py
├── main.py                    # FastAPI app initialization and middleware
├── config.py                  # Environment configuration, constants
├── database.py                # SQLAlchemy setup, connection pooling
├── models/                    # Pydantic request/response models
│   ├── __init__.py
│   ├── session.py             # TrivaSession, SessionStart request/response
│   ├── answer.py              # AnswerSubmit, AnswerResponse
│   ├── attempt.py             # AttemptRecord, AttemptsList
│   └── leaderboard.py         # LeaderboardEntry, LeaderboardResponse
├── schemas/                   # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── session.py             # TriviaSessionORM
│   ├── attempt.py             # AttemptORM
│   └── user_score.py          # UserScoreORM
├── services/                  # Business logic services
│   ├── __init__.py
│   ├── session_service.py     # Session creation, ending, retrieval
│   ├── answer_service.py      # Answer validation, scoring logic
│   ├── attempt_service.py     # Attempt history, recording
│   └── leaderboard_service.py # Leaderboard ranking, tie-breaking
├── api/                       # API route handlers
│   ├── __init__.py
│   ├── router.py              # API router aggregation
│   ├── session.py             # POST /start, POST /end endpoints
│   ├── question.py            # GET /question endpoint
│   ├── answer.py              # POST /answer endpoint
│   ├── attempts.py            # GET /attempts endpoint
│   └── leaderboard.py         # GET /leaderboard endpoint
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── auth.py                # API key authentication check
│   ├── validators.py          # Input validation helpers
│   └── timestamps.py          # ISO 8601 timestamp handling
└── errors.py                  # Custom exception classes

.env.example                   # Environment variables template
requirements.txt              # Python dependencies
docker-compose.yaml           # Local development stack
Dockerfile                    # API container definition
README.md                     # Project overview (updated from quickstart)
```

**Structure Decision**: Single Python project (Option 1) selected because:
- API-only implementation (no frontend in this phase)
- FastAPI best practices: models → schemas → services → routers
- Services layer enables business logic reuse across endpoints
- Clean separation: HTTP concerns (API routers) vs. business logic (services) vs. data persistence (schemas)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
