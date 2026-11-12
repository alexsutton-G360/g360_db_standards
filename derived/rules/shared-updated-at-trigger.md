---
slug: "shared-updated-at-trigger"
title: "Keep `updated_at` current with the shared trigger, not with application code"
temperature: "Rule"
origin: "house"
scope: "table"
why: "created-updated"
page: "tables"
group: "Row lifecycle"
companion: true
---

# Keep `updated_at` current with the shared trigger, not with application code

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

More: companions/shared-updated-at-trigger.md
