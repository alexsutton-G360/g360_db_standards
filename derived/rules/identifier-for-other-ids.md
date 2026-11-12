---
slug: "identifier-for-other-ids"
title: "Use `identifier` for any identifying value that is neither an id nor a guid"
temperature: "Rule"
origin: "house"
scope: "column"
why: "id-guid-identifier"
page: "columns"
group: "Identifiers"
companion: true
---

# Use `identifier` for any identifying value that is neither an id nor a guid

Spell out the full word `identifier`: `external_identifier` for a value that came from another system.

Because: `external_id` would look like a foreign key to a table named `externals`.

More: companions/identifier-for-other-ids.md
