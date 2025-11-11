# Feature Specification: Trivia API

**Feature Branch**: `001-trivia-api`  
**Created**: November 11, 2025  
**Status**: Draft  
**Input**: User description: "Trivia API: Admin should be able to start a new trivia question session. Users should be able to retrieve the current trivia question. Users should be able to retrieve a list of all attempts (date/time, username, correct/incorrect of the answer). Users should be able to submit an answer to the current trivia question with their username, and get back correct/incorrect feedback. If correct, their score should be incremented by 1 and future attempts for that question should be rejected. Admin should be able to end the current trivia question session and the answer shall be revealed. Users should be able to view a leaderboard of top scorers. Answer should be case insensitive."

## User Scenarios & API Flows *(mandatory)*

### User Story 1 - Admin Starts Trivia Session (Priority: P1)

An admin starts a new trivia question session by providing a question and its correct answer. The system marks the session as active and ready to receive participant answers.

**Why this priority**: This is the foundational operation that enables the entire trivia experience. Without the ability to start a session, no other functionality can be used.

**Independent Demo**: Can be fully demoed by an admin calling the start-session endpoint with a question and answer, and verifying the system accepts the submission and marks the session as active.

**Acceptance Scenarios** (API verification):

1. **Given** no active trivia session exists, **When** admin calls POST /api/trivia/session/start with question and correct_answer, **Then** system returns 200 with session_id and question is available to users
2. **Given** an active session exists, **When** admin calls POST /api/trivia/session/start, **Then** system returns 400 "A trivia session is already active"

---

### User Story 2 - User Views Current Question (Priority: P1)

Any user can retrieve the currently active trivia question to attempt answering it.

**Why this priority**: Users need immediate access to the question to participate. This is a core user-facing feature required before answering.

**Independent Demo**: Can be fully demoed by any user calling the get-current-question endpoint and receiving the active question.

**Acceptance Scenarios** (API verification):

1. **Given** an active trivia session exists, **When** user calls GET /api/trivia/question, **Then** system returns 200 with question text and session_id
2. **Given** no active session exists, **When** user calls GET /api/trivia/question, **Then** system returns 200 with null question and message "No active trivia session"

---

### User Story 3 - User Submits Answer with Instant Feedback (Priority: P1)

User submits their username and an answer to the current question, receives immediate feedback (correct/incorrect), and if correct, their score increments and they're prevented from submitting further answers for that question.

**Why this priority**: This is the core interactive feature - users need to participate and receive feedback. It directly delivers business value through engagement.

**Independent Demo**: Can be fully demoed by user submitting an answer and receiving feedback via API response, then verifying score changes or rejection on second attempt.

**Acceptance Scenarios** (API verification):

1. **Given** user has not yet answered current question, **When** user calls POST /api/trivia/answer with correct answer, **Then** system returns 200 with is_correct: true and incremented score
2. **Given** user has not yet answered current question, **When** user calls POST /api/trivia/answer with incorrect answer, **Then** system returns 200 with is_correct: false
3. **Given** user has already answered current question, **When** user calls POST /api/trivia/answer again, **Then** system returns 400 "You have already answered this question"
4. **Given** answer submission with case variation "PARIS", **When** compared to correct answer "paris", **Then** system returns is_correct: true

---

### User Story 4 - User Views All Attempts History (Priority: P2)

User can retrieve a list of all previous answer attempts showing date/time, username, and whether each answer was correct or incorrect.

**Why this priority**: This provides transparency and accountability for the trivia session. Users can review their participation history. Important for engagement but not required for basic participation.

**Independent Demo**: Can be fully demoed by calling the attempts endpoint and verifying entries contain timestamps, usernames, and correctness status.

**Acceptance Scenarios** (API verification):

1. **Given** trivia session with multiple answer submissions, **When** user calls GET /api/trivia/attempts, **Then** system returns 200 with list containing all attempts with timestamps, usernames, and is_correct values
2. **Given** attempts made at different times, **When** user calls GET /api/trivia/attempts, **Then** attempts are ordered chronologically (most recent first)
3. **Given** no attempts have been made, **When** user calls GET /api/trivia/attempts, **Then** system returns 200 with empty attempts list

