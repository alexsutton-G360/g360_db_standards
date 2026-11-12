# Tables

Rules about the table as a whole: what it carries, how its rows come and go, how it is named, and how it relates to other tables. The rules on Global Rules apply here too. Where a rule below says otherwise, this page wins. Ready-made tables, with the reasons behind them, are on Stock tables.

## Row lifecycle

What a table carries so that its rows can be tracked, changed, and removed safely, by the application and by everything downstream.

### Give almost every table `created_at` and `updated_at`, and let the database manage them
[Slug: created-at-updated-at-on-tables · Temperature: Rule · Origin: house · Scope: table · Why: created-updated]

Both columns are `timestamptz NOT NULL DEFAULT now()`. A table that is append-only, where a row is never updated, gets `created_at` only. A table that skips either one needs a reason, stated where the table is defined.

Because: a value the database maintains is true no matter which application or script touched the row, and anything downstream, like a warehouse sync, can rely on it.

How to name and type a timestamp column in general is covered on Columns, under Dates and times.

---

### Keep `updated_at` current with the shared trigger, not with application code
[Slug: shared-updated-at-trigger · Temperature: Rule · Origin: house · Scope: table · Why: created-updated]

Use one shared function, `ufn_set_updated_at`, and one `BEFORE UPDATE` trigger per table.

```sql
CREATE OR REPLACE FUNCTION ufn_set_updated_at() RETURNS trigger AS $$
DECLARE
  ignored text[] := COALESCE(TG_ARGV, ARRAY[]::text[]);
BEGIN
  IF (to_jsonb(NEW) - ignored) IS NOT DISTINCT FROM (to_jsonb(OLD) - ignored) THEN
    RETURN NEW;
  END IF;
  IF NEW.updated_at IS NOT DISTINCT FROM OLD.updated_at THEN
    NEW.updated_at := now();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_<table>_set_updated_at
  BEFORE UPDATE ON <table>
  FOR EACH ROW
  WHEN (OLD.* IS DISTINCT FROM NEW.*)
  EXECUTE FUNCTION ufn_set_updated_at();
```

A table with a stored generated column needs a different trigger. Postgres does not allow a whole-row `WHEN` condition on such a table, and a `BEFORE` trigger cannot see a generated column's new value. Leave off the `WHEN` and name each generated column as an argument, so the function ignores it when it checks whether the row changed.

```sql
CREATE TRIGGER trg_<table>_set_updated_at
  BEFORE UPDATE ON <table>
  FOR EACH ROW
  EXECUTE FUNCTION ufn_set_updated_at('base_price_major', 'service_charge_major');
```

If a generated column is left out of the arguments, the trigger errs toward bumping `updated_at` on an update that changed nothing, and never toward missing a change. When a generated column is added to a table later, add it to the arguments.

The two forms look equivalent, and in almost every case they behave the same. The difference is cost. The plain form lets Postgres skip the function entirely when a row has not changed. The generated-column form always runs the function and compares the two rows inside it, which is a little extra work on every update. At the sizes these rules grew up around that is not noticeable, and on a very large table that is updated constantly it is worth a look. See the note on scale on the Index.

An update that changes nothing leaves `updated_at` alone, which protects any sync keyed on it. An `updated_at` set on purpose is kept, so a backfill can preserve history without disabling the trigger. A bulk migration that changes other columns will otherwise stamp every row with the current time.

One edge: an update that changes other columns and also sets `updated_at` to the value it already had is treated as having no explicit value, and the trigger stamps the current time.

---

### Soft-delete rows by default, with a `deleted_at` timestamp, unless there is a reason not to
[Slug: soft-delete-default · Temperature: Default · Origin: house · Scope: table · Why: soft-deletes]

At Groups360, a row that is deleted from the application's point of view stays in the table, with a `deleted_at` timestamp set. The column is a `timestamptz` and is null while the row is live. The shared trigger moves `updated_at` in the same statement, so anything that follows `updated_at`, like a warehouse sync, sees the deletion as a change.

Start with soft delete, and ask whether you need anything else. Either of these is a reason to go another way:

- The data never changes or goes away, like an audit log or an event stream. It needs no `deleted_at` at all.
- The table is so large that keeping every deleted row would weigh on every query and index. Look to a retention policy or partitioning instead.

A row that stays also keeps the rows that point at it from being orphaned.

