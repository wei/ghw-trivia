# Trivia API

A FastAPI-based REST API for managing trivia question sessions, recording user answers, and maintaining a leaderboard of top scorers.

**Features**:
- ✅ Admin starts/ends trivia sessions with questions and answers
- ✅ Users submit answers and receive immediate feedback
- ✅ Case-insensitive answer matching
- ✅ Automatic scoring and cumulative leaderboard ranking
- ✅ Complete audit trail with ISO 8601 timestamps
- ✅ Handles concurrent requests (100+ concurrent users)
- ✅ Interactive API documentation (Swagger UI)
- ✅ OpenAPI 3.0 compliant

## Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **SQLite3** (usually bundled with Python)
- **Git**

## Project Setup

### 1. Create Virtual Environment

```bash
cd ghw-trivia
python3 -m venv venv

# Activate venv
source venv/bin/activate          # macOS/Linux
# or
venv\Scripts\activate              # Windows
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Configuration

Create `.env` file (or copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Admin API Key (generate a secure random string for production)
ADMIN_API_KEY=your-super-secret-admin-key-here

# Database
DATABASE_URL=sqlite:///./trivia.db

# Server
DEBUG=True
LOG_LEVEL=INFO
```

### 4. Initialize Database

```bash
# Create database tables from migrations
PYTHONPATH=src alembic upgrade head
```

## Running the Server

### Start Development Server

```bash
# From project root with venv activated
PYTHONPATH=src python3 -m uvicorn trivia_api.main:app --reload --host 0.0.0.0 --port 8000
```

Output should show:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Access API Documentation

Once server is running:

- **Swagger UI** (interactive): http://localhost:8000/docs
- **ReDoc** (alternative): http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Session Management

#### Start a Trivia Session
```bash
curl -X POST http://localhost:8000/api/trivia/session/start \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-super-secret-admin-key-here" \
  -d '{
    "question": "What is the capital of France?",
    "correct_answer": "Paris"
  }'
```

Response:
```json
{
  "status": "success",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Trivia session started",
  "question": "What is the capital of France?"
}
```

#### End a Trivia Session
```bash
curl -X POST http://localhost:8000/api/trivia/session/end \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-super-secret-admin-key-here"
```

Response:
```json
{
  "status": "success",
  "message": "Trivia session ended",
  "correct_answer": "Paris",
  "successful_attempts": ["john_doe"]
}
```

### Question & Answer

#### Get Current Question
```bash
curl -X GET http://localhost:8000/api/trivia/question
```

Response (active session):
```json
{
  "status": "success",
  "question": "What is the capital of France?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true,
  "correct_answer": null
}
```

#### Submit an Answer
```bash
curl -X POST http://localhost:8000/api/trivia/answer \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "answer": "PARIS"
  }'
```

Response (correct):
```json
{
  "status": "success",
  "is_correct": true,
  "message": "Correct!",
  "score": 1
}
```

Response (incorrect):
```json
{
  "status": "success",
  "is_correct": false,
  "message": "Incorrect!"
}
```

### History & Leaderboard

#### Get All Attempts
```bash
curl -X GET http://localhost:8000/api/trivia/attempts
```

Response:
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

#### Get Leaderboard
```bash
curl -X GET "http://localhost:8000/api/trivia/leaderboard?limit=10&offset=0"
```

Response:
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

## Running the Demo

Execute the demo script to run all 6 user story scenarios:

```bash
chmod +x demo.sh
./demo.sh
```

This runs through:
1. Admin starts a trivia session
2. User views the current question
3. User submits a correct answer
4. Another user submits an incorrect answer
5. View all attempts history
6. View the leaderboard
7. Admin ends session and reveals answer

## Project Structure

```
src/trivia_api/
├── __init__.py
├── main.py                    # FastAPI app initialization
├── config.py                  # Environment configuration
├── database.py                # SQLAlchemy setup
├── errors.py                  # Custom exceptions
├── models/                    # Pydantic request/response models
│   ├── session.py
│   ├── answer.py
│   ├── attempt.py
│   └── leaderboard.py
├── schemas/                   # SQLAlchemy ORM models
│   ├── session.py
│   ├── attempt.py
│   └── user_score.py
├── services/                  # Business logic
│   ├── session_service.py
│   ├── answer_service.py
│   ├── attempt_service.py
│   ├── user_score_service.py
│   └── leaderboard_service.py
├── api/                       # API route handlers
│   ├── session.py
│   ├── question.py
│   ├── answer.py
│   ├── attempts.py
│   └── leaderboard.py
└── utils/                     # Utilities
    ├── auth.py                # API key authentication
    ├── validators.py          # Input validation
    └── timestamps.py          # ISO 8601 timestamp handling

migrations/                    # Alembic database migrations
.env                          # Environment variables (create from .env.example)
requirements.txt              # Python dependencies
pyproject.toml               # Code style configuration
demo.sh                      # Demo script
```

