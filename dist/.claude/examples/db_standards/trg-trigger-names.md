# Name a trigger `trg_<table>_<descriptor>`

Rule line `RDBOB8` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A trigger name starts with `trg_`, then the table it sits on, then a descriptor of what it does. The shared trigger that keeps `updated_at` current is under Row lifecycle on Tables.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `trg_bookings_set_updated_at`
Bad:  `bookings_trigger`, `update_bookings`

Second opinion: DBA.
