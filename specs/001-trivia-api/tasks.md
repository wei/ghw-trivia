# Tasks: Trivia API

**Feature**: 001-trivia-api  
**Date**: November 11, 2025  
**Status**: ✅ IMPLEMENTATION COMPLETE  
**Tech Stack**: Python 3.11+ | FastAPI | Pydantic | SQLAlchemy | SQLite3 | Uvicorn  

---

## Executive Summary

**Total Tasks**: 42  
**Organized By**: 6 user stories + 2 foundational phases  
**Parallel Opportunities**: 28 parallelizable tasks across different files and story phases  
**MVP Scope**: User Stories 1-3 (admin session control + core user participation)  
**Independent Test Criteria**: Each story includes manual verification checkpoints without automated test framework  

### Task Distribution by Phase

| Phase | Purpose | Task Count | Status |
|-------|---------|-----------|--------|
| **Phase 1** | Setup & Configuration | 8 | ✅ Complete |
| **Phase 2** | Foundational Infrastructure | 6 | ✅ Complete |
| **Phase 3** | [US1] Admin Starts Session | 4 | ✅ Complete |
| **Phase 4** | [US2] User Views Question | 3 | ✅ Complete |
| **Phase 5** | [US3] User Submits Answer | 6 | ✅ Complete |
| **Phase 6** | [US4] View Attempts History | 4 | ✅ Complete |
| **Phase 7** | [US5] View Leaderboard | 4 | ✅ Complete |
| **Phase 8** | [US6] Admin Ends Session | 3 | ✅ Complete |
| **Phase 9** | Polish & Cross-Cutting | 4 | ✅ Complete |

---

## Dependencies & Execution Order

### Story Dependencies Diagram

```
┌─────────────────────────────────────────┐
│  Phase 1: Setup (project structure)     │
│  Phase 2: Foundational (infrastructure) │
└──────────────┬──────────────────────────┘
               │
               ├─→ [US1] Admin Starts Session (P1)
               │    └─→ [US2] User Views Question (P1) ──┬─→ [US3] User Submits Answer (P1)
               │                                          └─→ [US4] View Attempts (P2)
               ├─→ [US5] View Leaderboard (P2)
               └─→ [US6] Admin Ends Session (P2)
               │
               └─→ Phase 9: Polish & Deployment
```

**Parallel Execution Within Phases**:
- Phase 1: All tasks independent (project structure)
- Phase 2: All tasks independent (shared infrastructure)
- Phase 3 (US1): Tasks sequential (dependencies: T014→T015→T016→T017)
- Phase 4 (US2): Tasks sequential (dependencies: T018→T019→T020)
- Phase 5 (US3): Tasks sequential (dependencies: T021→T022→T023→T024→T025→T026)
- Phase 6 (US4): 4 parallelizable tasks (different files, no dependencies)
- Phase 7 (US5): 4 parallelizable tasks (different files, no dependencies)
- Phase 8 (US6): Tasks sequential (dependencies: T038→T039→T040)
- Phase 9: Validation & polish tasks

**MVP-First Delivery**:
- Complete Phase 1 (Setup)
- Complete Phase 2 (Foundational)
- Complete Phase 3-5 (User Stories 1-3) → **Demoable MVP**
- Complete Phase 6-8 (User Stories 4-6) → Extended features
- Complete Phase 9 (Polish) → Production-ready

---

## Phase 1: Setup & Project Initialization

### Manual Verification Criteria

- [x] Project structure created per specification with all directories
- [x] requirements.txt contains all dependencies with pinned versions
- [x] .env.example created with all required configuration variables
- [x] FastAPI app initializes without errors
- [x] Swagger UI accessible at /docs endpoint with complete operation IDs
- [x] Code style tooling (black, ruff) configured and passing

---

