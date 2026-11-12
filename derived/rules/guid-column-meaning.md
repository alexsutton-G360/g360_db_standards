---
slug: "guid-column-meaning"
title: "A column named `guid` is a uuid, and `_guid` points to one"
temperature: "Rule"
origin: "house"
scope: "column"
why: "id-guid-identifier"
page: "columns"
group: "Identifiers"
companion: true
---

# A column named `guid` is a uuid, and `_guid` points to one

Name a table's uuid identifier `guid`. Name a column that points to another table's `guid` for that table, in the singular: `rfp_guid` points to `rfps.guid`. Store nothing but a uuid in a column named `guid` or ending in `_guid`, and never put a guid in a column named `id`.

If several tables in different services share a name, add the service name to remove the doubt: `<service_name>_<table>_guid`.

Good: `guid`, `user_guid`, and `<service_name>_<table>_guid` when the table name alone is ambiguous
Bad:  a bigint stored in `user_guid`

More: companions/guid-column-meaning.md
