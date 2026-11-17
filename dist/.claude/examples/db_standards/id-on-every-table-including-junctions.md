# Give every table an `id`, junction tables included, unless there is a stated reason not to

Rule line `RDBID7` in `db_identifier_conventions.md`. Temperature: Default. Origin: house.

## Full rule

Every table carries an `id`. That includes junction tables, which also get a unique constraint on their pair of foreign keys so that the same two rows cannot be linked twice. A table that goes without an `id` needs a reason, stated where the table is defined.

The `id` is an operational column. Tools and scripts use it to address one specific row, and so does fixing or removing a single bad row, whether or not any query in the application ever reads it.

Because: this is how Groups360 builds tables, and it has found the `id` useful for tooling and for correcting one row. It is a house convention and not a claim about correctness elsewhere, so a team that identifies its junction rows by the foreign key pair is not making a mistake.

Good: a junction table with its own `id` and a unique constraint on its two foreign keys
Bad:  a junction table with an `id` and nothing to stop the same link from appearing twice
