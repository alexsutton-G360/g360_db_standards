---
slug: "schema-for-real-divisions"
title: "Use a schema where it divides a database into parts that mean something, and name it for what it holds"
temperature: "Default"
origin: "general"
scope: "schema"
why: "schema-meaning"
page: "other_objects"
group: "Databases and schemas"
second_opinion: "DBA or Data Architect."
companion: false
---

# Use a schema where it divides a database into parts that mean something, and name it for what it holds

A schema is a logical division of a database. When a database has parts with different purposes, a schema is a good way to show it, and its name should tell a reader what is stored under it.

`public` is the default schema in most Groups360 systems, and it is fine to use. This rule is neither for it nor against it. It is about the schemas you add, and about adding one where the division is real.

Because: a schema name that says what it holds is information a reader gets for free. One that says nothing gives them nothing.

Good: `ops`, for functional operation data such as worker run tracking
Good: `extraction`, for data pulled directly out of uploads
Good: `canonization`, for data being integrated into our systems
Bad:  `misc`, which says nothing about what is stored there

Second opinion: DBA or Data Architect.
