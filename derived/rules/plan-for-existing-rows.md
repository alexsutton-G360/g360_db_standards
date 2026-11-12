---
slug: "plan-for-existing-rows"
title: "Give a NOT NULL column a plan for the rows already in the table"
temperature: "Rule"
origin: "general"
scope: "column"
why: "not-null-existing-rows"
page: "columns"
group: "Nullability"
companion: false
---

# Give a NOT NULL column a plan for the rows already in the table

Adding a NOT NULL column to a table that already has rows, or tightening an existing nullable column to NOT NULL, needs a plan for the rows already there before the change ships. The plan is one of three:

- A default that fills the existing rows, when one value is honestly right for every old row.
- A backfill that finishes before the constraint is added, when the right value has to be worked out row by row.
- A staged deploy, when old code is still writing rows without the column. The column goes in nullable and the application starts writing it, then the backfill runs, and the constraint comes last.

Whichever plan is chosen, the values it puts in must be real. A value picked only to satisfy the constraint turns a NOT NULL column into one that lies.

The larger the table, the more care this takes. See the note on scale on the Index.

Because: the database refuses the change outright when existing rows would break it, and when a change does go through, tightening a column takes the strongest lock on the table while the rows are checked. On a busy table, either one is an outage.

Good: `is_archived` added with a default of false, because every existing row is genuinely not archived
Bad:  `contact_email` added as NOT NULL with a default of an empty string, only so the change would go through
