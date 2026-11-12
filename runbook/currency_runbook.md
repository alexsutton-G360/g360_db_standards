# WORLD EVENT: We need to handle a new or changed currency

*A rare event in the world, not a change we make in our own systems.*

**What this page is.** Something has happened outside Groups360: a new currency exists, an existing one has been replaced or redenominated, or the standard that says how many decimal places a currency has has changed. This is very rare. This page is not a guide for changing something in our own systems that has to do with currency. It is the in-case-of-emergency page, so nobody has to work out what to do under pressure, and it is deliberately **not** part of the database standards, which say what to do and when.

**Keywords:** currency, new currency, changed currency, currency change, currency replaced, currency withdrawn, redenomination, new ISO 4217 list, ISO 4217 update, ISO currency list, currency code, unlisted currency, decimal places, number of decimals, minor units, major units, `_minor_units`, major unit column, `base_price_major`, `service_charge_major`, generated column, standard block, currency block, CASE logic, `SET EXPRESSION`, wrong amount, wrong price, wrong total, amounts off by ten, amounts off by a hundred, amounts off by a thousand, cents, rounding, money shown wrong.

## Who to tell

Nobody watches for changes to the ISO 4217 currency list on a schedule, and there is no formal process behind this yet. If you learn that a currency is new, replaced, or has changed, which will most likely come from outside the data team, tell the data architect. The data architect owns the response, and brings in the DBA and anyone else who is needed.

**Status:** draft. Every command below was run on PostgreSQL 17.11 on 4 November 2026, against a test table of 500,000 rows, with the invented currency `ZZZ`. The currency lists come from the SIX ISO 4217 list one published on 2026-09-17.

**Requires PostgreSQL 17 or later.** Check with `SELECT version();`. The `SET EXPRESSION` command does not exist before 17 and fails with a syntax error.

## What this is about

Money is stored as whole minor units (cents, fils, yen) in columns ending in `_minor_units`. Next to each one sits a stored major-unit column, computed from it by a pasted block of `CASE` logic that knows how many decimal places each currency has. The block is described on Columns, under "Calculate major units in a generated column with the standard block".

If ISO 4217 ever changes a currency's decimal places, every copy of that block has to change. That is the job here. The steps are in order, and the order matters.

## Step 0. Check whether anything has to change at all

Look up the currency's number of decimal places in the current ISO 4217 list, list one, published by SIX. Then find the case:

- **A new currency with two decimal places.** Nothing to change. The standard block treats every code it does not list as two places, so the new code already works.
- **A new currency with zero, three, or four decimal places.** The block has to change: the code must be added to the right list. Continue.
- **An existing currency whose decimal places changed.** Rarer still. The block has to change, and stored amounts need a decision. Continue.
- **A currency that was replaced or withdrawn.** If its code is in one of the lists, leave it there, so rows that were written under it keep reading correctly. A replacement is a new code, so check it as a new currency. What to do about amounts still held in the old currency is a decision for finance and product.

## Step 1. Decide what happens to stored amounts, before changing anything

Changing the formula changes what every stored minor-unit count means for that currency. In the worked example below, a stored `150004` reads as 1,500.04 under the old formula and 150.004 under the new one. If those amounts were written under the old convention, they are now wrong by a factor of 10, unless they are converted.

Whether to convert them, and how, is a decision for finance and product, not for whoever holds the keyboard. This runbook changes the formula and **does not convert stored amounts**. If they must be converted, it has to happen in the same window as the formula change, so the two are never visible apart.

Settle this first and write the answer down.

## Step 2. Find every copy

List every generated column in the database:

```sql
SELECT n.nspname AS schema, c.relname AS table, a.attname AS column
FROM pg_attribute a
JOIN pg_class c ON c.oid = a.attrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE a.attgenerated <> ''
  AND NOT a.attisdropped
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY 1, 2, 3;
```

Narrow it to copies of the currency block. This matches a code that only the block contains, or a reference to `currency_code`:

```sql
SELECT n.nspname AS schema, c.relname AS table, a.attname AS column
FROM pg_attribute a
JOIN pg_class c ON c.oid = a.attrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
WHERE a.attgenerated <> ''
  AND NOT a.attisdropped
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND (pg_get_expr(d.adbin, d.adrelid) LIKE '%''KWD''%'
       OR pg_get_expr(d.adbin, d.adrelid) ILIKE '%currency_code%')
ORDER BY 1, 2, 3;
```

This step works because of the naming rule on Columns: every column that holds a currency code has `currency_code` in its name, and the block reads it by that name. The `'KWD'` match finds an unedited copy even under a different column name, and the `currency_code` match finds a copy that was edited. A copy that someone edited by hand, dropping `'KWD'`, and also renamed the code column would be missed by both. Also read the full list from the first query and look at anything that sounds like money.

Do this in every database that holds money columns, not only one.

