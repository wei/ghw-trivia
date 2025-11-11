"""SQLAlchemy ORM model for answer attempt records."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from trivia_api.database import Base
from trivia_api.utils.timestamps import get_utc_now


class AttemptRecordORM(Base):
    """SQLAlchemy ORM model for answer attempt audit trail."""

    __tablename__ = "attempt_records"

    attempt_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    session_id = Column(String(36), ForeignKey("trivia_sessions.session_id"), nullable=False, index=True)
    username = Column(String(100), nullable=False, index=True)
    submitted_answer = Column(String(200), nullable=False)  # Original case preserved
    is_correct = Column(Boolean, nullable=False)
    submitted_at = Column(DateTime, default=get_utc_now, nullable=False, index=True)

    # Relationships
    session = relationship("TriviaSessionORM", back_populates="attempts")

    def __repr__(self):
        """String representation."""
        return f"<AttemptRecordORM attempt_id={self.attempt_id} username={self.username} is_correct={self.is_correct}>"
