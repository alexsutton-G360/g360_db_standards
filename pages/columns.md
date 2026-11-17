# Columns

Rules for naming columns, choosing their types, and the columns almost every table carries. The rules on Global Rules apply here too, so a column name is lowercase, uses underscores between words, and so on. Where a rule below says otherwise, this page wins.

## Naming

### Name a column for the fact it stores, not the action it asks for
[Slug: name-column-for-the-fact · Temperature: Default · Origin: general · Scope: column · Why: declarative-names]

A table holds facts, so name columns as statements of fact. Avoid commands.

Because: a table records what is true about a row, not instructions for what to do with it.

Good: `excluded_properties`, `has_attachments`
Bad:  `exclude_properties`, `add_attachments`

A table that really does hold instructions, such as jobs to run, is the exception.

Agent: when a migration or model names a column, name it for the fact it stores, not the action it asks for (`excluded_properties`, not `exclude_properties`). A table that really holds instructions, such as jobs to run, is the exception. Reason: a table records what is true about a row, not instructions for what to do with it.

---

### Name columns in the positive voice
[Slug: columns-in-positive-voice · Temperature: Default · Origin: general · Scope: column · Why: positive-voice]

Name a flag for what is true, not for what is not. Avoid negations. Pairs that differ only by a negating verb lean the same way, less strictly.

Because: code that tests a negated name reads as a double negative, and the extra words add nothing.

Good: `is_active`, `has_attachments`
Bad:  `is_not_active`, `does_not_have_attachments`

This one bends when another name reads more clearly. Story: `hidden-vs-displayed`.

Agent: when a migration or model names a flag column, name it for what is true, not for what is not (`is_active`, not `is_not_active`). This bends when another name reads more clearly; see the story `hidden-vs-displayed`. Reason: code that tests a negated name reads as a double negative.

---

### Name columns in the singular
[Slug: columns-in-singular · Temperature: Default · Origin: house · Scope: column · Why: singular-columns]

Use the singular for a column name. A row is one instance of the thing its table holds, so its properties are named in the singular. Table names are plural, so a plural column name would also read as a plural inside a plural.

Good: `first_name`, `user_guid`
Bad:  `first_names`, `user_guids`

This one bends easily. A column that really holds many values, like an array, can be plural.

Agent: when a migration or model names a column, use the singular (`first_name`, `user_guid`); a column that really holds many values, like an array, can be plural. Reason: a row is one instance of what its plural-named table holds, so its properties are singular.

---

### Check what a numbered column name is really saying
[Slug: numbered-column-names · Temperature: Judgment call · Origin: house · Scope: column · Why: numbered-columns]

Digits in a column name are fine when the numbers are the point. Names that differ only by number, like `contact_1` and `contact_2`, tell a reader the two are parallel slots. A pair like `contact` and `contact_2` tells the reader that one outranks the other. If that is not what the data means, the reader's first assumption is wrong.

Before adding a numbered column, ask what the second column really is. If it is the newer version of the first, or one is the main one, name each for what it is.

Good: `contact_1` and `contact_2`, when there are two parallel contacts
Good: `primary_contact` and `secondary_contact`, when one outranks the other
Bad:  `contact` and `contact_2`

Agent: when a migration or model adds a column whose name ends in a number, such as `contact_2`, ask what the second column really is. Parallel slots can be `contact_1` and `contact_2`, but if one outranks the other or is the newer version, name each for what it is (`primary_contact` and `secondary_contact`), because a pair like `contact` and `contact_2` tells the reader that one outranks the other.

---

## Identifiers

### A column named `id` is the table's bigint key, and `_id` points to one
[Slug: id-column-meaning · Temperature: Rule · Origin: house · Scope: column · Why: id-guid-identifier]

Name a table's auto-incrementing bigint primary key `id`. Name a column that points to another table's `id` for that table, in the singular: `property_id` points to `properties.id`. Store nothing but that bigint in a column named `id` or ending in `_id`.

Because: readers take "id" to describe both the type and the job of a column, so a column with that name has to be exactly that.

Good: `id`, `property_id`
Bad:  a uuid stored in `id`, an external system's reference stored in `vendor_id`

Agent: when a migration or model adds a column named `id` or ending in `_id`, make it the table's auto-incrementing bigint primary key (`id`) or a bigint that points to another table's `id`, named for that table in the singular (`property_id` points to `properties.id`), and store nothing else in it, such as a uuid or an external system's reference. Reason: readers take "id" to describe both the type and the job of a column.

---

### A column named `guid` is a uuid, and `_guid` points to one
[Slug: guid-column-meaning · Temperature: Rule · Origin: house · Scope: column · Why: id-guid-identifier]

Name a table's uuid identifier `guid`. Name a column that points to another table's `guid` for that table, in the singular: `rfp_guid` points to `rfps.guid`. Store nothing but a uuid in a column named `guid` or ending in `_guid`, and never put a guid in a column named `id`.

If several tables in different services share a name, add the service name to remove the doubt: `<service_name>_<table>_guid`.

Good: `guid`, `user_guid`, and `<service_name>_<table>_guid` when the table name alone is ambiguous
Bad:  a bigint stored in `user_guid`

Agent: when a migration or model adds a column named `guid` or ending in `_guid`, make it a uuid: `guid` is the table's uuid identifier, and a column that points to another table's `guid` is named for that table in the singular (`rfp_guid` points to `rfps.guid`). Store nothing but a uuid in it, and never put a guid in a column named `id`. If several tables in different services share a name, add the service name: `<service_name>_<table>_guid`.

---

### Use `identifier` for any identifying value that is neither an id nor a guid
[Slug: identifier-for-other-ids · Temperature: Rule · Origin: house · Scope: column · Why: id-guid-identifier]

Spell out the full word `identifier`: `external_identifier` for a value that came from another system.

Because: `external_id` would look like a foreign key to a table named `externals`.

Agent: when a migration or model adds a column that holds an identifying value that is neither an id nor a guid, spell out the full word `identifier` (`external_identifier` for a value from another system). Reason: `external_id` would look like a foreign key to a table named `externals`.

---

### A column that points at a row in the same database needs a real foreign key
[Slug: same-database-pointer-needs-fk · Temperature: Rule · Origin: general · Scope: column · Why: real-foreign-keys]

If a column holds the `id` of a row in another table in the same database, declare a foreign key on it. A column that looks like a pointer but has no foreign key behind it is only a convention, and it holds only as long as every piece of code that touches the data respects it. The database cannot refuse a missing parent, cannot protect a parent that still has children, and cannot tell anyone the link exists.

When the row lives in another database, which happens often in a microservice setup, no foreign key is possible. That column is a `_guid` and not an `_id`, and having no key behind it is expected. Why a `guid` is what travels between databases is under Row identity on Tables.

One case inside a single database needs more than this rule says: a table that can belong to one of several parents. A plain pointer column and a foreign key do not fit it, and there is a good deal more to say about keeping real keys there. That is covered in the group Tables that belong to one of several parents, on Tables. It includes the pattern you will meet most often in existing tables (*rule: source-type-id-pattern*) and a short way to choose among the designs (*rule: polymorphic-decision-matrix*).

A foreign key does not index its column. Whether to add an index is a separate decision, covered under Indexes on Tables.

Because: the database is the lowest level at which something can be true. An application that knows about the link is not enough, because the link has to hold no matter what code touches the data.

Good: `property_id`, with a foreign key to `properties (id)`, and `rfp_guid`, pointing at another service, with no key
Bad:  `property_id` holding a real property id, with no foreign key declared

