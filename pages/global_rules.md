# Global Rules

These rules apply to every database object, whatever kind it is. An object's own page can say otherwise, and where it does, the object's page wins. Each rule below says so in its last line, so it still reads correctly on its own.

---

### Use lowercase for every name
[Slug: lowercase-every-name · Temperature: Rule · Origin: general · Scope: global · Why: lowercase-only]

Write every database object name in lowercase, with no capital letters anywhere.

Because: Postgres folds unquoted names to lowercase, so a name with capitals has to be wrapped in double quotes every time anyone refers to it.

Good: `booking_service`
Bad:  `BookingService`

Applies to every object unless its own page says otherwise.

Agent: when a change names any database object, use lowercase only, with no capital letters. Reason: Postgres folds unquoted names to lowercase, so a name with capitals has to be wrapped in double quotes every time anyone refers to it.

---

### Separate words with underscores, never at the start or end of a name
[Slug: underscores-between-words · Temperature: Rule · Origin: house · Scope: global · Why: underscores]

Put an underscore between the words of a name. Do not begin or end a name with one.

Because: a leading underscore means something elsewhere, like private names in Python, but means nothing in our tables, so a reader's first assumption is wrong. Postgres also names the array type of every table and type with a leading underscore, so a table named that way can collide with one. A trailing underscore carries no meaning at all.

Good: `customer_accounts`
Bad:  `_customer_accounts`, `customer_accounts_`

Applies to every object unless its own page says otherwise. Schema names are one such case: they allow no underscores at all.

Agent: when a change names any database object, put an underscore between the words of the name and never at its start or end; schema names are the exception, since they allow no underscores at all. Reason: a leading underscore means something elsewhere, like private names in Python, but nothing in our tables, and Postgres names the array type of every table with a leading underscore, so a table named that way can collide with one.

---

### Keep special characters out of names
[Slug: no-special-characters-in-names · Temperature: Rule · Origin: general · Scope: global · Why: no-special-characters]

Use only letters, digits, and underscores in names. No other characters.

Good: `guest_users`
Bad:  `guest-users`, `guest users`, `guest_users$`

Applies to every object unless its own page says otherwise.

Agent: when a change names any database object, use only letters, digits, and underscores (`guest_users`, not `guest-users`, `guest users`, or `guest_users$`).

---

### Spell names out in common terms, and use an approved short form where one exists
[Slug: spell-out-names-approved-acronyms · Temperature: Default · Origin: general · Scope: global · Why: clear-terms]

Choose clear, commonly accepted words for names. Do not invent abbreviations that only Groups360 uses. When a term has a short form in the approved acronym tables below, use the short form everywhere: `sqft`, not `square_feet`. Spell out every other word.

When a constraint or index name runs into Postgres's 63-character limit, the rule on shortening long names (see Keys, constraints, and indexes on Other objects and tools) adds a second, separate table of short forms for that case only.

Because: a newcomer who has never heard an abbreviation cannot guess it, and cannot search for it. The approved tables hold the short forms that have been agreed, so using them keeps names guessable and the same across the platform.

Good: `customer_account`, `meeting_room_sqft`
Bad:  `cust_acct`, `meeting_room_square_feet`

Applies to every object unless its own page says otherwise.

Agent: when a change names any database object, use the approved short form wherever the term has one (`meeting_room_sqft`, not `meeting_room_square_feet`) and spell every other word out (`customer_account`, not `cust_acct`); the approved short forms are in the reference file `approved-acronyms`. Reason: a newcomer who has never heard an abbreviation cannot guess it and cannot search for it.

---

## Approved acronyms

This list records which short forms Groups360 has agreed on. Use them wherever the term appears in a name: a name that uses one is still guessable, and the same term is written the same way everywhere. It is a house list: nothing here is right outside Groups360, it is only consistent inside it. Add to it deliberately, and keep entries lowercase.

### General technology terms

| Term | Short form |
|---|---|
| Database | `db` |
| View / user view | `v` / `uv` |
| Materialized view / user materialized view | `mv` / `umv` |
| Stored procedure / user stored procedure | `sp` / `usp` |
| Constraint | `ctx` |
| Function / user function | `fn` / `ufn` |
| Identity | `id` |
| Primary key | `pk` |
| Foreign key | `fk` |
| Index | `idx` |
| Trigger | `trg` |
| Application programming interface | `api` |
| Public key infrastructure | `pki` |
| Access control list | `acl` |
| Extract, transform, load | `etl` |
| Extract, load, transform | `elt` |
| Comma-separated values | `csv` |
| Business intelligence | `bi` |
| Quality assurance | `qa` |
| User acceptance testing | `uat` |
| Development | `dev` |
| Service level agreement | `sla` |
| Single sign-on | `sso` |
| Organization | `org` |
| Average | `avg` |

`dev` means development, not developer. On a name it usually marks something used in a lower environment, during development. `org` means organization. It is so common in our systems that anyone who sees it reads it that way.

### Industry-specific terms

| Term | Short form |
|---|---|
| Smith Travel Reports | `str` |
| Request for proposal | `rfp` |
| Food and beverage | `fb` |
| Certified market lead | `cml` |
| Global sales organization | `gso` |
| Intercontinental Hotels Group | `ihg` |
| Salesforce | `sf` |
| Property management system | `pms` |
| Central reservation system | `crs` |
| Square feet | `sqft` |

### Short forms for names at the limit

This table is not part of the everyday list above. It is for the case where a name is up against Postgres's 63-character limit, which happens when a table already has a long name and its constraints and indexes repeat that name and add column names. Use it only then, and only for constraint and index names. The default is still to spell every word out. The table and its columns are never shortened from this list.

Words are listed by the most characters they save, so the largest saving is easy to find. Each short form stands for one word only, so a short form is never reused for another word. Add a word deliberately, and never change or remove one that a name already uses.

| Word | Short form | Saves |
|---|---|---|
| configuration | `cfg` | 10 |
| reservation | `rsvtn` | 6 |
| template | `tmplt` | 3 |
| agenda | `agnd` | 2 |
| count | `cnt` | 2 |
