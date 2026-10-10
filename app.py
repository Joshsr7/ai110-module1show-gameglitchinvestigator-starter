"""Number guessing game built with Streamlit.

The game logic lives in logic_utils so it can be tested without the UI.
This file only reads input, calls the logic, and shows results.
"""

import random
import streamlit as st
from logic_utils import (
    MIN_NUMBER,
    MAX_NUMBER,
    MAX_ATTEMPTS,
    parse_guess,
    check_guess,
    apply_score,
    is_over,
)


def new_game():
    st.session_state.secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    st.session_state.attempts = 0
    st.session_state.score = 100
    st.session_state.history = []
    st.session_state.over = False


def main():
    st.title("Number Guessing Game")
    if "secret" not in st.session_state:
        new_game()
    if st.button("New game"):
        new_game()

    st.write("Score: %d" % st.session_state.score)
    st.write("Attempts: %d of %d" % (st.session_state.attempts, MAX_ATTEMPTS))
    raw = st.text_input("Your guess")

    if st.button("Submit guess") and not st.session_state.over:
        # FIX: parse_guess handles empty or non numeric input instead of crashing on int(raw)
        try:
            guess = parse_guess(raw)
        except ValueError:
            st.warning(
                "Please enter a whole number between %d and %d."
                % (MIN_NUMBER, MAX_NUMBER)
            )
            return

        st.session_state.attempts += 1

        # FIX: hint logic moved to check_guess and is no longer reversed
        outcome = check_guess(guess, st.session_state.secret)
        st.session_state.history.append((guess, outcome))

        # FIX: score only drops on a wrong guess, handled by apply_score
        st.session_state.score = apply_score(st.session_state.score, outcome)

        if outcome == "Correct":
            st.success("Correct. The number was %d." % st.session_state.secret)
        else:
            st.info(outcome)

        # FIX: game ends on a correct guess or when attempts reach the limit
        if is_over(st.session_state.attempts, outcome):
            st.session_state.over = True

    if st.session_state.over:
        won = any(o == "Correct" for _, o in st.session_state.history)
        if won:
            st.success("Game over. You guessed it.")
        else:
            st.error("Game over. The number was %d." % st.session_state.secret)

    if st.session_state.history:
        st.write("Guess history:")
        for g, o in st.session_state.history:
            st.write("%d gives %s" % (g, o))


if __name__ == "__main__":
    main()
