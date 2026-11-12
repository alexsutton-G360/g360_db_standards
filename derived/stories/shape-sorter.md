---
slug: "shape-sorter"
title: "The shape sorter"
serves: ["id-guid-identifier", "lowercase-only", "varchar-vs-text"]
page: "columns"
---

# The shape sorter

A table at Groups360 holds orchestration data that links two other kinds of record. It has a column called `id` and a column called `guid`, and both are what they say they are. It also has columns named `RoomBookingId` and `SpaceBookingId`, in capital letters and lowercase, exactly as written. Both point to records elsewhere in the same database, and both hold guids, not ids. Each is a `text` column.

Every decision in that design looks small by itself, and each one makes the next harder to see.

The mixed-case names are the first. Postgres folds an unquoted name to lowercase, so `RoomBookingId` has to be wrapped in double quotes every time it is written, or the query fails with a message that the column does not exist.

The `Id` ending is the second. An analyst who has learned what `id` means across the rest of the database reads it as a bigint key and writes the query to match. The table already holds a real `id` and a real `guid`, correctly labeled, which makes the guess more natural.

The guid inside it is the third, and the `text` type is the fourth, because it turns the mistake into a silence. A `uuid` column asked for the wrong kind of value says so at once: invalid input syntax for type uuid. A `text` column accepts anything and compares it as a string, so a query for an id that was never going to match returns no rows and no complaint. The analyst sees an empty result and takes it for missing data. A booking that is known to exist does not show up, and the analysis stops making sense. The explanation is in the name and the type, nowhere near the empty result. It has happened often enough that the table is known for it.

A child's shape-sorting toy makes the point. A `text` column is the hole that every shape fits through: guids, ids, stray spaces, a value in the wrong case. Nothing is refused, so nothing ever says what went wrong. A column typed for what it holds refuses what does not belong, and that refusal is the only message the person at the keyboard will get.

The table sits at the intersection of financial reporting, which is where the cost lands. Whoever named the columns was not the one who paid for them. Everyone who queries it afterward did, one empty result at a time. The names, the types, and the case cost the least to get right when the table is designed and the most to correct after it is in use, since correcting means a migration on a table that reporting depends on.
