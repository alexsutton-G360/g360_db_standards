# Spell names out in common terms, and use an approved short form where one exists

Rule line `RDBNM4` in `db_naming_conventions.md`. Temperature: Default. Origin: general.

## Full rule

Choose clear, commonly accepted words for names. Do not invent abbreviations that only Groups360 uses. When a term has a short form in the approved acronym tables below, use the short form everywhere: `sqft`, not `square_feet`. Spell out every other word.

When a constraint or index name runs into Postgres's 63-character limit, the rule on shortening long names (see Keys, constraints, and indexes on Other objects and tools) adds a second, separate table of short forms for that case only.

Because: a newcomer who has never heard an abbreviation cannot guess it, and cannot search for it. The approved tables hold the short forms that have been agreed, so using them keeps names guessable and the same across the platform.

Good: `customer_account`, `meeting_room_sqft`
Bad:  `cust_acct`, `meeting_room_square_feet`

Applies to every object unless its own page says otherwise.
