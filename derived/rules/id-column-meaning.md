---
slug: "id-column-meaning"
title: "A column named `id` is the table's bigint key, and `_id` points to one"
temperature: "Rule"
origin: "house"
scope: "column"
why: "id-guid-identifier"
page: "columns"
group: "Identifiers"
companion: true
---

# A column named `id` is the table's bigint key, and `_id` points to one

Name a table's auto-incrementing bigint primary key `id`. Name a column that points to another table's `id` for that table, in the singular: `property_id` points to `properties.id`. Store nothing but that bigint in a column named `id` or ending in `_id`.

Because: readers take "id" to describe both the type and the job of a column, so a column with that name has to be exactly that.

Good: `id`, `property_id`
Bad:  a uuid stored in `id`, an external system's reference stored in `vendor_id`

More: companions/id-column-meaning.md