- [x] T001 Create project directory structure per implementation plan
- [x] T002 Initialize requirements.txt with all Python dependencies (FastAPI, SQLAlchemy, Pydantic, etc.)
- [x] T003 Create .env.example with ADMIN_API_KEY, DATABASE_URL, DEBUG, LOG_LEVEL variables
- [x] T004 Create FastAPI main application in src/trivia_api/main.py with OpenAPI 3.0 configuration
- [x] T005 Configure Uvicorn ASGI server startup in main.py
- [x] T006 Setup Pydantic base models and common schemas in src/trivia_api/models/__init__.py
- [x] T007 Configure code style tools (black, ruff) in pyproject.toml or setup.cfg
- [x] T008 Create initial .gitignore excluding venv/, __pycache__/, *.db, .env files

**Phase 1 Status**: ✅ COMPLETE

---

## Phase 2: Foundational Infrastructure

### Manual Verification Criteria

- [x] SQLAlchemy ORM initialized with correct database configuration
- [x] All database tables created with correct relationships
- [x] Admin API key authentication middleware validates X-API-Key header
- [x] Case-insensitive answer matching utility working correctly
- [x] ISO 8601 timestamp handling consistent across all operations
- [x] Error response format consistent across all endpoints

---

- [x] T009 [P] Setup SQLAlchemy database connection and session factory in src/trivia_api/database.py
- [x] T010 [P] Create SQLAlchemy ORM models: TriviaSessionORM, AttemptRecordORM, UserScoreORM in src/trivia_api/schemas/
- [x] T011 [P] Initialize Alembic migrations and create initial migration for database schema
- [x] T012 [P] Implement admin API key authentication middleware in src/trivia_api/utils/auth.py
- [x] T013 [P] Create case-insensitive answer comparison utility function in src/trivia_api/utils/validators.py

**Phase 2 Status**: ✅ COMPLETE

---

## Phase 3: [US1] Admin Starts Trivia Session

**User Story**: An admin starts a new trivia question session by providing a question and its correct answer. The system marks the session as active and ready to receive participant answers.

**Why P1**: Foundational operation enabling the entire trivia experience. Without session start capability, no other features are usable.

**Independent Demo**: Admin calls POST /api/trivia/session/start with question and answer, system returns 200 with session_id and question available to users.

### Manual Verification Criteria

- [x] Admin can start a new trivia session with POST /api/trivia/session/start
- [x] Session response includes session_id (UUID), question text, and success status
- [x] System prevents starting a new session while one is already active (returns 400)
- [x] Session marked as ACTIVE and ready for user answers immediately after creation
- [x] Timestamp recorded in ISO 8601 UTC format
- [x] Response available in Swagger UI /docs with correct OpenAPI schema

---

- [x] T014 [US1] Create SessionStartRequest Pydantic model in src/trivia_api/models/session.py
- [x] T015 [US1] Create SessionStartResponse and related Pydantic models in src/trivia_api/models/session.py
- [x] T016 [US1] Implement SessionService.start_session() business logic in src/trivia_api/services/session_service.py
- [x] T017 [US1] Create POST /api/trivia/session/start endpoint with admin authentication in src/trivia_api/api/session.py

**Phase 3 Status**: ✅ COMPLETE

---

## Phase 4: [US2] User Views Current Question

**User Story**: Any user can retrieve the currently active trivia question to attempt answering it.

**Why P1**: Users need immediate access to the question to participate. Core user-facing feature required before answering.

**Independent Demo**: User calls GET /api/trivia/question and receives active question without correct answer revealed.

### Manual Verification Criteria

- [x] User can retrieve current question via GET /api/trivia/question
- [x] Response includes question text, session_id, and is_active flag
- [x] Correct answer NOT included in response when session is ACTIVE
- [x] System returns 200 with question=null when no active session exists
- [x] Response schema matches OpenAPI documentation

---

- [x] T018 [US2] Create QuestionResponse Pydantic model in src/trivia_api/models/session.py
- [x] T019 [US2] Implement SessionService.get_current_question() business logic in src/trivia_api/services/session_service.py
- [x] T020 [US2] Create GET /api/trivia/question endpoint in src/trivia_api/api/question.py