Agent: when a migration or model adds a column that holds the `id` of a row in another table in the same database, declare a foreign key on it; a pointer with no key is only a convention. A pointer to a row in another database is a `_guid` and has no key. A table that can belong to one of several parents follows the polymorphic rules (`source-type-id-pattern`, `polymorphic-decision-matrix`) instead. Reason: the link has to hold no matter what code touches the data.

---

### A column ending in `_by` holds a user guid from identity_service
[Slug: by-column-is-user-guid · Temperature: Rule · Origin: house · Scope: column · Why: by-columns]

If a column ends in `_by`, it holds a guid that points to a user in identity_service. Never a name, an email, or free text.

Use `_by` without further conversation when all three of these are true:

1. It is always a user guid pointing at identity_service.
2. It is never unknown, so it is `NOT NULL`.
3. There is no extra texture: no anonymous users, no automated actors, nobody it could be besides a logged-in person.

Everything else is an engineering question, so here are the questions:

- Is it really a user guid? If not, do not call it `_by`. Name it for what it holds.
- Can it genuinely be unknown or not applicable? Then it is nullable, and the author must be able to say in one sentence what null means.
- Can a machine or an anonymous person do this? That is a platform decision. See the next rule.

Null never means "a machine did it" or "anonymous". Null means unknown or not applicable, as everywhere else on these pages.

Because: enough columns already end in `_by` and mean this that it has become a default, so keeping one meaning costs less than a second dialect.

Second opinion: Data Architect.

Agent: when a migration or model adds a column ending in `_by`, it must hold a user guid that points to identity_service, never a name, an email, or free text. Use `_by` without further discussion only when the value is always a user guid, is never unknown (so NOT NULL), and is never a machine or an anonymous person. Otherwise name the column for what it holds, or make it nullable only if the author can say in one sentence what null means. Null never means "a machine did it" or "anonymous". Reason: enough columns already mean this that it is a default.

---

### What a `_by` column holds when no user acted is an open decision
[Slug: by-column-when-no-user · Temperature: Judgment call · Origin: house · Scope: column · Why: system-actors]

This question is open on purpose, and your design may be the reason to close it. The platform has no settled answer for what a `_by` column holds when the actor is a machine or an anonymous person, and this page does not guess.

If a design needs it, that is the signal the question is due. Bring it to the Data Architect, so it can be decided together with the other architects and directors and not by one team on its own.

Until it is decided, do not use null for it, since a null there could be read as unknown or as "no user acted" and the platform has not said which, and do not make up a stand-in value on your own.

Open since: October 2026.

Second opinion: Data Architect.

Agent: when a migration or model adds a `_by` column for an actor that may be a machine or an anonymous person, do not use null and do not make up a stand-in value; the platform has not decided what such a column holds. Reason: a null there could be read as unknown or as "no user acted", and the platform has not said which.

---

## Standard columns

The columns nearly every table carries, `created_at` and `updated_at`, are covered on Tables, under row lifecycle. They are a decision about the table and not about one piece of data. How to name and type a timestamp column in general is under Dates and times, below.

---

## Nullability

### Make every column NOT NULL until you can say what a null in it would mean
[Slug: not-null-until-null-has-meaning · Temperature: Default · Origin: general · Scope: column · Why: null-needs-a-meaning]

Start every column as NOT NULL. Allow null only when the author can say, in one sentence, what a null in that column means.

There are two honest answers. Null can mean the value is unknown: it exists, and the system does not have it. Or null can mean there is no such value for this row: it does not exist, does not apply, or does not exist yet. An answer vaguer than either, like "not sure yet" or "might be handy", means the column is not ready to be nullable.

The point is not to avoid nulls. It is to avoid errant ones, where a null means something the next reader would not guess. When several nullable columns together carry one fact, say so in a check constraint: if exactly one of them must be set, or at least one, enforce it, as the polymorphic rules on Tables do.

Because: a column that is nullable by accident lets someone create an invalid row, and the fault turns up months later, far from its cause. A NOT NULL column turns the same mistake into an error on the day it happens, when it is cheap to fix. A null used as a stand-in for false hides a decision nobody made, so give the column a default instead.

Good: a property's identifier in an outside system, null for properties that do not use that system, because there is none to store
Good: a booking's `confirmation_number`, null until the booking reaches its final phase, because it does not exist yet
Bad:  a hotel's room count left nullable. A hotel without one is an invalid record, so let the database refuse it.
Bad:  a lease's `end_date` left null both for "open-ended" and for "not entered yet". A reader cannot tell which, so settle on one meaning and give the other its own representation, such as a NOT NULL `is_open_ended` flag.
Bad:  a flag for whether a property shows in search, where null is treated as false. Give it a default of false.

Agent: when a migration or model adds a column, make it NOT NULL unless you can say in one sentence what a null in it means. "Unknown" and "does not apply" are honest answers; anything vaguer means the column is not ready to be nullable. Reason: an accidental null lets an invalid row in, and the fault surfaces months later.

---

### Give a NOT NULL column a plan for the rows already in the table
[Slug: plan-for-existing-rows · Temperature: Rule · Origin: general · Scope: column · Why: not-null-existing-rows]

Adding a NOT NULL column to a table that already has rows, or tightening an existing nullable column to NOT NULL, needs a plan for the rows already there before the change ships. The plan is one of three:

- A default that fills the existing rows, when one value is honestly right for every old row.
- A backfill that finishes before the constraint is added, when the right value has to be worked out row by row.
- A staged deploy, when old code is still writing rows without the column. The column goes in nullable and the application starts writing it, then the backfill runs, and the constraint comes last.

Whichever plan is chosen, the values it puts in must be real. A value picked only to satisfy the constraint turns a NOT NULL column into one that lies.

The larger the table, the more care this takes. See the note on scale on the Index.

Because: the database refuses the change outright when existing rows would break it, and when a change does go through, tightening a column takes the strongest lock on the table while the rows are checked. On a busy table, either one is an outage.

Good: `is_archived` added with a default of false, because every existing row is genuinely not archived
Bad:  `contact_email` added as NOT NULL with a default of an empty string, only so the change would go through

Agent: when a migration adds a NOT NULL column to a table that already has rows, or tightens a nullable column to NOT NULL, require one of three plans: a default that is honestly right for every old row, a backfill that finishes before the constraint is added, or a staged deploy (add nullable, start writing it, backfill, then add the constraint). The values must be real, not placeholders chosen to satisfy the constraint. Reason: the change fails outright, or takes the strongest lock on the table while rows are checked.

---

### Use a nullable boolean only when true, false, and unknown are all real answers
[Slug: nullable-boolean-three-states · Temperature: Rule · Origin: general · Scope: column · Why: null-needs-a-meaning]

A nullable boolean has three states, so use one only when all three mean something. For any other three-way choice, see the guidance on values from a fixed set on this page.

Good: "does this property charge for parking?", where null means it is not known whether it does
Bad:  a nullable boolean standing in for a three-way choice that has names, like draft, hold, and confirmed

Agent: when a migration or model adds a nullable boolean, use it only if true, false, and null each mean something; for any other three-way choice, use a constrained set. Reason: a nullable boolean has three states, so all three must carry a meaning.

---

## Dates and times

### Use `date` for a day and `timestamptz` for a moment
[Slug: date-for-day-timestamptz-for-moment · Temperature: Rule · Origin: general · Scope: column · Why: timestamptz-utc]

Use `date` when what matters is the day something happens, like availability on March 4 or an arrival on April 1. Use `timestamptz` when what matters is the moment, like when a record was created.

