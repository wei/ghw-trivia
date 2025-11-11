# Data Model: Trivia API

**Date**: November 11, 2025  
**Phase**: 1 - Design & Contracts  
**Specification Reference**: `spec.md`

## Entity Overview

The Trivia API data model consists of three primary entities managing question sessions, user answer tracking, and cumulative scoring:

1. **TriviaSession**: Manages the current question period
2. **AttemptRecord**: Tracks individual answer submissions
3. **UserScore**: Maintains cumulative scores per user

## Detailed Entity Definitions

### Entity 1: TriviaSession

**Purpose**: Represents a trivia question period with an active or closed state.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `session_id` | String (UUID) | Primary Key, NOT NULL | Unique identifier, generated on creation |
| `question` | String | NOT NULL, min_length=1, max_length=500 | Question text presented to users |
| `correct_answer` | String | NOT NULL, min_length=1, max_length=200 | Normalized (lowercase) correct answer for matching |
| `status` | Enum: `ACTIVE` \| `ENDED` | NOT NULL, default=`ACTIVE` | Current state of the session |
| `started_at` | DateTime (ISO 8601 UTC) | NOT NULL | Timestamp when session was created |
| `ended_at` | DateTime (ISO 8601 UTC) | Nullable | Timestamp when session was closed (null if active) |

**Relationships**:
- One-to-Many: One TriviaSession has many AttemptRecords
- Foreign Key: AttemptRecord.session_id → TriviaSession.session_id

**Validation Rules**:
- Question and correct_answer cannot be empty
- Status must be one of: ACTIVE, ENDED
- ended_at must be NULL if status is ACTIVE
- ended_at must be populated when status is ENDED
- started_at ≤ ended_at (when ended_at is not null)

**State Transitions**:

```
ACTIVE
  │
  └──→ [admin calls /session/end] ──→ ENDED (terminal state)
```

**Example**:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "What is the capital of France?",
  "correct_answer": "paris",
  "status": "ACTIVE",
  "started_at": "2025-11-11T14:30:00Z",
  "ended_at": null
}
```

---

### Entity 2: AttemptRecord

**Purpose**: Immutable record of each answer submission for audit trail and history.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `attempt_id` | Integer | Primary Key, Autoincrement | Internal unique identifier |
| `session_id` | String (UUID) | NOT NULL, Foreign Key | Reference to TriviaSession |
| `username` | String | NOT NULL, min_length=1, max_length=100 | User identifier (case-sensitive) |
| `submitted_answer` | String | NOT NULL, min_length=1, max_length=200 | User's submitted answer text (original case preserved) |
| `is_correct` | Boolean | NOT NULL | Whether answer matches correct_answer (case-insensitive) |
| `submitted_at` | DateTime (ISO 8601 UTC) | NOT NULL | Timestamp of submission |

**Relationships**:
- Many-to-One: AttemptRecord.session_id → TriviaSession.session_id
- Implicit: Multiple records can share same (session_id, username) pair across different sessions

**Validation Rules**:
- username cannot be empty
- submitted_answer cannot be empty
- submitted_at must be present
- is_correct is computed: normalize both submitted_answer and correct_answer to lowercase, then compare string equality
- session_id must reference an existing TriviaSession
- Constraint: Only one attempt per (session_id, username) pair per session (enforced by business logic)

**Example**:

```json
{
  "attempt_id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "submitted_answer": "Paris",
  "is_correct": true,
  "submitted_at": "2025-11-11T14:30:45Z"
}
```

---

### Entity 3: UserScore

**Purpose**: Aggregate cumulative score per user across all trivia sessions.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `user_id` | Integer | Primary Key, Autoincrement | Internal unique identifier |
| `username` | String | NOT NULL, UNIQUE | User identifier (case-sensitive) |
| `cumulative_score` | Integer | NOT NULL, default=0, min=0 | Total correct answers across all sessions |
| `first_correct_timestamp` | DateTime (ISO 8601 UTC) | Nullable | Timestamp of earliest correct answer (for tie-breaking) |
| `last_updated` | DateTime (ISO 8601 UTC) | NOT NULL | When this score was last modified |

**Relationships**:
- Implicit: Created on first correct answer, updated on subsequent correct answers

**Validation Rules**:
- username is unique and case-sensitive
- cumulative_score ≥ 0
- first_correct_timestamp is set on first correct answer, never updated
- last_updated is set on creation and updated every time score increases

**State Transitions**:

```
[User submits first correct answer]
  │
  └──→ Create UserScore: cumulative_score=1, first_correct_timestamp=now

