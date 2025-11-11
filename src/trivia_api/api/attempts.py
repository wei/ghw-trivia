"""Attempt history API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from trivia_api.database import get_db
from trivia_api.models.attempt import AttemptsResponse
from trivia_api.services.attempt_service import AttemptService

router = APIRouter(prefix="/api/trivia", tags=["Attempt History"])


@router.get("/attempts", response_model=AttemptsResponse)
async def get_all_attempts(db: Session = Depends(get_db)):
    """
    Retrieve all answer attempts across all sessions.

    Attempts are ordered chronologically (most recent first).
    Includes username, correctness status, and ISO 8601 timestamp.
    """
    attempts = AttemptService.get_all_attempts(db)

    return AttemptsResponse(
        status="success",
        attempts=attempts,
    )
