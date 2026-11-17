# Other objects and tools

Rules for the database objects that are not tables or columns: databases, schemas, keys, constraints, indexes, triggers, functions, procedures, views, materialized views, roles, and users. The rules on Global Rules apply here too. Where a rule below says otherwise, this page wins.

Almost every rule on this page is a house rule in the purest sense. The abbreviations are arbitrary, and nothing here argues that `idx` is a better prefix than any other. What matters is that every object follows the same pattern, so anyone can tell what kind of object it is from its name alone.

---

## Databases and schemas

### Name a database in the singular, short and descriptive
[Slug: database-name-form · Temperature: Rule · Origin: house · Scope: database · Why: object-naming]

A database name is lowercase and singular, short, and descriptive. Use underscores between words where it has more than one, though one word is preferred. A test copy takes the same name with a suffix. Abbreviate only as Global Rules allows.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `booking_service`, `booking_service_test`
Bad:  `bookings`, `booking_services`

Second opinion: DBA.

Agent: when a change creates or names a database, make the name lowercase, singular, short, and descriptive, with underscores between words where there is more than one (one word is preferred); a test copy takes the same name with a suffix (`booking_service`, `booking_service_test`, not `bookings`). Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

### Name a schema in the singular with no underscores
[Slug: schema-name-form · Temperature: Rule · Origin: house · Scope: schema · Why: object-naming]

A schema name is lowercase and singular, with no underscores and no special characters. Postgres allows underscores in a schema name, so this is a convention and not a limit. It is the one place where the underscore rule on Global Rules gives way, because a schema name has no underscores at all.

Because: a schema is a division of the database that you can name in a word. If the name needs an underscore, the schema is probably too specific, and that is the moment to ask what it really is. Consistency also lets a reader tell an object from its name.

Good: `extraction`, `public`
Bad:  `booking_service_test`, `bookings`

Second opinion: DBA.

Agent: when a change creates or names a schema, make the name lowercase and singular, with no underscores and no special characters (`extraction`, `public`, not `booking_service_test`); this is a convention and not a Postgres limit. A schema name that needs an underscore probably means the schema is too specific. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

### Use a schema where it divides a database into parts that mean something, and name it for what it holds
[Slug: schema-for-real-divisions · Temperature: Default · Origin: general · Scope: schema · Why: schema-meaning]

A schema is a logical division of a database. When a database has parts with different purposes, a schema is a good way to show it, and its name should tell a reader what is stored under it.

`public` is the default schema in most Groups360 systems, and it is fine to use. This rule is neither for it nor against it. It is about the schemas you add, and about adding one where the division is real.

Because: a schema name that says what it holds is information a reader gets for free. One that says nothing gives them nothing.

Good: `ops`, for functional operation data such as worker run tracking
Good: `extraction`, for data pulled directly out of uploads
Good: `canonization`, for data being integrated into our systems
Bad:  `misc`, which says nothing about what is stored there

Second opinion: DBA or Data Architect.

Agent: when a change adds a schema, add it only where the database has parts with different purposes, and name it for what it holds (`ops`, `extraction`, `canonization`, not `misc`); `public` is fine, and this rule is neither for nor against it. Reason: a schema name that says what it holds is information a reader gets for free.

---

### Do not name a schema after its own database
[Slug: schema-never-named-for-database · Temperature: Rule · Origin: general · Scope: schema · Why: schema-meaning]

A schema inside a database called `invoice_service` is not called `invoice_service`. The name repeats what the reader already knows and adds nothing.

It also costs something. A table reaches the warehouse named for its database, its schema, and its table, so an `invoices` table in that schema arrives as `invoice_service_invoice_service_invoices`. A long name is part of how the warehouse works, and the `public` schema produces one too, as `invoice_service_public_invoices`. But a schema that repeats the database makes the long name worse and gives nothing back.

Because: the schema name is the one place in the full name that can say something new, and repeating the database spends it on nothing.

Good: `invoice_service` as a database holding an `accounting` schema
Bad:  `invoice_service` as a database holding an `invoice_service` schema

