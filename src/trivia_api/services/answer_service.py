"""Business logic for answer submission and validation."""
from sqlalchemy.orm import Session

from trivia_api.errors import DuplicateAnswerError, NoActiveSessionError
from trivia_api.schemas import AttemptRecordORM, TriviaSessionORM, SessionStatus
from trivia_api.services.session_service import SessionService
from trivia_api.utils.timestamps import get_utc_now
from trivia_api.utils.validators import check_answers_match


class AnswerService:
    """Service layer for answer submission and validation."""

    @staticmethod
    def check_duplicate_answer(db: Session, session_id: str, username: str) -> bool:
        """
        Check if user has already answered this session's question.

        Args:
            db: Database session
            session_id: Session identifier
            username: Username

        Returns:
            True if user has already answered, False otherwise
        """
        existing = (
            db.query(AttemptRecordORM)
            .filter(
                AttemptRecordORM.session_id == session_id,
                AttemptRecordORM.username == username,
            )
            .first()
        )

        return existing is not None

    @staticmethod
    def submit_answer(
        db: Session, username: str, answer: str
    ) -> dict:
        """
        Submit an answer to the current active question.

        Args:
            db: Database session
            username: Username of participant
            answer: Submitted answer text

        Returns:
            Dictionary with submission result including correctness and updated score

        Raises:
            NoActiveSessionError: If no active session exists
            DuplicateAnswerError: If user already answered this session's question
        """
        # Get active session
        session = SessionService.get_active_session(db)
        if not session:
            raise NoActiveSessionError()

        # Check for duplicate answer
        if AnswerService.check_duplicate_answer(db, session.session_id, username):
            raise DuplicateAnswerError()

        # Check if answer is correct (case-insensitive)
        is_correct = check_answers_match(answer, session.correct_answer)

        # Record attempt
        attempt = AttemptRecordORM(
            session_id=session.session_id,
            username=username,
            submitted_answer=answer,  # Original case preserved
            is_correct=is_correct,
            submitted_at=get_utc_now(),
        )

        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        result = {
            "is_correct": is_correct,
            "message": "Correct!" if is_correct else "Incorrect!",
            "score": None,
        }

        return result
