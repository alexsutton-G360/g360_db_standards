# Name a primary key `pk_<table>` and a foreign key `fk_<table>_<column>`

Rule line `RDBOB5` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

Name the constraint when you create it. A primary key left unnamed gets a default name such as `notes_pkey`, which does not follow the pattern.

A foreign key creates a constraint and no index, so there is no such thing as a foreign key index. Whether the column needs an index is a separate question, answered under Indexes on Tables.

Postgres cuts any name at 63 characters and gives only a notice, and two names cut to the same text will collide. When a pattern would run past that, shorten the table or column part and keep the prefix.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `pk_users`, `fk_notes_user_id`
Bad:  `notes_pkey`, the default name an unnamed primary key gets

Second opinion: DBA.
