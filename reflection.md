# Reflection

## 1. What was broken when you started?

The starter game ran but behaved wrong in several ways. The hints were backwards, so a guess above the secret was called Too Low. The score dropped every time I guessed correctly instead of rewarding the win. Empty or text input crashed the app because the code called int on the raw text with no check. The game also never ended, because the end condition compared attempts to the limit plus one hundred, which is never true in normal play.

### Bug Reproduction Logs

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
| --- | --- | --- | --- |
| guess of 60 with secret 50 | hint shows Too High | hint shows Too Low | none |
| correct guess on first try | score stays near 100 | score drops by 10 times the attempt count | none |
| empty box then Submit guess | a friendly message asking for a number | app crashes | ValueError: invalid literal for int() with base 10: '' |
| text input of abc | a friendly message asking for a number | app crashes | ValueError: invalid literal for int() with base 10: 'abc' |
| seven wrong guesses | game ends at the attempt limit | game keeps asking forever | none |

## 2. How did you use AI as a teammate?

I worked one bug at a time and started a fresh chat for each so the assistant stayed focused. I attached app.py and logic_utils.py so it could see how the interface and the logic relate.

Correct suggestion: for the reversed hint, the assistant suggested moving the comparison into a check_guess function in logic_utils.py that returns Correct, Too High, or Too Low. That was correct. I verified it by writing pytest tests where a guess of 60 against a secret of 50 returns Too High, and by playing the live game.

Incorrect or misleading suggestion: for the score bug, the assistant first suggested changing the line on a correct guess from score minus points to score plus points. That was misleading, because it still tied the score change to the correct guess and let the score grow without any limit. I rejected it. Instead I made a wrong guess cost points, kept the score unchanged on a correct guess, and floored the score at zero in an apply_score function. I verified this with tests that a correct guess keeps the score, a wrong guess loses ten, and the score never goes below zero.

## 3. Debugging and testing your fixes

I reproduced each bug from the log first, then marked the spot in the code with a FIXME comment before changing anything. I refactored the logic out of app.py into logic_utils.py so it could be tested without Streamlit, then fixed one bug at a time and reviewed every diff the assistant produced before accepting it. After each fix I ran pytest and also ran the app with streamlit to confirm the live game matched the tests. The final suite has fifteen passing tests covering the hint direction, the scoring, the end condition, the input parsing, and the edges of the number range.

## Final reflection

The main thing I learned is that AI can produce code that looks right and still behaves wrong, so my job is to verify it rather than trust it. The reversed hint and the never ending game both looked like reasonable code at a glance. Writing a test that compared expected and actual behavior is what actually proved each fix. I accepted the suggestion that matched a test and rejected the one that did not, which is the habit I want to keep: use AI as a collaborator for ideas and drafts, but let tests and my own reading of the code make the final call.
