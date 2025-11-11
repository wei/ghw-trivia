"""Input validation and normalization utilities."""


def normalize_answer(answer: str) -> str:
    """
    Normalize answer text for comparison.

    Converts to lowercase and strips whitespace for case-insensitive matching.

    Args:
        answer: Raw answer text

    Returns:
        Normalized answer for comparison
    """
    return answer.lower().strip()


def check_answers_match(submitted: str, correct: str) -> bool:
    """
    Check if submitted answer matches correct answer (case-insensitive).

    Args:
        submitted: User-submitted answer
        correct: Correct answer from question

    Returns:
        True if answers match (case-insensitive), False otherwise
    """
    return normalize_answer(submitted) == normalize_answer(correct)
