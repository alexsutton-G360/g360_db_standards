---
slug: "shared-updated-at-trigger"
why: "created-updated"
---

# Keep `updated_at` current with the shared trigger, not with application code

## Full rule

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

## Why this rule exists

Rules that share this explanation (why: `created-updated`):

- `created-at-updated-at-on-tables`: Give almost every table `created_at` and `updated_at`, and let the database manage them

### Story: Labels on the bags

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
