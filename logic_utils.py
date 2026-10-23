"""Game logic for the Glitchy Guesser number game.

These functions were refactored out of app.py so they can be tested with
pytest without running Streamlit. app.py imports them and only handles the
interface and session state.
"""

DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 200),
}

WRONG_GUESS_PENALTY = 5


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive (low, high) range for a difficulty.

    FIX: Hard used to be 1 to 50, which made it easier than Normal.
    Hard is now the widest range. Unknown values fall back to Normal.
    """
    return DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES["Normal"])


def parse_guess(raw: str, low: int = None, high: int = None):
    """Parse user input into a whole number guess.

    Returns (ok, guess_int, error_message). When low and high are given,
    a guess outside the range is rejected so it does not cost an attempt.
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    text = raw.strip()
    try:
        value = int(text)
    except ValueError:
        try:
            float(text)
        except ValueError:
            return False, None, "That is not a number."
        # FIX: decimals used to be silently cut down, 3.9 became 3.
        return False, None, "Enter a whole number."

    if low is not None and high is not None and not low <= value <= high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """Compare a guess to the secret and return the outcome.

    Returns "Win", "Too High", or "Too Low". Both values are compared as
    integers.

    FIX: the starter turned the secret into a string on every other
    attempt, which raised a TypeError and fell back to comparing text, so
    "9" counted as higher than "50". The string fallback is removed.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint_message(outcome: str):
    """Return the hint shown to the player for an outcome.

    FIX: the starter told the player to go HIGHER when the guess was
    already too high. The hint now points toward the secret.
    """
    messages = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }
    return messages.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Return the new score after a guess.

    A win earns 100 points on the first attempt and 10 fewer for each extra
    attempt, never less than 10. Every wrong guess costs the same penalty.

    FIX: the starter added 5 points for a Too High guess on even attempts,
    so a wrong guess could raise the score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    if outcome in ("Too High", "Too Low"):
        return current_score - WRONG_GUESS_PENALTY

    return current_score
