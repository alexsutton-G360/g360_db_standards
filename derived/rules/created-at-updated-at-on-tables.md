---
slug: "created-at-updated-at-on-tables"
title: "Give almost every table `created_at` and `updated_at`, and let the database manage them"
temperature: "Rule"
origin: "house"
scope: "table"
why: "created-updated"
page: "tables"
group: "Row lifecycle"
companion: true
---

# Give almost every table `created_at` and `updated_at`, and let the database manage them

Both columns are `timestamptz NOT NULL DEFAULT now()`. A table that is append-only, where a row is never updated, gets `created_at` only. A table that skips either one needs a reason, stated where the table is defined.

Because: a value the database maintains is true no matter which application or script touched the row, and anything downstream, like a warehouse sync, can rely on it.

How to name and type a timestamp column in general is covered on Columns, under Dates and times.

More: companions/created-at-updated-at-on-tables.md
