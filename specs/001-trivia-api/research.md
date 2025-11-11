# Research: Trivia API

**Date**: November 11, 2025  
**Phase**: 0 - Outline & Research

## Summary

All technical requirements in the feature specification are clearly defined and standard. No critical unknowns identified. All technology choices are well-established in the Python web development ecosystem.

## Findings

### 1. FastAPI Framework Choice

**Decision**: Use FastAPI as the primary web framework for all API endpoints.

**Rationale**:
- Automatic OpenAPI 3.0 schema generation from route decorators and type hints (required by constitution)
- Built-in interactive API documentation (Swagger UI, ReDoc) at `/docs` and `/redoc`
- Pydantic integration for automatic JSON schema validation and serialization
- Excellent performance benchmarks (comparable to Go/Rust frameworks)
- Strong async/await support for handling concurrent requests
- Large, active community with extensive third-party integrations

**Alternatives Considered**:
- **Django**: Too heavyweight for API-only project, adds unnecessary ORM abstraction over SQLAlchemy
- **Flask**: Requires manual OpenAPI integration via Flask-RESTX or similar; less ergonomic
- **Starlette**: Lower-level ASGI framework; would require more manual setup for API documentation

### 2. Database Choice: SQLite

**Decision**: Use SQLite with SQLAlchemy ORM for persistent data storage.

**Rationale**:
- Per spec assumptions: "System uses SQLite for persistent data storage"
- File-based, zero-configuration database suitable for demo and development
- SQLAlchemy ORM provides database abstraction and relationship modeling
- Sufficient for demo scale (100+ concurrent requests manageable with proper connection pooling)
- Alembic migrations support for schema versioning

**Alternatives Considered**:
- **PostgreSQL**: Over-engineered for demo project; adds deployment complexity
- **MongoDB**: Document database; suboptimal for relational data model (sessions, attempts, users, scores)
- **In-memory (Redis)**: Data would be lost on restart; violates spec requirement for persistence

### 3. Pydantic Models for Request/Response Validation

**Decision**: Use Pydantic v2 models for all API request and response schemas.

**Rationale**:
- Automatic JSON Schema generation for OpenAPI documentation (constitution requirement)
- Field-level validation with descriptive error messages
- Type safety enforced at Python level (editor autocompletion, type checking)
- FastAPI native integration: automatic request validation, response serialization
- Example values can be defined at model level via `Field(examples=[...])`

**Alternatives Considered**:
- **dataclasses**: Lighter weight but lack built-in validation and schema generation
- **Plain dicts**: No type safety or automatic validation; less maintainable

### 4. Concurrency Handling: Async/Await with asyncio

**Decision**: Use FastAPI's native async/await with Uvicorn ASGI server for handling concurrent requests.

**Rationale**:
- Spec requires handling 100+ concurrent user submissions without data loss
- Uvicorn worker threads + asyncio event loop handles I/O-bound operations efficiently
- Async database queries via SQLAlchemy's asyncio support
- Horizontal scaling via Uvicorn workers or containerization

**Alternatives Considered**:
- **Gunicorn + synchronous workers**: Works but less efficient for I/O-bound demo workloads
- **Custom threading**: Error-prone; Uvicorn/asyncio abstractions are battle-tested

### 5. Authentication: API Key via Environment Variable

**Decision**: Admin authentication via API key in `.env` file, validated per request header.

**Rationale**:
- Per spec assumptions: "Admin authentication is performed using an API key stored in `.env`"
- Simple, suitable for demo/internal use cases
- No need for complex OAuth2 or JWT infrastructure in initial release
- Can be extended to database-backed credential storage if needed

**Alternatives Considered**:
- **OAuth2 with password flow**: Unnecessary complexity for demo project
- **JWT tokens**: Adds token generation/refresh complexity; API key simpler for static demo credentials

### 6. Timestamp Format: ISO 8601 with UTC

**Decision**: All timestamps stored and returned in ISO 8601 format (UTC timezone).

**Rationale**:
- Per spec: "All timestamps use ISO 8601 format (UTC)"
- Native support in Python `datetime` module and Pydantic
- ISO 8601 is language/platform agnostic for frontend/client consumption
- Sortable as strings; suitable for leaderboard tie-breaking by earliest acquisition

**Alternatives Considered**:
- **Unix timestamps (seconds/milliseconds)**: Less human-readable; requires conversion in queries
- **Local time zones**: Inconsistent across regions; complicates tie-breaking logic

### 7. Case-Insensitive Answer Matching

**Decision**: Store answers in normalized form (lowercase), compare submitted answers case-insensitively.

**Rationale**:
- Per spec requirement: "Answer should be case insensitive"
- Normalize on storage and at comparison time; no special database functions required
- Python string `.lower()` method sufficient; works across Unicode characters

**Alternatives Considered**:
- **Database case-insensitive collation**: Database-specific; adds deployment complexity
- **Regex matching**: Overkill for simple string comparison

### 8. Leaderboard Tie-Breaking: Earliest Score Acquisition

**Decision**: When users have identical cumulative scores, order by earliest timestamp of first correct answer.

**Rationale**:
- Per spec: "For users with identical cumulative scores, ordering is by earliest score acquisition timestamp"
- Implement via database query ORDER BY: `ORDER BY score DESC, first_correct_timestamp ASC`
- Track `first_correct_timestamp` per user in UserScore model

**Alternatives Considered**:
- **Most recent score acquisition**: Penalizes early participants; contradicts spec intent
- **Alphabetical username**: Arbitrary; no fairness basis

## Unknowns Resolved

- ✅ Language: Python 3.11+ confirmed from tech context
- ✅ Framework: FastAPI selected per constitution requirement
- ✅ Storage: SQLite per spec assumptions
- ✅ Concurrency: Asyncio + Uvicorn confirmed suitable
- ✅ Auth: API key environment variable per spec assumptions
- ✅ Timestamps: ISO 8601 UTC per spec requirements

## Risk Assessment

**Low Risk**: All technical choices are standard, well-documented, and proven in production environments.

**Deployment readiness**: Project can be containerized with Docker for consistent demo delivery.

---

**Phase 0 Status**: ✅ **COMPLETE - All research items resolved. Proceed to Phase 1 design.**
