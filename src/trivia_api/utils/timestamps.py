"""ISO 8601 timestamp utilities."""
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    """
    Get current UTC timestamp.

    Returns:
        Current datetime in UTC timezone
    """
    return datetime.now(timezone.utc)


def to_iso8601(dt: datetime) -> str:
    """
    Convert datetime to ISO 8601 string format.

    Args:
        dt: Datetime object

    Returns:
        ISO 8601 formatted string (e.g., "2025-11-11T14:30:45Z")
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")
