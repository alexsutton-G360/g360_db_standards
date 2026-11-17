# Give a table a `guid` when something outside the database may point at its rows, and decide when the table is created

Rule line `RDBID9` in `db_identifier_conventions.md`. Temperature: Default. Origin: house.

## Full rule

Most tables are never referred to from outside their own database, and carry only an `id`. A junction table does not get a `guid`. A table that something outside may point at gets one, and the time to decide is when the table is created. If in doubt, add it. An unused `guid` column costs almost nothing. Adding one later is routine, but it is more work than adding it now. Every existing row needs a value, and the NOT NULL and UNIQUE constraints go on after that backfill, so what would have been part of the create statement becomes a migration in steps (*rule: plan-for-existing-rows*).

Declare the `guid` unique when the column is created. The constraint is what makes it safe to rely on as an identifier, and it creates the index that lookups by it will need. That index enforces something true about the data and is not a guess about future queries, so it is not the kind of index the rule under Indexes on this page warns against.

Because: a `guid` is simplest on the day the table is created, because every row is born with one. Adding it later is routine, but it takes steps: a value for every existing row, then the constraints, and the cost grows with the size of the table.
