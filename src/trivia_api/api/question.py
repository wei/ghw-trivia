"""Question retrieval API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from trivia_api.database import get_db
from trivia_api.models.session import QuestionResponse
from trivia_api.services.session_service import SessionService

router = APIRouter(prefix="/api/trivia", tags=["Questions"])


@router.get("/question", response_model=QuestionResponse)
async def get_question(db: Session = Depends(get_db)):
    """
    Retrieve the currently active trivia question.

    If a session is active, the correct answer is not included.
    If a session has ended, the correct answer is included.
    Returns null question if no session exists.
    """
    question_data = SessionService.get_current_question(db, reveal_answer=False)

    if not question_data:
        return QuestionResponse(
            status="success",
            question=None,
            session_id=None,
            is_active=None,
        )

    return QuestionResponse(
        status="success",
        question=question_data["question"],
        session_id=question_data["session_id"],
        is_active=question_data["is_active"],
        correct_answer=question_data["correct_answer"],
    )