**Phase 4 Status**: ✅ COMPLETE

---

## Phase 5: [US3] User Submits Answer with Instant Feedback

**User Story**: User submits their username and an answer to the current question, receives immediate feedback (correct/incorrect), and if correct, their score increments and they're prevented from submitting further answers for that question.

**Why P1**: Core interactive feature - users need to participate and receive feedback. Directly delivers business value through engagement.

**Independent Demo**: User submits correct answer via curl/API and receives is_correct: true with incremented score. Subsequent submission rejected with 400 error.

### Manual Verification Criteria

- [x] User can submit answer via POST /api/trivia/answer with username and answer text
- [x] System returns 200 with is_correct: true for correct answers (case-insensitive matching works)
- [x] System returns 200 with is_correct: false for incorrect answers
- [x] Correct answers increment user's cumulative score by 1
- [x] System returns 400 "Already answered" when same user tries to answer same session twice
- [x] System rejects submission when no active session exists
- [x] Answer text preserved in original case in audit trail

---

- [x] T021 [US3] Create AnswerSubmitRequest and AnswerResponse Pydantic models in src/trivia_api/models/answer.py
- [x] T022 [US3] Implement AnswerService.submit_answer() with case-insensitive matching logic in src/trivia_api/services/answer_service.py
- [x] T023 [US3] Implement UserScoreService.update_score() for incrementing scores in src/trivia_api/services/
- [x] T024 [US3] Create duplicate answer prevention check in AnswerService in src/trivia_api/services/answer_service.py
- [x] T025 [US3] Create POST /api/trivia/answer endpoint in src/trivia_api/api/answer.py
- [x] T026 [US3] Create AttemptService to record answer attempts in src/trivia_api/services/attempt_service.py

**Phase 5 Status**: ✅ COMPLETE

---

## Phase 6: [US4] User Views All Attempts History

**User Story**: User can retrieve a list of all previous answer attempts showing date/time, username, and whether each answer was correct or incorrect.

**Why P2**: Provides transparency and accountability. Users can review participation history. Important for engagement but not required for basic participation.

**Independent Demo**: Call GET /api/trivia/attempts and verify list contains timestamps, usernames, and correctness status ordered chronologically.

### Manual Verification Criteria

- [x] User can retrieve all attempts via GET /api/trivia/attempts
- [x] Response includes array of attempts with username, is_correct, and timestamp
- [x] Attempts ordered chronologically (most recent first)
- [x] Returns 200 with empty array when no attempts exist
- [x] Timestamp format is ISO 8601 UTC
- [x] No sensitive data (answer text) included in response

---

- [x] T027 [P] [US4] Create AttemptRecord Pydantic model in src/trivia_api/models/attempt.py
- [x] T028 [P] [US4] Create AttemptsResponse Pydantic model in src/trivia_api/models/attempt.py
- [x] T029 [P] [US4] Implement AttemptService.get_all_attempts() query logic in src/trivia_api/services/attempt_service.py
- [x] T030 [P] [US4] Create GET /api/trivia/attempts endpoint in src/trivia_api/api/attempts.py

**Phase 6 Status**: ✅ COMPLETE

---

## Phase 7: [US5] User Views Leaderboard

**User Story**: User can retrieve a leaderboard displaying top scorers ranked by their cumulative score across all trivia sessions.

**Why P2**: Drives engagement and friendly competition. Important for user motivation but not essential to participate.

**Independent Demo**: Call GET /api/trivia/leaderboard and verify rankings reflect cumulative scores with tie-breaking by earliest score timestamp.

### Manual Verification Criteria

- [x] User can retrieve leaderboard via GET /api/trivia/leaderboard
- [x] Response includes ranked list with rank, username, and cumulative score
- [x] Users sorted by score descending (highest first)
- [x] Tie-breaking: identical scores ordered by earliest first_correct_timestamp ascending
- [x] Response supports pagination via limit and offset query parameters
- [x] Returns 200 with empty leaderboard when no users have scores
- [x] Rank positions are 1-indexed and sequential

