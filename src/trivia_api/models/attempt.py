"""Pydantic models for attempt history endpoints."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AttemptRecord(BaseModel):
    """Model for a single attempt record."""

    username: str = Field(description="Username who submitted answer")
    is_correct: bool = Field(description="Whether answer was correct")
    timestamp: str = Field(description="ISO 8601 UTC timestamp of submission")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "is_correct": True,
                "timestamp": "2025-11-11T14:30:45Z",
            }
        }
    }


class AttemptsResponse(BaseModel):
    """Response model for retrieving all attempts."""

    status: str = Field(description="Status of operation")
    attempts: list[AttemptRecord] = Field(
        default_factory=list, description="List of all answer attempts, ordered chronologically (most recent first)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "attempts": [
                    {
                        "username": "jane_smith",
                        "is_correct": False,
                        "timestamp": "2025-11-11T14:31:20Z",
                    },
                    {
                        "username": "john_doe",
                        "is_correct": True,
                        "timestamp": "2025-11-11T14:30:45Z",
                    },
                ],
            }
        }
    }
