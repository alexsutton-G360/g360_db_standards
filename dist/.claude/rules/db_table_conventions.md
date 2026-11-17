---
description: Table design conventions: created_at, updated_at, soft delete, editing in place, lists of values, and derived copies. Apply when a change creates or alters a table.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All tables rules are enumerated using the RDBTB (Rules DataBase TaBle conventions) code.

> Generated from the Groups360 database standards repository. Edit the pages there, not this file.

## Row lifecycle

RDBTB1: when a migration creates a table, give it `created_at` and `updated_at`, both `timestamptz NOT NULL DEFAULT now()`. An append-only table, where a row is never updated, gets `created_at` only. A table that skips either needs a reason stated where the table is defined. Reason: a value the database maintains is true no matter which application or script touched the row, and anything downstream, like a warehouse sync, can rely on it. [Rule; slug: created-at-updated-at-on-tables; full rule: .claude/examples/db_standards/created-at-updated-at-on-tables.md]

RDBTB2: when a migration adds `updated_at` to a table, keep it current with the shared function `ufn_set_updated_at` and one `BEFORE UPDATE` trigger per table, not with application code. A table with a stored generated column needs the variant with no whole-row `WHEN` that names each generated column as an argument; the exact trigger text is in the full rule (`shared-updated-at-trigger`). Reason: the trigger maintains the value for every writer, and an update that changes nothing leaves `updated_at` alone, which protects any sync keyed on it. [Rule; slug: shared-updated-at-trigger; full rule: .claude/examples/db_standards/shared-updated-at-trigger.md]

RDBTB3: when a migration creates a table whose rows can be deleted from the application's point of view, soft-delete by default: a `deleted_at timestamptz` that is null while the row is live, with the shared trigger moving `updated_at` in the same statement. Skip it when the data never changes or goes away (an audit log, an event stream), or when the table is so large that keeping deleted rows would weigh on every query and index, where a retention policy or partitioning fits instead. Reason: a deleted row that stays can still be explained, followed by a sync, and pointed at. [Default; slug: soft-delete-default; full rule: .claude/examples/db_standards/soft-delete-default.md]

RDBTB4: when a change deletes a row and creates it again in order to change its data, update the row that exists instead; use `INSERT ... ON CONFLICT DO UPDATE` for insert-or-update, which needs a unique key to conflict on. If rebuilding rows is really right, the reason must be written down. Reason: an updated row keeps its `id` and leaves nothing behind, and whatever already saw the old row is not left holding a stray. Second opinion: any teammate. [Default; slug: change-row-in-place; full rule: .claude/examples/db_standards/change-row-in-place.md]

## Lists of values

RDBTB5: when a migration or model adds an array column, check that it is not a second table not yet made. An array fits only when each value is bare, with nothing else attached. Use a table when a value carries something of its own (a flag, a date, a status), points at another table (an array element cannot have a foreign key), or must be unique across the rows (a unique constraint compares whole arrays). The question to settle is what each value might come to carry. Reason: an array looks like a column until a value needs a fact or a link of its own, and by then the data is in the wrong shape. [Judgment call; slug: array-or-second-table; full rule: .claude/examples/db_standards/array-or-second-table.md]

## Derived values and copies

RDBTB6: when a migration or model adds a second table filled by copying from another, or a stored column worked out from rows in other tables (such as a header's status that sums up its bookings), derive it with a view instead of keeping a copy that code keeps in step. If something must be stored, store only what cannot be derived and put the derived part in a view on top. Reason: a stored copy can differ from its source, and everything downstream, including the warehouse, inherits the difference. [Default; slug: no-second-copy-use-a-view; full rule: .claude/examples/db_standards/no-second-copy-use-a-view.md]

RDBTB7: when a migration creates a materialized view, check that a plain view will not do: start with a plain view, and use a materialized view only when the query is heavy, read often, and the data can safely be a little behind. A materialized view needs a refresh plan, and it puts the object on the DBA's path (refresh timing, load, and monitoring). Reason: a materialized view can go stale, which is the same drift a stored copy has. Second opinion: DBA. [Default; slug: plain-view-before-materialized; full rule: .claude/examples/db_standards/plain-view-before-materialized.md]
