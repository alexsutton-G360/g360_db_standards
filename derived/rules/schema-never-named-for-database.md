---
slug: "schema-never-named-for-database"
title: "Do not name a schema after its own database"
temperature: "Rule"
origin: "general"
scope: "schema"
why: "schema-meaning"
page: "other_objects"
group: "Databases and schemas"
second_opinion: "DBA or Data Architect."
companion: false
---

# Do not name a schema after its own database

A schema inside a database called `invoice_service` is not called `invoice_service`. The name repeats what the reader already knows and adds nothing.

It also costs something. A table reaches the warehouse named for its database, its schema, and its table, so an `invoices` table in that schema arrives as `invoice_service_invoice_service_invoices`. A long name is part of how the warehouse works, and the `public` schema produces one too, as `invoice_service_public_invoices`. But a schema that repeats the database makes the long name worse and gives nothing back.

Because: the schema name is the one place in the full name that can say something new, and repeating the database spends it on nothing.

Good: `invoice_service` as a database holding an `accounting` schema
Bad:  `invoice_service` as a database holding an `invoice_service` schema

Second opinion: DBA or Data Architect.
