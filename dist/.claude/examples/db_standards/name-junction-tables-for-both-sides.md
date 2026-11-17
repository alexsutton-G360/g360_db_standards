# Name a table that joins two others for the two things it joins

Rule line `RDBNM9` in `db_naming_conventions.md`. Temperature: Default. Origin: house.

## Full rule

At Groups360, a table name made of two nouns, like `user_roles`, tells the reader that the table is a relationship: it joins the two things it names. Name junction tables that way, so the name alone says what kind of table it is.

That meaning is reserved, and readers rely on it, so a table that is not a junction table should not be given a two-noun name that reads as one. Name it for what a row is, and put who owns the rows in a column.

Because: a reader should be able to tell what kind of table they are looking at from its name alone, and the two-noun shape is the one signal that says the table joins things.

Good: `user_roles`, a table that joins users and roles
Good: `role_permissions`, a table that joins roles and permissions