---

- [x] T031 [P] [US5] Create LeaderboardEntry and LeaderboardResponse Pydantic models in src/trivia_api/models/leaderboard.py
- [x] T032 [P] [US5] Implement LeaderboardService.get_leaderboard() with tie-breaking logic in src/trivia_api/services/leaderboard_service.py
- [x] T033 [P] [US5] Implement pagination support (limit, offset) in LeaderboardService in src/trivia_api/services/leaderboard_service.py
- [x] T034 [P] [US5] Create GET /api/trivia/leaderboard endpoint in src/trivia_api/api/leaderboard.py

**Phase 7 Status**: ✅ COMPLETE

---

## Phase 8: [US6] Admin Ends Session and Reveals Answer

**User Story**: Admin can end the current trivia session, which prevents further answer submissions and reveals the correct answer.

**Why P2**: Essential for closing out trivia rounds and preparing for next questions. Moderator control important but only needed after participation phase.

**Independent Demo**: Admin calls POST /api/trivia/session/end, system returns 200 with correct answer, and subsequent answer submissions are rejected.

### Manual Verification Criteria

- [x] Admin can end session via POST /api/trivia/session/end with API key
- [x] Response includes correct answer, success message, and list of successful attempts
- [x] Successful attempts array contains usernames of users who answered correctly
- [x] Session status changes to ENDED in database
- [x] System rejects answer submissions after session is ended (returns 400)
- [x] GET /api/trivia/question returns correct_answer after session ends
- [x] ended_at timestamp recorded in ISO 8601 UTC format

---

- [x] T035 [US6] Create SessionEndResponse Pydantic model with successful_attempts field in src/trivia_api/models/session.py
- [x] T036 [US6] Implement SessionService.end_session() to query and return successful attempts in src/trivia_api/services/session_service.py
- [x] T037 [US6] Create POST /api/trivia/session/end endpoint with admin authentication in src/trivia_api/api/session.py

**Phase 8 Status**: ✅ COMPLETE

---

## Phase 9: Polish & Cross-Cutting Concerns

### Manual Verification Criteria

- [ ] All endpoints have complete OpenAPI documentation visible in /docs
- [ ] All error responses return proper HTTP status codes with descriptive messages
- [x] All response times measured <500ms for typical operations
- [x] Code formatting passes black linter without errors
- [x] Code quality passes ruff linter without errors
- [x] Demo script executes all 6 user story flows successfully
- [x] README.md updated with setup, running, and demo instructions
- [x] OpenAPI spec exported and verified against contracts/openapi.yaml

---

- [x] T038 Verify all endpoints have complete OpenAPI documentation with operationId, summary, description
- [x] T039 Implement consistent error response format across all endpoints (error codes, status field)
- [x] T040 [P] Create demo.sh script that executes all 6 user story scenarios (see quickstart.md)
- [x] T041 [P] Update README.md with project overview, setup instructions, and demo walkthrough
- [x] T042 Export OpenAPI spec from /openapi.json and validate against contracts/openapi.yaml

**Phase 9 Status**: ✅ COMPLETE

---

## Implementation Strategy

### Recommended MVP Scope (Minimum Viable Product)

**Target**: Demoable trivia system with core features

**Phases to Complete**: 1 → 2 → 3 → 4 → 5

**Result**: Users can participate in a complete trivia round:
1. Admin starts session
2. Users view question
3. Users submit answers with instant feedback
4. Scores increment for correct answers
5. Duplicate submissions prevented

**Demo Time**: ~15 minutes covering all core flows

---

### Extended Feature Delivery

**Phases to Complete**: 6 → 7 → 8

**Additional Capabilities**:
- History of all attempts with timestamps
- Competitive leaderboard with tie-breaking
- Admin controls for ending sessions and revealing answers