Second opinion: DBA or Data Architect.

Agent: when a change creates a schema, do not name it after its own database (an `invoice_service` database does not hold an `invoice_service` schema). Reason: the warehouse names a table by its database, schema, and table, so a repeated name makes the long name longer and says nothing new.

---

## Keys, constraints, and indexes

Postgres gives a constraint and the index behind it the same name, so there is one name to choose and not two. A primary key and a unique constraint each create an index that takes the constraint's name. A foreign key and a check constraint create none.

### Name a primary key `pk_<table>` and a foreign key `fk_<table>_<column>`
[Slug: pk-and-fk-names · Temperature: Rule · Origin: house · Scope: constraint · Why: object-naming]

Name the constraint when you create it. A primary key left unnamed gets a default name such as `notes_pkey`, which does not follow the pattern.

A foreign key creates a constraint and no index, so there is no such thing as a foreign key index. Whether the column needs an index is a separate question, answered under Indexes on Tables.

Postgres cuts any name at 63 characters and gives only a notice, and two names cut to the same text will collide. When a pattern would run past that, shorten the table or column part and keep the prefix.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `pk_users`, `fk_notes_user_id`
Bad:  `notes_pkey`, the default name an unnamed primary key gets

Second opinion: DBA.

Agent: when a migration creates a primary key or a foreign key, name the constraint when creating it: `pk_<table>` for a primary key and `fk_<table>_<column>` for a foreign key (`pk_users`, `fk_notes_user_id`), never a default such as `notes_pkey`. Postgres cuts a name at 63 characters, so shorten the table or column part and keep the prefix. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

### Name every other constraint `ctx_<descriptor>`
[Slug: ctx-constraint-names · Temperature: Rule · Origin: house · Scope: constraint · Why: object-naming]

A check, unique, or exclusion constraint is `ctx_` followed by what it enforces. A unique constraint creates an index, which takes the constraint's name, so that index keeps its `ctx_` name.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `ctx_exactly_one_parent`, `ctx_unique_note_rfp`
Bad:  `notes_body_check`, the default name an unnamed check constraint gets

Second opinion: DBA.

Agent: when a migration creates a check, unique, or exclusion constraint, name it `ctx_<descriptor>` for what it enforces (`ctx_exactly_one_parent`, `ctx_unique_note_rfp`), never a default such as `notes_body_check`; the index behind a unique constraint keeps the `ctx_` name. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

### Name every other index `idx_<table>_<column>`
[Slug: idx-index-names · Temperature: Rule · Origin: house · Scope: index · Why: object-naming]

A standalone index is `idx_` followed by its table and the column or columns it covers. An index that a primary key or a unique constraint creates takes that constraint's name, and keeps it.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `idx_users_first_name`
Bad:  `users_first_name_idx`, the name Postgres would give it

Second opinion: DBA.

Agent: when a migration creates a standalone index, name it `idx_<table>_<column>` for its table and the columns it covers (`idx_users_first_name`), not the name Postgres would give it; an index that a primary key or unique constraint creates keeps that constraint's name. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

## Triggers, functions, procedures, and views

### Name a trigger `trg_<table>_<descriptor>`
[Slug: trg-trigger-names · Temperature: Rule · Origin: house · Scope: trigger · Why: object-naming]

A trigger name starts with `trg_`, then the table it sits on, then a descriptor of what it does. The shared trigger that keeps `updated_at` current is under Row lifecycle on Tables.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `trg_bookings_set_updated_at`
Bad:  `bookings_trigger`, `update_bookings`

Second opinion: DBA.

Agent: when a migration creates a trigger, name it `trg_<table>_<descriptor>`, with the table it sits on and what it does (`trg_bookings_set_updated_at`, not `bookings_trigger`). Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

### Name a function `ufn_<descriptor>`
[Slug: ufn-function-names · Temperature: Rule · Origin: house · Scope: function · Why: object-naming]

A function you write starts with `ufn_`, followed by a descriptor of what it does.

Because: the pattern is a house convention. The prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

