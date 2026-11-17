# Separate words with underscores, never at the start or end of a name

Rule line `RDBNM2` in `db_naming_conventions.md`. Temperature: Rule. Origin: house.

## Full rule

Put an underscore between the words of a name. Do not begin or end a name with one.

Because: a leading underscore means something elsewhere, like private names in Python, but means nothing in our tables, so a reader's first assumption is wrong. Postgres also names the array type of every table and type with a leading underscore, so a table named that way can collide with one. A trailing underscore carries no meaning at all.

Good: `customer_accounts`
Bad:  `_customer_accounts`, `customer_accounts_`

Applies to every object unless its own page says otherwise. Schema names are one such case: they allow no underscores at all.
