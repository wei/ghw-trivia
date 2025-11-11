"""Base Pydantic models and response types."""
from typing import Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Base response model for all API responses."""

    status: str
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response model."""

    status: str = "error"
    message: str
