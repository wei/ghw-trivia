"""Pydantic models for answer submission endpoints."""
from typing import Optional
from pydantic import BaseModel, Field


class AnswerSubmitRequest(BaseModel):
    """Request model for submitting an answer."""

    username: str = Field(..., min_length=1, max_length=100, description="Username of the participant")
    answer: str = Field(..., min_length=1, max_length=200, description="Answer text submission")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "answer": "Paris",
            }
        }
    }


class AnswerResponse(BaseModel):
    """Response model for answer submission."""

    status: str = Field(description="Status of operation")
    is_correct: bool = Field(description="Whether the submitted answer is correct")
    message: str = Field(description="Human-readable message")
    score: Optional[int] = Field(default=None, description="Updated score if answer was correct")

    model_config = {
        "json_schema_extra": {
            "example_correct": {
                "status": "success",
                "is_correct": True,
                "message": "Correct!",
                "score": 1,
            },
            "example_incorrect": {
                "status": "success",
                "is_correct": False,
                "message": "Incorrect!",
            },
        }
    }