How to name and type a timestamp column in general is covered on Columns, under Dates and times. This rule assumes tables of modest size. See the note on scale on the Index.

Because: a deleted row that stays can still be explained, followed by a sync, and pointed at, and Groups360's tables are small enough that keeping it is cheap.

Good: a row marked with `deleted_at` when a user removes it
Bad:  a row removed with `DELETE`, leaving no trace that it ever existed

---

### Change a row in place, and do not delete it and create it again
[Slug: change-row-in-place · Temperature: Default · Origin: general · Scope: table · Why: edit-in-place]

When the data in a row changes, update the row that exists. An updated row keeps its `id`, and anything downstream, like a warehouse sync, can see that it changed. A row that is deleted and created again gets a new `id`, and whatever already saw the old row is left holding a stray.

If what you need is "insert this row, or update it if it is already there", that is an upsert, and it is a different thing from rebuilding. Postgres does it directly with `INSERT ... ON CONFLICT DO UPDATE`. It needs a unique key to conflict on, such as the unique constraint on a junction table's pair of foreign keys. The habit of deleting and re-creating rows made sense once, when Postgres had no upsert. It does now.

There may be times when rebuilding is right. If you think yours is one, say why in writing, and ask someone before you do it.

Because: an updated row keeps its identity and leaves nothing behind. In Groups360's tables, each time rebuilding rows has been looked at, it has turned out to be the wrong choice.

Good: a child row updated where it stands when its booking changes
Bad:  all of a booking's child rows deleted and inserted again on every save

Second opinion: any teammate.

---

## Naming tables

A table name is read as a sentence. The rule here says what a two-noun name means at Groups360.

### Name a table that joins two others for the two things it joins
[Slug: name-junction-tables-for-both-sides · Temperature: Default · Origin: house · Scope: table · Why: compound-table-names]

At Groups360, a table name made of two nouns, like `user_roles`, tells the reader that the table is a relationship: it joins the two things it names. Name junction tables that way, so the name alone says what kind of table it is.

That meaning is reserved, and readers rely on it, so a table that is not a junction table should not be given a two-noun name that reads as one. Name it for what a row is, and put who owns the rows in a column.

Because: a reader should be able to tell what kind of table they are looking at from its name alone, and the two-noun shape is the one signal that says the table joins things.

Good: `user_roles`, a table that joins users and roles
Good: `role_permissions`, a table that joins roles and permissions

---

## Row identity

Every table identifies its rows by an `id` for use inside its own database, and a table that something outside refers to also has a `guid` for use everywhere else. These chunks say which tables get which, and when. What the columns are, and how they are named and typed, is on Columns under Identifiers.

### Give every table an `id`, junction tables included, unless there is a stated reason not to
[Slug: id-on-every-table-including-junctions · Temperature: Default · Origin: house · Scope: table · Why: id-on-every-table]

Every table carries an `id`. That includes junction tables, which also get a unique constraint on their pair of foreign keys so that the same two rows cannot be linked twice. A table that goes without an `id` needs a reason, stated where the table is defined.

The `id` is an operational column. Tools and scripts use it to address one specific row, and so does fixing or removing a single bad row, whether or not any query in the application ever reads it.

Because: this is how Groups360 builds tables, and it has found the `id` useful for tooling and for correcting one row. It is a house convention and not a claim about correctness elsewhere, so a team that identifies its junction rows by the foreign key pair is not making a mistake.

Good: a junction table with its own `id` and a unique constraint on its two foreign keys
Bad:  a junction table with an `id` and nothing to stop the same link from appearing twice

---

### An `id` is an internal reference, so outside the database a row is found by its `guid`
[Slug: id-internal-guid-external · Temperature: Rule · Origin: general · Scope: table · Why: ids-stay-inside]

An `id` is a counter, and it means something only inside the database that issued it. Never let an `id` be the value that finds a row from outside: not in an API, not in a URL, not in anything a person could substitute, replay, or edit on a live page. Look the row up by its `guid` instead. A reference held by another service is a `guid` for the same reason, since an `id` means nothing outside its own database.

Showing an `id` is fine. It can appear in a report or a user panel. What it cannot be is the lookup value.

Because: an `id` can be walked. Someone who sees `/users/42` can try 43, then 44, then 45, and every row is one guess from the next. A `guid` cannot be walked, and it keeps its meaning across databases, where an `id` does not.

