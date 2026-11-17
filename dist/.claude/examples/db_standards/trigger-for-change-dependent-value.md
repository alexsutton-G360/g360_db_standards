# When a value depends on how a row changed, let a trigger maintain it

Rule line `RDBCL19` in `db_column_conventions.md`. Temperature: Default. Origin: general.

## Full rule

When a value cannot be worked out from the other columns of the same row, because it depends on when or how the row changed, let a trigger maintain it and do not leave it to application code. A generated column cannot do this job, since its formula has to give the same answer every time. A timestamp stamped at the moment of a change is the standard case, and the shared trigger for `updated_at` is the worked example (*rule: shared-updated-at-trigger*, on Tables). That function maintains `updated_at` and nothing else, so a different value gets a function of its own, written in the same shape. Name the trigger and the function by the rules on Other objects and tools (*rule: trg-trigger-names*, *rule: ufn-function-names*).

Because: a trigger maintains the value for every writer, whichever application or script touched the row.

Good: a trigger that sets `updated_at` on every real change
Bad:  every piece of application code that writes the row setting `updated_at` itself

## Why this rule exists

Rules that share this explanation (why: `calculated-columns`):

- `same-row-value-generated-column`: Compute a value from other columns in the same row in the database, not in application code

### Story: The value that never needed a process

In 2018, Groups360 stored a property's latitude and longitude as two plain columns, kept current by a script. A separate application process took those two values and built a point value from them whenever it ran. The point depended on nothing but the two columns beside it. It was a function of them and nothing more.

For years that caused no trouble. The process worked, and nothing about the design looked like a mistake. Then, three or four years in, it began to matter. An application process is code, and code fails. Sometimes an earlier step stopped before the point was written. Sometimes the process was never started when it should have been. Each time, the point was left behind with no error and no trace, while the two columns it came from moved on without it.

By the time the gaps were a problem, they were a problem everywhere. The fix took until 2025, many developers, and about six months from planning to finished work, because the stale values, and the code that produced them, had spread through the database. The finished fix is short to describe: the point became a generated column over latitude and longitude.

A generated column cannot disagree with its inputs. The database computes it whenever they change, and nothing can write to it directly. The failure was never about careless code. A derived value that code keeps in step is only as reliable as every run of that code, and a generated column has no run to miss. That is the case for the rule, and the reason it is a default and not a preference. The point never needed a process at all.