Agent: when a migration or model adds a column for a point in time, use `date` when what matters is the day (availability on March 4, an arrival on April 1) and `timestamptz` when what matters is the moment (when a record was created).

---

### If a date or timestamp name ends in a preposition, make it match the type
[Slug: date-name-preposition-match · Temperature: Default · Origin: general · Scope: column · Why: date-prepositions]

End a name with `_on` only when the column is a date, and with `_at` only when it is a timestamp. Never put `_on` on a timestamp or `_at` on a date. A name with no preposition, like `arrival_date`, is always fine.

Because: a thing happens on a day and at a moment, so the preposition tells a reader the type before they look it up. A mismatch gives the reader a wrong first assumption.

Good: `created_at` holding a `timestamptz`, `arrival_date` holding a `date`
Bad:  `approved_on` holding a `timestamptz`, `arrival_at` holding a `date`

This is mostly a prohibition. It does not require a preposition, and it does not require `_on` for dates.

Agent: when a migration or model names a date or timestamp column, end the name with `_on` only if it is a date and with `_at` only if it is a timestamp; a name with no preposition, like `arrival_date`, is always fine, and no preposition is required. Reason: a thing happens on a day and at a moment, so a mismatched preposition gives the reader a wrong first assumption.

---

### Never use `timestamp` without a time zone
[Slug: no-timestamp-without-time-zone · Temperature: Rule · Origin: general · Scope: column · Why: timestamptz-utc]

Use `timestamptz`. If something truly forces a plain `timestamp`, store only UTC in it, with no exceptions.

Because: a plain timestamp drops the time zone when a value is inserted, so a value that looks the same can mean different times depending on the session that wrote it, and a column of mixed zones cannot be untangled afterward.

Agent: never use `timestamp` without a time zone; use `timestamptz`. If something truly forces a plain `timestamp`, store only UTC in it, with no exceptions. Reason: a plain timestamp drops the time zone on insert, so values that look the same can mean different times, and a column of mixed zones cannot be untangled afterward.

---

### Store timestamps in UTC and convert only for display
[Slug: store-utc-convert-for-display · Temperature: Rule · Origin: general · Scope: column · Why: timestamptz-utc]

Store every timestamp in UTC and convert to local time in the display layer. Local time almost never belongs in storage.

There is nuance here, but not much. The one arguable case is told in `future-local-time`.

Agent: store every timestamp in UTC and convert to local time only in the display layer; local time almost never belongs in storage. If a case seems to need local time, read the story `future-local-time` before deciding.

---

## Text

### Use varchar, not char or text
[Slug: varchar-over-char-and-text · Temperature: Rule · Origin: general · Scope: column · Why: varchar-vs-text]

Use varchar, with a limit. Do not use char. Text is almost never right either, but there are a few narrow situations where it is, mainly data with no honest upper limit, covered below.

Because: text can outgrow the warehouse and crash billing views, while char pads values with whitespace for no benefit.

Agent: when a migration or model adds a text column, use `varchar` with a limit. Do not use `char`, and `text` is almost never right; the narrow exception is data with no honest upper limit (`no-honest-limit-decide-where`). Reason: text can outgrow the warehouse and crash billing views, while char pads values with whitespace for no benefit.

---

### Give every varchar the smallest limit your data honestly allows
[Slug: smallest-honest-varchar-limit · Temperature: Default · Origin: general · Scope: column · Why: varchar-limits]

Understand your data and constrain it as far as you practically can.

Because: a limit the database does not enforce is only an opinion, and raising a limit later is lossless while lowering one is not.

Good: `varchar(3)` for an ISO currency code, `varchar(50)` for a free-form event name
Bad:  `text` or `varchar(255)` for a currency code, `varchar(65535)` for an event name

Agent: when a migration or model adds a varchar, give it the smallest limit the data honestly allows (`varchar(3)` for an ISO currency code, `varchar(50)` for a free-form event name), not `text`, `varchar(255)`, or `varchar(65535)` by habit. Reason: a limit the database does not enforce is only an opinion, and raising a limit later is lossless while lowering one is not.

---

### Never go above varchar(65,535)
[Slug: varchar-ceiling-65535 · Temperature: Rule · Origin: general · Scope: column · Why: redshift-varchar-ceiling]

Do not create a varchar longer than 65,535 characters, even though Postgres allows much more.

Because: the warehouse cannot hold more, and one oversized value takes down every view built on that column.

One special case: Postgres counts the length of a varchar in characters, but the warehouse counts bytes. Non-Latin text takes more bytes per character, so under the same ceiling the warehouse holds fewer characters of it than of Latin text. A column that may hold heavily non-Latin text can pass Postgres's limit and still hold a value too big for the warehouse. Story: `multibyte-text`, which has the arithmetic.

Second opinion: DBA or Data Architect, before creating anything longer.

Agent: never create a varchar longer than 65,535 characters, even though Postgres allows more. Non-Latin text takes more bytes per character in the warehouse, so a column that may hold heavily non-Latin text can pass Postgres's limit and still hold a value too big for the warehouse (story `multibyte-text`). Reason: the warehouse cannot hold more, and one oversized value takes down every view built on that column.

---

### Email addresses: varchar(254)
[Slug: email-varchar-254 · Temperature: Default · Origin: general · Scope: column · Why: email-limits]

Use `varchar(254)` for an email address. Use 320 only with a very good reason.

Because: 320 is the RFC maximum, but 254 is the practical limit that mail servers along the way enforce.

Agent: when a migration or model adds a column for an email address, use `varchar(254)`; use 320 only with a very good reason. Reason: 320 is the RFC maximum, but 254 is the practical limit that mail servers along the way enforce.

---

### Store a URL in varchar(2048)
[Slug: url-varchar-2048 · Temperature: Default · Origin: general · Scope: column · Why: url-limits]

Use `varchar(2048)` for a column that holds a URL. It is a good default limit, and about as big as a URL should be. Go longer only if it really makes sense to, which it probably does not. If the URL comes from something you know and control, you are encouraged to use a smaller field. You do not have to, but a smaller limit is better design whenever the data allows it (*rule: smallest-honest-varchar-limit*).

Because: no standard limits the length of a URL, but around 2,000 characters works in virtually any combination of browser, server, and search tooling, and the sitemap protocol caps URLs at 2,048. A URL that follows the standard is plain ASCII, so 2,048 characters is 2,048 bytes in the warehouse, far under its ceiling.

Good: `varchar(2048)` for an image URL
Bad:  `text`, or `varchar(65535)` for a URL

Agent: when a migration or model adds a column that holds a URL, use `varchar(2048)`, or a smaller limit when the URL comes from something known and controlled; go longer only with a good reason, and never use `text` or `varchar(65535)`. Reason: about 2,000 characters works in virtually any browser, server, and search tooling, and the sitemap protocol caps URLs at 2,048.

---

### When data has no honest upper limit, decide on purpose where the limit lives
[Slug: no-honest-limit-decide-where · Temperature: Judgment call · Origin: general · Scope: column · Why: unbounded-data]

Some columns exist to hold whatever arrived, like the markdown extracted from a document or a raw vendor response. For these the length is a fact about the data, and a limit would invent a rule the data does not have. A comment typed by a user is different: it could be long in principle, but how long it should be is a decision, and that decision belongs in the column.

Work through these in order:

