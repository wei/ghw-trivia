"""Business logic for trivia session management."""
from typing import Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from trivia_api.errors import ActiveSessionExistsError, NoActiveSessionError
from trivia_api.schemas import TriviaSessionORM, SessionStatus, AttemptRecordORM
from trivia_api.utils.timestamps import get_utc_now
from trivia_api.utils.validators import normalize_answer


class SessionService:
    """Service layer for session management."""

    @staticmethod
    def start_session(db: Session, question: str, correct_answer: str) -> TriviaSessionORM:
        """
        Start a new trivia session.

        Args:
            db: Database session
            question: Question text
            correct_answer: Correct answer text

        Returns:
            Created TriviaSessionORM instance

        Raises:
            ActiveSessionExistsError: If a session is already active
        """
        # Check if active session already exists
        active_session = (
            db.query(TriviaSessionORM)
            .filter(TriviaSessionORM.status == SessionStatus.ACTIVE)
            .first()
        )

        if active_session:
            raise ActiveSessionExistsError()

        # Create new session
        session_id = str(uuid4())
        new_session = TriviaSessionORM(
            session_id=session_id,
            question=question,
            correct_answer=normalize_answer(correct_answer),  # Store normalized
            status=SessionStatus.ACTIVE,
            started_at=get_utc_now(),
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return new_session

    @staticmethod
    def get_active_session(db: Session) -> Optional[TriviaSessionORM]:
        """
        Get the currently active session, if any.

        Args:
            db: Database session

        Returns:
            Active TriviaSessionORM or None if no active session
        """
        return (
            db.query(TriviaSessionORM)
            .filter(TriviaSessionORM.status == SessionStatus.ACTIVE)
            .first()
        )

    @staticmethod
    def get_current_question(
        db: Session, reveal_answer: bool = False
    ) -> Optional[dict]:
        """
        Get current question and session info.

        Args:
            db: Database session
            reveal_answer: Whether to include correct answer in response

        Returns:
            Dictionary with question data or None if no active session
        """
        session = SessionService.get_active_session(db)

        if not session:
            # Check if there's a recently ended session to still display
            recent_session = (
                db.query(TriviaSessionORM)
                .order_by(TriviaSessionORM.ended_at.desc())
                .first()
            )
            if recent_session and recent_session.status == SessionStatus.ENDED:
                session = recent_session
            else:
                return None

        return {
            "question": session.question,
            "session_id": session.session_id,
            "is_active": session.status == SessionStatus.ACTIVE,
            "correct_answer": session.correct_answer if reveal_answer or session.status == SessionStatus.ENDED else None,
        }

    @staticmethod
    def end_session(db: Session) -> TriviaSessionORM:
        """
        End the currently active session.

        Args:
            db: Database session

        Returns:
            Updated TriviaSessionORM instance

        Raises:
            NoActiveSessionError: If no active session exists
        """
        session = SessionService.get_active_session(db)

        if not session:
            raise NoActiveSessionError()

        session.status = SessionStatus.ENDED
        session.ended_at = get_utc_now()

        db.commit()
        db.refresh(session)

        return session

    @staticmethod
    def get_successful_attempts(db: Session, session_id: str) -> list[str]:
        """
        Get list of usernames who answered correctly for a session.

        Args:
            db: Database session
            session_id: Session identifier

        Returns:
            List of usernames who answered correctly
        """
        attempts = (
            db.query(AttemptRecordORM.username)
            .filter(
                AttemptRecordORM.session_id == session_id,
                AttemptRecordORM.is_correct == True,
            )
            .distinct()
            .all()
        )

        return [attempt[0] for attempt in attempts]
