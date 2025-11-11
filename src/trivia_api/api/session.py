"""Session management API endpoints."""
from fastapi import APIRouter, Depends, Header, HTTPException

from sqlalchemy.orm import Session

from trivia_api.database import get_db
from trivia_api.errors import TriviaAPIException
from trivia_api.models.session import (
    SessionStartRequest,
    SessionStartResponse,
    SessionEndResponse,
)
from trivia_api.services.session_service import SessionService
from trivia_api.utils.auth import verify_admin_api_key
from trivia_api.utils.timestamps import to_iso8601

router = APIRouter(prefix="/api/trivia", tags=["Session Management"])


@router.post("/session/start", response_model=SessionStartResponse)
async def start_session(
    request: SessionStartRequest,
    db: Session = Depends(get_db),
    x_api_key: str = Header(None),
):
    """
    Start a new trivia session.

    Requires admin authentication via X-API-Key header.
    """
    try:
        verify_admin_api_key(x_api_key)
    except TriviaAPIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    try:
        session = SessionService.start_session(db, request.question, request.correct_answer)

        return SessionStartResponse(
            status="success",
            session_id=session.session_id,
            message="Trivia session started",
            question=session.question,
        )
    except TriviaAPIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/session/end", response_model=SessionEndResponse)
async def end_session(
    db: Session = Depends(get_db),
    x_api_key: str = Header(None),
):
    """
    End the current trivia session and reveal the answer.

    Requires admin authentication via X-API-Key header.
    """
    try:
        verify_admin_api_key(x_api_key)
    except TriviaAPIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    try:
        session = SessionService.end_session(db)
        successful_attempts = SessionService.get_successful_attempts(
            db, session.session_id
        )

        return SessionEndResponse(
            status="success",
            message="Trivia session ended",
            correct_answer=session.correct_answer,
            successful_attempts=successful_attempts,
        )
    except TriviaAPIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
