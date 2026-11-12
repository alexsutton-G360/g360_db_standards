---
slug: "no-honest-limit-decide-where"
title: "When data has no honest upper limit, decide on purpose where the limit lives"
temperature: "Judgment call"
origin: "general"
scope: "column"
why: "unbounded-data"
page: "columns"
group: "Text"
second_opinion: "DBA or Data Architect."
companion: true
---

# When data has no honest upper limit, decide on purpose where the limit lives

Some columns exist to hold whatever arrived, like the markdown extracted from a document or a raw vendor response. For these the length is a fact about the data, and a limit would invent a rule the data does not have. A comment typed by a user is different: it could be long in principle, but how long it should be is a decision, and that decision belongs in the column.

Work through these in order:

1. Is the length a fact about the data, or a choice someone should make? If it is a choice, make it and set the limit.
2. Will this data ever reach the warehouse? Raw fields like this rarely belong there. If not, tell the data teams the table must never be ported, so a sync does not break.
3. If it must reach the warehouse, can it be cut at 65,535 characters? The warehouse counts bytes and not characters, so see `multibyte-text`. The data teams need to know either way.
4. If it must arrive whole and cannot be cut, that is a Data Architect task. Expect the document to move to object storage, with a reference kept in the table.

Because: the database should enforce what is true about the data. For a document of any length, no limit is the true statement.

Second opinion: DBA or Data Architect.

More: companions/no-honest-limit-decide-where.md
