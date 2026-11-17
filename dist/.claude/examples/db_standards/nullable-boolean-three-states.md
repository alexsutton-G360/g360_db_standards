# Use a nullable boolean only when true, false, and unknown are all real answers

Rule line `RDBCL3` in `db_column_conventions.md`. Temperature: Rule. Origin: general.

## Full rule

A nullable boolean has three states, so use one only when all three mean something. For any other three-way choice, see the guidance on values from a fixed set on this page.

Good: "does this property charge for parking?", where null means it is not known whether it does
Bad:  a nullable boolean standing in for a three-way choice that has names, like draft, hold, and confirmed
