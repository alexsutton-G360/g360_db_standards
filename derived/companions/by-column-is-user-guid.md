---
slug: "by-column-is-user-guid"
why: "by-columns"
---

# A column ending in `_by` holds a user guid from identity_service

## Full rule

If a column ends in `_by`, it holds a guid that points to a user in identity_service. Never a name, an email, or free text.

Use `_by` without further conversation when all three of these are true:

1. It is always a user guid pointing at identity_service.
2. It is never unknown, so it is `NOT NULL`.
3. There is no extra texture: no anonymous users, no automated actors, nobody it could be besides a logged-in person.

Everything else is an engineering question, so here are the questions:

- Is it really a user guid? If not, do not call it `_by`. Name it for what it holds.
- Can it genuinely be unknown or not applicable? Then it is nullable, and the author must be able to say in one sentence what null means.
- Can a machine or an anonymous person do this? That is a platform decision. See the next rule.

Null never means "a machine did it" or "anonymous". Null means unknown or not applicable, as everywhere else on these pages.

Because: enough columns already end in `_by` and mean this that it has become a default, so keeping one meaning costs less than a second dialect.

Second opinion: Data Architect.

## Why this rule exists

### Story: Almost on every table

Groups360 came close to making `created_by` and `updated_by` a default on every table, filled in however the application developer saw fit. The case for doing it was strong, and it deserves to be stated at full strength.

Friction decides whether a column ever exists. If the columns arrive on every table with no questions attached, they will actually be there. The moment a developer has to stop and work through a list of conditions, many will skip the column, and the data it would have held is never recorded. A column that is right in even a fraction of cases is worth more than no column at all, and who made a change is some of the most useful information a table can hold. All of that is true.

What kept it from becoming the default is a different kind of cost. A table teaches the people who read it how to use it. A column that is meaningful in some tables and a junk drawer in others teaches readers to distrust it, and then to distrust the data around it. Some bad data will always arrive by neglect. It should never be arranged in advance. The platform also has no settled answer for what the column holds when the actor is a machine or an anonymous person, so a column filled in however each team saw fit would soon have several meanings.

The two kinds of columns also differ in what stands behind them. The database can guarantee `created_at`, because it knows when a row was written. It cannot know who the application user was, so `_by` is only as good as the application code that writes it, and that is where the value is won or lost.

That is the reason for the shape of the rule. The clean case has no gate. Anyone can add the column without asking, as long as it is always a user guid, is never unknown, and has no extra texture. Putting the friction where the risk is meets the first argument halfway, since the common case has none. Outside the clean case, the answer is not "do not". It is "start the conversation, and then, if there is time, try". These columns are valuable enough that a design able to write them consistently, in a way that is reportable and makes no assumptions others must then follow, should have them.
