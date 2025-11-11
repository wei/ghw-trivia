"""Custom exception classes for the Trivia API."""


class TriviaAPIException(Exception):
    """Base exception for Trivia API."""

    def __init__(self, message: str, status_code: int = 400):
        """Initialize exception."""
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ActiveSessionExistsError(TriviaAPIException):
    """Raised when trying to start a session while one is already active."""

    def __init__(self):
        super().__init__("A trivia session is already active", 400)


class NoActiveSessionError(TriviaAPIException):
    """Raised when trying to interact with a non-existent active session."""

    def __init__(self):
        super().__init__("No active trivia session", 400)


class DuplicateAnswerError(TriviaAPIException):
    """Raised when user tries to answer the same question twice."""

    def __init__(self):
        super().__init__("You have already answered this question", 400)


class InvalidAPIKeyError(TriviaAPIException):
    """Raised when admin API key is missing or invalid."""

    def __init__(self):
        super().__init__("Admin access required", 403)
