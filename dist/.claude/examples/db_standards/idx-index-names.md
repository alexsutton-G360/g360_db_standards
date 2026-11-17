# Name every other index `idx_<table>_<column>`

Rule line `RDBOB7` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A standalone index is `idx_` followed by its table and the column or columns it covers. An index that a primary key or a unique constraint creates takes that constraint's name, and keeps it.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `idx_users_first_name`
Bad:  `users_first_name_idx`, the name Postgres would give it

Second opinion: DBA.
