# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and the game was unplayable. This repo is the
repaired version.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `python -m pytest`

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Purpose.** The player picks a difficulty and guesses a secret number within that range. Each guess gets a Go HIGHER or Go LOWER hint, the score drops for wrong guesses and rises for a win, and the round ends on a correct guess or when attempts run out.

**Bugs found and fixes applied.**

| Bug | Cause | Fix |
|-----|-------|-----|
| Hints pointed the wrong way | check_guess paired Too High with Go HIGHER | Hint text moved to get_hint_message and now points toward the secret |
| Same guess gave different hints | app.py turned the secret into a string on even attempts, so text was compared | Secret stays an integer and the string fallback was removed |
| A wrong guess could raise the score | update_score added 5 for Too High on even attempts | Every wrong guess now costs 5, a first try win scores 100 |
| New Game stayed stuck after a round | status was never reset and the secret ignored difficulty | One start_new_game function resets every piece of state |
| Invalid input used up an attempt, Attempts left was off by one | Counter started at 1 and went up before the input was checked | Counter starts at 0 and only goes up for a valid guess |
| Changing difficulty kept an out of range secret, Hard was easier than Normal | Secret was chosen once, message hardcoded to 1 to 100, Hard was 1 to 50 | A new game starts when difficulty changes, the message shows the real range, Hard is 1 to 200 |

The game logic was refactored out of app.py into logic_utils.py as get_range_for_difficulty, parse_guess, check_guess, get_hint_message, and update_score, so it can be tested without Streamlit.

## 📸 Demo Walkthrough

1. The game opens on Normal and shows Guess a number between 1 and 100. Attempts left: 8
2. User enters a guess of 60 while the secret is 50, and the game returns Go LOWER. Score goes to -5 and attempts left drops to 7
3. User enters 9, and the game returns Go HIGHER. Entering 9 again gives Go HIGHER again
4. User types abc, and the game shows That is not a number. without using an attempt
5. User enters 50, and the game shows Correct!, balloons, and You won! The secret was 50
6. User clicks New Game, and a fresh round starts with attempts and score reset
7. User switches to Easy, and the game starts a new round with Guess a number between 1 and 20. Attempts left: 6

Scripted run of the fixed game with the secret set to 50:

```
SCENARIO 1  Normal difficulty, secret 50
  start   -> info: Guess a number between 1 and 100. Attempts left: 8
  guess   '60' -> warning: Go LOWER!
           state: attempts=1 score=-5 status=playing secret=50
  guess    '9' -> warning: Go HIGHER!
           state: attempts=2 score=-10 status=playing secret=50
  guess    '9' -> warning: Go HIGHER!
           state: attempts=3 score=-15 status=playing secret=50

SCENARIO 2  win, then press New Game
  guess   '50' -> warning: Correct! | success: You won! The secret was 50. Final score: 100
           state: attempts=1 score=100 status=won secret=50
  New Game -> info: Guess a number between 1 and 100. Attempts left: 8
           state: attempts=0 score=0 status=playing secret=10

SCENARIO 3  invalid input
  guess  'abc' -> error: That is not a number.
           state: attempts=0 score=0 status=playing secret=50

SCENARIO 4  switch to Easy after the game started
  Easy selected -> info: Guess a number between 1 and 20. Attempts left: 6
           state: attempts=0 score=0 status=playing secret=19
```

## 🧪 Test Results

```
$ python -m pytest -v
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED
tests/test_game_logic.py::test_single_digit_guess_is_too_low_against_two_digit_secret PASSED
tests/test_game_logic.py::test_wrong_guess_never_raises_score PASSED
tests/test_game_logic.py::test_first_try_win_scores_100 PASSED
tests/test_game_logic.py::test_late_win_scores_at_least_10 PASSED
tests/test_game_logic.py::test_hard_range_is_wider_than_normal PASSED
tests/test_game_logic.py::test_easy_range_is_1_to_20 PASSED
tests/test_game_logic.py::test_parse_valid_number PASSED
tests/test_game_logic.py::test_parse_empty_input PASSED
tests/test_game_logic.py::test_parse_whitespace_only_input PASSED
tests/test_game_logic.py::test_parse_non_numeric_text PASSED
tests/test_game_logic.py::test_parse_decimal_is_rejected_not_truncated PASSED
tests/test_game_logic.py::test_parse_negative_number_out_of_range PASSED
tests/test_game_logic.py::test_parse_huge_number_out_of_range PASSED
tests/test_game_logic.py::test_parse_range_edges_are_allowed PASSED

============================== 19 passed in 0.06s ==============================
```

## 🚀 Stretch Features

- [x] Challenge 1, Advanced Edge Case Testing: tests for empty input, whitespace, non numeric text, decimals, negative numbers, huge numbers, and range edges. All pass, see the output above. Prompts and reasoning are in ai_interactions.md.
- [x] Challenge 3, Professional Documentation and Linting: every function in logic_utils.py has a docstring, and pycodestyle reports no warnings. The lint output and changes are in ai_interactions.md.