Good: a lookup by `/users/<guid>`, and an `id` shown in an admin report
Bad:  a lookup by `/users/42`

---

### Give a table a `guid` when something outside the database may point at its rows, and decide when the table is created
[Slug: guid-for-externally-referenced-tables · Temperature: Default · Origin: house · Scope: table · Why: ids-stay-inside]

Most tables are never referred to from outside their own database, and carry only an `id`. A junction table does not get a `guid`. A table that something outside may point at gets one, and the time to decide is when the table is created. If in doubt, add it. An unused `guid` column costs almost nothing. Adding one later is routine, but it is more work than adding it now. Every existing row needs a value, and the NOT NULL and UNIQUE constraints go on after that backfill, so what would have been part of the create statement becomes a migration in steps (*rule: plan-for-existing-rows*).

Declare the `guid` unique when the column is created. The constraint is what makes it safe to rely on as an identifier, and it creates the index that lookups by it will need. That index enforces something true about the data and is not a guess about future queries, so it is not the kind of index the rule under Indexes on this page warns against.

Because: a `guid` is simplest on the day the table is created, because every row is born with one. Adding it later is routine, but it takes steps: a value for every existing row, then the constraints, and the cost grows with the size of the table.

---

### Make a `guid` NOT NULL and UNIQUE, and generate it wherever it is first needed
[Slug: guid-not-null-unique-generated-anywhere · Temperature: Default · Origin: general · Scope: table · Why: guid-generation]

A `guid` column is NOT NULL and UNIQUE, enforced by the database. With those two in place, a guid that was never generated is refused, and so is one that repeats, so the data stays safe whoever generates the value.

That makes the choice of who generates it a question of convenience and not of safety. Either way works:

- The application generates it. The guid is known before the insert, so it can go into an S3 key, a message, or a request before the row exists, and the row can be found by it from the start. A guid the application forgot to send shows up as an error.
- The database generates it, with a default such as `gen_random_uuid()`. A row is valid even when the application sends no guid, and the application can read the value back from the insert.

Generate it where it is first needed, which is often the application. The user uploads table on Stock tables is an example of the first.

Because: the database enforces what is true about the data whoever fills the column in, so the guarantee does not depend on the writer, and the choice of writer can follow what the design needs.

Good: a guid the application generates and sends with the insert, so it can go into an S3 key before the row exists
Good: a guid that defaults to `gen_random_uuid()`, for a table where nothing needs it before the row does
Bad:  a guid column that allows null or has no unique constraint, whichever side generates it

---

## Lists of values

Sometimes a row has several values of one kind: tags, contact emails, nicknames. There are three ways to hold them, and they are not equal. A delimited string is never one of them, which is the rule on Columns. This chunk is about the other two.

### Before using an array column, check that it is not a second table you have not made
[Slug: array-or-second-table · Temperature: Judgment call · Origin: general · Scope: table · Why: lists-or-tables]

An array column is the right home for a list when each value is bare: a plain value that belongs to the row and has nothing else attached to it, such as the tags on a record. It is simple, it keeps one fact in one place, and a search can match whole values.

It is a second table you have not made when any of these is true:

- A value carries something of its own, such as a flag, a date, or a status.
- A value points at another table. A foreign key cannot be placed on the elements of an array.
- A value must be unique across the rows of the table. A unique constraint on an array column compares whole arrays and not their elements.

If none of these is true, use the array. If one is, make the table, however much easier the array feels today. The easy moment to ask is when the column is created, and the question to ask is what each value might come to carry.

Because: an array looks like a column and behaves like one until the first time a value needs a fact or a link of its own, and by then the data is already in the wrong shape.

Good: `tags varchar(50)[]`, where a tag is only a word
Bad:  `contact_emails text[]`, where each address will need its own flag

---

## Derived values and copies

Sometimes a table is tempted to hold a value that could be worked out from data that already exists. The two chunks here are about not keeping a copy, and about which kind of view to use instead.

### Do not keep a second copy of data that a view can derive
[Slug: no-second-copy-use-a-view · Temperature: Default · Origin: general · Scope: table · Why: derived-in-view]

When data already exists in one place and another place needs a different view of it, derive it with a view. Do not store a copy that application code keeps in step. That covers a whole second table filled by copying from the first, and it covers a stored column whose value is worked out from rows in other tables, such as a header's status that sums up the bookings beneath it.