1. Is the length a fact about the data, or a choice someone should make? If it is a choice, make it and set the limit.
2. Will this data ever reach the warehouse? Raw fields like this rarely belong there. If not, tell the data teams the table must never be ported, so a sync does not break.
3. If it must reach the warehouse, can it be cut at 65,535 characters? The warehouse counts bytes and not characters, so see `multibyte-text`. The data teams need to know either way.
4. If it must arrive whole and cannot be cut, that is a Data Architect task. Expect the document to move to object storage, with a reference kept in the table.

Because: the database should enforce what is true about the data. For a document of any length, no limit is the true statement.

Second opinion: DBA or Data Architect.

Agent: when a migration or model adds a column that may have no honest upper limit, such as extracted document text or a raw vendor response, decide on purpose where the limit lives. Ask in order: is the length a fact about the data or a choice someone should make (a choice gets a limit); will the data reach the warehouse (if not, the data teams must be told the table is never to be ported); can it be cut at 65,535 characters; and if it must arrive whole and cannot be cut, that is a Data Architect task. Reason: the database should enforce what is true about the data.

---

### Never store a list of values as one delimited string
[Slug: no-delimited-list-strings · Temperature: Rule · Origin: general · Scope: column · Why: lists-or-tables]

A comma-separated string in a text or varchar column is a list that the database cannot see. It cannot check the values, count them, or tell where one ends and the next begins, so a search for one value can match part of another. If a field holds several values, use an array column or a second table. Choosing between the two is covered under Lists of values on Tables. An array column keeps the varchar rules: the limit in `varchar(254)[]` applies to each element, so the array can hold any number of values of up to 254 characters each.

Because: a delimited string only works while every value avoids the delimiter and every reader splits it the same way, and nothing in the database enforces either.

Good: `emails` as a `varchar(254)[]`, or a table of emails
Bad:  `emails varchar(500)` holding `a@example.com,b@example.com`

Agent: when a migration or model adds a text or varchar column that holds several values in one delimited string, use an array column or a second table instead; an array such as `varchar(254)[]` keeps the varchar limit on each element. Reason: a delimited string only works while every value avoids the delimiter and every reader splits it the same way, and nothing in the database enforces either.

---

## Values from a fixed set

### Treat a short text column as a fixed set unless there is a reason it is not
[Slug: short-text-is-a-fixed-set · Temperature: Default · Origin: general · Scope: column · Why: constrained-values]

Before adding a short text column, ask whether it holds one of a known set of values. If it does, or might, treat it as constrained and say so in the design. Leaving it open is the exception, and the reason is worth a sentence.

If a column is named `status`, `type`, `kind`, `mode`, or `category`, or names a strategy or a method, stop and check. There is a decent chance a fixed set is hiding in it.

Because: a column left open collects whatever anyone writes into it, and every reader downstream has to cope with the variations. The database is the lowest level at which something can be true, so a set enforced there is inherited by everything downstream, including places where such a limit would be hard to enforce, the warehouse among them.

Good: a `status` column limited to `draft`, `hold`, and `confirmed`
Bad:  a `status` column with no limit, holding `confirmed`, `Confirmed`, `CONFIRMED`, and `conf`

Agent: when a migration or model adds a short text column, ask whether it holds one of a known set of values; if it does or might, treat it as constrained and say so in the design, and leave it open only for a stated reason. A column named `status`, `type`, `kind`, `mode`, or `category`, or one that names a strategy or a method, likely hides a fixed set. Reason: an open column collects whatever anyone writes into it, and every reader downstream has to cope with the variations.

---

### Have the database enforce a fixed set of values
[Slug: database-enforces-fixed-set · Temperature: Rule · Origin: general · Scope: column · Why: constrained-values]

When a column holds one of a fixed set of values, the database enforces the set. A check in application code alone does not count, because anything that writes to the table without going through that code can still write a value outside the set.

Because: a limit kept in application code is an opinion. A limit in the database is true for every writer.

Agent: when a column holds one of a fixed set of values, enforce the set in the database; a check in application code alone does not count. Reason: a limit kept in application code is an opinion, and a limit in the database is true for every writer.

---

### Choose how to enforce a fixed set by asking what each value carries
[Slug: choose-fixed-set-mechanism · Temperature: Judgment call · Origin: general · Scope: column · Why: constrained-values]

Start with one question: does each value carry anything with it, such as a display label, a sort order, an active flag, or a description, or is it only a string that must be one of the set?

- Use a lookup table with a foreign key when the values carry something, or when the set is likely to expand regularly. Adding a value is then an insert and not a change to the table's structure. The code stays stable, the label can change, and a value is retired by marking it inactive.
- Use a check constraint on a varchar, or an enum, when each value is only a string and the set rarely changes. Booking statuses are the standard example.

A booking shows both. It has a status, and it can have a cancellation reason.

A cancellation reason carries things with it. Staff pick from a dropdown, so each reason has a label and a place in the order. An old reason has to be retired without breaking the bookings that used it, so each has an active flag. And support will keep asking for new ones. That is a lookup table.

```sql
CREATE TABLE cancellation_reasons (
  id         bigint GENERATED ALWAYS AS IDENTITY,
  code       varchar(30)  NOT NULL,
  label      varchar(100) NOT NULL,
  sort_order integer      NOT NULL,
  is_active  boolean      NOT NULL DEFAULT true,
  CONSTRAINT pk_cancellation_reasons PRIMARY KEY (id),
  CONSTRAINT ctx_unique_cancellation_reason_code UNIQUE (code)
);

ALTER TABLE bookings
  ADD COLUMN cancellation_reason_id bigint,
  ADD CONSTRAINT fk_bookings_cancellation_reason_id
    FOREIGN KEY (cancellation_reason_id) REFERENCES cancellation_reasons (id);
```

Adding a reason is an insert, and retiring one is an update. Neither changes the structure of any table, and neither needs a deploy.

```sql
INSERT INTO cancellation_reasons (code, label, sort_order)
VALUES ('weather', 'Weather event', 40);

UPDATE cancellation_reasons SET is_active = false WHERE code = 'duplicate_booking';
```

The label can be reworded at any time, because a booking holds only the `id`. The `code` is the stable handle for people and queries, and the unique constraint keeps it that way. The column on `bookings` is nullable because a booking that was not cancelled has no reason, which is a real answer (*rule: not-null-until-null-has-meaning*).

A booking status is only a string. There are a few values, the set rarely changes, and none of them carries anything else. A check constraint is enough.

```sql
ALTER TABLE bookings
  ADD COLUMN status varchar(20) NOT NULL DEFAULT 'draft',
  ADD CONSTRAINT ctx_status_values
    CHECK (status IN ('draft', 'hold', 'confirmed', 'cancelled'));
```

A value outside the set, such as a misspelled `'confrimed'`, is refused. No second table or join is needed to make that true.

The check constraint and the enum cost different things. A check constraint leaves the column an ordinary varchar, and changing the set means replacing the constraint. An enum is its own type. A value can be added or renamed but not dropped. A new value cannot be used until the transaction that adds it commits. `LIKE` needs a cast to text, and values sort in the order they were declared, not alphabetically. Moving a column onto an enum, or from one enum type to another, rewrites the table. Costs like these grow with the size of the table. See the note on scale on the Index.

For a column that has three states only because one of them means unknown, see the nullable boolean rule under Nullability.

Agent: when a migration or model enforces a fixed set of values, choose the mechanism by asking whether each value carries anything with it, such as a display label, sort order, active flag, or description. Use a lookup table with a foreign key when values carry something or the set will expand regularly. Use a check constraint on a varchar, or an enum, when each value is only a string and the set rarely changes; an enum costs more to change, since a value cannot be dropped and moving a column onto one rewrites the table.

---

## Currency

