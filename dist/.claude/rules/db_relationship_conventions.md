---
description: Relationship and index conventions: tables with several possible parents, foreign keys, and indexes. Apply when a change adds a key, a parent pointer, or an index.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All relationships and indexes rules are enumerated using the RDBRL (Rules DataBase RelationaL conventions) code.

> Generated from the Groups360 database standards repository. Edit the pages there, not this file.

## Tables that belong to one of several parents

RDBRL1: when a migration creates parallel tables for the same kind of row, one per parent (such as separate address tables for users and for orgs), keep one table when the rows have the same shape whatever they belong to; separate tables are right only when the rows really differ in shape. Reason: with two tables, every change to what a row is has to be made in both places, and someone working on one may never learn the other exists. [Default; slug: one-table-for-same-shape-rows; full rule: .claude/examples/db_standards/one-table-for-same-shape-rows.md]

RDBRL2: when a migration or model adds a pair of columns where one names the parent's table (`source_type`) and the other holds the id of a row in it (`source_id`), treat it as an exception to the real-foreign-key rule: the database cannot enforce it, so deleting a parent leaves its children and an id can point at a row that never existed. It is acceptable only when both hold: the fan-out is large enough that the other two designs would add serious schema overhead, and orphans genuinely do not matter (an activity log is the standard example). If only one holds, use another design. Second opinion: Data Architect. [Judgment call; slug: source-type-id-pattern; full rule: .claude/examples/db_standards/source-type-id-pattern.md]

RDBRL3: when a table can belong to one of several parents, give it one nullable foreign key per parent, each a real foreign key, and a check constraint that counts how many are filled in (`num_nonnulls(...) = 1`, or `<= 1` if a row may belong to no parent); the full example is in the rule (`exclusive-arc-default`). Adding a parent later takes an `ALTER TABLE` with a new column, its foreign key, and a replacement check, so if parents keep multiplying see `junction-table-per-parent`. Reason: the database is the lowest level at which something can be true, and the check enforces this on every write. [Default; slug: exclusive-arc-default; full rule: .claude/examples/db_standards/exclusive-arc-default.md]

RDBRL4: when a table can belong to one of many parents, or the parents keep growing, and a dangling reference would do real harm, keep the core table lean and give each kind of parent its own junction table, with real foreign keys and a unique constraint on the pair; a new parent is then a new table, with no migration on a live table. For a small, stable set of parents this is more than needed (use `exclusive-arc-default`). Reason: the extra tables are what it costs to keep the database enforcing the relationship. [Judgment call; slug: junction-table-per-parent; full rule: .claude/examples/db_standards/junction-table-per-parent.md]

RDBRL5: when a table can belong to one of several parents, choose by how many kinds of parent there are and how much a dangling reference would hurt: nullable foreign keys, one per parent, for few parents; junction tables when the parents are many or growing and integrity matters; `source_type` and `source_id` only when the parents are many and orphans do no harm. Start with nullable foreign keys. This decision is hard to undo later. Second opinion: Data Architect. [Judgment call; slug: polymorphic-decision-matrix; full rule: .claude/examples/db_standards/polymorphic-decision-matrix.md]

## Indexes

RDBRL6: when a migration adds an index, check that a query that exists needs it (a lookup, a join, or a sort the table is genuinely asked to do) and that it is added in the same change that introduces the query; do not add one in case it is needed someday. A missing index fails quietly as the table grows. A unique constraint that enforces something true about the data, such as a unique `guid`, makes its index a consequence of that guarantee and not a guess. Reason: every index slows every write and takes space whether or not a query uses it, so an index should name the query it serves. [Default; slug: index-when-a-lookup-exists; full rule: .claude/examples/db_standards/index-when-a-lookup-exists.md]

RDBRL7: when a migration adds a foreign key, decide on purpose whether its column needs an index, because the database does not make one. Index it when parent rows are deleted or changed, or when queries go from a parent to its children; leave it alone when neither happens, as with a small table that never changes or a parent that is never deleted. A table with several nullable foreign keys, like the exclusive arc, asks once per column. Reason: the database enforces the link but does not make it fast. [Judgment call; slug: foreign-key-index-decision; full rule: .claude/examples/db_standards/foreign-key-index-decision.md]
