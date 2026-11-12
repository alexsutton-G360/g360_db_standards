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

---

### Separate words with underscores, never at the start or end of a name
[Slug: underscores-between-words · Temperature: Rule · Origin: house · Scope: global · Why: underscores]

Put an underscore between the words of a name. Do not begin or end a name with one.

Because: a leading underscore means something elsewhere, like private names in Python, but means nothing in our tables, so a reader's first assumption is wrong. Postgres also names the array type of every table and type with a leading underscore, so a table named that way can collide with one. A trailing underscore carries no meaning at all.

Good: `customer_accounts`
Bad:  `_customer_accounts`, `customer_accounts_`

Applies to every object unless its own page says otherwise. Schema names are one such case: they allow no underscores at all.

---

### Keep special characters out of names
[Slug: no-special-characters-in-names · Temperature: Rule · Origin: general · Scope: global · Why: no-special-characters]

Use only letters, digits, and underscores in names. No other characters.

Good: `guest_users`
Bad:  `guest-users`, `guest users`, `guest_users$`

Applies to every object unless its own page says otherwise.

---

### Spell names out in common terms, and abbreviate only with an approved acronym
[Slug: spell-out-names-approved-acronyms · Temperature: Default · Origin: general · Scope: global · Why: clear-terms]

Choose clear, commonly accepted words for names. Do not invent abbreviations that only Groups360 uses. A short form is fine when it appears in the approved acronym list below.

Because: a newcomer who has never heard an abbreviation cannot guess it, and cannot search for it either.

Good: `customer_account`
Bad:  `cust_acct`

Applies to every object unless its own page says otherwise.

---

## Approved acronyms

This list is a reference, not a rule. It records which short forms Groups360 has agreed on, so a name that uses one is still guessable. It is a house list: nothing here is right outside Groups360, it is only consistent inside it. Add to it deliberately, and keep entries lowercase.

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
