# Compute a value from other columns in the same row in the database, not in application code

Rule line `RDBCL18` in `db_column_conventions.md`. Temperature: Default. Origin: general.

## Full rule

When a value can be worked out from other columns in the same row, make it a generated column and let the database keep it current.

A generated column is stored, cannot be written to directly, and can use only the other columns of its own row, not other tables and not subqueries. If a value needs data from other tables, or has to be computed when it is read, use a view or a materialized view instead. Which one, and when, is covered on Tables (*rule: no-second-copy-use-a-view*, *rule: plain-view-before-materialized*).

A stored value takes space on every row, and adding a generated column to a table that already holds rows rewrites it, so on a very large table that is a bigger decision. See the note on scale on the Index.

A value that depends on when or how the row changed, and not on its other columns, cannot be a generated column. The next rule covers it.

Because: a derived value that code keeps in step is only as reliable as every run of that code, and a generated column has no run to miss.

Good: `total_minor_units bigint GENERATED ALWAYS AS (base_price_minor_units + service_charge_minor_units) STORED`
Bad:  application code adds the two values and writes the total

## Why this rule exists

Rules that share this explanation (why: `calculated-columns`):

- `trigger-for-change-dependent-value`: When a value depends on how a row changed, let a trigger maintain it

### Story: The value that never needed a process

In 2018, Groups360 stored a property's latitude and longitude as two plain columns, kept current by a script. A separate application process took those two values and built a point value from them whenever it ran. The point depended on nothing but the two columns beside it. It was a function of them and nothing more.

For years that caused no trouble. The process worked, and nothing about the design looked like a mistake. Then, three or four years in, it began to matter. An application process is code, and code fails. Sometimes an earlier step stopped before the point was written. Sometimes the process was never started when it should have been. Each time, the point was left behind with no error and no trace, while the two columns it came from moved on without it.

By the time the gaps were a problem, they were a problem everywhere. The fix took until 2025, many developers, and about six months from planning to finished work, because the stale values, and the code that produced them, had spread through the database. The finished fix is short to describe: the point became a generated column over latitude and longitude.

A generated column cannot disagree with its inputs. The database computes it whenever they change, and nothing can write to it directly. The failure was never about careless code. A derived value that code keeps in step is only as reliable as every run of that code, and a generated column has no run to miss. That is the case for the rule, and the reason it is a default and not a preference. The point never needed a process at all.
