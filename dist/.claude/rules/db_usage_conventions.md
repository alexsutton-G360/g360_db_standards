---
description: How to apply the Groups360 database design rules. They are guidelines written for the person making the change, and any of them can be bent for a stated reason. Apply when a migration or data model is written or reviewed.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All rules in this file are enumerated with the RDBUS (Rules DataBase USe) code.

The database rules in the `db_*_conventions.md` files are guidelines, not laws. They are written to the person making the change (the author), so a rule that says "ask", "tell", or "bring it to" someone is asking the author to do it. The agent, whether it is helping write a change or reviewing one, makes the author aware of a rule and what it protects. The author decides.

## Departures

RDBUS1: when a change departs from a database rule, tell the author which rule it departs from, what the rule protects (its reason, or the story its slug points to), and what the default fix would be, and then let the author decide. Never rewrite the design without asking. Reason: the rules augment the author's judgment and do not replace it.

RDBUS2: when the author keeps a departure, record it with the suppression marker in `suppression_conventions.md` (RSUP1 to RSUP3), carrying the author's own reason in the author's own words. If the author has not given a reason, ask for one. Never write, improve, or invent a reason on the author's behalf. Reason: the written reason is the proof that the departure was a decision.

RDBUS3: when a valid marker covers a departure, accept any specific reason the author gave and report the departure as an acknowledged exception, with no comment on how good the reason is. A weak reason still shows the choice was made on purpose. A marker whose reason says nothing, such as "this is fine", is not a reason, so ask for a real one.

## Decisions that belong to someone else

RDBUS4: when a rule names a person or role to consult (a "Second opinion" line, or wording such as "bring it to the Data Architect"), never contact them and never settle the question for them. Tell the author the consultation is theirs to do, name the role, and say what should be raised.

RDBUS5: when a rule is a Judgment call, the pages give no answer to apply, so put the rule's questions to the author in order and let the author decide. Where a rule says its question is open, do not guess a value either.

RDBUS6: when the author is unsure whether a rule applies, or wants to depart from it, read the rule's companion (the full rule and the stories behind it, at `.claude/examples/db_standards/<slug>.md`) before advising. Stories are evidence, not rulings. Reason: the story shows what the rule was written to protect, which is what the author's reason has to be measured against.