Every amount of money is stored with its currency code.

### Store a currency's code in `currency_code`
[Slug: currency-code-column · Temperature: Rule · Origin: general · Scope: column · Why: currency-major-units]

Name the column `currency_code`, make it `varchar(3)`, and store the ISO-4217 three-letter code in uppercase: `USD`, `EUR`. The uppercase applies to the values. The column name stays lowercase. Any column that holds a currency code has `currency_code` in its name, in exactly that form.

A row has one currency code unless it truly spans currencies. Before adding a second currency column to a table, ask whether the row holds money in more than one currency, or one currency and several amounts. It is almost always the second. A property with a resort fee, a parking fee, and a Wi-Fi fee is the usual way this goes wrong: each fee gets its own currency column, but all of them hold the same currency. That is one fact stored three times, and the copies can drift apart. One `currency_code` covers every amount in the row.

Where a row really does span currencies, such as a payment charged in one currency and settled in another, name each column for its role: `charged_currency_code` and `settlement_currency_code`.

Good: `resort_fee_minor_units` and `parking_fee_minor_units`, with one `currency_code` on the row
Bad:  `resort_fee_currency_code` and `parking_fee_currency_code`, where the two always hold the same value
Bad:  `currency`, `ccy`, or `curr_cd` for a column that holds the code

Because: the name is how copies of the standard major-unit block are found later. The block reads the code column by this name, and the currency runbook searches for it, so a column that holds a currency code under any other name is the one that gets missed when a currency changes.

Agent: when a migration or model adds a column that holds a currency code, name it `currency_code` exactly, make it `varchar(3)`, and store the uppercase ISO-4217 code (`USD`, `EUR`). Use one `currency_code` per row for all its amounts, because a second currency column on a row that holds one currency stores one fact several times. Only where a row really spans currencies, name each column for its role (`charged_currency_code`, `settlement_currency_code`). Reason: the standard major-unit block and the currency runbook find currency codes by this name.

---

### Never store money in float, real, or double
[Slug: no-float-for-money · Temperature: Rule · Origin: general · Scope: column · Why: currency-major-units]

Because: binary floating point cannot represent most decimal amounts exactly, so totals drift. Each error is tiny, but they stack when amounts are added together, and a report can end up off by a few cents with no one able to say where.

Storing an amount only to display it is not an exception in practice. A value kept for display tends to be summed, exported, or reported on later, and by then the float is already in the pipeline. A value that really is display-only, and will stay so, carries little risk, and as with any Rule it can be crossed with a strong reason written down. Be suspicious of the claim that it will stay display-only.

Agent: never store money in `float`, `real`, or `double`. A value kept for display tends to be summed, exported, or reported on later, so be suspicious of a claim that it will stay display-only; crossing this rule needs a strong written reason. Reason: binary floating point cannot represent most decimal amounts exactly, so totals drift.

---

### Store money as minor units in a bigint
[Slug: money-in-minor-units · Temperature: Default · Origin: general · Scope: column · Why: currency-major-units]

Store an amount as a count of the currency's smallest unit in a `bigint`. In US dollars that is cents, so $5.00 is stored as 500. A currency with no minor unit, like yen, stores ¥10,000 as 10000.

Why not `numeric`, which is exact? Nothing is wrong with it, and it is what the derived major-unit column below uses. The case against it as the stored form is scale. A `numeric` column has to be given a number of decimal places, and the right number depends on the currency: none for yen, three for the Kuwaiti dinar. One scale cannot be right for every currency. A count of minor units in a `bigint` needs no scale, stays exact in every tool and language, and has no decimal type for anything downstream to mishandle. Using `numeric` instead is a deviation from this Default, and it needs a reason written down like any other.

Agent: when a migration or model adds an amount of money, store it as a count of the currency's smallest unit in a `bigint` (5.00 US dollars is 500; a currency with no minor unit, like yen, stores 10,000 yen as 10000). Using `numeric` as the stored form is a deviation and needs a written reason. Reason: `numeric` needs a scale, and the right number of decimal places depends on the currency, none for yen and three for the Kuwaiti dinar.

---

### Name each money column for what it holds, ending in `_minor_units`
[Slug: money-column-minor-units-name · Temperature: Default · Origin: house · Scope: column · Why: currency-major-units]

A single amount is `amount_minor_units`. Where a table stores several, name each and end it in `_minor_units`: `base_price_minor_units`, `service_charge_minor_units`.

Agent: when a migration or model adds a money column, name it for what it holds and end it in `_minor_units`: a single amount is `amount_minor_units`, and several are `base_price_minor_units`, `service_charge_minor_units`.

---

### Derive major units from minor units instead of storing a second copy
[Slug: derive-major-from-minor · Temperature: Default · Origin: general · Scope: column · Why: currency-major-units]

When dollars, euros, and the like are needed, calculate them from the minor-unit column. The type is `numeric(23,4)`, or `decimal(23,4)` in Redshift. Store a major-unit column directly only when the value needs fractions of a minor unit, like half a cent.

Agent: when a migration or model needs dollars, euros, or other major units, calculate them from the minor-unit column as `numeric(23,4)` (`decimal(23,4)` in Redshift) instead of storing a second copy. Store a major-unit column directly only when the value needs fractions of a minor unit, like half a cent.

---

### Never turn minor units into major units with a flat divide by 100
[Slug: no-flat-divide-by-100 · Temperature: Rule · Origin: general · Scope: column · Why: currency-major-units]

How many minor units make a major unit depends on the currency. Most use two decimal places, a few use none, like the yen, some use three, like the Kuwaiti dinar, and two use four. A flat divide by 100 is right for most currencies and wrong for the rest, and the error is easy to miss because testing rarely covers every currency.

Because: the number of decimal places is a property of the currency, not a constant.

Good: the standard block below
Bad:  `amount_minor_units / 100` for every currency

Story: `major-units-by-paste`.

Agent: never turn minor units into major units with a flat divide by 100; use the standard block (`major-units-standard-block`). Reason: the number of decimal places is a property of the currency: most use two, a few use none (yen), some use three (Kuwaiti dinar), and two use four.

---

### Calculate major units in a generated column with the standard block
[Slug: major-units-standard-block · Temperature: Default · Origin: house · Scope: column · Why: currency-major-units]

Copy this block as written and change only the column names. Every copy is identical, so every copy can be found and compared.

```sql
base_price_major numeric(23,4) GENERATED ALWAYS AS (
  base_price_minor_units::numeric / CASE
    WHEN currency_code IN ('BIF','CLP','DJF','GNF','ISK','JPY','KMF','KRW','PYG','RWF','UGX','UYI','VND','VUV','XAF','XOF','XPF') THEN 1
    WHEN currency_code IN ('BHD','IQD','JOD','KWD','LYD','OMR','TND') THEN 1000
    WHEN currency_code IN ('CLF','UYW') THEN 10000
    ELSE 100
  END
) STORED
```

The block lists the currencies that use zero, three, or four decimal places, from the official ISO 4217 list published on 2026-09-17, and treats every other code as two. Two things to know before using it:

- A currency that is not on the list is treated as two decimal places. That is right for the large majority of currencies. It is a deliberate bet and not a guarantee.
- A generated column stores its value. If the standard ever changes a currency's decimal places, every copy of the block has to be found and updated. That is expected to be rare.

A shared function that holds the lists is the alternative when a database has many such columns and wants one place to edit. Check whether the function already exists in that database before creating one.

A separate [runbook](../runbook/currency_runbook.md), outside these standards, covers what to do if a new or changed currency means the block has to change. Nobody watches for ISO changes on a schedule, so whoever learns of one should tell the data architect.

