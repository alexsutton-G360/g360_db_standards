---
slug: "varchar-over-char-and-text"
why: "varchar-vs-text"
---

# Use varchar, not char or text

## Full rule

Use varchar, with a limit. Do not use char. Text is almost never right either, but there are a few narrow situations where it is, mainly data with no honest upper limit, covered below.

Because: text can outgrow the warehouse and crash billing views, while char pads values with whitespace for no benefit.

## Why this rule exists

### Story: The shape sorter

A table at Groups360 holds orchestration data that links two other kinds of record. It has a column called `id` and a column called `guid`, and both are what they say they are. It also has columns named `RoomBookingId` and `SpaceBookingId`, in capital letters and lowercase, exactly as written. Both point to records elsewhere in the same database, and both hold guids, not ids. Each is a `text` column.

Every decision in that design looks small by itself, and each one makes the next harder to see.

The mixed-case names are the first. Postgres folds an unquoted name to lowercase, so `RoomBookingId` has to be wrapped in double quotes every time it is written, or the query fails with a message that the column does not exist.

The `Id` ending is the second. An analyst who has learned what `id` means across the rest of the database reads it as a bigint key and writes the query to match. The table already holds a real `id` and a real `guid`, correctly labeled, which makes the guess more natural.

The guid inside it is the third, and the `text` type is the fourth, because it turns the mistake into a silence. A `uuid` column asked for the wrong kind of value says so at once: invalid input syntax for type uuid. A `text` column accepts anything and compares it as a string, so a query for an id that was never going to match returns no rows and no complaint. The analyst sees an empty result and takes it for missing data. A booking that is known to exist does not show up, and the analysis stops making sense. The explanation is in the name and the type, nowhere near the empty result. It has happened often enough that the table is known for it.

A child's shape-sorting toy makes the point. A `text` column is the hole that every shape fits through: guids, ids, stray spaces, a value in the wrong case. Nothing is refused, so nothing ever says what went wrong. A column typed for what it holds refuses what does not belong, and that refusal is the only message the person at the keyboard will get.

The table sits at the intersection of financial reporting, which is where the cost lands. Whoever named the columns was not the one who paid for them. Everyone who queries it afterward did, one empty result at a time. The names, the types, and the case cost the least to get right when the table is designed and the most to correct after it is in use, since correcting means a migration on a table that reporting depends on.

### Story: The text field that took down the views

Groups360 runs two kinds of database. The operational databases sit under Groupsync and the private label apps, and run PostgreSQL (version 17.11 as of November 2026, which may have changed since). Downstream is a data warehouse in Amazon Redshift, which is built differently and has a different toolkit. A sync tool, currently Stitch, copies flagged tables from one to the other and reshapes the data to fit.

Postgres allows far longer values than the warehouse does. Redshift has no `text` type at all, and its `varchar` stops at 65,535. A `text` column is where the mismatch bites, and the same sequence has played out more than once:

1. A field in Groupsync is defined as `text`.
2. The sync tool keeps up, raising the `varchar` size on the warehouse copy each time a longer value arrives.
3. A value arrives that is longer than any before it. The sync tool pulls it into the source table in the warehouse and updates that table's definition to fit.
4. The views built on top of that table do not follow. A materialized view fixes its column sizes when it is created and does not inherit later changes to the table underneath.
5. The next time a view tries to pull in the new value, it fails, and stays unavailable until someone finds the offending value and widens the column in the warehouse by hand.

Those views are critical infrastructure for billing and revenue recognition, so a column type chosen at design time becomes an outage in finance reporting. That is the whole case for `varchar` over `text`, and for never going above 65,535.
