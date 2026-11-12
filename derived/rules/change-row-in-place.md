---
slug: "change-row-in-place"
title: "Change a row in place, and do not delete it and create it again"
temperature: "Default"
origin: "general"
scope: "table"
why: "edit-in-place"
page: "tables"
group: "Row lifecycle"
second_opinion: "any teammate."
companion: true
---

# Change a row in place, and do not delete it and create it again

When the data in a row changes, update the row that exists. An updated row keeps its `id`, and anything downstream, like a warehouse sync, can see that it changed. A row that is deleted and created again gets a new `id`, and whatever already saw the old row is left holding a stray.

If what you need is "insert this row, or update it if it is already there", that is an upsert, and it is a different thing from rebuilding. Postgres does it directly with `INSERT ... ON CONFLICT DO UPDATE`. It needs a unique key to conflict on, such as the unique constraint on a junction table's pair of foreign keys. The habit of deleting and re-creating rows made sense once, when Postgres had no upsert. It does now.

There may be times when rebuilding is right. If you think yours is one, say why in writing, and ask someone before you do it.

Because: an updated row keeps its identity and leaves nothing behind. In Groups360's tables, each time rebuilding rows has been looked at, it has turned out to be the wrong choice.

Good: a child row updated where it stands when its booking changes
Bad:  all of a booking's child rows deleted and inserted again on every save

Second opinion: any teammate.

More: companions/change-row-in-place.md
