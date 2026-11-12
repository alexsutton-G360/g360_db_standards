---
slug: "no-honest-limit-decide-where"
why: "unbounded-data"
---

# When data has no honest upper limit, decide on purpose where the limit lives

## Full rule

Some columns exist to hold whatever arrived, like the markdown extracted from a document or a raw vendor response. For these the length is a fact about the data, and a limit would invent a rule the data does not have. A comment typed by a user is different: it could be long in principle, but how long it should be is a decision, and that decision belongs in the column.

Work through these in order:

1. Is the length a fact about the data, or a choice someone should make? If it is a choice, make it and set the limit.
2. Will this data ever reach the warehouse? Raw fields like this rarely belong there. If not, tell the data teams the table must never be ported, so a sync does not break.
3. If it must reach the warehouse, can it be cut at 65,535 characters? The warehouse counts bytes and not characters, so see `multibyte-text`. The data teams need to know either way.
4. If it must arrive whole and cannot be cut, that is a Data Architect task. Expect the document to move to object storage, with a reference kept in the table.

Because: the database should enforce what is true about the data. For a document of any length, no limit is the true statement.

Second opinion: DBA or Data Architect.

## Why this rule exists

### Story: When the document is the data

A design at Groups360 for an image-processing service split the work into discrete steps. The older approach was a single process: query an image vendor, get back a document describing the images for a property, parse it, and write the results to the database. The new design split that into stages. One step queries the vendor and stores the document it gets back. A second step reads the stored document and cuts it into an image set. A third pushes the image set out to the services that need it. Each stage can be run, tested, and repeated on its own.

That design had one consequence for the database. The stored documents would be large. Each is only a collection of URLs, but one hotel's document from the vendor can run past 100,000 characters. The operational Postgres databases can hold that as a `text` column or a very wide `varchar` without trouble, but no choice of type makes it fit in the data warehouse.

The length of such a document is not a decision anyone makes. It is simply how long the vendor's response is, so the length is a fact about the data. A limit would mean inventing a rule the data does not have, which is the opposite of what a constraint is for. What matters is where the data goes next. Raw documents like this are rarely useful in the warehouse, and the likeliest outcome of the conversation with the data teams is a note that the table is never to be synced, so a sync does not break. If the warehouse does need the data, the options are to keep only the first 65,535 characters (see `multibyte-text` for why that count needs care) or to move the documents to object storage and keep a reference in the table.

The project was later pared down, and the large documents never became a live problem. The questions it raised are still the ones to ask of any column that could grow that large.

### Story: When characters and bytes disagree

Postgres counts the length of a varchar in characters. The warehouse counts it in bytes. For plain English text the two are the same, because every character takes one byte. For other text they are not. In UTF-8, accented European letters and Greek, Cyrillic, and Hebrew letters take two bytes, most Chinese, Japanese, and Korean characters take three, and emoji take four.

So a `varchar(65535)` in Postgres can hold a value that does not fit under the warehouse's 65,535-byte ceiling. A column of Greek text can need up to twice the room, and one of Chinese text or emoji three or four times as much. The result is the failure the ceiling rule exists to prevent: one oversized value reaches the warehouse, and every view built on that column can fail.

In practice this is a corner case on top of a corner case. A column near the ceiling is rare, because 65,000 characters is a lot of text for almost any field, and a column near the ceiling that also holds non-Latin text is rarer still. Names, codes, and URLs never come close.

When it does apply, set the limit lower, so that the worst case in bytes still fits. Dividing 65,535 by the widest character expected gives the ceiling: 32,767 characters for text that is at most two bytes per character, 21,845 for three, and 16,383 for four.

To check a value that is misbehaving, compare `char_length(value)` with `octet_length(value)` in Postgres. If the second is much larger than the first, the text is multibyte, and that is probably the reason.
