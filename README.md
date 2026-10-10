# Game Glitch Investigator

A small number guessing game built with Streamlit. The AI generated starter
had several glitches. This repo contains the repaired game, with the core
logic refactored into logic_utils.py and automated tests in tests.

## How to run

1. pip install -r requirements.txt
2. python -m streamlit run app.py

## How to test

Run pytest from the project root:

```
python -m pytest
```

## Demo Walkthrough

1. User enters a guess of 40
2. Game returns Too Low
3. User enters a guess of 70, game returns Too High
4. Score drops by ten for each wrong guess and stays put on a correct guess
5. User enters the secret number, game returns Correct and shows the number
6. Game ends after the correct guess, or after seven attempts if the number is not found

## What was fixed

1. The hint was reversed, so a high guess said Too Low. Moved into check_guess and corrected.
2. The score dropped on a correct guess. Now a wrong guess costs points, a correct guess keeps the score, and the score never goes below zero.
3. Empty or text input crashed the app. parse_guess now raises a clear error and the app shows a friendly message.
4. The game never ended. is_over now ends the game on a correct guess or when attempts reach the limit.

## Document Your Experience

The core logic was moved out of app.py into logic_utils.py as four small
functions: parse_guess, check_guess, apply_score, and is_over. Keeping the
logic pure made it easy to test without the interface. The reflection file
records the bug reproduction log, how AI was used as a teammate including one
suggestion that was rejected, and how each fix was verified.

## Test output

```
...............                                                          [100%]
15 passed
```

## Files

- app.py: the Streamlit interface
- logic_utils.py: the game logic
- tests/test_game_logic.py: automated tests
- reflection.md: bug log and reflection
- requirements.txt: dependencies
