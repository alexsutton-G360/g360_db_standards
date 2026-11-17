# Name columns in the singular

Rule line `RDBNM7` in `db_naming_conventions.md`. Temperature: Default. Origin: house.

## Full rule

Use the singular for a column name. A row is one instance of the thing its table holds, so its properties are named in the singular. Table names are plural, so a plural column name would also read as a plural inside a plural.

Good: `first_name`, `user_guid`
Bad:  `first_names`, `user_guids`

This one bends easily. A column that really holds many values, like an array, can be plural.
