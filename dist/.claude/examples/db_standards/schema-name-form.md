# Name a schema in the singular with no underscores

Rule line `RDBOB2` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A schema name is lowercase and singular, with no underscores and no special characters. Postgres allows underscores in a schema name, so this is a convention and not a limit. It is the one place where the underscore rule on Global Rules gives way, because a schema name has no underscores at all.

Because: a schema is a division of the database that you can name in a word. If the name needs an underscore, the schema is probably too specific, and that is the moment to ask what it really is. Consistency also lets a reader tell an object from its name.

Good: `extraction`, `public`
Bad:  `booking_service_test`, `bookings`

Second opinion: DBA.
