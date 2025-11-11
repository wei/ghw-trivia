# Feature Specification: Trivia API

**Feature Branch**: `001-trivia-api`  
**Created**: November 11, 2025  
**Status**: Draft  
**Input**: User description: "Trivia API: Admin should be able to start a new trivia question session. Users should be able to retrieve the current trivia question. Users should be able to retrieve a list of all attempts (date/time, username, correct/incorrect of the answer). Users should be able to submit an answer to the current trivia question with their username, and get back correct/incorrect feedback. If correct, their score should be incremented by 1 and future attempts for that question should be rejected. Admin should be able to end the current trivia question session and the answer shall be revealed. Users should be able to view a leaderboard of top scorers. Answer should be case insensitive."

## User Scenarios & UX Flow *(mandatory)*

### User Story 1 - Admin Starts Trivia Session (Priority: P1)

An admin starts a new trivia question session by providing a question and its correct answer. The system marks the session as active and ready to receive participant answers.

**Why this priority**: This is the foundational operation that enables the entire trivia experience. Without the ability to start a session, no other functionality can be used.

**Independent Demo**: Can be fully demoed by an admin calling the start-session endpoint with a question and answer, and verifying the system accepts the submission and marks the session as active.

**UX Requirements**:
- Visual design: Admin interface for entering question and answer
- User feedback: Confirmation message showing session started with question visible
- Accessibility: Form labels for all input fields, keyboard navigation

**Acceptance Scenarios** (manual verification):

1. **Given** no active trivia session exists, **When** admin provides a question and correct answer, **Then** system confirms session started and the question becomes available to users
2. **Given** an active session exists, **When** admin attempts to start a new session, **Then** system rejects the request with clear message (session already active)

---

### User Story 2 - User Views Current Question (Priority: P1)

Any user can retrieve the currently active trivia question to attempt answering it.

**Why this priority**: Users need immediate access to the question to participate. This is a core user-facing feature required before answering.

**Independent Demo**: Can be fully demoed by any user calling the get-current-question endpoint and seeing the active question displayed.

**UX Requirements**:
- Visual design: Clear display of question text, readable formatting
- User feedback: Indicates whether a session is active or no question available
- Accessibility: Question text is readable by screen readers, sufficient contrast

**Acceptance Scenarios** (manual verification):

1. **Given** an active trivia session exists, **When** user requests current question, **Then** user receives question text
2. **Given** no active session exists, **When** user requests current question, **Then** user receives message indicating no active session

---

### User Story 3 - User Submits Answer with Instant Feedback (Priority: P1)

User submits their username and an answer to the current question, receives immediate feedback (correct/incorrect), and if correct, their score increments and they're prevented from submitting further answers for that question.

**Why this priority**: This is the core interactive feature - users need to participate and receive feedback. It directly delivers business value through engagement.

**Independent Demo**: Can be fully demoed by user submitting an answer and seeing feedback, then verifying score changes or rejection on second attempt.

**UX Requirements**:
- Visual design: Clear form for entering username and answer, prominent feedback message
- User feedback: Immediate feedback showing "Correct!" or "Incorrect!" with visual distinction (color, icon)
- Error messaging: "You have already answered this question" when attempting duplicate
- Accessibility: Form labels, error announcements for screen readers

**Acceptance Scenarios** (manual verification):

1. **Given** user has not yet answered current question, **When** user submits correct answer with username, **Then** system confirms "Correct!" and increments their score by 1
2. **Given** user has not yet answered current question, **When** user submits incorrect answer with username, **Then** system confirms "Incorrect!" and score remains unchanged
3. **Given** user has already answered current question correctly, **When** user attempts to submit another answer, **Then** system rejects with message "You have already answered this question"
4. **Given** answer submission with any case variation, **When** compared to correct answer, **Then** match is case-insensitive (e.g., "Paris", "paris", "PARIS" all match)

---

### User Story 4 - User Views All Attempts History (Priority: P2)

User can retrieve a list of all previous answer attempts showing date/time, username, and whether each answer was correct or incorrect.

**Why this priority**: This provides transparency and accountability for the trivia session. Users can review their participation history. Important for engagement but not required for basic participation.

**Independent Demo**: Can be fully demoed by retrieving attempts list and verifying entries show timestamps, usernames, and correctness status.

**UX Requirements**:
- Visual design: Table or list showing attempts chronologically, clear correct/incorrect indicators
- User feedback: Indicates when no attempts exist yet
- Accessibility: Table headers properly marked, status clearly indicated for screen readers

**Acceptance Scenarios** (manual verification):

1. **Given** trivia session with multiple answer submissions, **When** user requests all attempts, **Then** system returns complete list with timestamps, usernames, and correct/incorrect status
2. **Given** attempts made at different times, **When** user views list, **Then** attempts are ordered chronologically (most recent first)
3. **Given** no attempts have been made, **When** user requests attempts list, **Then** system indicates "No attempts yet"

---

### User Story 5 - User Views Leaderboard (Priority: P2)

