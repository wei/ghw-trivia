"""Pydantic models for session management endpoints."""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SessionStartRequest(BaseModel):
    """Request model for starting a trivia session."""

    question: str = Field(
        ..., min_length=1, max_length=500, description="Trivia question text"
    )
    correct_answer: str = Field(
        ..., min_length=1, max_length=200, description="Correct answer text"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "What is the capital of France?",
                "correct_answer": "Paris",
            }
        }
    }


class SessionStartResponse(BaseModel):
    """Response model for starting a trivia session."""

    status: str = Field(description="Status of operation")
    session_id: str = Field(description="Unique identifier for the session")
    message: str = Field(description="Human-readable message")
    question: str = Field(description="Question text")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "Trivia session started",
                "question": "What is the capital of France?",
            }
        }
    }


class QuestionResponse(BaseModel):
    """Response model for retrieving the current question."""

    status: str = Field(description="Status of operation")
    question: Optional[str] = Field(default=None, description="Question text or null if no active session")
    session_id: Optional[str] = Field(default=None, description="Session ID if session exists")
    is_active: Optional[bool] = Field(default=None, description="Whether session is active")
    correct_answer: Optional[str] = Field(default=None, description="Correct answer (only shown if session ended)")

    model_config = {
        "json_schema_extra": {
            "example_active": {
                "status": "success",
                "question": "What is the capital of France?",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "is_active": True,
            },
            "example_ended": {
                "status": "success",
                "question": "What is the capital of France?",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "is_active": False,
                "correct_answer": "Paris",
            },
        }
    }


class SessionEndResponse(BaseModel):
    """Response model for ending a trivia session."""

    status: str = Field(description="Status of operation")
    message: str = Field(description="Human-readable message")
    correct_answer: str = Field(description="The correct answer revealed")
    successful_attempts: list = Field(
        default_factory=list, description="List of usernames who answered correctly"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "message": "Trivia session ended",
                "correct_answer": "Paris",
                "successful_attempts": ["john_doe", "alice_smith"],
            }
        }
    }
