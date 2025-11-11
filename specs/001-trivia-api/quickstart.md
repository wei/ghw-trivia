# Quickstart: Trivia API

**Date**: November 11, 2025  
**Phase**: 1 - Design & Contracts  
**Status**: Ready for Development

## Overview

The Trivia API is a FastAPI-based REST API for managing trivia question sessions, recording user answers, and maintaining a leaderboard of top scorers.

**Key Features**:
- ✅ Admin starts/ends trivia sessions with questions and answers
- ✅ Users submit answers and receive immediate feedback
- ✅ Case-insensitive answer matching
- ✅ Automatic scoring and leaderboard ranking
- ✅ Complete audit trail with timestamps
- ✅ Concurrent request handling (100+ users)
- ✅ Interactive API documentation (Swagger UI)

---

## Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **SQLite3** (usually bundled with Python)
- **Git** (for cloning the repository)

---

## Project Setup

### 1. Clone the Repository

```bash
cd /path/to/ghw-trivia
git checkout 001-trivia-api
```

### 2. Create Virtual Environment

```bash
# Create venv in project root
python3 -m venv venv

# Activate venv
source venv/bin/activate          # macOS/Linux
# or
venv\Scripts\activate              # Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Required packages** (in `requirements.txt`):
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
alembic==1.13.0
python-dotenv==1.0.0
```

### 4. Environment Configuration

Create `.env` file in repo root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Admin API Key (generate a secure random string)
ADMIN_API_KEY=your-super-secret-admin-key-here

# Database
DATABASE_URL=sqlite:///./trivia.db

# Server
DEBUG=True
LOG_LEVEL=INFO
```

### 5. Initialize Database

```bash
# Create database tables
alembic upgrade head
```

This creates:
- `trivia_sessions` table
- `attempt_records` table
- `user_scores` table

---

## Running the Server

### Start Development Server

```bash
# From project root with venv activated
uvicorn trivia_api.main:app --reload --host 0.0.0.0 --port 8000
```

Output should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Access API Documentation

Once server is running:

- **Swagger UI** (interactive): http://localhost:8000/docs
- **ReDoc** (alternative): http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Demo Scenarios

### Scenario 1: Start Session and Submit Answers

**Step 1: Start a trivia session (Admin)**

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

**Step 2: View current question (User)**

```bash
curl -X GET http://localhost:8000/api/trivia/question
```

Response:
```json
{
  "status": "success",
  "question": "What is the capital of France?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": true
}
```

**Step 3: Submit correct answer (User 1)**

```bash
curl -X POST http://localhost:8000/api/trivia/answer \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "answer": "PARIS"
  }'
```

Response (note: case-insensitive matching):
```json
{
  "status": "success",
  "is_correct": true,
  "message": "Correct!",
  "score": 1
}
```

**Step 4: Submit incorrect answer (User 2)**

```bash
curl -X POST http://localhost:8000/api/trivia/answer \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_smith",
    "answer": "London"
  }'
```

Response:
```json
{
  "status": "success",
  "is_correct": false,
  "message": "Incorrect!"
}
```

**Step 5: Prevent duplicate answers (User 1 tries again)**

```bash
curl -X POST http://localhost:8000/api/trivia/answer \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "answer": "Paris"
  }'
```

Response:
```json
{
  "status": "error",
  "message": "You have already answered this question"
}
```

**Step 6: View all attempts**

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

**Step 7: View leaderboard**

```bash
curl -X GET "http://localhost:8000/api/trivia/leaderboard?limit=10"
```

Response:
```json
{
  "status": "success",
  "leaderboard": [
    {
      "rank": 1,
      "username": "john_doe",
      "score": 1
    },
    {
      "rank": 2,
      "username": "jane_smith",
      "score": 0
    }
  ]
}
```

**Step 8: End session and reveal answer (Admin)**

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
  "correct_answer": "Paris"
}
```

**Step 9: Verify session ended - question now shows answer**

```bash
curl -X GET http://localhost:8000/api/trivia/question
```

Response:
```json
{
  "status": "success",
  "question": "What is the capital of France?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_active": false,
  "correct_answer": "Paris"
}
```

### Scenario 2: Demo Script (All Steps Automated)

Create `demo.sh` in project root:

```bash
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API="http://localhost:8000"
ADMIN_KEY="your-super-secret-admin-key-here"

echo -e "${BLUE}🎯 Trivia API Demo Script${NC}\n"

# Step 1: Start session
echo -e "${BLUE}1️⃣  Starting trivia session...${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$API/api/trivia/session/start" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ADMIN_KEY" \
  -d '{
    "question": "What is the capital of France?",
    "correct_answer": "Paris"
  }')
SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
echo -e "${GREEN}✓ Session started: $SESSION_ID${NC}\n"

# Step 2: Get question
echo -e "${BLUE}2️⃣  Retrieving question...${NC}"
curl -s -X GET "$API/api/trivia/question" | jq '.'
echo ""

# Step 3: Submit correct answer
echo -e "${BLUE}3️⃣  John submitting correct answer...${NC}"
curl -s -X POST "$API/api/trivia/answer" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "answer": "PARIS"}' | jq '.'
echo ""

# Step 4: Submit incorrect answer
echo -e "${BLUE}4️⃣  Jane submitting incorrect answer...${NC}"
curl -s -X POST "$API/api/trivia/answer" \
  -H "Content-Type: application/json" \
  -d '{"username": "jane_smith", "answer": "London"}' | jq '.'
echo ""

# Step 5: View attempts
echo -e "${BLUE}5️⃣  Viewing all attempts...${NC}"
curl -s -X GET "$API/api/trivia/attempts" | jq '.'
echo ""

# Step 6: View leaderboard
echo -e "${BLUE}6️⃣  Viewing leaderboard...${NC}"
curl -s -X GET "$API/api/trivia/leaderboard" | jq '.'
echo ""

# Step 7: End session
echo -e "${BLUE}7️⃣  Ending session and revealing answer...${NC}"
curl -s -X POST "$API/api/trivia/session/end" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ADMIN_KEY" | jq '.'
echo ""

echo -e "${GREEN}✅ Demo complete!${NC}"
```

Run the demo:
```bash
chmod +x demo.sh
./demo.sh
```

---

## Testing with Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Click on each endpoint to expand details
3. Click **"Try it out"** button on any endpoint
4. Fill in request parameters
5. Click **"Execute"** to see response

**Important**: For admin endpoints (`/session/start`, `/session/end`), add the API key header:
- Click the lock icon 🔒 (Authorize button)
- Enter your `X-API-Key` value
- Click "Authorize"

---

## Project Structure

```
trivia_api/
├── __init__.py
├── main.py                    # FastAPI app setup
├── config.py                  # Environment config
├── database.py                # SQLAlchemy setup
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
│   └── leaderboard_service.py
├── api/                       # API routes
│   ├── session.py
│   ├── question.py
│   ├── answer.py
│   ├── attempts.py
│   └── leaderboard.py
└── utils/                     # Utilities
    ├── auth.py
    ├── validators.py
    └── timestamps.py

migrations/                    # Alembic database migrations
.env                          # Environment variables (create from .env.example)
requirements.txt              # Python dependencies
docker-compose.yaml           # Docker development stack
Dockerfile                    # Container configuration
```

---

## Common Commands

### Run with Different Settings

```bash
# Production-like (no auto-reload)
uvicorn trivia_api.main:app --host 0.0.0.0 --port 8000

# With debug logging
uvicorn trivia_api.main:app --reload --log-level debug
```

### Database Management

```bash
# Create new migration after schema changes
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Reset database to blank state
rm trivia.db && alembic upgrade head
```

### Reset Demo Data

```bash
# Delete database and reinitialize (for fresh demo)
rm trivia.db && alembic upgrade head
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process (macOS/Linux)
kill -9 <PID>
```

### Database Lock Error

```bash
# SQLite sometimes locks; simple fix is to delete and reinit
rm trivia.db
alembic upgrade head
```

### ImportError: No module named 'trivia_api'

Ensure you:
1. Are in the repo root directory
2. Have venv activated
3. Have run `pip install -r requirements.txt`

---

## Next Steps

**To build the implementation**:

1. Create the FastAPI main app (`trivia_api/main.py`)
2. Define Pydantic models (`trivia_api/models/`)
3. Define SQLAlchemy schemas (`trivia_api/schemas/`)
4. Implement services (`trivia_api/services/`)
5. Create API routers (`trivia_api/api/`)
6. Set up authentication middleware
7. Test each endpoint via Swagger UI

**See**: `/speckit.tasks` command to generate task breakdown for implementation.

---

**Phase 1 Status**: ✅ **QUICKSTART COMPLETE - Ready for Phase 1 agent context update**