User can view a leaderboard displaying top scorers ranked by their cumulative score from correct answers across all trivia sessions.

**Why this priority**: Leaderboard drives engagement and friendly competition. Important for user motivation and retention but not essential to participate.

**Independent Demo**: Can be fully demoed by viewing leaderboard and verifying rankings reflect scores from submitted answers.

**UX Requirements**:
- Visual design: Ranked list showing position, username, and score; highlight top scorers (gold/silver/bronze styling)
- User feedback: Clear ranking position, visual distinction for different tiers
- Accessibility: Rankings clearly announced for screen readers, logical tab order

**Acceptance Scenarios** (manual verification):

1. **Given** multiple users with different scores, **When** user requests leaderboard, **Then** users are ranked by score in descending order
2. **Given** users with identical scores, **When** they appear on leaderboard, **Then** they are ordered by earliest submission time (tie-breaking)
3. **Given** no scores yet, **When** user views leaderboard, **Then** leaderboard is empty with message "No scores yet"

---

### User Story 6 - Admin Ends Session and Reveals Answer (Priority: P2)

Admin can end the current trivia session, which prevents further answer submissions and reveals the correct answer to all users.

**Why this priority**: Essential for closing out trivia rounds and preparing for next questions. Moderator control is important but only needed after participation phase.

**Independent Demo**: Can be fully demoed by admin ending session, verifying no new answers accepted, and correct answer becomes visible to users.

**UX Requirements**:
- Visual design: Admin button to end session with confirmation dialog
- User feedback: Clear confirmation that session has ended, correct answer prominently displayed
- Accessibility: Confirmation dialog properly labeled and navigable

**Acceptance Scenarios** (manual verification):

1. **Given** active trivia session, **When** admin ends session, **Then** system closes session and reveals correct answer
2. **Given** session has been ended, **When** user attempts to submit an answer, **Then** system rejects with message "Session has ended"
3. **Given** session ended, **When** any user views current question, **Then** correct answer is displayed alongside question

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
- **FR-008**: System MUST increment user's score by 1 when they submit a correct answer
- **FR-009**: System MUST prevent same user from submitting additional answers to the same question
- **FR-010**: System MUST record all answer attempts with timestamp, username, and correctness status
- **FR-011**: Users MUST be able to retrieve complete history of all answer attempts with timestamps, usernames, and correctness
- **FR-012**: Users MUST be able to retrieve leaderboard showing users ranked by score in descending order
- **FR-013**: System MUST use earliest submission time as tie-breaker for users with identical scores
- **FR-014**: Admin MUST be able to end current trivia session
- **FR-015**: System MUST prevent answer submissions after session is ended
- **FR-016**: System MUST reveal correct answer to all users when session is ended
- **FR-017**: System MUST handle concurrent user submissions without data loss or corruption

### Key Entities

- **Trivia Session**: Represents the current active question period with question text, correct answer, start time, end time, and status (active/ended)
- **Answer Attempt**: Records user's submission containing username, submitted answer text, timestamp, and correctness status
- **User Score**: Maintains aggregate score per username across all correct answers in current session

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

**Description**: Returns the question text of the currently active trivia session. Does not reveal the correct answer until session is ended.

**Request**:
- **Path Parameters**: None
- **Query Parameters**: None

**Response** (HTTP 200 Success):
```json
{
  "status": "success",
  "question": "What is the capital of France?",
  "session_id": "session_123",
  "is_active": true
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

**Description**: Returns complete history of answer submissions with timestamps, usernames, and correctness status. Ordered chronologically.

**Request**:
- **Query Parameters**: None

**Response** (HTTP 200 Success):
```json
{
  "status": "success",
  "attempts": [
    {
      "username": "john_doe",
      "answer": "Paris",
      "is_correct": true,
      "timestamp": "2025-11-11T14:30:45Z"
    },
    {
      "username": "jane_smith",
      "answer": "London",
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

**Summary**: Retrieve ranked leaderboard of top scorers

**Description**: Returns users ranked by score in descending order. Users with identical scores are ordered by earliest submission time.

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
      "score": 5
    },
    {
      "rank": 2,
      "username": "jane_smith",
      "score": 3
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

- **Admin Context**: The system will have admin authentication/authorization in place. This specification assumes admin checks are performed by the calling service/middleware.
- **Session Scope**: Trivia sessions are managed per-session basis. Only one session is active at a time.
- **Score Persistence**: User scores are calculated per session and are not carried over between sessions.
- **Username Format**: No specific validation on username format. Usernames are case-sensitive for identity but answers are case-insensitive.
- **Concurrent Submissions**: System has adequate infrastructure to handle typical concurrent user loads (tested with 100+ simultaneous requests).
- **Data Storage**: System stores all attempts and session data persistently for the duration of the session.
- **Timestamp Format**: All timestamps use ISO 8601 format (UTC).
- **First Attempt Wins**: For tie-breaking on leaderboard, users are ordered by earliest submission time (not by update time).