Agent: when a migration or model adds a generated major-unit column, copy the standard block from the full rule (`major-units-standard-block`) exactly as written and change only the column names, so every copy can be found and compared. A currency not on the block's list is treated as two decimal places, and a change to a currency's decimal places means every copy must be found and updated (see the currency runbook). Reason: identical copies can all be found and compared.

---

## Values the database maintains

### Compute a value from other columns in the same row in the database, not in application code
[Slug: same-row-value-generated-column · Temperature: Default · Origin: general · Scope: column · Why: calculated-columns]

When a value can be worked out from other columns in the same row, make it a generated column and let the database keep it current.

A generated column is stored, cannot be written to directly, and can use only the other columns of its own row, not other tables and not subqueries. If a value needs data from other tables, or has to be computed when it is read, use a view or a materialized view instead. Which one, and when, is covered on Tables (*rule: no-second-copy-use-a-view*, *rule: plain-view-before-materialized*).

A stored value takes space on every row, and adding a generated column to a table that already holds rows rewrites it, so on a very large table that is a bigger decision. See the note on scale on the Index.

A value that depends on when or how the row changed, and not on its other columns, cannot be a generated column. The next rule covers it.

Because: a derived value that code keeps in step is only as reliable as every run of that code, and a generated column has no run to miss.

Good: `total_minor_units bigint GENERATED ALWAYS AS (base_price_minor_units + service_charge_minor_units) STORED`
Bad:  application code adds the two values and writes the total

Agent: when a migration or model adds a column whose value can be worked out from other columns in the same row, make it a generated column and not application code. A generated column can use only columns of its own row; if the value needs other tables, or must be computed when read, use a view instead (`no-second-copy-use-a-view`, `plain-view-before-materialized`). A value that depends on how the row changed cannot be generated (`trigger-for-change-dependent-value`). Reason: a derived value that code keeps in step is only as reliable as every run of that code.

---

### When a value depends on how a row changed, let a trigger maintain it
[Slug: trigger-for-change-dependent-value · Temperature: Default · Origin: general · Scope: column · Why: calculated-columns]

When a value cannot be worked out from the other columns of the same row, because it depends on when or how the row changed, let a trigger maintain it and do not leave it to application code. A generated column cannot do this job, since its formula has to give the same answer every time. A timestamp stamped at the moment of a change is the standard case, and the shared trigger for `updated_at` is the worked example (*rule: shared-updated-at-trigger*, on Tables). That function maintains `updated_at` and nothing else, so a different value gets a function of its own, written in the same shape. Name the trigger and the function by the rules on Other objects and tools (*rule: trg-trigger-names*, *rule: ufn-function-names*).

Because: a trigger maintains the value for every writer, whichever application or script touched the row.

Good: a trigger that sets `updated_at` on every real change
Bad:  every piece of application code that writes the row setting `updated_at` itself

Agent: when a migration or model adds a value that depends on when or how a row changed, and not on its other columns, let a trigger maintain it rather than application code; a generated column cannot, because its formula must give the same answer every time. The shared `updated_at` trigger is the worked example (`shared-updated-at-trigger`). A different value gets a function of its own in the same shape, named by `trg-trigger-names` and `ufn-function-names`. Reason: a trigger maintains the value for every writer.

---

## Stories

### A table is a ledger, not a to-do list
*slug: table-of-facts · serves: declarative-names*

A table in a database is almost always a store of facts. The properties table is a collection of what properties exist in the world: which ones are hidden, and which are not. It is not a set of requests about how property data should be displayed. It is the property data. The same goes for "this RFP was created at such a time" and "this brand contains these hotels". Each row is a statement that is true.

A ledger and a to-do list make a useful pair. A ledger records what happened, and a reader can trust every line as a fact. A to-do list asks someone to do something, and a reader cannot tell whether the thing has been done, will be done, or was dropped. A column named `is_hidden` is a ledger line. A column named `hide` is a to-do item, and reading it raises questions the table cannot answer: whether the property is hidden now, or someone has asked for it to be.

This does not hold for every table. A table that really holds instructions, such as jobs waiting to run, is a to-do list on purpose, and its columns can be named that way. For most tables the facts framing is the right one, and column names that follow it need no explanation.

### A column named for the button
*slug: hidden-vs-displayed · serves: bend-or-break, positive-voice*

Columns are named in the positive voice by default. That is not about affirmation or feel-good positivity. It is about making code easier to read and reason about. `if not is_hidden` reads more cleanly than `if not is_not_shown`, because extra words and negations in a column name make the code that uses it less intuitive than it needs to be.

There is flexibility here. `is_displayed` can be argued to be the better column, because `if is_displayed` is even cleaner than `if not is_hidden`. That is absolutely true. But in a given context the word "display" may be less clear than "hidden", for example when the field is controlled by a button labeled "hide".

The goal is clarity and intuitiveness. The rule bends when doing so makes things more understandable, and a short check with another engineer confirms the choice reads the way the author thinks it does.

### What an analyst assumes in the first week
*slug: first-week-assumption · serves: id-guid-identifier, first-assumption-correct*

Of all the naming misses in Groups360's databases, this family may have caused more grief than any other. It comes from the way data analysts read the data.

Within a few days of looking at the data models, an analyst learns what the common words mean. A column called `id` is a bigint primary key. A column ending in `_id` is a foreign key to the table it is named for. A column called `guid` is a uuid, and one ending in `_guid` points to another table's `guid`, often in another database. The words declare both the type and the job of the column, and the pattern is so common that the assumption forms almost at once.

After that, the analyst stops checking and starts guessing from the name. When the name is honest, the guess is right and the work moves fast. When one column breaks the pattern, such as a vendor's reference stored in `external_id`, the guess is wrong in a way nothing warns about. The name promises a foreign key to a table called `externals`, and no such table exists. The full word `identifier` avoids the false promise, because it makes no claim about type or function.

The damage also spreads. One `_id` column that does not behave like the others means every `_id` column has to be checked, and the convention stops saving anyone time. One real table where this happened is told in `shape-sorter`.

### The shape sorter
*slug: shape-sorter · serves: id-guid-identifier, lowercase-only, varchar-vs-text*

A table at Groups360 holds orchestration data that links two other kinds of record. It has a column called `id` and a column called `guid`, and both are what they say they are. It also has columns named `RoomBookingId` and `SpaceBookingId`, in capital letters and lowercase, exactly as written. Both point to records elsewhere in the same database, and both hold guids, not ids. Each is a `text` column.

Every decision in that design looks small by itself, and each one makes the next harder to see.

The mixed-case names are the first. Postgres folds an unquoted name to lowercase, so `RoomBookingId` has to be wrapped in double quotes every time it is written, or the query fails with a message that the column does not exist.

The `Id` ending is the second. An analyst who has learned what `id` means across the rest of the database reads it as a bigint key and writes the query to match. The table already holds a real `id` and a real `guid`, correctly labeled, which makes the guess more natural.

The guid inside it is the third, and the `text` type is the fourth, because it turns the mistake into a silence. A `uuid` column asked for the wrong kind of value says so at once: invalid input syntax for type uuid. A `text` column accepts anything and compares it as a string, so a query for an id that was never going to match returns no rows and no complaint. The analyst sees an empty result and takes it for missing data. A booking that is known to exist does not show up, and the analysis stops making sense. The explanation is in the name and the type, nowhere near the empty result. It has happened often enough that the table is known for it.

