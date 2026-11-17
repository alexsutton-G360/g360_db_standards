---
description: Column design conventions for database changes. Apply when a migration or data model adds, changes, or names a column.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All column rules are enumerated using the RDBCL (Rules DataBase CoLumn conventions) code.

> Generated from the database standards repository. Edit the pages and overlay there, not this file.

## Nullability

RDBCL1: when a migration or model adds a column, make it NOT NULL unless you can say in one sentence what a null in it means. "Unknown" and "does not apply" are honest answers; anything vaguer means the column is not ready to be nullable. Reason: an accidental null lets an invalid row in, and the fault surfaces months later. [slug: not-null-until-null-has-meaning]

RDBCL2: a nullable boolean has three states, so use one only when all three mean something. For any other three-way choice, use a constrained set. [slug: nullable-boolean-three-states]

## Dates and times

RDBCL3: use `timestamptz` for a moment in time. Never use a plain `timestamp` unless something forces it, and then store only UTC. Reason: a plain timestamp drops the time zone on insert, so values that look the same can mean different instants. [slug: no-timestamp-without-time-zone]
