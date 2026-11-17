---
description: Database naming conventions for columns, tables, and every other object. Apply when a migration or model names anything.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All naming rules are enumerated using the RDBNM (Rules DataBase NaMing conventions) code.

> Generated from the Groups360 database standards repository. Edit the pages there, not this file.

Approved short forms for names are listed in .claude/examples/db_standards/approved-acronyms.md.

## Global Rules

RDBNM1: when a change names any database object, use lowercase only, with no capital letters. Reason: Postgres folds unquoted names to lowercase, so a name with capitals has to be wrapped in double quotes every time anyone refers to it. [Rule; slug: lowercase-every-name; story: shape-sorter; full rule: .claude/examples/db_standards/lowercase-every-name.md]

RDBNM2: when a change names any database object, put an underscore between the words of the name and never at its start or end; schema names are the exception, since they allow no underscores at all. Reason: a leading underscore means something elsewhere, like private names in Python, but nothing in our tables, and Postgres names the array type of every table with a leading underscore, so a table named that way can collide with one. [Rule; slug: underscores-between-words; full rule: .claude/examples/db_standards/underscores-between-words.md]

RDBNM3: when a change names any database object, use only letters, digits, and underscores (`guest_users`, not `guest-users`, `guest users`, or `guest_users$`). [Rule; slug: no-special-characters-in-names; full rule: .claude/examples/db_standards/no-special-characters-in-names.md]

RDBNM4: when a change names any database object, choose clear, commonly accepted words, and abbreviate only with an approved acronym (`customer_account`, not `cust_acct`); the approved list is the reference file `approved-acronyms`. Reason: a newcomer who has never heard an abbreviation cannot guess it and cannot search for it. [Default; slug: spell-out-names-approved-acronyms; full rule: .claude/examples/db_standards/spell-out-names-approved-acronyms.md]

## Naming

RDBNM5: when a migration or model names a column, name it for the fact it stores, not the action it asks for (`excluded_properties`, not `exclude_properties`). A table that really holds instructions, such as jobs to run, is the exception. Reason: a table records what is true about a row, not instructions for what to do with it. [Default; slug: name-column-for-the-fact; story: table-of-facts; full rule: .claude/examples/db_standards/name-column-for-the-fact.md]

RDBNM6: when a migration or model names a flag column, name it for what is true, not for what is not (`is_active`, not `is_not_active`). This bends when another name reads more clearly; see the story `hidden-vs-displayed`. Reason: code that tests a negated name reads as a double negative. [Default; slug: columns-in-positive-voice; story: hidden-vs-displayed; full rule: .claude/examples/db_standards/columns-in-positive-voice.md]

RDBNM7: when a migration or model names a column, use the singular (`first_name`, `user_guid`); a column that really holds many values, like an array, can be plural. Reason: a row is one instance of what its plural-named table holds, so its properties are singular. [Default; slug: columns-in-singular; full rule: .claude/examples/db_standards/columns-in-singular.md]

RDBNM8: when a migration or model adds a column whose name ends in a number, such as `contact_2`, ask what the second column really is. Parallel slots can be `contact_1` and `contact_2`, but if one outranks the other or is the newer version, name each for what it is (`primary_contact` and `secondary_contact`), because a pair like `contact` and `contact_2` tells the reader that one outranks the other. [Judgment call; slug: numbered-column-names; full rule: .claude/examples/db_standards/numbered-column-names.md]

## Naming tables

RDBNM9: when a migration creates a table, name a junction table that joins two others for the two things it joins (`user_roles`, `role_permissions`), and do not give a table that is not a junction a two-noun name that reads as one; name it for what a row is and put who owns the rows in a column. Reason: the two-noun shape is the one signal that says the table joins things. [Default; slug: name-junction-tables-for-both-sides; full rule: .claude/examples/db_standards/name-junction-tables-for-both-sides.md]
