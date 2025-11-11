"""Business logic for managing user scores."""
from sqlalchemy.orm import Session

from trivia_api.schemas import UserScoreORM
from trivia_api.utils.timestamps import get_utc_now


class UserScoreService:
    """Service layer for user score management."""

    @staticmethod
    def get_or_create_user_score(db: Session, username: str) -> UserScoreORM:
        """
        Get or create user score record.

        Args:
            db: Database session
            username: Username

        Returns:
            UserScoreORM instance (existing or newly created)
        """
        user_score = db.query(UserScoreORM).filter(UserScoreORM.username == username).first()

        if not user_score:
            user_score = UserScoreORM(
                username=username,
                cumulative_score=0,
                last_updated=get_utc_now(),
            )
            db.add(user_score)
            db.commit()
            db.refresh(user_score)

        return user_score

    @staticmethod
    def increment_score(db: Session, username: str) -> UserScoreORM:
        """
        Increment user's cumulative score by 1.

        Args:
            db: Database session
            username: Username

        Returns:
            Updated UserScoreORM instance
        """
        user_score = UserScoreService.get_or_create_user_score(db, username)

        # Set first_correct_timestamp only on first correct answer
        if user_score.cumulative_score == 0:
            user_score.first_correct_timestamp = get_utc_now()

        user_score.cumulative_score += 1
        user_score.last_updated = get_utc_now()

        db.commit()
        db.refresh(user_score)

        return user_score

    @staticmethod
    def get_user_score(db: Session, username: str) -> int:
        """
        Get user's current cumulative score.

        Args:
            db: Database session
            username: Username

        Returns:
            Cumulative score (0 if user not found)
        """
        user_score = db.query(UserScoreORM).filter(UserScoreORM.username == username).first()
        return user_score.cumulative_score if user_score else 0
