"""Pydantic models for leaderboard endpoints."""
from pydantic import BaseModel, Field


class LeaderboardEntry(BaseModel):
    """Model for a single leaderboard entry."""

    rank: int = Field(description="Rank position (1-indexed)")
    username: str = Field(description="Username of the participant")
    score: int = Field(description="Cumulative score across all sessions")

    model_config = {
        "json_schema_extra": {
            "example": {
                "rank": 1,
                "username": "john_doe",
                "score": 5,
            }
        }
    }


class LeaderboardResponse(BaseModel):
    """Response model for retrieving leaderboard."""

    status: str = Field(description="Status of operation")
    leaderboard: list[LeaderboardEntry] = Field(
        default_factory=list, description="Ranked list of top scorers, ordered by score descending, with tie-breaking by earliest score acquisition"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "leaderboard": [
                    {
                        "rank": 1,
                        "username": "john_doe",
                        "score": 5,
                    },
                    {
                        "rank": 2,
                        "username": "alice_smith",
                        "score": 3,
                    },
                    {
                        "rank": 3,
                        "username": "bob_jones",
                        "score": 0,
                    },
                ],
            }
        }
    }