[User submits subsequent correct answers]
  │
  └──→ Increment cumulative_score, preserve first_correct_timestamp
```

**Example**:

```json
{
  "user_id": 1,
  "username": "john_doe",
  "cumulative_score": 5,
  "first_correct_timestamp": "2025-11-11T14:30:45Z",
  "last_updated": "2025-11-11T14:35:20Z"
}
```

---

## Relationships Diagram

```
┌─────────────────────┐
│   TriviaSession     │
├─────────────────────┤
│ session_id (PK)     │
│ question            │
│ correct_answer      │
│ status              │
│ started_at          │
│ ended_at            │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────┐
│   AttemptRecord     │
├─────────────────────┤
│ attempt_id (PK)     │
│ session_id (FK)     │
│ username            │
│ submitted_answer    │
│ is_correct          │
│ submitted_at        │
└─────────────────────┘

┌─────────────────────┐
│   UserScore         │
├─────────────────────┤
│ user_id (PK)        │
│ username (UNIQUE)   │
│ cumulative_score    │
│ first_correct_time  │
│ last_updated        │
└─────────────────────┘
  (Implicit: linked by username field in AttemptRecord)
```

---

## State & Workflow

### Session Lifecycle

1. **Creation** (POST /api/trivia/session/start):
   - Admin provides question and correct_answer
   - System creates TriviaSession with status=ACTIVE, started_at=now, session_id=UUID()
   - Question immediately available to all users

2. **Active Period** (User interactions):
   - Users retrieve question (GET /api/trivia/question) → returns question text without answer
   - Users submit answers (POST /api/trivia/answer)
   - Each attempt recorded in AttemptRecord
   - Correct answers increment UserScore.cumulative_score

3. **Ending** (POST /api/trivia/session/end):
   - Admin calls endpoint
   - System updates TriviaSession: status=ENDED, ended_at=now
   - Subsequent answer submissions to this session rejected
   - Query GET /api/trivia/question returns correct_answer for all users

### Answer Submission Flow

1. User calls POST /api/trivia/answer with {username, answer}
2. System validates:
   - Active session exists
   - No prior attempt from this user in this session
   - Username and answer fields non-empty
3. System normalizes: `normalized_answer = submitted_answer.lower().strip()`
4. System compares: `is_correct = (normalized_answer == correct_answer.lower().strip())`
5. Create AttemptRecord with is_correct result
6. If is_correct:
   - Check/create UserScore for username
   - Increment UserScore.cumulative_score by 1
   - Set UserScore.first_correct_timestamp if new user
   - Update UserScore.last_updated = now
7. Return {status: "success", is_correct: true/false, score: updated_score (if correct)}

### Leaderboard Ranking Logic

1. Query all UserScore records ordered by: `ORDER BY cumulative_score DESC, first_correct_timestamp ASC`
2. Assign rank based on result position (1-indexed)
3. Return paginated leaderboard: [{rank, username, score}, ...]

---

## Data Integrity Constraints

**Business Rules**:

1. **Session Uniqueness**: Only ONE active session at a time
   - Check: `TriviaSession.status == ACTIVE` count must be ≤ 1
   - Enforce: Reject start_session if active session exists

2. **Duplicate Prevention**: Same user cannot answer same session twice
   - Constraint: UNIQUE(session_id, username) on AttemptRecord
   - Enforce: Query AttemptRecord before allowing submission

3. **Score Immutability**: Once recorded, attempt outcomes cannot change
   - AttemptRecord is write-once (insert only, no updates)
   - UserScore updated only on new correct answers (increment only)

4. **Answer Validation**: Comparison is case-insensitive, whitespace-trimmed
   - Both submitted_answer and correct_answer normalized before comparison
   - Original values preserved in AttemptRecord for audit trail

---

## Migration Path (Alembic)

**Initial Schema** (migration 001):

```
tables:
  - trivia_sessions (session_id UUID PRIMARY KEY, ...)
  - attempt_records (attempt_id INTEGER PRIMARY KEY, ...)
  - user_scores (user_id INTEGER PRIMARY KEY, ...)
  
indexes:
  - attempt_records.session_id (for fast filtering)
  - attempt_records.(session_id, username) UNIQUE (for duplicate prevention)
  - user_scores.username UNIQUE (for score lookup)
  - user_scores.cumulative_score DESC (for leaderboard sorting)
  - attempt_records.submitted_at (for chronological ordering)
```

---

**Phase 1 Status**: ✅ **DATA MODEL COMPLETE - Ready for API contract generation**