---

### User Story 5 - User Views Leaderboard (Priority: P2)

User can retrieve a leaderboard displaying top scorers ranked by their cumulative score across all trivia sessions.

**Why this priority**: Leaderboard drives engagement and friendly competition. Important for user motivation and retention but not essential to participate.

**Independent Demo**: Can be fully demoed by calling the leaderboard endpoint and verifying rankings reflect cumulative scores from all sessions.

**Acceptance Scenarios** (API verification):

1. **Given** multiple users with different cumulative scores across all sessions, **When** user calls GET /api/trivia/leaderboard, **Then** system returns 200 with users ranked by score in descending order
2. **Given** users with identical cumulative scores, **When** user calls GET /api/trivia/leaderboard, **Then** users with same score are ordered by earliest score acquisition timestamp (tie-breaking)
3. **Given** no users with scores, **When** user calls GET /api/trivia/leaderboard, **Then** system returns 200 with empty leaderboard

---

### User Story 6 - Admin Ends Session and Reveals Answer (Priority: P2)

Admin can end the current trivia session, which prevents further answer submissions and reveals the correct answer.

**Why this priority**: Essential for closing out trivia rounds and preparing for next questions. Moderator control is important but only needed after participation phase.

**Independent Demo**: Can be fully demoed by admin calling the end-session endpoint, verifying no new answers are accepted, and correct answer is returned in API response.

**Acceptance Scenarios** (API verification):

1. **Given** active trivia session, **When** admin calls POST /api/trivia/session/end, **Then** system returns 200 with correct_answer and session is closed
2. **Given** session has been ended, **When** user calls POST /api/trivia/answer, **Then** system returns 400 "Session has ended"
3. **Given** session ended, **When** any user calls GET /api/trivia/question, **Then** response includes the correct_answer field

---

### Edge Cases & Error States

- What happens when multiple users submit answers simultaneously? → All attempts are recorded with accurate timestamps, no data loss
- How does system handle submission without username? → Reject with error message "Username is required"
- What happens if admin tries to start session while one is active? → Reject with error "A trivia session is already active"
- What happens when submitting answer for non-existent session? → Reject with error "No active trivia session"
- How does system handle special characters or spaces in answers? → Answers are trimmed and compared case-insensitively (special characters preserved)
- What if question text or answer is empty? → Reject with error "Question and answer text required"

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Admin MUST be able to start a new trivia question session by providing question text and correct answer
- **FR-002**: System MUST prevent starting a new session while one is already active
- **FR-003**: Users MUST be able to retrieve the current active trivia question
- **FR-004**: System MUST return appropriate message when no active session exists
- **FR-005**: Users MUST be able to submit an answer with their username to the current question
- **FR-006**: System MUST provide immediate feedback (correct/incorrect) for each answer submission
- **FR-007**: System MUST perform case-insensitive comparison of submitted answers against correct answer
- **FR-008**: System MUST increment user's cumulative score by 1 when they submit a correct answer to any question
- **FR-009**: System MUST prevent same user from submitting additional answers to the same question in the same session
- **FR-010**: System MUST record all answer attempts with timestamp, username, session_id, and correctness status
- **FR-011**: Users MUST be able to retrieve complete history of all answer attempts with timestamps, usernames, and correctness
- **FR-012**: Users MUST be able to retrieve leaderboard showing users ranked by cumulative score across all sessions in descending order
- **FR-013**: System MUST use earliest score acquisition timestamp as tie-breaker for users with identical cumulative scores
- **FR-014**: Admin MUST be able to end current trivia session
- **FR-015**: System MUST prevent answer submissions after session is ended
- **FR-016**: System MUST reveal correct answer when session is ended
- **FR-017**: System MUST handle concurrent user submissions without data loss or corruption

### Key Entities

