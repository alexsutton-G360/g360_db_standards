---
slug: "same-row-value-generated-column"
title: "Compute a value from other columns in the same row in the database, not in application code"
temperature: "Default"
origin: "general"
scope: "column"
why: "calculated-columns"
page: "columns"
group: "Values the database maintains"
companion: true
---

# Compute a value from other columns in the same row in the database, not in application code

When a value can be worked out from other columns in the same row, make it a generated column and let the database keep it current.

A generated column is stored, cannot be written to directly, and can use only the other columns of its own row, not other tables and not subqueries. If a value needs data from other tables, or has to be computed when it is read, use a view or a materialized view instead. Which one, and when, is covered on Tables (*rule: no-second-copy-use-a-view*, *rule: plain-view-before-materialized*).

A stored value takes space on every row, and adding a generated column to a table that already holds rows rewrites it, so on a very large table that is a bigger decision. See the note on scale on the Index.

A value that depends on when or how the row changed, and not on its other columns, cannot be a generated column. The next rule covers it.

Because: a derived value that code keeps in step is only as reliable as every run of that code, and a generated column has no run to miss.

Good: `total_minor_units bigint GENERATED ALWAYS AS (base_price_minor_units + service_charge_minor_units) STORED`
Bad:  application code adds the two values and writes the total

More: companions/same-row-value-generated-column.md
