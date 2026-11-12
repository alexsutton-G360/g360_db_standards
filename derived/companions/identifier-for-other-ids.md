---
slug: "identifier-for-other-ids"
why: "id-guid-identifier"
---

# Use `identifier` for any identifying value that is neither an id nor a guid

## Full rule

Spell out the full word `identifier`: `external_identifier` for a value that came from another system.

Because: `external_id` would look like a foreign key to a table named `externals`.

## Why this rule exists

Rules that share this explanation (why: `id-guid-identifier`):

- `id-column-meaning`: A column named `id` is the table's bigint key, and `_id` points to one
- `guid-column-meaning`: A column named `guid` is a uuid, and `_guid` points to one

### Story: What an analyst assumes in the first week

Of all the naming misses in Groups360's databases, this family may have caused more grief than any other. It comes from the way data analysts read the data.

Within a few days of looking at the data models, an analyst learns what the common words mean. A column called `id` is a bigint primary key. A column ending in `_id` is a foreign key to the table it is named for. A column called `guid` is a uuid, and one ending in `_guid` points to another table's `guid`, often in another database. The words declare both the type and the job of the column, and the pattern is so common that the assumption forms almost at once.

After that, the analyst stops checking and starts guessing from the name. When the name is honest, the guess is right and the work moves fast. When one column breaks the pattern, such as a vendor's reference stored in `external_id`, the guess is wrong in a way nothing warns about. The name promises a foreign key to a table called `externals`, and no such table exists. The full word `identifier` avoids the false promise, because it makes no claim about type or function.

The damage also spreads. One `_id` column that does not behave like the others means every `_id` column has to be checked, and the convention stops saving anyone time. One real table where this happened is told in `shape-sorter`.

### Story: The shape sorter

A table at Groups360 holds orchestration data that links two other kinds of record. It has a column called `id` and a column called `guid`, and both are what they say they are. It also has columns named `RoomBookingId` and `SpaceBookingId`, in capital letters and lowercase, exactly as written. Both point to records elsewhere in the same database, and both hold guids, not ids. Each is a `text` column.

Every decision in that design looks small by itself, and each one makes the next harder to see.

The mixed-case names are the first. Postgres folds an unquoted name to lowercase, so `RoomBookingId` has to be wrapped in double quotes every time it is written, or the query fails with a message that the column does not exist.

The `Id` ending is the second. An analyst who has learned what `id` means across the rest of the database reads it as a bigint key and writes the query to match. The table already holds a real `id` and a real `guid`, correctly labeled, which makes the guess more natural.

The guid inside it is the third, and the `text` type is the fourth, because it turns the mistake into a silence. A `uuid` column asked for the wrong kind of value says so at once: invalid input syntax for type uuid. A `text` column accepts anything and compares it as a string, so a query for an id that was never going to match returns no rows and no complaint. The analyst sees an empty result and takes it for missing data. A booking that is known to exist does not show up, and the analysis stops making sense. The explanation is in the name and the type, nowhere near the empty result. It has happened often enough that the table is known for it.

A child's shape-sorting toy makes the point. A `text` column is the hole that every shape fits through: guids, ids, stray spaces, a value in the wrong case. Nothing is refused, so nothing ever says what went wrong. A column typed for what it holds refuses what does not belong, and that refusal is the only message the person at the keyboard will get.

The table sits at the intersection of financial reporting, which is where the cost lands. Whoever named the columns was not the one who paid for them. Everyone who queries it afterward did, one empty result at a time. The names, the types, and the case cost the least to get right when the table is designed and the most to correct after it is in use, since correcting means a migration on a table that reporting depends on.
