# AI Interactions Log

> **Stretch features only.** This file covers the two stretch features I attempted: Test Generation and Linting and Style.

---

## Test Generation (SF7)

I used Claude in Claude Code with logic_utils.py attached. Main prompt:

```
Here is parse_guess from logic_utils.py. Suggest edge case inputs that could
still break it, and write one small pytest test for each. Test the returned
(ok, value, error) tuple, not how the function is written.
```

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Empty string | prompt above | test_parse_empty_input checks ok is False and an error message is returned | Yes | A player can press Submit with an empty box, and that must not crash or count as a guess |
| Whitespace only | prompt above | test_parse_whitespace_only_input checks "   " is rejected | Yes | A stray space looks empty to the player and should be treated as empty |
| Non numeric text | prompt above | test_parse_non_numeric_text checks "abc" gives That is not a number. | Yes | The original crash risk for any number game |
| Decimal | prompt above | test_parse_decimal_is_rejected_not_truncated checks "3.9" is rejected | Yes after a fix | The starter silently turned 3.9 into 3. The first run failed, which showed the truncation bug, so I changed parse_guess to ask for a whole number |
| Negative number | follow up: "add tests for numbers outside the difficulty range" | test_parse_negative_number_out_of_range checks "-5" with range 1 to 100 is rejected | Yes | A negative guess can never be right, so it should not waste an attempt |
| Huge number | same follow up | test_parse_huge_number_out_of_range checks "999999999" is rejected | Yes | Same reason, a guess far outside the range should be refused |
| Range edges | my own addition | test_parse_range_edges_are_allowed checks 1 and 100 are accepted | Yes | I added this so the range check does not reject valid edge guesses by mistake |

Every test checks the value parse_guess returns, not how the function works inside, so the tests keep passing if the code is rewritten later.

---

## Linting & Style (SF9)

**Prompt used:**

```
Review logic_utils.py and app.py for PEP 8 style. Add a clear docstring to
every function in logic_utils.py that says what it returns. Do not change
any game behavior.
```

**Linting output before** (pycodestyle on the starter app.py):

```
app.py:4:1: E302 expected 2 blank lines, found 1
app.py:67:1: E305 expected 2 blank lines after class or function definition, found 1
```

**Linting output after:**

```
$ python -m pycodestyle --max-line-length=100 app.py logic_utils.py tests/test_game_logic.py
(no output, zero warnings)
```

**Changes applied:**

- Moved the game functions out of app.py into logic_utils.py, which removed both blank line warnings.
- Added docstrings to all five functions in logic_utils.py, each stating what it returns and which bug it fixed.
- Replaced the bare except Exception in parse_guess with except ValueError, which Claude flagged as too broad.
- I kept the three starter tests unchanged, because they are the original spec for check_guess.
