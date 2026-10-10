"""Core game logic for the number guessing game.

The functions here are pure, so they can be tested with pytest without
running Streamlit. app.py imports them and only handles the interface.
"""

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 7
WRONG_GUESS_PENALTY = 10


def parse_guess(raw):
    """Turn raw text input into a whole number guess.

    Raises ValueError when the input is empty or not a whole number, so the
    interface can show a friendly message instead of crashing.
    """
    if raw is None:
        raise ValueError("Please enter a number.")
    text = raw.strip()
    if text == "":
        raise ValueError("Please enter a number.")
    return int(text)


def check_guess(guess, secret):
    """Compare a guess to the secret and return the hint.

    Returns "Correct", "Too High", or "Too Low".
    """
    if guess == secret:
        return "Correct"
    if guess > secret:
        return "Too High"
    return "Too Low"


def apply_score(score, outcome, penalty=WRONG_GUESS_PENALTY):
    """Return the new score after one guess.

    A wrong guess costs points. A correct guess keeps the current score.
    The score never drops below zero.
    """
    if outcome == "Correct":
        return score
    return max(0, score - penalty)


def is_over(attempts, outcome):
    """Return True when the game should end.

    The game ends on a correct guess or once attempts reach the limit.
    """
    return outcome == "Correct" or attempts >= MAX_ATTEMPTS