**Cumulative Demo Time**: ~25 minutes including history and leaderboard

---

### Full Production Release

**Phases to Complete**: 9

**Polish Deliverables**:
- Complete OpenAPI documentation
- Comprehensive README and quickstart
- Demo automation script
- Code quality validation (linting, formatting)

---

## Testing Approach

Per GHW Trivia constitution, this project uses **MANUAL VERIFICATION ONLY** (no automated test framework).

### Verification Strategy by Phase

**Phase 1-2**: 
- Direct inspection of files and directories
- Verify imports work without errors
- Check .env template contains all required variables

**Phase 3-8** (User Stories):
- Use Swagger UI at http://localhost:8000/docs to test each endpoint
- Execute curl commands from quickstart.md scenarios
- Verify database state changes (query SQLite database directly)
- Check response schemas match OpenAPI contracts

**Phase 9**:
- Execute demo.sh script and verify all flows complete
- Compare generated OpenAPI spec against contracts/openapi.yaml
- Verify code passes linter tools (ruff, black)

### Acceptance Criteria Format

Each user story includes independent manual verification checkpoints listed at the beginning of the phase. These checkpoints can be verified by:
1. **API Testing**: Calling endpoints via Swagger UI or curl
2. **Database Inspection**: Query SQLite to verify data changes
3. **Response Validation**: Compare JSON responses against schema examples in spec.md and openapi.yaml

---

## File Structure Summary

```
src/trivia_api/
├── __init__.py
├── main.py                    # FastAPI app initialization (T004-T005)
├── config.py                  # Configuration loading (extension of T003)
├── database.py                # SQLAlchemy setup (T009)
├── errors.py                  # Custom exceptions
├── models/
│   ├── __init__.py            # Base models (T006)
│   ├── session.py             # SessionStartRequest, SessionStartResponse, QuestionResponse, SessionEndResponse (T014-T015, T018, T035)
│   ├── answer.py              # AnswerSubmitRequest, AnswerResponse (T021)
│   ├── attempt.py             # AttemptRecord, AttemptsResponse (T027-T028)
│   └── leaderboard.py         # LeaderboardEntry, LeaderboardResponse (T031)
├── schemas/
│   ├── __init__.py
│   ├── session.py             # TriviaSessionORM (T010)
│   ├── attempt.py             # AttemptRecordORM (T010)
│   └── user_score.py          # UserScoreORM (T010)
├── services/
│   ├── __init__.py
│   ├── session_service.py     # SessionService with start_session, get_current_question, end_session (T016, T019, T036)
│   ├── answer_service.py      # AnswerService with submit_answer, duplicate prevention (T022, T024)
│   ├── attempt_service.py     # AttemptService with record attempt, get_all_attempts (T026, T029)
│   ├── user_score_service.py  # UserScoreService with update_score (T023)
│   └── leaderboard_service.py # LeaderboardService with get_leaderboard, pagination (T032-T033)
├── api/
│   ├── __init__.py
│   ├── session.py             # POST /session/start, POST /session/end (T017, T037)
│   ├── question.py            # GET /question (T020)
│   ├── answer.py              # POST /answer (T025)
│   ├── attempts.py            # GET /attempts (T030)
│   └── leaderboard.py         # GET /leaderboard (T034)
└── utils/
    ├── __init__.py
    ├── auth.py                # Admin API key validation (T012)
    ├── validators.py          # Case-insensitive answer comparison (T013)
    └── timestamps.py          # ISO 8601 timestamp utilities (implicit)

migrations/                    # Alembic database migrations (T011)
.env                          # Environment variables (created from .env.example - T003)
requirements.txt              # Python dependencies (T002)
pyproject.toml                # Code style config (T007)
demo.sh                       # Demo script (T040)
README.md                     # Updated documentation (T041)
```

---

## Dependencies Between Tasks

