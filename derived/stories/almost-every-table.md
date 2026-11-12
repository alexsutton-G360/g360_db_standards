---
slug: "almost-every-table"
title: "Almost on every table"
serves: ["by-columns"]
page: "columns"
---

# Almost on every table

Groups360 came close to making `created_by` and `updated_by` a default on every table, filled in however the application developer saw fit. The case for doing it was strong, and it deserves to be stated at full strength.

Friction decides whether a column ever exists. If the columns arrive on every table with no questions attached, they will actually be there. The moment a developer has to stop and work through a list of conditions, many will skip the column, and the data it would have held is never recorded. A column that is right in even a fraction of cases is worth more than no column at all, and who made a change is some of the most useful information a table can hold. All of that is true.

What kept it from becoming the default is a different kind of cost. A table teaches the people who read it how to use it. A column that is meaningful in some tables and a junk drawer in others teaches readers to distrust it, and then to distrust the data around it. Some bad data will always arrive by neglect. It should never be arranged in advance. The platform also has no settled answer for what the column holds when the actor is a machine or an anonymous person, so a column filled in however each team saw fit would soon have several meanings.

The two kinds of columns also differ in what stands behind them. The database can guarantee `created_at`, because it knows when a row was written. It cannot know who the application user was, so `_by` is only as good as the application code that writes it, and that is where the value is won or lost.

That is the reason for the shape of the rule. The clean case has no gate. Anyone can add the column without asking, as long as it is always a user guid, is never unknown, and has no extra texture. Putting the friction where the risk is meets the first argument halfway, since the common case has none. Outside the clean case, the answer is not "do not". It is "start the conversation, and then, if there is time, try". These columns are valuable enough that a design able to write them consistently, in a way that is reportable and makes no assumptions others must then follow, should have them.
