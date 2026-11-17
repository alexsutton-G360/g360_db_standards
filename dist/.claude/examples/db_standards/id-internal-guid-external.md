# An `id` is an internal reference, so outside the database a row is found by its `guid`

Rule line `RDBID8` in `db_identifier_conventions.md`. Temperature: Rule. Origin: general.

## Full rule

An `id` is a counter, and it means something only inside the database that issued it. Never let an `id` be the value that finds a row from outside: not in an API, not in a URL, not in anything a person could substitute, replay, or edit on a live page. Look the row up by its `guid` instead. A reference held by another service is a `guid` for the same reason, since an `id` means nothing outside its own database.

Showing an `id` is fine. It can appear in a report or a user panel. What it cannot be is the lookup value.

Because: an `id` can be walked. Someone who sees `/users/42` can try 43, then 44, then 45, and every row is one guess from the next. A `guid` cannot be walked, and it keeps its meaning across databases, where an `id` does not.

Good: a lookup by `/users/<guid>`, and an `id` shown in an admin report
Bad:  a lookup by `/users/42`
