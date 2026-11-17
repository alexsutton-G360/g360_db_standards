---
description: Column design conventions: nullability, dates and times, text limits, fixed sets, and database-maintained values. Apply when a change adds or alters a column.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All columns rules are enumerated using the RDBCL (Rules DataBase CoLumn conventions) code.

> Generated from the Groups360 database standards repository. Edit the pages there, not this file.

## Nullability

RDBCL1: when a migration or model adds a column, make it NOT NULL unless you can say in one sentence what a null in it means. "Unknown" and "does not apply" are honest answers; anything vaguer means the column is not ready to be nullable. Reason: an accidental null lets an invalid row in, and the fault surfaces months later. [Default; slug: not-null-until-null-has-meaning; full rule: .claude/examples/db_standards/not-null-until-null-has-meaning.md]

RDBCL2: when a migration adds a NOT NULL column to a table that already has rows, or tightens a nullable column to NOT NULL, require one of three plans: a default that is honestly right for every old row, a backfill that finishes before the constraint is added, or a staged deploy (add nullable, start writing it, backfill, then add the constraint). The values must be real, not placeholders chosen to satisfy the constraint. Reason: the change fails outright, or takes the strongest lock on the table while rows are checked. [Rule; slug: plan-for-existing-rows; full rule: .claude/examples/db_standards/plan-for-existing-rows.md]

RDBCL3: when a migration or model adds a nullable boolean, use it only if true, false, and null each mean something; for any other three-way choice, use a constrained set. Reason: a nullable boolean has three states, so all three must carry a meaning. [Rule; slug: nullable-boolean-three-states; full rule: .claude/examples/db_standards/nullable-boolean-three-states.md]

## Dates and times

RDBCL4: when a migration or model adds a column for a point in time, use `date` when what matters is the day (availability on March 4, an arrival on April 1) and `timestamptz` when what matters is the moment (when a record was created). [Rule; slug: date-for-day-timestamptz-for-moment; story: unlabeled-timestamps, future-local-time; full rule: .claude/examples/db_standards/date-for-day-timestamptz-for-moment.md]

RDBCL5: when a migration or model names a date or timestamp column, end the name with `_on` only if it is a date and with `_at` only if it is a timestamp; a name with no preposition, like `arrival_date`, is always fine, and no preposition is required. Reason: a thing happens on a day and at a moment, so a mismatched preposition gives the reader a wrong first assumption. [Default; slug: date-name-preposition-match; full rule: .claude/examples/db_standards/date-name-preposition-match.md]

RDBCL6: never use `timestamp` without a time zone; use `timestamptz`. If something truly forces a plain `timestamp`, store only UTC in it, with no exceptions. Reason: a plain timestamp drops the time zone on insert, so values that look the same can mean different times, and a column of mixed zones cannot be untangled afterward. [Rule; slug: no-timestamp-without-time-zone; story: unlabeled-timestamps, future-local-time; full rule: .claude/examples/db_standards/no-timestamp-without-time-zone.md]

RDBCL7: store every timestamp in UTC and convert to local time only in the display layer; local time almost never belongs in storage. If a case seems to need local time, read the story `future-local-time` before deciding. [Rule; slug: store-utc-convert-for-display; story: unlabeled-timestamps, future-local-time; full rule: .claude/examples/db_standards/store-utc-convert-for-display.md]

## Text

RDBCL8: when a migration or model adds a text column, use `varchar` with a limit. Do not use `char`, and `text` is almost never right; the narrow exception is data with no honest upper limit (`no-honest-limit-decide-where`). Reason: text can outgrow the warehouse and crash billing views, while char pads values with whitespace for no benefit. [Rule; slug: varchar-over-char-and-text; story: shape-sorter, warehouse-view-crash; full rule: .claude/examples/db_standards/varchar-over-char-and-text.md]

RDBCL9: when a migration or model adds a varchar, give it the smallest limit the data honestly allows (`varchar(3)` for an ISO currency code, `varchar(50)` for a free-form event name), not `text`, `varchar(255)`, or `varchar(65535)` by habit. Reason: a limit the database does not enforce is only an opinion, and raising a limit later is lossless while lowering one is not. [Default; slug: smallest-honest-varchar-limit; story: notes-field-surprises; full rule: .claude/examples/db_standards/smallest-honest-varchar-limit.md]

RDBCL10: never create a varchar longer than 65,535 characters, even though Postgres allows more. Non-Latin text takes more bytes per character in the warehouse, so a column that may hold heavily non-Latin text can pass Postgres's limit and still hold a value too big for the warehouse (story `multibyte-text`). Reason: the warehouse cannot hold more, and one oversized value takes down every view built on that column. Second opinion: DBA or Data Architect, before creating anything longer. [Rule; slug: varchar-ceiling-65535; story: warehouse-view-crash, multibyte-text; full rule: .claude/examples/db_standards/varchar-ceiling-65535.md]