## Database

The application uses SQLite with three main tables:

### trivia_sessions
- `session_id` (UUID): Unique session identifier
- `question` (String): Question text
- `correct_answer` (String): Normalized correct answer (lowercase)
- `status` (Enum): ACTIVE or ENDED
- `started_at` (DateTime): ISO 8601 UTC timestamp
- `ended_at` (DateTime): ISO 8601 UTC timestamp (null if active)

### attempt_records
- `attempt_id` (Integer): Autoincrement ID
- `session_id` (FK): Reference to trivia_sessions
- `username` (String): User identifier
- `submitted_answer` (String): Original answer text (case preserved)
- `is_correct` (Boolean): Whether answer was correct
- `submitted_at` (DateTime): ISO 8601 UTC timestamp

### user_scores
- `user_id` (Integer): Autoincrement ID
- `username` (String): Unique user identifier
- `cumulative_score` (Integer): Total correct answers across all sessions
- `first_correct_timestamp` (DateTime): Timestamp of first correct answer (for tie-breaking)
- `last_updated` (DateTime): Last score update timestamp

## Code Quality

### Formatting with Black

```bash
black src/
```

### Linting with Ruff

```bash
ruff check src/
```

Configuration is in `pyproject.toml`.

## Common Commands

### Run with Debug Logging

```bash
PYTHONPATH=src python3 -m uvicorn trivia_api.main:app --reload --log-level debug
```

### Database Management

```bash
# Create a new migration after schema changes
PYTHONPATH=src alembic revision --autogenerate -m "Description"

# Apply all pending migrations
PYTHONPATH=src alembic upgrade head

# Rollback one migration
PYTHONPATH=src alembic downgrade -1

# Reset database to blank state
rm trivia.db && PYTHONPATH=src alembic upgrade head
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process (macOS/Linux)
kill -9 <PID>
```

### Database Lock Error

SQLite occasionally locks; simple fix:
```bash
rm trivia.db
PYTHONPATH=src alembic upgrade head
```

### ImportError: No module named 'trivia_api'

Ensure you:
1. Are in the repo root directory
2. Have venv activated
3. Set PYTHONPATH correctly: `export PYTHONPATH=src`
4. Have run `pip install -r requirements.txt`

## Testing with Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Click on each endpoint to expand details
3. Click **"Try it out"** button
4. Fill in request parameters
5. Click **"Execute"** to see response

**For admin endpoints** (`/session/start`, `/session/end`):
- Scroll to top and click the lock icon 🔒 (Authorize button)
- Enter your `ADMIN_API_KEY` value
- Click "Authorize"

## API Design Principles

- **REST conventions**: All endpoints follow standard HTTP methods (GET, POST)
- **Consistent response format**: All responses include `status` field ("success" or "error")
- **Case-insensitive answers**: Submitted answers compared in lowercase
- **ISO 8601 timestamps**: All timestamps in UTC with "Z" suffix
- **Immutable audit trail**: Answer attempts are write-once, never modified
- **Leaderboard tie-breaking**: Users with equal scores ranked by earliest correct answer acquisition

## Performance

- API responses typically <100ms for normal operations
- Handles 100+ concurrent user submissions
- SQLite suitable for demo and small-scale deployments
- For production scale, consider PostgreSQL or similar

## Architecture

- **FastAPI**: Modern async web framework with automatic OpenAPI documentation
- **SQLAlchemy**: ORM for database abstraction
- **Pydantic**: Request/response validation and serialization
- **Alembic**: Database schema migrations
- **Uvicorn**: ASGI server for async request handling

## Security Notes

- Admin API key should be changed from default in production
- All timestamps normalized to UTC to prevent timezone-based exploits
- Answer matching validates input length and prevents injection
- Database uses parameterized queries (SQLAlchemy handles this)

## Future Enhancements

- User authentication (OAuth2/JWT for regular users, not just admin API key)
- WebSocket support for real-time session updates
- Redis caching for leaderboard hot path
- PostgreSQL support for production deployments
- Rate limiting and request throttling
- Comprehensive logging and monitoring
- Automated test suite

## License

MIT

## Support

For issues, feature requests, or questions, please refer to the specification documents in `specs/001-trivia-api/`.