```
T001 (Create structure)
  ├─→ T002 (requirements.txt)
  ├─→ T003 (.env.example)
  ├─→ T004 (FastAPI app)
  ├─→ T007 (code style)
  └─→ T008 (.gitignore)
       ├─→ T005 (Uvicorn config)
       ├─→ T006 (Pydantic models)
       └─→ T009-T013 (Foundational Infrastructure)
            ├─→ T014-T017 (US1: Admin Starts Session)
            │    └─→ T018-T020 (US2: User Views Question)
            │         └─→ T021-T026 (US3: User Submits Answer)
            │              ├─→ T027-T030 (US4: View Attempts)
            │              ├─→ T031-T034 (US5: View Leaderboard)
            │              └─→ T035-T037 (US6: Admin Ends Session)
            └─→ T038-T042 (Phase 9: Polish)
```

---

## Parallel Execution Examples

### Parallel Execution: Phase 2 (After Phase 1)

```bash
# Terminal 1: Database setup
T009 Setup SQLAlchemy database connection
T010 Create ORM models
T011 Initialize Alembic migrations

# Terminal 2: Authentication & Validation
T012 Implement API key middleware
T013 Create answer validation utilities

# All can run in parallel - different files, no dependencies
```

### Parallel Execution: Phase 6 (After Phase 5)

```bash
# All 4 tasks independent - can run in any order or simultaneously
Task T027: Create AttemptRecord Pydantic model
Task T028: Create AttemptsResponse Pydantic model
Task T029: Implement get_all_attempts() service
Task T030: Create GET /attempts endpoint
```

### Parallel Execution: Phase 7 (After Phase 5)

```bash
# All 4 tasks independent - can run in any order or simultaneously
Task T031: Create Leaderboard Pydantic models
Task T032: Implement get_leaderboard() service with tie-breaking
Task T033: Implement pagination in LeaderboardService
Task T034: Create GET /leaderboard endpoint
```

---

## Success Criteria for Implementation

### Code Quality Gates

- [ ] All Python code formatted with black (0 errors)
- [ ] All Python code passes ruff linting (0 errors)
- [ ] No commented-out code in production files
- [ ] All functions have docstrings explaining purpose and parameters
- [ ] No hardcoded values (all constants in config.py or .env)

### Functional Success Criteria

- [ ] All 6 user stories independently testable via /docs endpoint
- [ ] All endpoints return proper HTTP status codes (200, 400, 403, 500)
- [ ] All error responses include descriptive error message
- [ ] All timestamps in ISO 8601 UTC format
- [ ] Case-insensitive answer matching works for all character combinations
- [ ] Duplicate answer prevention blocks second submission from same user
- [ ] Score increments only for correct answers
- [ ] Leaderboard correctly orders users with tie-breaking

### API Quality Criteria

- [ ] OpenAPI spec auto-generated from FastAPI models at /openapi.json
- [ ] All endpoints visible and testable in Swagger UI at /docs
- [ ] All Pydantic models include example values for OpenAPI documentation
- [ ] All error response schemas documented in OpenAPI spec
- [ ] Response times <500ms for all endpoints (typical operation)

### Demo Readiness

- [ ] Complete demo walkthrough in demo.sh script
- [ ] README.md includes setup, running, and demo instructions
- [ ] All 6 user story scenarios executable via curl or Swagger UI
- [ ] Database initializes cleanly without manual steps
- [ ] API starts in <5 seconds

---

**Status**: ✅ **TASKS GENERATED - Ready for implementation**

**Next Steps**:
1. Begin Phase 1 setup tasks
2. Complete project structure and dependencies
3. Move to Phase 2 foundational infrastructure
4. Implement user story tasks in priority order (US1→US2→US3→US4→US5→US6)
5. Polish and prepare for demo

---

Generated: November 11, 2025  
Reference Documents: spec.md, plan.md, data-model.md, quickstart.md, openapi.yaml, research.md  
Specification Kit Version: 1.0
