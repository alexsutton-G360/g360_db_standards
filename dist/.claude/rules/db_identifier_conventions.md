---
description: Identifier conventions: id and guid columns, pointers, and which tables get a guid. Apply when a migration or model adds a key or a pointer column.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All identifiers rules are enumerated using the RDBID (Rules DataBase IDentifier conventions) code.

> Generated from the Groups360 database standards repository. Edit the pages there, not this file.

## Identifiers

RDBID1: when a migration or model adds a column named `id` or ending in `_id`, make it the table's auto-incrementing bigint primary key (`id`) or a bigint that points to another table's `id`, named for that table in the singular (`property_id` points to `properties.id`), and store nothing else in it, such as a uuid or an external system's reference. Reason: readers take "id" to describe both the type and the job of a column. [Rule; slug: id-column-meaning; full rule: .claude/examples/db_standards/id-column-meaning.md]

RDBID2: when a migration or model adds a column named `guid` or ending in `_guid`, make it a uuid: `guid` is the table's uuid identifier, and a column that points to another table's `guid` is named for that table in the singular (`rfp_guid` points to `rfps.guid`). Store nothing but a uuid in it, and never put a guid in a column named `id`. If several tables in different services share a name, add the service name: `<service_name>_<table>_guid`. [Rule; slug: guid-column-meaning; full rule: .claude/examples/db_standards/guid-column-meaning.md]

RDBID3: when a migration or model adds a column that holds an identifying value that is neither an id nor a guid, spell out the full word `identifier` (`external_identifier` for a value from another system). Reason: `external_id` would look like a foreign key to a table named `externals`. [Rule; slug: identifier-for-other-ids; full rule: .claude/examples/db_standards/identifier-for-other-ids.md]

RDBID4: when a migration or model adds a column that holds the `id` of a row in another table in the same database, declare a foreign key on it; a pointer with no key is only a convention. A pointer to a row in another database is a `_guid` and has no key. A table that can belong to one of several parents follows the polymorphic rules (`source-type-id-pattern`, `polymorphic-decision-matrix`) instead. Reason: the link has to hold no matter what code touches the data. [Rule; slug: same-database-pointer-needs-fk; full rule: .claude/examples/db_standards/same-database-pointer-needs-fk.md]

RDBID5: when a migration or model adds a column ending in `_by`, it must hold a user guid that points to identity_service, never a name, an email, or free text. Use `_by` without further discussion only when the value is always a user guid, is never unknown (so NOT NULL), and is never a machine or an anonymous person. Otherwise name the column for what it holds, or make it nullable only if the author can say in one sentence what null means. Null never means "a machine did it" or "anonymous". Reason: enough columns already mean this that it is a default. Second opinion: Data Architect. [Rule; slug: by-column-is-user-guid; full rule: .claude/examples/db_standards/by-column-is-user-guid.md]

RDBID6: when a migration or model adds a `_by` column for an actor that may be a machine or an anonymous person, do not use null and do not make up a stand-in value; the platform has not decided what such a column holds. Reason: a null there could be read as unknown or as "no user acted", and the platform has not said which. Second opinion: Data Architect. [Judgment call; slug: by-column-when-no-user; full rule: .claude/examples/db_standards/by-column-when-no-user.md]

## Row identity

RDBID7: when a migration creates a table, give it an `id`, junction tables included; a junction table also gets a unique constraint on its pair of foreign keys so the same two rows cannot be linked twice. A table without an `id` needs a reason stated where the table is defined. Reason: Groups360 finds the `id` useful for tooling and for correcting one row; it is a house convention and not a claim about correctness elsewhere. [Default; slug: id-on-every-table-including-junctions; full rule: .claude/examples/db_standards/id-on-every-table-including-junctions.md]

RDBID8: never let an `id` be the value that finds a row from outside the database, whether in an API, a URL, or anything a person could substitute, replay, or edit; look the row up by its `guid`, and hold a reference to another service's row as a `guid`. Showing an `id` in a report or an admin panel is fine. Reason: an `id` can be walked (`/users/42`, then 43, then 44) and means nothing outside the database that issued it. [Rule; slug: id-internal-guid-external; full rule: .claude/examples/db_standards/id-internal-guid-external.md]

RDBID9: when a migration creates a table that something outside the database may point at, give it a `guid` and decide that when the table is created; if in doubt, add it. A junction table does not get a `guid`. Declare it unique when the column is created. Reason: a `guid` is simplest on the day the table is created, since adding it later takes a backfill and then the constraints, and costs more as the table grows. [Default; slug: guid-for-externally-referenced-tables; full rule: .claude/examples/db_standards/guid-for-externally-referenced-tables.md]

RDBID10: when a migration adds a `guid` column, make it NOT NULL and UNIQUE, enforced by the database. Either the application or the database (for example a `gen_random_uuid()` default) may generate it, so generate it where it is first needed. Reason: with those two constraints a guid that was never generated is refused, and so is one that repeats, whoever fills it in. [Default; slug: guid-not-null-unique-generated-anywhere; full rule: .claude/examples/db_standards/guid-not-null-unique-generated-anywhere.md]
