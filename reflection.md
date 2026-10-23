# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The first time I ran the game it looked finished, with a difficulty sidebar, a guess box, and a debug panel, but it did not play fairly. The hints pointed the wrong way, so guessing 60 when the secret was 50 told me to go HIGHER. The same guess could get different hints on different turns, a wrong guess sometimes raised my score, and after I won, the New Game button did not actually start a new game. Switching to Easy after starting also left the secret outside the new range, so that round could never be won.

I ran the starter in a scripted Streamlit session with the secret set to 50 so the results were repeatable. This is the trace:

```
SCENARIO 1  Normal difficulty, secret 50
  start   -> info: Guess a number between 1 and 100. Attempts left: 7
  guess   '60' -> warning: Go HIGHER!
           state: attempts=2 score=5 status=playing secret=50
  guess    '9' -> warning: Go LOWER!
           state: attempts=3 score=0 status=playing secret=50
  guess    '9' -> warning: Go HIGHER!
           state: attempts=4 score=5 status=playing secret=50

SCENARIO 2  win, then press New Game
  guess   '50' -> warning: Correct! | success: You won! The secret was 50. Final score: 70
           state: attempts=2 score=70 status=won secret=50
  New Game -> info: Guess a number between 1 and 100. Attempts left: 8 | success: You already won. Start a new game to play again.
           state: attempts=0 score=70 status=won secret=2

SCENARIO 3  invalid input
  guess  'abc' -> error: That is not a number.
           state: attempts=2 score=0 status=playing secret=50

SCENARIO 4  switch to Easy after the game started
  Easy selected -> info: Guess a number between 1 and 100. Attempts left: 5
           state: attempts=1 score=0 status=playing secret=73
```

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, secret 50, Normal | Hint says Go LOWER and the score drops | Hint says Go HIGHER and the score rises from 0 to 5 | none |
| Guess 9 on attempt 3, then 9 again on attempt 4, secret 50 | Go HIGHER both times | Go LOWER first, then Go HIGHER for the same guess | none, a TypeError is caught silently inside check_guess |
| Win, then click New Game | A fresh game starts | Message says You already won and the game stays stuck | none |
| Type abc and submit | Error shown and no attempt used | Error shown but attempts go from 1 to 2 | That is not a number. |
| Switch to Easy after the game starts | Range 1 to 20 with a secret inside it | Message still says 1 to 100 and the secret stays 73, so the round cannot be won | none |
| First load on Normal | Attempts left: 8 | Attempts left: 7 | none |

**Code level causes**

1. Reversed hints: check_guess returned the message Go HIGHER for the Too High outcome and Go LOWER for Too Low.
2. Inconsistent hints: app.py turned the secret into a string on every even attempt with str(st.session_state.secret). Comparing an int to a str raised a TypeError, and the fallback compared text, so "9" counted as higher than "50".
3. Score going up on a wrong guess: update_score added 5 points for Too High whenever attempt_number was even.
4. Stuck after a round: the New Game handler reset attempts and the secret but never set status back to playing, so st.stop ran on every rerun. It also picked the secret from 1 to 100 no matter the difficulty.
5. Off by one attempts and wasted attempts: attempts started at 1, and the counter went up before the input was checked, so invalid input used up a turn.
6. Difficulty range: the secret was only chosen once, so switching difficulty kept the old secret, the info message was hardcoded to 1 to 100, and Hard used 1 to 50, which was easier than Normal.

---

## 2. How did you use AI as a teammate?

I used Claude in Claude Code inside VS Code, with app.py and logic_utils.py attached, and I started a new chat for each bug so it stayed focused.

**AI explanation of a bug:** I asked Claude why the same guess of 9 gave two different hints. It explained that on even attempts the code replaced the secret with str(st.session_state.secret), so 9 > "50" raised a TypeError, and the except block converted the guess to text and compared strings, where "9" sorts after "50".

**Correct suggestion:** Claude suggested deleting the even attempt string conversion and the TypeError fallback so check_guess always compares two integers. That was correct. I verified it with a test that check_guess(9, 50) returns Too Low and by rerunning the scripted session, where guessing 9 twice now says Go HIGHER both times.

**Suggestion I did not accept as written:** To make the three starter tests pass, Claude suggested editing the tests to unpack a tuple, outcome, message = check_guess(50, 50). I rejected that because the starter tests describe the expected behavior, so I should change the code, not the tests, and because mixing display text into the comparison made it harder to test. Instead I made check_guess return only the outcome and moved the text into a separate get_hint_message function. I verified my version by running pytest, where the original three tests pass unchanged along with the new hint tests.

---

## 3. Debugging and testing your fixes

I counted a bug as fixed only when two things agreed: a pytest test for that exact behavior passed, and the same scenario in the scripted Streamlit session showed the right result. For example, the starter test test_guess_too_high failed at first because check_guess returned a tuple, and after the refactor it passed without editing the test. For the string bug, test_single_digit_guess_is_too_low_against_two_digit_secret locks in that 9 against 50 is Too Low, and the scripted session confirmed that guessing 9 twice now gives the same hint both times. I also added edge case tests for empty input, whitespace, text, decimals, negative numbers, and huge numbers, and the final suite has 19 passing tests. Claude helped draft the edge case tests, and I kept the ones that check behavior from the outside and dropped any that tested how the code was written.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole script from top to bottom every time you click a button or type something, so a normal variable is created fresh on every click. Session state is a small dictionary that survives those reruns, which is where the secret, attempts, score, and status have to live. The New Game bug came from forgetting that rule, because it reset some session values but left status behind, so the old value kept winning on every rerun. Putting every reset in one start_new_game function fixed it, because now nothing gets forgotten.

---

## 5. Looking ahead: your developer habits

The habit I want to reuse is writing a small test that reproduces the bug before changing any code, then watching it go from failing to passing. Next time I would ask the AI to explain the logic before asking it to fix anything, since the explanation of the string comparison is what pointed me at the real cause. This project showed me that AI generated code can look complete and polished while being wrong in small ways, so I treat it as a draft that I have to prove, not an answer I can trust.
