---
slug: "hidden-vs-displayed"
title: "A column named for the button"
serves: ["bend-or-break", "positive-voice"]
page: "columns"
---

# A column named for the button

Columns are named in the positive voice by default. That is not about affirmation or feel-good positivity. It is about making code easier to read and reason about. `if not is_hidden` reads more cleanly than `if not is_not_shown`, because extra words and negations in a column name make the code that uses it less intuitive than it needs to be.

There is flexibility here. `is_displayed` can be argued to be the better column, because `if is_displayed` is even cleaner than `if not is_hidden`. That is absolutely true. But in a given context the word "display" may be less clear than "hidden", for example when the field is controlled by a button labeled "hide".

The goal is clarity and intuitiveness. The rule bends when doing so makes things more understandable, and a short check with another engineer confirms the choice reads the way the author thinks it does.
