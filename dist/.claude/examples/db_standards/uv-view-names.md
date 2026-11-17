# Name a view `uv_<table>_<descriptor>`

Rule line `RDBOB11` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A view starts with `uv_`, followed by the table it reads from and a descriptor of what it does. When to choose a view, and which kind, is under Derived values and copies on Tables.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `uv_bookings_status`
Bad:  `bookings_status`

Second opinion: DBA.
