"""Answer submission API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from trivia_api.database import get_db
from trivia_api.errors import TriviaAPIException
from trivia_api.models.answer import AnswerSubmitRequest, AnswerResponse
from trivia_api.services.answer_service import AnswerService
from trivia_api.services.user_score_service import UserScoreService

router = APIRouter(prefix="/api/trivia", tags=["Answer Submission"])


@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    request: AnswerSubmitRequest,
    db: Session = Depends(get_db),
):
    """
    Submit an answer to the current active question.

    Returns immediate feedback with correctness and updated score if correct.
    """
    try:
        result = AnswerService.submit_answer(db, request.username, request.answer)

        # If answer was correct, increment score
        score = None
        if result["is_correct"]:
            user_score = UserScoreService.increment_score(db, request.username)
            score = user_score.cumulative_score

        return AnswerResponse(
            status="success",
            is_correct=result["is_correct"],
            message=result["message"],
            score=score,
        )
    except TriviaAPIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
