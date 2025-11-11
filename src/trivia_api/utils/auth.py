"""Admin API key authentication utilities."""
from fastapi import Header

from trivia_api.config import get_settings
from trivia_api.errors import InvalidAPIKeyError


def verify_admin_api_key(x_api_key: str = Header(None)) -> None:
    """
    Verify admin API key from request header.

    Args:
        x_api_key: API key from X-API-Key header

    Raises:
        InvalidAPIKeyError: If API key is missing or invalid
    """
    settings = get_settings()
    if not x_api_key or x_api_key != settings.ADMIN_API_KEY:
        raise InvalidAPIKeyError()
