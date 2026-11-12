---
slug: "major-units-standard-block"
title: "Calculate major units in a generated column with the standard block"
temperature: "Default"
origin: "house"
scope: "column"
why: "currency-major-units"
page: "columns"
group: "Currency"
companion: true
---

# Calculate major units in a generated column with the standard block

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

A separate [runbook](../../runbook/currency_runbook.md), outside these standards, covers what to do if a new or changed currency means the block has to change. Nobody watches for ISO changes on a schedule, so whoever learns of one should tell the data architect.

More: companions/major-units-standard-block.md