A child's shape-sorting toy makes the point. A `text` column is the hole that every shape fits through: guids, ids, stray spaces, a value in the wrong case. Nothing is refused, so nothing ever says what went wrong. A column typed for what it holds refuses what does not belong, and that refusal is the only message the person at the keyboard will get.

The table sits at the intersection of financial reporting, which is where the cost lands. Whoever named the columns was not the one who paid for them. Everyone who queries it afterward did, one empty result at a time. The names, the types, and the case cost the least to get right when the table is designed and the most to correct after it is in use, since correcting means a migration on a table that reporting depends on.

### Almost on every table
*slug: almost-every-table · serves: by-columns*

Groups360 came close to making `created_by` and `updated_by` a default on every table, filled in however the application developer saw fit. The case for doing it was strong, and it deserves to be stated at full strength.

Friction decides whether a column ever exists. If the columns arrive on every table with no questions attached, they will actually be there. The moment a developer has to stop and work through a list of conditions, many will skip the column, and the data it would have held is never recorded. A column that is right in even a fraction of cases is worth more than no column at all, and who made a change is some of the most useful information a table can hold. All of that is true.

What kept it from becoming the default is a different kind of cost. A table teaches the people who read it how to use it. A column that is meaningful in some tables and a junk drawer in others teaches readers to distrust it, and then to distrust the data around it. Some bad data will always arrive by neglect. It should never be arranged in advance. The platform also has no settled answer for what the column holds when the actor is a machine or an anonymous person, so a column filled in however each team saw fit would soon have several meanings.

The two kinds of columns also differ in what stands behind them. The database can guarantee `created_at`, because it knows when a row was written. It cannot know who the application user was, so `_by` is only as good as the application code that writes it, and that is where the value is won or lost.

That is the reason for the shape of the rule. The clean case has no gate. Anyone can add the column without asking, as long as it is always a user guid, is never unknown, and has no extra texture. Putting the friction where the risk is meets the first argument halfway, since the common case has none. Outside the clean case, the answer is not "do not". It is "start the conversation, and then, if there is time, try". These columns are valuable enough that a design able to write them consistently, in a way that is reportable and makes no assumptions others must then follow, should have them.

### Which clock was that?
*slug: unlabeled-timestamps · serves: timestamptz-utc*

Early in Groupsync's history, most date-and-time columns at Groups360 were plain `timestamp`. A plain `timestamp` holds a clock reading with no time zone attached, so the column itself does not say which clock was read. The intent was to store UTC in them. In practice that was applied unevenly, and the result is a set of columns where some values are UTC, some are Central time, and nothing in the data says which. Untangling them has been slow, and it is not finished.

A quieter hazard sits on top of that, and it comes from `NOW()`. The function returns a moment with a time zone attached, and shows it in whatever zone the session is set to. That setting belongs to the connection, so two people running the same statement can get different results. When the value is written into a plain `timestamp` column, Postgres drops the zone and keeps the clock reading.

The same statement, `UPDATE ... SET updated_at = NOW()`, therefore writes UTC from a session set to UTC and local time from a session set to Chicago. In a test, the Chicago session wrote 13:11 where the UTC session wrote 19:11 for the same instant: six hours in the past, with no error and nothing to show it. A workaround exists, `NOW() AT TIME ZONE 'UTC'`, but a standard that depends on every author remembering a workaround to avoid a trap leaves the trap in place.

So the standard removes the trap and does not ask anyone to step around it: always `timestamptz`. A `timestamptz` column stores the moment itself, and the same `NOW()` writes the same value from any session. It also says what it holds. A reader never has to guess whether the column is UTC, Central time, or something else, because it holds moments and shows them in whatever zone the session asks for.

### A time that is a promise, not a moment
*slug: future-local-time · serves: timestamptz-utc*

A UTC timestamp records an instant, an exact moment on one universal clock. That is what a record of something that already happened needs, and it is why the standard stores UTC. It is not always what a person means. Someone who schedules an event for 9:00 in the morning, local time, in a given city next March means a clock reading in a place, not an instant.

For most events the two come to the same thing, and storing UTC works. The difference appears when the rules change. Governments change their daylight saving rules, sometimes with little notice. A stored instant is an answer worked out in advance under the old rules. What the organizer meant was closer to the question: 9:00 on the clock in that city. If the rules change, the question can be asked again and will give the new answer. The old answer cannot fix itself, and nothing in the database shows that it has gone wrong.

This is where `timestamptz` alone falls short. A `timestamptz` value is converted to UTC the moment it is written, and the zone it arrived in is thrown away. A value entered as 9:00 in Athens and a value entered as 7:00 UTC are identical once stored. The intent is gone at write time, so there is nothing left to work from later. Keeping it takes a pair of columns beside each other, the local clock reading and the name of the time zone, like `Europe/Athens`, with the instant calculated from them whenever it is needed.

That arrangement has costs, and they are the reason the standard does not simply recommend it.

- The local clock reading has no zone of its own, so it has to sit in a plain `timestamp`, the one type the standard otherwise forbids.
- Calculating again only helps once Postgres has caught up with the new rule. Until its time zone data is updated, every calculation for that place is wrong, stored or not. That is outside Groups360's hands, in the same way a currency changing its decimal places is.
- Not every local time exists, and not every local time is unique. When clocks jump forward, 2:30 in the morning never happens. When they fall back, 1:30 happens twice. Postgres raises no error for either and silently picks one, so the pair can hold a reading that was never a real moment.
- Postgres will accept the calculated instant in a generated column, but a stored value is a snapshot of the rules as they were when the row was written. Calculating when the value is read keeps it current.

So the case is arguable, and in most systems it does not earn its cost. A rule change that lands between scheduling and the event is rare, and many times that look like promises about a clock are perfectly well served as moments. Where the intent has to survive, as with an event that must happen at 9:00 on the wall clock whatever a government decides, the pair of columns is the way to keep it. Everywhere else, `timestamptz` and UTC. The question to ask first is whether anyone needs the intent preserved.

None of this applies to something that has already happened. A record of when something happened is a moment, and a later rule change does not move it. Storing the zone name beside a past moment, so it can be shown in that place's local time, is fine and is not an exception.

### The text field that took down the views
*slug: warehouse-view-crash · serves: varchar-vs-text, redshift-varchar-ceiling*

Groups360 runs two kinds of database. The operational databases sit under Groupsync and the private label apps, and run PostgreSQL (version 17.11 as of November 2026, which may have changed since). Downstream is a data warehouse in Amazon Redshift, which is built differently and has a different toolkit. A sync tool, currently Stitch, copies flagged tables from one to the other and reshapes the data to fit.

Postgres allows far longer values than the warehouse does. Redshift has no `text` type at all, and its `varchar` stops at 65,535. A `text` column is where the mismatch bites, and the same sequence has played out more than once:

1. A field in Groupsync is defined as `text`.
2. The sync tool keeps up, raising the `varchar` size on the warehouse copy each time a longer value arrives.
3. A value arrives that is longer than any before it. The sync tool pulls it into the source table in the warehouse and updates that table's definition to fit.
4. The views built on top of that table do not follow. A materialized view fixes its column sizes when it is created and does not inherit later changes to the table underneath.
5. The next time a view tries to pull in the new value, it fails, and stays unavailable until someone finds the offending value and widens the column in the warehouse by hand.

Those views are critical infrastructure for billing and revenue recognition, so a column type chosen at design time becomes an outage in finance reporting. That is the whole case for `varchar` over `text`, and for never going above 65,535.

### What turned up in the notes fields
*slug: notes-field-surprises · serves: varchar-limits*

