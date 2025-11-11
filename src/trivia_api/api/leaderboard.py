"""Leaderboard API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from trivia_api.database import get_db
from trivia_api.models.leaderboard import LeaderboardResponse
from trivia_api.services.leaderboard_service import LeaderboardService

router = APIRouter(prefix="/api/trivia", tags=["Leaderboard"])


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100, description="Maximum entries to return"),
    offset: int = Query(0, ge=0, description="Number of entries to skip"),
    db: Session = Depends(get_db),
):
    """
    Retrieve the leaderboard with top scorers.

    Leaderboard is ranked by cumulative score (descending).
    For users with identical scores, ordering is by earliest score acquisition timestamp (ascending).
    Supports pagination via limit and offset query parameters.
    """
    leaderboard = LeaderboardService.get_leaderboard(db, limit=limit, offset=offset)

    return LeaderboardResponse(
        status="success",
        leaderboard=leaderboard,
    )
