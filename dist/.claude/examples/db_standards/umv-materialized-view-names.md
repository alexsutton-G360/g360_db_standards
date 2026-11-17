# Name a materialized view `umv_<table>_<descriptor>`

Rule line `RDBOB12` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A materialized view starts with `umv_`, followed by the table it reads from and a descriptor of what it does. A materialized view that an application creates, and not a person, is not covered by this rule.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `umv_bookings_monthly_totals`
Bad:  `monthly_totals`

Second opinion: DBA.
