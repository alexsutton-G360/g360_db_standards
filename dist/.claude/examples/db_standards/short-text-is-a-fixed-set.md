# Treat a short text column as a fixed set unless there is a reason it is not

Rule line `RDBCL15` in `db_column_conventions.md`. Temperature: Default. Origin: general.

## Full rule

Before adding a short text column, ask whether it holds one of a known set of values. If it does, or might, treat it as constrained and say so in the design. Leaving it open is the exception, and the reason is worth a sentence.

If a column is named `status`, `type`, `kind`, `mode`, or `category`, or names a strategy or a method, stop and check. There is a decent chance a fixed set is hiding in it.

Because: a column left open collects whatever anyone writes into it, and every reader downstream has to cope with the variations. The database is the lowest level at which something can be true, so a set enforced there is inherited by everything downstream, including places where such a limit would be hard to enforce, the warehouse among them.

Good: a `status` column limited to `draft`, `hold`, and `confirmed`
Bad:  a `status` column with no limit, holding `confirmed`, `Confirmed`, `CONFIRMED`, and `conf`