## Step 3. Write the new expression

Start from the standard block and change only the lists. Move the code into the list for its new number of decimal places: zero places divide by 1, three by 1000, four by 10000, and everything else falls to 100.

```sql
<minor_units_column>::numeric / CASE
  WHEN currency_code IN ('BIF','CLP','DJF','GNF','ISK','JPY','KMF','KRW','PYG','RWF','UGX','UYI','VND','VUV','XAF','XOF','XPF') THEN 1
  WHEN currency_code IN ('BHD','IQD','JOD','KWD','LYD','OMR','TND') THEN 1000
  WHEN currency_code IN ('CLF','UYW') THEN 10000
  ELSE 100
END
```

The only thing that differs between columns is the name of the minor-unit column. Update the block on Columns too, so the next copy is the new one.

## Step 4. Rehearse

Run the whole thing, Steps 5 to 7, in a lower environment first. For the largest tables, rehearse on a copy, because Step 5 locks the table.

## Step 5. Apply

`SET EXPRESSION` recomputes every stored value in the column. It **rewrites the whole table and holds an `ACCESS EXCLUSIVE` lock the entire time**, so nothing can read or write the table until it finishes. On the 500,000-row test table that was well under a second. Plan from the row count, not from that number.

A table with several money columns needs every one of them changed, because changing one leaves the others on the old formula. Put all of a table's generated columns into a **single** `ALTER TABLE`, one action each. The table is rewritten once and not once per column. In the test, two columns in one statement took about 0.66 seconds, against about 1.1 seconds for two separate statements.

```sql
BEGIN;
ALTER TABLE <schema>.<table>
  ALTER COLUMN base_price_major SET EXPRESSION AS (
    base_price_minor_units::numeric / CASE
      WHEN currency_code IN ('BIF','CLP','DJF','GNF','ISK','JPY','KMF','KRW','PYG','RWF','UGX','UYI','VND','VUV','XAF','XOF','XPF') THEN 1
      WHEN currency_code IN ('BHD','IQD','JOD','KWD','LYD','OMR','TND','ZZZ') THEN 1000
      WHEN currency_code IN ('CLF','UYW') THEN 10000
      ELSE 100
    END),
  ALTER COLUMN service_charge_major SET EXPRESSION AS (
    service_charge_minor_units::numeric / CASE
      WHEN currency_code IN ('BIF','CLP','DJF','GNF','ISK','JPY','KMF','KRW','PYG','RWF','UGX','UYI','VND','VUV','XAF','XOF','XPF') THEN 1
      WHEN currency_code IN ('BHD','IQD','JOD','KWD','LYD','OMR','TND','ZZZ') THEN 1000
      WHEN currency_code IN ('CLF','UYW') THEN 10000
      ELSE 100
    END);
COMMIT;
```

The example moves the invented currency `ZZZ` to three decimal places.

## Step 6. Make the change visible downstream

`SET EXPRESSION` is not an `UPDATE`. No trigger runs, so `updated_at` does **not** move. Anything that follows `updated_at`, like the warehouse sync, will not see that the stored major-unit values changed.

Set `updated_at` on purpose, for the affected currency only. The shared trigger keeps an explicit value.

```sql
UPDATE <schema>.<table> SET updated_at = now() WHERE currency_code = 'ZZZ';
```

This was tested to select exactly the affected rows. Whether the warehouse then re-sends those rows is not something this page tested. Confirm that with whoever owns the sync.

## Step 7. Check

For the changed currency, minor units and major units should now line up under the new divisor:

```sql
SELECT currency_code, base_price_minor_units, base_price_major
FROM <schema>.<table>
WHERE currency_code = 'ZZZ'
ORDER BY id
LIMIT 5;
```

In the test, `150004` minor units went from `1500.0400` to `150.0040`. Check a currency that did not change too, and confirm it is untouched.

## Step 8. Undo

Run Step 5 again with the old expression, then Step 6 again. It takes the same lock and does the same rewrite.

## If a database uses a shared function instead of the pasted block

The standards name a shared function as an alternative for a database with many such columns. Changing the function **does not recompute stored values**. In the test, a stored value stayed at `1500.0000` after the function changed. Re-state each column's expression, with the same expression, to force the recompute: it went to `150.0000`.

```sql
CREATE OR REPLACE FUNCTION ufn_divisor(code text) RETURNS int LANGUAGE sql IMMUTABLE AS $$
  SELECT CASE WHEN code IN ('KWD','ZZZ') THEN 1000 ELSE 100 END
$$;

ALTER TABLE <schema>.<table>
  ALTER COLUMN x_major SET EXPRESSION AS (x::numeric / ufn_divisor(currency_code));
```

The same lock and rewrite apply, so Steps 4, 6, and 7 apply too.

## Not covered here

Converting stored amounts (Step 1). The warehouse's own copy of the major-unit columns.
