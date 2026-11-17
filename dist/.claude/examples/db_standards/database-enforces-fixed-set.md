# Have the database enforce a fixed set of values

Rule line `RDBCL16` in `db_column_conventions.md`. Temperature: Rule. Origin: general.

## Full rule

When a column holds one of a fixed set of values, the database enforces the set. A check in application code alone does not count, because anything that writes to the table without going through that code can still write a value outside the set.

Because: a limit kept in application code is an opinion. A limit in the database is true for every writer.
