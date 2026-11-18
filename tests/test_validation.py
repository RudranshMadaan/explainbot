
import pytest

from app.llm import validate_explanation


def test_valid_explanation():
    answer = (
        "A cache stores frequently used data for quick access. "
        "Think of it like keeping your favorite toy nearby. "
        "This saves time when you need it."
    )

    assert validate_explanation(answer) == answer


def test_empty_answer_rejected():
    with pytest.raises(ValueError):
        validate_explanation("")


def test_whitespace_answer_rejected():
    with pytest.raises(ValueError):
        validate_explanation("   ")


def test_missing_analogy_rejected():
    answer = (
        "A cache stores frequently used data. "
        "It helps computers retrieve information faster."
    )

    with pytest.raises(ValueError, match="analogy"):
        validate_explanation(answer)


def test_more_than_four_sentences_rejected():
    answer = (
        "First sentence. Second sentence. Third sentence. "
        "Fourth sentence. Fifth sentence."
    )

    with pytest.raises(ValueError, match="2-4 sentences"):
        validate_explanation(answer)


def test_one_sentence_rejected():
    answer = "A cache is like a nearby storage box."

    with pytest.raises(ValueError, match="2-4 sentences"):
        validate_explanation(answer)


def test_suspicious_spacing_rejected():
    answer = (
        "A cache stores data. "
        "Think of it as a nearby storage box. "
        "ThisIsSuspicious."
    )

    with pytest.raises(ValueError, match="spacing"):
        validate_explanation(answer)


def test_missing_space_rejected():
    answer = (
        "A cache stores data. "
        "Think of it like a box. "
        "This helps pocketinstead."
    )

    with pytest.raises(ValueError, match="spacing"):
        validate_explanation(answer)