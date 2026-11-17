---
description: Conventions for databases, schemas, constraints, indexes, triggers, functions, views, roles, and users. Apply when a migration creates or names one.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All database objects rules are enumerated using the RDBOB (Rules DataBase OBject conventions) code.

> Generated from the Groups360 database standards repository. Edit the pages there, not this file.

## Databases and schemas

RDBOB1: when a change creates or names a database, make the name lowercase, singular, short, and descriptive, with underscores between words where there is more than one (one word is preferred); a test copy takes the same name with a suffix (`booking_service`, `booking_service_test`, not `bookings`). Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: database-name-form; full rule: .claude/examples/db_standards/database-name-form.md]

RDBOB2: when a change creates or names a schema, make the name lowercase and singular, with no underscores and no special characters (`extraction`, `public`, not `booking_service_test`); this is a convention and not a Postgres limit. A schema name that needs an underscore probably means the schema is too specific. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: schema-name-form; full rule: .claude/examples/db_standards/schema-name-form.md]

RDBOB3: when a change adds a schema, add it only where the database has parts with different purposes, and name it for what it holds (`ops`, `extraction`, `canonization`, not `misc`); `public` is fine, and this rule is neither for nor against it. Reason: a schema name that says what it holds is information a reader gets for free. Second opinion: DBA or Data Architect. [Default; slug: schema-for-real-divisions; full rule: .claude/examples/db_standards/schema-for-real-divisions.md]

RDBOB4: when a change creates a schema, do not name it after its own database (an `invoice_service` database does not hold an `invoice_service` schema). Reason: the warehouse names a table by its database, schema, and table, so a repeated name makes the long name longer and says nothing new. Second opinion: DBA or Data Architect. [Rule; slug: schema-never-named-for-database; full rule: .claude/examples/db_standards/schema-never-named-for-database.md]

## Keys, constraints, and indexes

RDBOB5: when a migration creates a primary key or a foreign key, name the constraint when creating it: `pk_<table>` for a primary key and `fk_<table>_<column>` for a foreign key (`pk_users`, `fk_notes_user_id`), never a default such as `notes_pkey`. Postgres cuts a name at 63 characters, so shorten the table or column part and keep the prefix. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: pk-and-fk-names; full rule: .claude/examples/db_standards/pk-and-fk-names.md]

RDBOB6: when a migration creates a check, unique, or exclusion constraint, name it `ctx_<descriptor>` for what it enforces (`ctx_exactly_one_parent`, `ctx_unique_note_rfp`), never a default such as `notes_body_check`; the index behind a unique constraint keeps the `ctx_` name. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: ctx-constraint-names; full rule: .claude/examples/db_standards/ctx-constraint-names.md]

RDBOB7: when a migration creates a standalone index, name it `idx_<table>_<column>` for its table and the columns it covers (`idx_users_first_name`), not the name Postgres would give it; an index that a primary key or unique constraint creates keeps that constraint's name. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: idx-index-names; full rule: .claude/examples/db_standards/idx-index-names.md]

## Triggers, functions, procedures, and views

RDBOB8: when a migration creates a trigger, name it `trg_<table>_<descriptor>`, with the table it sits on and what it does (`trg_bookings_set_updated_at`, not `bookings_trigger`). Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: trg-trigger-names; full rule: .claude/examples/db_standards/trg-trigger-names.md]

RDBOB9: when a migration creates a function, name it `ufn_<descriptor>` for what it does (`ufn_set_updated_at`, not `set_updated_at`). Reason: the prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it. Second opinion: DBA. [Rule; slug: ufn-function-names; full rule: .claude/examples/db_standards/ufn-function-names.md]

RDBOB10: when a migration creates a stored procedure, name it `usp_<descriptor>` for what it does (`usp_db_backups`, not `backup_databases`). Reason: the prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it. Second opinion: DBA. [Rule; slug: usp-procedure-names; full rule: .claude/examples/db_standards/usp-procedure-names.md]

RDBOB11: when a migration creates a view, name it `uv_<table>_<descriptor>`, with the table it reads from and what it does (`uv_bookings_status`, not `bookings_status`). Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: uv-view-names; full rule: .claude/examples/db_standards/uv-view-names.md]

RDBOB12: when a person creates a materialized view, name it `umv_<table>_<descriptor>`, with the table it reads from and what it does (`umv_bookings_monthly_totals`, not `monthly_totals`); a materialized view that an application creates is not covered. Reason: the pattern is a house convention, and consistency is what lets a reader tell an object from its name. Second opinion: DBA. [Rule; slug: umv-materialized-view-names; full rule: .claude/examples/db_standards/umv-materialized-view-names.md]

## Roles and users

RDBOB13: when a change creates a role, create it with no login rights and name it for the one thing it covers, in the singular, followed by its access level with an underscore between (`booking_ro`, `booking_rw`). Grant the access to the role and then grant the role to each person or service that needs it. Reason: when access has to grow, one role changes and not every user. Second opinion: DBA. [Rule; slug: role-no-login; full rule: .claude/examples/db_standards/role-no-login.md]

RDBOB14: when a change creates a database user, name a personal account `<name>_<team>_<access>` and a service account `svc` followed by the database and the access type (`svcbooking_ro`), and describe what a service account is for in the object's comment. Reason: the comment is what lets someone who finds a service account later learn what it is for. Second opinion: DBA. [Rule; slug: user-and-service-account-names; full rule: .claude/examples/db_standards/user-and-service-account-names.md]
