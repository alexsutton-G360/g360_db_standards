# Never go above varchar(65,535)

Rule line `RDBCL10` in `db_column_conventions.md`. Temperature: Rule. Origin: general. Second opinion: DBA or Data Architect, before creating anything longer.

## Full rule

Do not create a varchar longer than 65,535 characters, even though Postgres allows much more.

Because: the warehouse cannot hold more, and one oversized value takes down every view built on that column.

One special case: Postgres counts the length of a varchar in characters, but the warehouse counts bytes. Non-Latin text takes more bytes per character, so under the same ceiling the warehouse holds fewer characters of it than of Latin text. A column that may hold heavily non-Latin text can pass Postgres's limit and still hold a value too big for the warehouse. Story: `multibyte-text`, which has the arithmetic.

Second opinion: DBA or Data Architect, before creating anything longer.

## Why this rule exists

### Story: The text field that took down the views

Groups360 runs two kinds of database. The operational databases sit under Groupsync and the private label apps, and run PostgreSQL (version 17.11 as of November 2026, which may have changed since). Downstream is a data warehouse in Amazon Redshift, which is built differently and has a different toolkit. A sync tool, currently Stitch, copies flagged tables from one to the other and reshapes the data to fit.

Postgres allows far longer values than the warehouse does. Redshift has no `text` type at all, and its `varchar` stops at 65,535. A `text` column is where the mismatch bites, and the same sequence has played out more than once:

1. A field in Groupsync is defined as `text`.
2. The sync tool keeps up, raising the `varchar` size on the warehouse copy each time a longer value arrives.
3. A value arrives that is longer than any before it. The sync tool pulls it into the source table in the warehouse and updates that table's definition to fit.
4. The views built on top of that table do not follow. A materialized view fixes its column sizes when it is created and does not inherit later changes to the table underneath.
5. The next time a view tries to pull in the new value, it fails, and stays unavailable until someone finds the offending value and widens the column in the warehouse by hand.

Those views are critical infrastructure for billing and revenue recognition, so a column type chosen at design time becomes an outage in finance reporting. That is the whole case for `varchar` over `text`, and for never going above 65,535.

### Story: When characters and bytes disagree

Postgres counts the length of a varchar in characters. The warehouse counts it in bytes. For plain English text the two are the same, because every character takes one byte. For other text they are not. In UTF-8, accented European letters and Greek, Cyrillic, and Hebrew letters take two bytes, most Chinese, Japanese, and Korean characters take three, and emoji take four.

So a `varchar(65535)` in Postgres can hold a value that does not fit under the warehouse's 65,535-byte ceiling. A column of Greek text can need up to twice the room, and one of Chinese text or emoji three or four times as much. The result is the failure the ceiling rule exists to prevent: one oversized value reaches the warehouse, and every view built on that column can fail.

In practice this is a corner case on top of a corner case. A column near the ceiling is rare, because 65,000 characters is a lot of text for almost any field, and a column near the ceiling that also holds non-Latin text is rarer still. Names, codes, and URLs never come close.

When it does apply, set the limit lower, so that the worst case in bytes still fits. Dividing 65,535 by the widest character expected gives the ceiling: 32,767 characters for text that is at most two bytes per character, 21,845 for three, and 16,383 for four.

To check a value that is misbehaving, compare `char_length(value)` with `octet_length(value)` in Postgres. If the second is much larger than the first, the text is multibyte, and that is probably the reason.