A stored copy can differ from its source, and it is only as reliable as every run of the code that maintains it. A view cannot differ, because it is the source, read a different way. If a value must be stored in a table at all, store only what cannot be derived, and put the derived part in a read view on top.

A generated column does not fit here, because it can read only the row it sits in. Anything that needs other tables is a view. See Values the database maintains on Columns.

Because: a value that can differ from its source will, sooner or later, and everything downstream of it, including the warehouse and reporting, inherits the difference. A value that can be made true by construction should not be left to stay true by effort.

Good: a parent's status read through a view that derives it from the child rows
Bad:  a status column on a parent, filled in by application code from its child rows, with a standing clean-up to correct the drift

---

### Start with a plain view, and move to a materialized view only when the query has earned it
[Slug: plain-view-before-materialized · Temperature: Default · Origin: general · Scope: table · Why: derived-in-view]

A plain view is always current, and it needs nothing from operations. It pays at read time, since the query runs each time the view is read. That is the right place to start, and most views never need more.

Look at a materialized view when the query behind the view is heavy, it is read often, and the data can safely be a little behind. A materialized view stores its result and goes stale as the data underneath changes, until it is refreshed. Keeping it fresh is a plan and a commitment, and creating it is not the end of the job. It puts the object on the DBA's path, with refresh timing, load, and monitoring. That is a bigger decision than it looks.

Which kind is right depends on size. A query that is cheap on a small table may not be on a large one. See the note on scale on the Index.

Because: a plain view cannot drift. A materialized view can, and its staleness is the same kind of drift a stored copy has, so choose one deliberately and with a refresh plan in place.

Good: a view over the room and space bookings that derives a header's status when it is read
Good: a materialized view for a heavy summary that is read constantly, with a refresh plan agreed with the DBA
Bad:  a materialized view created for a cheap query, with no refresh plan, so that it goes stale unnoticed

Second opinion: DBA.

---

## Tables that belong to one of several parents

Sometimes a table needs to belong to one of several other tables. An addresses table might hold addresses for a user or for an org. This is a polymorphic association, and there are three ways to model it. Each has a place. Wherever a table points at a row in the same database, the starting point is a real foreign key (*rule: same-database-pointer-needs-fk*). This group is about keeping that when a table has several possible parents.

The chunks in this group are one line of thought and are meant to be read in order: why the rows share one table, what Groups360 used to do and why you will still meet it, what Groups360 does now, what to reach for when that strains, and a short way to choose.

### When rows have the same shape whatever they belong to, keep one table and not one per parent
[Slug: one-table-for-same-shape-rows · Temperature: Default · Origin: general · Scope: table · Why: polymorphic-associations]

If an address has the same structure whether it belongs to a user or an org, give addresses one table. Two separate address tables, each with its own `street` and its own copy of every rule about an address, mean that any change to what an address is has to be made in two places. Someone working on one of them may never learn the other exists.

When the rows really do differ in shape, separate tables are the honest design, and this default does not apply.

Because: the structure of the database should say what is true about the data. If an address is the same thing everywhere, one table says so.

---

### Recognize `source_type` and `source_id`, and use it only when the fan-out is large and an orphan is harmless
[Slug: source-type-id-pattern · Temperature: Judgment call · Origin: general · Scope: table · Why: polymorphic-associations]

You will find this pattern in many existing Groups360 tables. One column holds a string naming the parent's table, such as `'user'` or `'org'`, and another holds the id of a row in that table. It is appealing because it is narrow, and a new kind of parent needs no change to the schema.

The cost is that the database cannot know what the two columns mean. To it they are two values, as unrelated as a first name and a street address, so it cannot hold a real foreign key on them. That makes it the exception to the rule that a pointer to a row in the same database gets a real foreign key (*rule: same-database-pointer-needs-fk*). Deleting a parent leaves its children behind. A misspelled type is accepted. An id can point at a row that never existed. Every guarantee falls to application code, and joins across the pattern are awkward to write.

Both of these must be true before the pattern is acceptable:

- The fan-out is large. The table may point at many kinds of parent, enough that the other two approaches, one nullable foreign key per parent (*rule: exclusive-arc-default*) and one junction table per parent (*rule: junction-table-per-parent*), would generate serious schema overhead.
- Orphans genuinely do not matter. The data is historical, ephemeral, or low-stakes, so a dangling reference harms nothing.

