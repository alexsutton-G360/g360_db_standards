# Make a `guid` NOT NULL and UNIQUE, and generate it wherever it is first needed

Rule line `RDBID10` in `db_identifier_conventions.md`. Temperature: Default. Origin: general.

## Full rule

A `guid` column is NOT NULL and UNIQUE, enforced by the database. With those two in place, a guid that was never generated is refused, and so is one that repeats, so the data stays safe whoever generates the value.

That makes the choice of who generates it a question of convenience and not of safety. Either way works:

- The application generates it. The guid is known before the insert, so it can go into an S3 key, a message, or a request before the row exists, and the row can be found by it from the start. A guid the application forgot to send shows up as an error.
- The database generates it, with a default such as `gen_random_uuid()`. A row is valid even when the application sends no guid, and the application can read the value back from the insert.

Generate it where it is first needed, which is often the application. The user uploads table on Stock tables is an example of the first.

Because: the database enforces what is true about the data whoever fills the column in, so the guarantee does not depend on the writer, and the choice of writer can follow what the design needs.

Good: a guid the application generates and sends with the insert, so it can go into an S3 key before the row exists
Good: a guid that defaults to `gen_random_uuid()`, for a table where nothing needs it before the row does
Bad:  a guid column that allows null or has no unique constraint, whichever side generates it
