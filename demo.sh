#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API="http://localhost:8000"
ADMIN_KEY="your-super-secret-admin-key-here"

echo -e "${BLUE}🎯 Trivia API Demo Script${NC}\n"
echo "Make sure the API server is running: PYTHONPATH=src python3 -m uvicorn trivia_api.main:app"
echo ""

# Step 1: Start session
echo -e "${BLUE}1️⃣  Starting trivia session...${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$API/api/trivia/session/start" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ADMIN_KEY" \
  -d '{
    "question": "What is the capital of France?",
    "correct_answer": "Paris"
  }')
SESSION_ID=$(echo $SESSION_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])")
echo -e "${GREEN}✓ Session started: $SESSION_ID${NC}\n"

# Step 2: Get question
echo -e "${BLUE}2️⃣  Retrieving question...${NC}"
curl -s -X GET "$API/api/trivia/question" | python3 -m json.tool
echo ""

# Step 3: Submit correct answer
echo -e "${BLUE}3️⃣  John submitting correct answer...${NC}"
curl -s -X POST "$API/api/trivia/answer" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "answer": "PARIS"}' | python3 -m json.tool
echo ""

# Step 4: Submit incorrect answer
echo -e "${BLUE}4️⃣  Jane submitting incorrect answer...${NC}"
curl -s -X POST "$API/api/trivia/answer" \
  -H "Content-Type: application/json" \
  -d '{"username": "jane_smith", "answer": "London"}' | python3 -m json.tool
echo ""

# Step 5: View attempts
echo -e "${BLUE}5️⃣  Viewing all attempts...${NC}"
curl -s -X GET "$API/api/trivia/attempts" | python3 -m json.tool
echo ""

# Step 6: View leaderboard
echo -e "${BLUE}6️⃣  Viewing leaderboard...${NC}"
curl -s -X GET "$API/api/trivia/leaderboard" | python3 -m json.tool
echo ""

# Step 7: End session
echo -e "${BLUE}7️⃣  Ending session and revealing answer...${NC}"
curl -s -X POST "$API/api/trivia/session/end" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ADMIN_KEY" | python3 -m json.tool
echo ""

echo -e "${GREEN}✅ Demo complete!${NC}"