A free-form notes field raises an old question. Nobody knows how much a customer might want to write, so why not use `varchar(65535)` and move on? Storage is cheap, and a field that is not indexed costs little to keep wide.

Groups360 has had notes fields with no real limit, and they did receive values far beyond anything a limit would have allowed. That can look like proof that leaving them wide open was wise. It was the opposite. In one case a user pasted the contents of an entire 20-page PDF into the field. In another, a large block of HTML code arrived. In a third, the field held a contact list that had nothing to do with the booking. Every one of those values was garbage or an input error, and every one broke something downstream that took many hours across several teams to fix.

Where this has happened, the ending is the same: a constraint ends up on the database column, because it always does eventually. Skipping the work at the start does not remove it. It hands the work to someone else, later, with more hours attached.

The deeper reason is that the database is the source of truth. A constraint kept in a front end or an API is only an opinion, and it disappears when that code changes. A database constraint is true at the lowest level a thing can be true, and stays true. A limit set too low has an easy remedy, because raising a `varchar` limit loses nothing. Lowering one cannot be done without deciding what to do with the data that no longer fits.

### Two limits on one address
*slug: email-length-limits · serves: email-limits*

The two numbers in the email rule look oddly specific, and each comes from a different place.

The first is 320. Under the standard (RFC 5321), the part before the `@` can be up to 64 characters and the domain after it up to 255, so 64 plus the `@` plus 255 is 320. On the rules for how an address looks, an address that long is valid.

The second is 254, and it comes from a separate rule about the SMTP conversation between mail servers. The address travels inside a path that is limited to 256 characters, and the path includes the angle brackets around the address. That leaves 254 for the address itself.

The two limits are like the rules for addressing a letter. The post office might accept an address of one length, while the standard envelope fits only a shorter one. An address can be valid by the post office's own rules and still not fit the envelope that so many hops along the way happen to use. An address of 320 characters is valid on paper, but many servers between sender and recipient enforce the shorter limit, and the message can bounce off infrastructure nobody controls.

So the practical limit is 254, which is why the standard uses `varchar(254)`. A column wider than that would only invite addresses that cannot be delivered anyway.

### When the document is the data
*slug: image-documents · serves: unbounded-data*

A design at Groups360 for an image-processing service split the work into discrete steps. The older approach was a single process: query an image vendor, get back a document describing the images for a property, parse it, and write the results to the database. The new design split that into stages. One step queries the vendor and stores the document it gets back. A second step reads the stored document and cuts it into an image set. A third pushes the image set out to the services that need it. Each stage can be run, tested, and repeated on its own.

That design had one consequence for the database. The stored documents would be large. Each is only a collection of URLs, but one hotel's document from the vendor can run past 100,000 characters. The operational Postgres databases can hold that as a `text` column or a very wide `varchar` without trouble, but no choice of type makes it fit in the data warehouse.

The length of such a document is not a decision anyone makes. It is simply how long the vendor's response is, so the length is a fact about the data. A limit would mean inventing a rule the data does not have, which is the opposite of what a constraint is for. What matters is where the data goes next. Raw documents like this are rarely useful in the warehouse, and the likeliest outcome of the conversation with the data teams is a note that the table is never to be synced, so a sync does not break. If the warehouse does need the data, the options are to keep only the first 65,535 characters (see `multibyte-text` for why that count needs care) or to move the documents to object storage and keep a reference in the table.

The project was later pared down, and the large documents never became a live problem. The questions it raised are still the ones to ask of any column that could grow that large.

### When characters and bytes disagree
*slug: multibyte-text · serves: redshift-varchar-ceiling, unbounded-data*

Postgres counts the length of a varchar in characters. The warehouse counts it in bytes. For plain English text the two are the same, because every character takes one byte. For other text they are not. In UTF-8, accented European letters and Greek, Cyrillic, and Hebrew letters take two bytes, most Chinese, Japanese, and Korean characters take three, and emoji take four.

So a `varchar(65535)` in Postgres can hold a value that does not fit under the warehouse's 65,535-byte ceiling. A column of Greek text can need up to twice the room, and one of Chinese text or emoji three or four times as much. The result is the failure the ceiling rule exists to prevent: one oversized value reaches the warehouse, and every view built on that column can fail.

In practice this is a corner case on top of a corner case. A column near the ceiling is rare, because 65,000 characters is a lot of text for almost any field, and a column near the ceiling that also holds non-Latin text is rarer still. Names, codes, and URLs never come close.

When it does apply, set the limit lower, so that the worst case in bytes still fits. Dividing 65,535 by the widest character expected gives the ceiling: 32,767 characters for text that is at most two bytes per character, 21,845 for three, and 16,383 for four.

To check a value that is misbehaving, compare `char_length(value)` with `octet_length(value)` in Postgres. If the second is much larger than the first, the text is multibyte, and that is probably the reason.

### Why a copied block, and why that is worth it
*slug: major-units-by-paste · serves: currency-major-units*

A major-units column was once built by dividing the minor units by 100 for every currency. It is right for most currencies and wrong for the rest, and the yen is the one that exposed it. The wrong values reached financial reporting, where some bookings showed costs that made no sense. The cause was nowhere near the place the symptom showed up, and it was found only by tracing the numbers backwards, step by step, to the column that produced them. A wrong value that surfaces far from its source takes a long time to trace, and that is the cost the rule exists to avoid. Whatever the standard recommends has to make the correct version at least as easy as the wrong one.

Three ways of doing it were weighed.

A reference table of currencies and their decimal places, joined in a view, is the cleanest. It keeps the data in one place. It was set aside because it is a table to build, fill, and keep in every database that needs it, and the path that takes real setup is the path people skip. The flat divide takes none.

A shared function that holds the lists is tidier than a copied block, since a change means editing one place. It was set aside as the default because it is one more thing to find or create before first use, and the change it protects against, a currency's decimal places shifting, is expected almost never to happen.

A block copied into each generated column was chosen. It takes the least effort, so it is the version people will actually use. Its costs are real and accepted. A change means finding every copy, which is a text search because every copy is identical, and then updating each one, which also recomputes the stored values. An unlisted currency is treated as two decimal places, which is right for nearly all of them.

A shared function is the better choice once a database has many such columns and its authors want one place to edit, and moving to one at that point is reasonable. Copying the block is a shortcut taken on purpose, in the cheapest place, to avoid a worse mistake that is easy to make.

### The value that never needed a process
*slug: derived-by-process · serves: calculated-columns*

In 2018, Groups360 stored a property's latitude and longitude as two plain columns, kept current by a script. A separate application process took those two values and built a point value from them whenever it ran. The point depended on nothing but the two columns beside it. It was a function of them and nothing more.

For years that caused no trouble. The process worked, and nothing about the design looked like a mistake. Then, three or four years in, it began to matter. An application process is code, and code fails. Sometimes an earlier step stopped before the point was written. Sometimes the process was never started when it should have been. Each time, the point was left behind with no error and no trace, while the two columns it came from moved on without it.

By the time the gaps were a problem, they were a problem everywhere. The fix took until 2025, many developers, and about six months from planning to finished work, because the stale values, and the code that produced them, had spread through the database. The finished fix is short to describe: the point became a generated column over latitude and longitude.

A generated column cannot disagree with its inputs. The database computes it whenever they change, and nothing can write to it directly. The failure was never about careless code. A derived value that code keeps in step is only as reliable as every run of that code, and a generated column has no run to miss. That is the case for the rule, and the reason it is a default and not a preference. The point never needed a process at all.