- **Trivia Session**: Represents an active or ended question period with question text, correct answer, start time, end time, and status (active/ended)
- **Answer Attempt**: Records user's submission containing username, submitted answer text, timestamp, associated session_id, and correctness status
- **User Score**: Maintains aggregate cumulative score per username across all trivia sessions (cumulative total of all correct answers)

## API Contract *(mandatory if feature involves endpoints)*

### Endpoint 1: [POST] /api/trivia/session/start - Start New Trivia Session

**Summary**: Start a new trivia question session with a question and correct answer

**Description**: Creates and activates a new trivia session. Only admins can perform this action. Returns error if a session is already active.

**Request**:
- **Query Parameters**: None
- **Request Body**:
  ```json
  {
    "question": "What is the capital of France?",
    "correct_answer": "Paris"
  }
  ```

**Response** (HTTP 200 Success):
```json
{
  "status": "success",
  "session_id": "session_123",
  "message": "Trivia session started",
  "question": "What is the capital of France?"
}
```

**Error Responses**:
- **400 Bad Request**: "Question and answer text are required"
- **400 Bad Request**: "A trivia session is already active"
- **403 Forbidden**: "Admin access required"
- **500 Internal Server Error**: "Failed to start session"

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/trivia/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the capital of France?",
    "correct_answer": "Paris"
  }'
```

---

### Endpoint 2: [GET] /api/trivia/question - Get Current Trivia Question

**Summary**: Retrieve the current active trivia question

**Description**: Returns the question text of the currently active or most recently ended trivia session. Does not reveal the correct answer until session is ended. After a session ends, the correct answer is included in the response.

**Request**:
- **Path Parameters**: None
- **Query Parameters**: None

**Response** (HTTP 200 Success - Active Session):
```json
{
  "status": "success",
  "question": "What is the capital of France?",
  "session_id": "session_123",
  "is_active": true
}
```

**Response** (HTTP 200 Success - Ended Session with Answer Revealed):
```json
{
  "status": "success",
  "question": "What is the capital of France?",
  "session_id": "session_123",
  "is_active": false,
  "correct_answer": "Paris"
}
```

**Response** (HTTP 200 No Active Session):
```json
{
  "status": "success",
  "question": null,
  "message": "No active trivia session"
}
```

**Error Responses**:
- **500 Internal Server Error**: "Failed to retrieve question"

**Example Usage**:
```bash
curl -X GET http://localhost:8000/api/trivia/question
```

---

### Endpoint 3: [POST] /api/trivia/answer - Submit Answer to Current Question

**Summary**: Submit an answer to the current trivia question

**Description**: Records a user's answer submission to the active trivia question. Returns immediate feedback (correct/incorrect) and updates user score if correct. Rejects if user already answered this question or if no session is active.

**Request**:
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "answer": "Paris"
  }
  ```

**Response** (HTTP 200 Success - Correct):
```json
{
  "status": "success",
  "is_correct": true,
  "message": "Correct!",
  "score": 5
}
```

**Response** (HTTP 200 Success - Incorrect):
```json
{
  "status": "success",
  "is_correct": false,
  "message": "Incorrect!"
}
```

**Error Responses**:
- **400 Bad Request**: "Username and answer are required"
- **400 Bad Request**: "You have already answered this question"
- **400 Bad Request**: "No active trivia session"
- **500 Internal Server Error**: "Failed to submit answer"

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/trivia/answer \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "answer": "Paris"
  }'
