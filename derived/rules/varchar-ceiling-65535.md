---
slug: "varchar-ceiling-65535"
title: "Never go above varchar(65,535)"
temperature: "Rule"
origin: "general"
scope: "column"
why: "redshift-varchar-ceiling"
page: "columns"
group: "Text"
second_opinion: "DBA or Data Architect, before creating anything longer."
companion: true
---

# Never go above varchar(65,535)

Do not create a varchar longer than 65,535 characters, even though Postgres allows much more.

Because: the warehouse cannot hold more, and one oversized value takes down every view built on that column.

One special case: Postgres counts the length of a varchar in characters, but the warehouse counts bytes. Non-Latin text takes more bytes per character, so under the same ceiling the warehouse holds fewer characters of it than of Latin text. A column that may hold heavily non-Latin text can pass Postgres's limit and still hold a value too big for the warehouse. Story: `multibyte-text`, which has the arithmetic.

Second opinion: DBA or Data Architect, before creating anything longer.

More: companions/varchar-ceiling-65535.md
