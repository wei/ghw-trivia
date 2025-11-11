"""Business logic for managing attempt records."""
from typing import List
from sqlalchemy.orm import Session

from trivia_api.models.attempt import AttemptRecord
from trivia_api.schemas import AttemptRecordORM
from trivia_api.utils.timestamps import to_iso8601


class AttemptService:
    """Service layer for attempt record management."""

    @staticmethod
    def get_all_attempts(db: Session) -> List[AttemptRecord]:
        """
        Get all attempts ordered chronologically (most recent first).

        Args:
            db: Database session

        Returns:
            List of AttemptRecord Pydantic models
        """
        attempts = (
            db.query(AttemptRecordORM)
            .order_by(AttemptRecordORM.submitted_at.desc())
            .all()
        )

        return [
            AttemptRecord(
                username=attempt.username,
                is_correct=attempt.is_correct,
                timestamp=to_iso8601(attempt.submitted_at),
            )
            for attempt in attempts
        ]

    @staticmethod
    def get_attempts_for_session(db: Session, session_id: str) -> List[AttemptRecord]:
        """
        Get all attempts for a specific session.

        Args:
            db: Database session
            session_id: Session identifier

        Returns:
            List of AttemptRecord Pydantic models ordered chronologically
        """
        attempts = (
            db.query(AttemptRecordORM)
            .filter(AttemptRecordORM.session_id == session_id)
            .order_by(AttemptRecordORM.submitted_at.desc())
            .all()
        )

        return [
            AttemptRecord(
                username=attempt.username,
                is_correct=attempt.is_correct,
                timestamp=to_iso8601(attempt.submitted_at),
            )
            for attempt in attempts
        ]
