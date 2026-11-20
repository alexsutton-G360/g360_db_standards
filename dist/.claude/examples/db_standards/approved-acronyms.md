# Approved acronyms

This list records which short forms Groups360 has agreed on. Use them wherever the term appears in a name: a name that uses one is still guessable, and the same term is written the same way everywhere. It is a house list: nothing here is right outside Groups360, it is only consistent inside it. Add to it deliberately, and keep entries lowercase.

## General technology terms

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

## Industry-specific terms

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

## Short forms for names at the limit

This table is not part of the everyday list above. It is for the case where a name is up against Postgres's 63-character limit, which happens when a table already has a long name and its constraints and indexes repeat that name and add column names. Use it only then, and only for constraint and index names. The default is still to spell every word out. The table and its columns are never shortened from this list.

Words are listed by the most characters they save, so the largest saving is easy to find. Each short form stands for one word only, so a short form is never reused for another word. Add a word deliberately, and never change or remove one that a name already uses.

| Word | Short form | Saves |
|---|---|---|
| configuration | `cfg` | 10 |
| reservation | `rsvtn` | 6 |
| template | `tmplt` | 3 |
| agenda | `agnd` | 2 |
| count | `cnt` | 2 |

