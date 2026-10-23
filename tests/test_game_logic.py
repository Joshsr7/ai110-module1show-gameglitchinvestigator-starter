from logic_utils import (
    check_guess,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# Starter tests. These failed at first because check_guess returned a tuple.
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# Bug: hints were backwards, a high guess said Go HIGHER.
def test_too_high_hint_says_go_lower():
    assert "LOWER" in get_hint_message("Too High")


def test_too_low_hint_says_go_higher():
    assert "HIGHER" in get_hint_message("Too Low")


# Bug: the secret became a string on even attempts, so "9" beat "50".
def test_single_digit_guess_is_too_low_against_two_digit_secret():
    assert check_guess(9, 50) == "Too Low"


# Bug: a Too High guess on an even attempt added 5 points.
def test_wrong_guess_never_raises_score():
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5
    assert update_score(0, "Too Low", 2) == -5


def test_first_try_win_scores_100():
    assert update_score(0, "Win", 1) == 100


def test_late_win_scores_at_least_10():
    assert update_score(0, "Win", 20) == 10


# Bug: Hard used 1 to 50, which was easier than Normal.
def test_hard_range_is_wider_than_normal():
    hard_low, hard_high = get_range_for_difficulty("Hard")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    assert hard_high - hard_low > normal_high - normal_low


def test_easy_range_is_1_to_20():
    assert get_range_for_difficulty("Easy") == (1, 20)


# Edge cases for parse_guess.
def test_parse_valid_number():
    assert parse_guess("42") == (True, 42, None)


def test_parse_empty_input():
    ok, value, err = parse_guess("")
    assert ok is False and value is None and err


def test_parse_whitespace_only_input():
    ok, _, _ = parse_guess("   ")
    assert ok is False


def test_parse_non_numeric_text():
    ok, value, err = parse_guess("abc")
    assert ok is False and value is None and "not a number" in err


def test_parse_decimal_is_rejected_not_truncated():
    ok, value, _ = parse_guess("3.9")
    assert ok is False and value is None


def test_parse_negative_number_out_of_range():
    ok, _, err = parse_guess("-5", 1, 100)
    assert ok is False and "between 1 and 100" in err


def test_parse_huge_number_out_of_range():
    ok, _, _ = parse_guess("999999999", 1, 100)
    assert ok is False


def test_parse_range_edges_are_allowed():
    assert parse_guess("1", 1, 100)[0] is True
    assert parse_guess("100", 1, 100)[0] is True
