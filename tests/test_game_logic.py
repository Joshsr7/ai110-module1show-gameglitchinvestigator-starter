"""Automated tests for the number guessing game logic.

Each group of tests locks in one of the bugs that was fixed, so the glitch
cannot come back without a test failing.
"""

import pytest
from logic_utils import (
    parse_guess,
    check_guess,
    apply_score,
    is_over,
    MAX_ATTEMPTS,
)


# check_guess: the starter hint was reversed, so a high guess said Too Low.
def test_guess_higher_than_secret_says_too_high():
    assert check_guess(60, 50) == "Too High"


def test_guess_lower_than_secret_says_too_low():
    assert check_guess(40, 50) == "Too Low"


def test_correct_guess_says_correct():
    assert check_guess(50, 50) == "Correct"


# apply_score: the starter subtracted points on a correct guess.
def test_correct_guess_keeps_score():
    assert apply_score(100, "Correct") == 100


def test_wrong_guess_loses_points():
    assert apply_score(100, "Too High") == 90


def test_score_never_goes_below_zero():
    assert apply_score(5, "Too Low") == 0


# is_over: the starter game never ended.
def test_game_ends_on_correct_guess():
    assert is_over(1, "Correct") is True


def test_game_ends_when_attempts_reach_limit():
    assert is_over(MAX_ATTEMPTS, "Too High") is True


def test_game_continues_when_attempts_remain():
    assert is_over(1, "Too High") is False


# parse_guess: the starter crashed on empty or non numeric input.
def test_parse_valid_number():
    assert parse_guess("42") == 42


def test_parse_strips_whitespace():
    assert parse_guess("  7 ") == 7


def test_parse_empty_raises_value_error():
    with pytest.raises(ValueError):
        parse_guess("")


def test_parse_text_raises_value_error():
    with pytest.raises(ValueError):
        parse_guess("abc")


# Edge cases at the ends of the range.
def test_lowest_guess_against_secret():
    assert check_guess(1, 100) == "Too Low"


def test_highest_guess_against_secret():
    assert check_guess(100, 1) == "Too High"