Good: `ufn_set_updated_at`
Bad:  `set_updated_at`

Second opinion: DBA.

Agent: when a migration creates a function, name it `ufn_<descriptor>` for what it does (`ufn_set_updated_at`, not `set_updated_at`). Reason: the prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

---

### Name a stored procedure `usp_<descriptor>`
[Slug: usp-procedure-names · Temperature: Rule · Origin: house · Scope: procedure · Why: object-naming]

A stored procedure you write starts with `usp_`, followed by a descriptor of what it does.

Because: the pattern is a house convention. The prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

Good: `usp_db_backups`
Bad:  `backup_databases`

Second opinion: DBA.

Agent: when a migration creates a stored procedure, name it `usp_<descriptor>` for what it does (`usp_db_backups`, not `backup_databases`). Reason: the prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

---

### Name a view `uv_<table>_<descriptor>`
[Slug: uv-view-names · Temperature: Rule · Origin: house · Scope: view · Why: object-naming]

A view starts with `uv_`, followed by the table it reads from and a descriptor of what it does. When to choose a view, and which kind, is under Derived values and copies on Tables.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `uv_bookings_status`
Bad:  `bookings_status`

Second opinion: DBA.

Agent: when a migration creates a view, name it `uv_<table>_<descriptor>`, with the table it reads from and what it does (`uv_bookings_status`, not `bookings_status`). Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

### Name a materialized view `umv_<table>_<descriptor>`
[Slug: umv-materialized-view-names · Temperature: Rule · Origin: house · Scope: materialized_view · Why: object-naming]

A materialized view starts with `umv_`, followed by the table it reads from and a descriptor of what it does. A materialized view that an application creates, and not a person, is not covered by this rule.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `umv_bookings_monthly_totals`
Bad:  `monthly_totals`

Second opinion: DBA.

Agent: when a person creates a materialized view, name it `umv_<table>_<descriptor>`, with the table it reads from and what it does (`umv_bookings_monthly_totals`, not `monthly_totals`); a materialized view that an application creates is not covered. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

---

## Roles and users

While PostgreSQL is not SOC Type 2 compliant by design, the practices here aim to align naming and access with SOC Type 2 recommendations wherever technically possible.

### Create a role with no login rights, named for what it covers and its access level
[Slug: role-no-login · Temperature: Rule · Origin: house · Scope: role · Why: role-access]

A role is a named bundle of permissions that is granted to users, and a role created this way has no login rights, so no one connects as it. In Postgres a user is a role that is allowed to log in, and a role that is not is a group. Grant the access to the role, and then grant the role to each person or service that needs it. When access later has to grow, one role changes, and not every user. Name the role for the one thing it covers, in the singular, followed by its access level, with an underscore between.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `booking_ro`, `booking_rw`
Bad:  `bookingro`, `_bookingro`

Second opinion: DBA.

Agent: when a change creates a role, create it with no login rights and name it for the one thing it covers, in the singular, followed by its access level with an underscore between (`booking_ro`, `booking_rw`). Grant the access to the role and then grant the role to each person or service that needs it. Reason: when access has to grow, one role changes and not every user.

---

### Name a user for the person or service it stands for, and describe a service account in its comment
[Slug: user-and-service-account-names · Temperature: Rule · Origin: house · Scope: user · Why: role-access]

A user is a personal account or a service account. A personal account is named `<name>_<team>_<access>`. A service account begins with `svc`, followed by the database and the access type. Describe what a service account is for in the object's comment.

Because: the pattern is a house convention, and the comment is what lets someone who finds a service account later learn what it is for.

Good: `svcbooking_ro`, a read-only service account for the booking database
Good: `svcroom_rw`, a read and write service account for the room database
Bad:  a service account with no comment saying what it is for

Second opinion: DBA.

Agent: when a change creates a database user, name a personal account `<name>_<team>_<access>` and a service account `svc` followed by the database and the access type (`svcbooking_ro`), and describe what a service account is for in the object's comment. Reason: the comment is what lets someone who finds a service account later learn what it is for.