An activity log is the standard example. Entries about an RFP that was later deleted still have historical value, and logging a new kind of event needs no migration. If only one of the two is true, one of the other approaches is the better call. If you are not certain the second is true, it probably is not. An addresses table for users and orgs is not such a case: two parents is a small fan-out, so one of the other approaches is the better call.

A `source_type` column is itself a set of allowed values, so the rule on fixed sets applies to it (*rule: database-enforces-fixed-set*, on Columns).

Because: a rule the database does not enforce is a convention and not a standard, and conventions stop holding when the code around them changes.

Second opinion: Data Architect.

---

### Give a table that belongs to one of several parents one nullable foreign key per parent, and a check that exactly one is set
[Slug: exclusive-arc-default · Temperature: Default · Origin: general · Scope: table · Why: polymorphic-associations]

Add one column for each possible parent, each a real foreign key, and a check constraint that counts how many are filled in.

```sql
CREATE TABLE addresses (
  id      bigint GENERATED ALWAYS AS IDENTITY,
  street  varchar(200) NOT NULL,
  city    varchar(100) NOT NULL,
  user_id bigint,
  org_id  bigint,
  CONSTRAINT pk_addresses         PRIMARY KEY (id),
  CONSTRAINT fk_addresses_user_id FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT fk_addresses_org_id  FOREIGN KEY (org_id)  REFERENCES orgs (id),
  CONSTRAINT ctx_exactly_one_parent
    CHECK (num_nonnulls(user_id, org_id) = 1)
);
```

Every filled-in column is a real, enforced foreign key. A parent that does not exist is rejected, a parent that still has addresses cannot be deleted by accident, and the database knows what each column means. The check does the job that would otherwise fall to application code, on every write, whatever the application does. If a row is allowed to belong to no parent, change `= 1` to `<= 1`.

These columns are nullable for a reason the nullability rule on Columns accepts. Here null means "this address is not attached to a user", which is a real answer: that parent does not apply to this row. The check constraint keeps it honest. The nulls are there on purpose, and the constraint makes sure no row has the wrong number of them. Whatever the count is, exactly one or at most one, say it in the constraint.

Adding a new kind of parent takes an `ALTER TABLE`, a new nullable column with its foreign key, and a replacement check constraint. That is a migration on a live table and needs care, and the larger the table, the more care. See the note on scale on the Index. If the parents keep multiplying, see the junction-table chunk below.

Because: the database is the lowest level at which something can be true, and a check constraint enforces this on every write, for good.

---

### When the parents are many or keep growing and integrity still matters, use one junction table per parent
[Slug: junction-table-per-parent · Temperature: Judgment call · Origin: general · Scope: table · Why: polymorphic-associations]

Keep the core table lean and give each kind of parent a small table of its own that joins the two.

```sql
CREATE TABLE addresses (
  id     bigint GENERATED ALWAYS AS IDENTITY,
  street varchar(200) NOT NULL,
  city   varchar(100) NOT NULL,
  CONSTRAINT pk_addresses PRIMARY KEY (id)
);

CREATE TABLE user_addresses (
  id         bigint GENERATED ALWAYS AS IDENTITY,
  address_id bigint NOT NULL,
  user_id    bigint NOT NULL,
  CONSTRAINT pk_user_addresses            PRIMARY KEY (id),
  CONSTRAINT fk_user_addresses_address_id FOREIGN KEY (address_id) REFERENCES addresses (id),
  CONSTRAINT fk_user_addresses_user_id    FOREIGN KEY (user_id)    REFERENCES users (id),
  CONSTRAINT ctx_unique_address_user      UNIQUE (address_id, user_id)
);
```

Every foreign key is real. A new kind of parent is a new table, and nothing that already exists has to change, so there is no migration on a live table. If the link itself carries data, such as a timestamp, an order, or a status, that data has a natural home on the junction row. Name each junction table for the two things it joins, as under Naming tables on this page. Like every table it carries an `id`, and the unique constraint on the pair keeps the same link from being made twice, as under Row identity.

The cost is more tables. Finding out what a row is attached to means checking several of them and not reading one row. For a small, stable set of parents that is more infrastructure than the problem needs, which is why this is not the default.

Because: when there are many parents and a dangling reference would do real harm, the extra tables are what it costs to keep the database enforcing the relationship.

---

