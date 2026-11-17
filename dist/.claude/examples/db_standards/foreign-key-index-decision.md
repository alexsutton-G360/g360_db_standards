# Decide on purpose whether a foreign key column needs an index, because the database does not make one

Rule line `RDBRL7` in `db_relationship_conventions.md`. Temperature: Judgment call. Origin: general.

## Full rule

A foreign key makes the database check the link. It does not index the column that holds it. When a parent row is deleted or its key changes, the database has to find that parent's child rows, and with no index on the foreign key column that means scanning the whole child table.

Index a foreign key column when parent rows are deleted or changed, or when queries go from a parent to its children. Leave it alone when neither happens, as with a small table that never changes or a parent that is never deleted. A table with several nullable foreign keys, like the exclusive arc, asks the question once per column.

Because: the database enforces the link but does not make it fast, and it is easy to assume the second part came with the first.

Good: an index on `user_id` in an addresses table, because addresses are always loaded by their user
Bad:  assuming a foreign key made the column fast to search, and finding out when the table is large
