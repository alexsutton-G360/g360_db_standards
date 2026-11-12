---
slug: "soft-delete-default"
title: "Soft-delete rows by default, with a `deleted_at` timestamp, unless there is a reason not to"
temperature: "Default"
origin: "house"
scope: "table"
why: "soft-deletes"
page: "tables"
group: "Row lifecycle"
companion: true
---

# Soft-delete rows by default, with a `deleted_at` timestamp, unless there is a reason not to

At Groups360, a row that is deleted from the application's point of view stays in the table, with a `deleted_at` timestamp set. The column is a `timestamptz` and is null while the row is live. The shared trigger moves `updated_at` in the same statement, so anything that follows `updated_at`, like a warehouse sync, sees the deletion as a change.

Start with soft delete, and ask whether you need anything else. Either of these is a reason to go another way:

- The data never changes or goes away, like an audit log or an event stream. It needs no `deleted_at` at all.
- The table is so large that keeping every deleted row would weigh on every query and index. Look to a retention policy or partitioning instead.

A row that stays also keeps the rows that point at it from being orphaned.

How to name and type a timestamp column in general is covered on Columns, under Dates and times. This rule assumes tables of modest size. See the note on scale on the Index.

Because: a deleted row that stays can still be explained, followed by a sync, and pointed at, and Groups360's tables are small enough that keeping it is cheap.

Good: a row marked with `deleted_at` when a user removes it
Bad:  a row removed with `DELETE`, leaving no trace that it ever existed

More: companions/soft-delete-default.md