### Choose among the three by how many parents there are and how much integrity matters
[Slug: polymorphic-decision-matrix · Temperature: Judgment call · Origin: general · Scope: table · Why: polymorphic-associations]

Two questions decide it: how many kinds of parent the table can belong to, and how much a dangling reference would hurt.

| | Few parents (five or six or fewer) | Many parents |
|---|---|---|
| **Integrity matters** | Nullable foreign keys, one per parent | Junction tables |
| **Integrity is low-stakes** | Nullable foreign keys, still the easy choice | `source_type` and `source_id`, acceptable here |

Start with nullable foreign keys. For most tables that is the right default, with real referential integrity that is easy to join against and easy to understand. Reach for junction tables when the fan-out is large or growing and the data still needs protecting: the schema gets busier and the data stays safe. Consider `source_type` and `source_id` only when the fan-out is large and the table is one where an orphan truly causes no harm.

When in doubt, talk to the Data Architect before building. This is one of the places where the decision made on day one is hard to undo on day three hundred.

Second opinion: Data Architect.

---

## Indexes

An index speeds up one kind of read and taxes every write. The two chunks here are about deciding when a table has earned one.

### Add an index when something looks the column up, in the same change that adds the lookup
[Slug: index-when-a-lookup-exists · Temperature: Default · Origin: general · Scope: table · Why: indexes-need-a-reason]

An index is a cost paid in advance. It takes space, and every insert, update, and delete on the table has to maintain it too. An index that nothing uses pays that cost for nothing. So add one when a query that exists needs it, whether that is a lookup, a join, or a sort the table is genuinely asked to do, and add it in the same change that introduces the query. Do not add one in case it is needed someday.

The other direction fails quietly. A lookup with no index works on a small table and slows as the table grows, with no error to say why. That is the reason the index belongs in the same change as the lookup and not in a follow-up.

A unique constraint creates an index, so it carries the same cost. When the constraint enforces something true about the data, as a `guid` being unique does, the index is a consequence of that guarantee and not a guess about future queries.

We do this badly today. Many of our databases carry indexes that no query has ever used, and every one of them is still maintained on every write.

Because: every index slows every write to the table and takes space whether or not a query ever uses it, so an index should be able to name the query it serves.

Good: an index on `check_in_date`, added in the same change as the report that filters bookings by it
Bad:  indexes put on three columns when the table is created, in case someone searches by them later

---

### Decide on purpose whether a foreign key column needs an index, because the database does not make one
[Slug: foreign-key-index-decision · Temperature: Judgment call · Origin: general · Scope: table · Why: indexes-need-a-reason]

A foreign key makes the database check the link. It does not index the column that holds it. When a parent row is deleted or its key changes, the database has to find that parent's child rows, and with no index on the foreign key column that means scanning the whole child table.

Index a foreign key column when parent rows are deleted or changed, or when queries go from a parent to its children. Leave it alone when neither happens, as with a small table that never changes or a parent that is never deleted. A table with several nullable foreign keys, like the exclusive arc, asks the question once per column.

Because: the database enforces the link but does not make it fast, and it is easy to assume the second part came with the first.

Good: an index on `user_id` in an addresses table, because addresses are always loaded by their user
Bad:  assuming a foreign key made the column fast to search, and finding out when the table is large

---

## Stories

### Labels on the bags
*slug: rebuilt-rows · serves: created-updated, soft-deletes, edit-in-place*

Reporting in the data warehouse went out of step with the operational system. Rows were turning up there for a booking's room types that did not exist in the operational databases at all.

A booking at Groups360 is one record, the roll-up: when it was created, the total cost, the arrival and departure dates. The room types booked sit in a child table, with one row for each room type on each day, so a five-night booking with five room types is 25 rows. The booking carried `created_at` and `updated_at`. The child table did not. From the application's side that looked reasonable. The booking already says when it was created and when it last changed, and the rows inside it could simply inherit that.

The warehouse does not see it that way. To the sync, every table is just a table. It does not know that these rows belong to a booking, and it cannot borrow the booking's timestamps. Each row is a package that is moved around on its own, long before anything opens the box it belongs to. A package with no label gives the sync nothing to go on, and the only thing left to follow was the `id`.

Then the way the application "updated" those rows came into it. It deleted the old rows and created new ones. The old rows had often been copied to the warehouse already. Deleting them in the operational database told the warehouse nothing, because a hard delete leaves nothing behind to notice. The new rows arrived with new ids and were copied as new. The old rows stayed, and reporting counted both.

