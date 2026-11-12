---
slug: "database-is-source-of-truth"
title: "The database is the source of truth"
---

# The database is the source of truth

At the end of the day, the database is our source of truth for our data. If the database doesn't enforce a constraint, then the constraint is only really an opinion delivered by other parts of our system, and it will stop existing when we change front end code, API code, anything else. Database constraints are true at the lowest level a thing can be true, and they are true forever.

If the database layer doesn't enforce something, it's not a standard, it's just a convention.

This is why so many of our rules are constraints and not advice: varchar limits, `NOT NULL`, real foreign keys, check constraints. We always end up adding the constraint at the database layer eventually. The only thing you do by not doing the work up front is pass the buck to someone else and multiply the number of man-hours required to fix it.

Database structures should also reflect the truth of your data. If an address has the same structure whether it belongs to a user or an org, the design should say so, and not hold two copies of the same table.