RDBCL11: when a migration or model adds a column for an email address, use `varchar(254)`; use 320 only with a very good reason. Reason: 320 is the RFC maximum, but 254 is the practical limit that mail servers along the way enforce. [Default; slug: email-varchar-254; story: email-length-limits; full rule: .claude/examples/db_standards/email-varchar-254.md]

RDBCL12: when a migration or model adds a column that holds a URL, use `varchar(2048)`, or a smaller limit when the URL comes from something known and controlled; go longer only with a good reason, and never use `text` or `varchar(65535)`. Reason: about 2,000 characters works in virtually any browser, server, and search tooling, and the sitemap protocol caps URLs at 2,048. [Default; slug: url-varchar-2048; full rule: .claude/examples/db_standards/url-varchar-2048.md]

RDBCL13: when a migration or model adds a column that may have no honest upper limit, such as extracted document text or a raw vendor response, decide on purpose where the limit lives. Ask in order: is the length a fact about the data or a choice someone should make (a choice gets a limit); will the data reach the warehouse (if not, the data teams must be told the table is never to be ported); can it be cut at 65,535 characters; and if it must arrive whole and cannot be cut, that is a Data Architect task. Reason: the database should enforce what is true about the data. Second opinion: DBA or Data Architect. [Judgment call; slug: no-honest-limit-decide-where; story: image-documents, multibyte-text; full rule: .claude/examples/db_standards/no-honest-limit-decide-where.md]

RDBCL14: when a migration or model adds a text or varchar column that holds several values in one delimited string, use an array column or a second table instead; an array such as `varchar(254)[]` keeps the varchar limit on each element. Reason: a delimited string only works while every value avoids the delimiter and every reader splits it the same way, and nothing in the database enforces either. [Rule; slug: no-delimited-list-strings; story: contact-list; full rule: .claude/examples/db_standards/no-delimited-list-strings.md]

## Values from a fixed set

RDBCL15: when a migration or model adds a short text column, ask whether it holds one of a known set of values; if it does or might, treat it as constrained and say so in the design, and leave it open only for a stated reason. A column named `status`, `type`, `kind`, `mode`, or `category`, or one that names a strategy or a method, likely hides a fixed set. Reason: an open column collects whatever anyone writes into it, and every reader downstream has to cope with the variations. [Default; slug: short-text-is-a-fixed-set; full rule: .claude/examples/db_standards/short-text-is-a-fixed-set.md]

RDBCL16: when a column holds one of a fixed set of values, enforce the set in the database; a check in application code alone does not count. Reason: a limit kept in application code is an opinion, and a limit in the database is true for every writer. [Rule; slug: database-enforces-fixed-set; full rule: .claude/examples/db_standards/database-enforces-fixed-set.md]

RDBCL17: when a migration or model enforces a fixed set of values, choose the mechanism by asking whether each value carries anything with it, such as a display label, sort order, active flag, or description. Use a lookup table with a foreign key when values carry something or the set will expand regularly. Use a check constraint on a varchar, or an enum, when each value is only a string and the set rarely changes; an enum costs more to change, since a value cannot be dropped and moving a column onto one rewrites the table. [Judgment call; slug: choose-fixed-set-mechanism; full rule: .claude/examples/db_standards/choose-fixed-set-mechanism.md]

## Values the database maintains

RDBCL18: when a migration or model adds a column whose value can be worked out from other columns in the same row, make it a generated column and not application code. A generated column can use only columns of its own row; if the value needs other tables, or must be computed when read, use a view instead (`no-second-copy-use-a-view`, `plain-view-before-materialized`). A value that depends on how the row changed cannot be generated (`trigger-for-change-dependent-value`). Reason: a derived value that code keeps in step is only as reliable as every run of that code. [Default; slug: same-row-value-generated-column; story: derived-by-process; full rule: .claude/examples/db_standards/same-row-value-generated-column.md]

RDBCL19: when a migration or model adds a value that depends on when or how a row changed, and not on its other columns, let a trigger maintain it rather than application code; a generated column cannot, because its formula must give the same answer every time. The shared `updated_at` trigger is the worked example (`shared-updated-at-trigger`). A different value gets a function of its own in the same shape, named by `trg-trigger-names` and `ufn-function-names`. Reason: a trigger maintains the value for every writer. [Default; slug: trigger-for-change-dependent-value; story: derived-by-process; full rule: .claude/examples/db_standards/trigger-for-change-dependent-value.md]
