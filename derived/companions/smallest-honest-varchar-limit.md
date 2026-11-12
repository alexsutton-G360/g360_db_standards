---
slug: "smallest-honest-varchar-limit"
why: "varchar-limits"
---

# Give every varchar the smallest limit your data honestly allows

## Full rule

Understand your data and constrain it as far as you practically can.

Because: a limit the database does not enforce is only an opinion, and raising a limit later is lossless while lowering one is not.

Good: `varchar(3)` for an ISO currency code, `varchar(50)` for a free-form event name
Bad:  `text` or `varchar(255)` for a currency code, `varchar(65535)` for an event name

## Why this rule exists

### Story: What turned up in the notes fields

A free-form notes field raises an old question. Nobody knows how much a customer might want to write, so why not use `varchar(65535)` and move on? Storage is cheap, and a field that is not indexed costs little to keep wide.

Groups360 has had notes fields with no real limit, and they did receive values far beyond anything a limit would have allowed. That can look like proof that leaving them wide open was wise. It was the opposite. In one case a user pasted the contents of an entire 20-page PDF into the field. In another, a large block of HTML code arrived. In a third, the field held a contact list that had nothing to do with the booking. Every one of those values was garbage or an input error, and every one broke something downstream that took many hours across several teams to fix.

Where this has happened, the ending is the same: a constraint ends up on the database column, because it always does eventually. Skipping the work at the start does not remove it. It hands the work to someone else, later, with more hours attached.

The deeper reason is that the database is the source of truth. A constraint kept in a front end or an API is only an opinion, and it disappears when that code changes. A database constraint is true at the lowest level a thing can be true, and stays true. A limit set too low has an easy remedy, because raising a `varchar` limit loses nothing. Lowering one cannot be done without deciding what to do with the data that no longer fits.
