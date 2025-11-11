"""SQLAlchemy ORM model for user scores."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String

from trivia_api.database import Base
from trivia_api.utils.timestamps import get_utc_now


class UserScoreORM(Base):
    """SQLAlchemy ORM model for cumulative user scores."""

    __tablename__ = "user_scores"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    cumulative_score = Column(Integer, default=0, nullable=False)
    first_correct_timestamp = Column(DateTime, nullable=True)  # For tie-breaking
    last_updated = Column(DateTime, default=get_utc_now, nullable=False)

    def __repr__(self):
        """String representation."""
        return f"<UserScoreORM username={self.username} score={self.cumulative_score}>"
