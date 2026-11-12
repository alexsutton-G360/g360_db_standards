---
slug: "name-column-for-the-fact"
title: "Name a column for the fact it stores, not the action it asks for"
temperature: "Default"
origin: "general"
scope: "column"
why: "declarative-names"
page: "columns"
group: "Naming"
companion: true
---

# Name a column for the fact it stores, not the action it asks for

A table holds facts, so name columns as statements of fact. Avoid commands.

Because: a table records what is true about a row, not instructions for what to do with it.

Good: `excluded_properties`, `has_attachments`
Bad:  `exclude_properties`, `add_attachments`

A table that really does hold instructions, such as jobs to run, is the exception.

More: companions/name-column-for-the-fact.md
