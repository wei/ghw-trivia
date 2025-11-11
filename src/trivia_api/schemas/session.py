"""SQLAlchemy ORM model for trivia sessions."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, String, create_engine
from sqlalchemy.orm import relationship

from trivia_api.database import Base
from trivia_api.utils.timestamps import get_utc_now
import enum


class SessionStatus(str, enum.Enum):
    """Enumeration for session status."""

    ACTIVE = "ACTIVE"
    ENDED = "ENDED"


class TriviaSessionORM(Base):
    """SQLAlchemy ORM model for trivia sessions."""

    __tablename__ = "trivia_sessions"

    session_id = Column(String(36), primary_key=True, index=True)
    question = Column(String(500), nullable=False)
    correct_answer = Column(String(200), nullable=False)  # Stored in normalized form
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE, nullable=False)
    started_at = Column(DateTime, default=get_utc_now, nullable=False)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    attempts = relationship("AttemptRecordORM", back_populates="session")

    def __repr__(self):
        """String representation."""
        return f"<TriviaSessionORM session_id={self.session_id} status={self.status}>"
