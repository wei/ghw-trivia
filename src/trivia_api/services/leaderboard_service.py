"""Business logic for leaderboard management."""
from typing import Optional
from sqlalchemy.orm import Session

from trivia_api.models.leaderboard import LeaderboardEntry
from trivia_api.schemas import UserScoreORM


class LeaderboardService:
    """Service layer for leaderboard generation and ranking."""

    @staticmethod
    def get_leaderboard(
        db: Session, limit: int = 10, offset: int = 0
    ) -> list:
        """
        Get leaderboard with pagination support.

        Ranking order: Score descending, then first_correct_timestamp ascending (tie-breaking).

        Args:
            db: Database session
            limit: Maximum number of entries to return
            offset: Number of entries to skip

        Returns:
            List of LeaderboardEntry models with rank positions
        """
        # Query all users sorted by score descending, then by first_correct_timestamp ascending
        users = (
            db.query(UserScoreORM)
            .filter(UserScoreORM.cumulative_score > 0)  # Only include users with scores
            .order_by(
                UserScoreORM.cumulative_score.desc(),
                UserScoreORM.first_correct_timestamp.asc(),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        # Build leaderboard with rank positions
        leaderboard = []

        # Get total count for accurate ranking
        total_users = (
            db.query(UserScoreORM).filter(UserScoreORM.cumulative_score > 0).count()
        )

        for idx, user in enumerate(users):
            rank = offset + idx + 1

            leaderboard.append(
                LeaderboardEntry(
                    rank=rank,
                    username=user.username,
                    score=user.cumulative_score,
                )
            )

        return leaderboard

    @staticmethod
    def get_user_rank(db: Session, username: str) -> Optional[int]:
        """
        Get a specific user's rank on the leaderboard.

        Args:
            db: Database session
            username: Username to get rank for

        Returns:
            User's rank (1-indexed) or None if user not on leaderboard
        """
        user_score = (
            db.query(UserScoreORM).filter(UserScoreORM.username == username).first()
        )

        if not user_score or user_score.cumulative_score == 0:
            return None

        # Count users ranked above this user
        rank = (
            db.query(UserScoreORM)
            .filter(
                (UserScoreORM.cumulative_score > user_score.cumulative_score)
                | (
                    (UserScoreORM.cumulative_score == user_score.cumulative_score)
                    & (
                        UserScoreORM.first_correct_timestamp
                        < user_score.first_correct_timestamp
                    )
                )
            )
            .count()
        ) + 1

        return rank