```

---

### Endpoint 4: [GET] /api/trivia/attempts - Get All Answer Attempts

**Summary**: Retrieve list of all answer attempts for current session

**Description**: Returns complete history of answer submissions with timestamps, usernames, and correctness status. Ordered chronologically. Answer text is not included in the response.

**Request**:
- **Query Parameters**: None

**Response** (HTTP 200 Success):
```json
{
  "status": "success",
  "attempts": [
    {
      "username": "john_doe",
      "is_correct": true,
      "timestamp": "2025-11-11T14:30:45Z"
    },
    {
      "username": "jane_smith",
      "is_correct": false,
      "timestamp": "2025-11-11T14:31:20Z"
    }
  ]
}
```

**Error Responses**:
- **500 Internal Server Error**: "Failed to retrieve attempts"

**Example Usage**:
```bash
curl -X GET http://localhost:8000/api/trivia/attempts
```

---

### Endpoint 5: [GET] /api/trivia/leaderboard - Get Leaderboard

**Summary**: Retrieve ranked leaderboard of top scorers across all sessions

**Description**: Returns users ranked by their cumulative score in descending order, combining scores from all trivia sessions. Users with identical cumulative scores are ordered by earliest score acquisition time.

**Request**:
- **Query Parameters**: None

**Response** (HTTP 200 Success):
```json
{
  "status": "success",
  "leaderboard": [
    {
      "rank": 1,
      "username": "john_doe",
      "score": 15
    },
    {
      "rank": 2,
      "username": "jane_smith",
      "score": 12
    }
  ]
}
```

**Error Responses**:
- **500 Internal Server Error**: "Failed to retrieve leaderboard"

**Example Usage**:
```bash
curl -X GET http://localhost:8000/api/trivia/leaderboard
```

---

### Endpoint 6: [POST] /api/trivia/session/end - End Current Trivia Session

**Summary**: End the current trivia session and reveal answer

**Description**: Closes the active trivia session and reveals the correct answer. Only admins can perform this action. Subsequent answer submissions will be rejected.

**Request**:
- **Request Body**: Empty

**Response** (HTTP 200 Success):
```json
{
  "status": "success",
  "message": "Trivia session ended",
  "correct_answer": "Paris"
}
```

**Error Responses**:
- **400 Bad Request**: "No active trivia session"
- **403 Forbidden**: "Admin access required"
- **500 Internal Server Error**: "Failed to end session"

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/trivia/session/end \
  -H "Content-Type: application/json"
```

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Admin can start a new trivia session and question is immediately available to users
- **SC-002**: Users can submit answers and receive feedback within 500ms
- **SC-003**: Case-insensitive answer matching works correctly for all character combinations
- **SC-004**: System correctly prevents duplicate answers from same user
- **SC-005**: User scores increment only for correct answers
- **SC-006**: Leaderboard displays accurate rankings reflecting all correct answers
- **SC-007**: System handles 100+ concurrent answer submissions without data loss
- **SC-008**: Session can be ended by admin and correct answer is immediately revealed to all users
- **SC-009**: All answer attempts are recorded with accurate timestamps
- **SC-010**: Users cannot submit answers after admin ends session

### API Quality Criteria

- **SC-API-001**: All endpoints have complete OpenAPI documentation with examples
- **SC-API-002**: Interactive Swagger UI accessible at /docs endpoint
- **SC-API-003**: All error responses return proper HTTP status codes with descriptive messages
- **SC-API-004**: Response time <500ms for all API endpoints
- **SC-API-005**: All endpoints return consistent JSON response structure

## Assumptions

- **Admin Authentication**: Admin authentication is performed using an API key stored in `.env` environment file. Admin endpoints require this API key to be passed in request headers.
- **Session Scope**: Trivia sessions are managed per-session basis. Only one session is active at a time. Previous sessions remain in history for scoring purposes.
- **Score Persistence**: User scores are cumulative across all trivia sessions. Scores earned in one session contribute to the total score for leaderboard ranking.
- **Username Format**: No specific validation on username format. Usernames are case-sensitive for identity but answers are case-insensitive.
- **API-Only Implementation**: This is an API-only specification with no user interface elements. All interactions are performed via REST API endpoints.
- **Concurrent Submissions**: System has adequate infrastructure to handle typical concurrent user loads (tested with 100+ simultaneous requests).
- **Data Storage**: System uses SQLite for persistent data storage of all attempts, sessions, and user scores.
- **Timestamp Format**: All timestamps use ISO 8601 format (UTC).
- **Leaderboard Scope**: Leaderboard displays cumulative scores across all historical trivia sessions, not just the current session.
- **Tie-Breaking**: For users with identical cumulative scores, ordering is by earliest score acquisition timestamp across all sessions.