Three things were weak at once, and each is a layer that was missing:

- **Rows were rebuilt when they should have been edited.** Changing the row that exists keeps its id and leaves nothing behind.
- **Rows were hard-deleted.** A deleted row leaves nothing for a sync to find. A `deleted_at` timestamp on a soft-deleted row turns a deletion into a change that can be seen.
- **The sync followed `id` and not `updated_at`.** An id can say that a row exists. It cannot say that the row has changed.

An `updated_at` on the table would not have fixed this on its own, since the rebuilt rows would still have been strays. It is one of the pillars the design should have stood on. A sync that follows `updated_at`, together with a `deleted_at` on soft-deleted rows, sees every change, deletions included, even when application code rebuilds rows it should have edited. Each layer covers a gap the others leave, which is the case for supplying all of them.

The lesson underneath is about whose point of view a table is designed from. In the application, a timestamp answers a question the application asks. In the warehouse, the same column has another job: it is how a row is tracked. A table that leaves the columns off has quietly taken itself out of that.

### The contact list that grew up
*slug: contact-list · serves: lists-or-tables*

This is an illustration and not a real case. It shows how a series of reasonable choices ends at the wrong shape.

A property needs a few contact emails. The simplest thing is one field, `contact_emails`, holding them separated by commas. For a while that is enough. The screen shows the field, and nobody needs more from it.

Then someone asks to find the property that an address belongs to. A search for `ann@example.com` returns a property that holds `joann@example.com`, because the search is matching pieces of text and the database has no idea where one address ends and the next begins. The fix is a sensible one: make the field an array. The same search now matches whole addresses, and the column is better for it.

Then someone asks which of the addresses should receive invoices. There is nowhere to put that. A flag belongs to one address, and an array element is only a value, with nothing to hang a flag on. The addresses were never a list of values that belonged to the property. Each one was a thing with facts of its own, and the property had a collection of them. That is a table, and it was a table from the start.

Each earlier step was a reasonable answer to the question in front of it. The question that would have found this at the first step is what each value might come to carry, and whether anyone will ever need to say something about one address and not about all of them together.

### The scoreboard kept by hand
*slug: header-status · serves: derived-in-view*

A booking at Groups360 has a header, and beneath it sit the things that were actually booked: sleeping rooms at a hotel, and spaces such as a conference room, an event space, or a banquet hall. Rooms and spaces began as separate services and were later combined in the booking service, which holds the orchestration data that ties them together, the header among it. The header carries a status, meant to sum up the status of the room and space bookings beneath it. Sometimes only one of the two exists.

That status was kept by application code. Whatever changed a room booking or a space booking was supposed to update the header to match. That code did its work as separate steps and not as one transaction, and it handled exceptions piece by piece. So one update could succeed and commit, and then an exception in a later step was caught and handled, and the update that should have followed never ran. The room and space tables stayed accurate, and the header's status drifted away from them.

A standing weekly correction now exists to bring them back in step. The mismatch also carries into the group sync and the data warehouse, and from there into reporting, where it makes problems that had no reason to exist.

A scoreboard kept by hand makes the point. When a person writes the score on a board while the game is played somewhere else, the board is right for as long as the person sees every play. The first play that is missed, the board is wrong, and the game goes on without it. The game was never wrong, and here the game was the room and space tables. A scoreboard that reads the score from the game cannot be wrong.

The immediate bug has a fix of its own. Several changes that must succeed or fail together belong in one transaction, so that a failure part way through undoes the earlier steps instead of leaving them committed. The better answer removes the need for it.

Nothing about the status needed to be stored. It is a mapping from the statuses of the bookings below it, so it can be read through a view that derives it, with no code to keep it in step. A generated column could not do this, because it can read only its own row. The sibling case, a value derived from the same row but still kept by a separate process, is told in *derived-by-process* on Columns. The design that fits is a header table that holds only what is really stored, with a read view on top that adds the derived status. A view that sums up other rows cannot be written to, so the application writes to the table and reads through the view, and nothing writes the status. Groups360 has not built this yet. It is described here because it would remove the drift by construction, and it is worth building the first time it can be.

Nobody was at fault. This is the design most people reach for, and it looks right until the first time it drifts. The question that finds it early is whether the value could simply be derived. If a value can be made true by construction, there is no reason to store one that can differ.
