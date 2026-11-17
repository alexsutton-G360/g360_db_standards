# Make every column NOT NULL until you can say what a null in it would mean

Rule line `RDBCL1` in `db_column_conventions.md`. Temperature: Default. Origin: general.

## Full rule

Start every column as NOT NULL. Allow null only when the author can say, in one sentence, what a null in that column means.

There are two honest answers. Null can mean the value is unknown: it exists, and the system does not have it. Or null can mean there is no such value for this row: it does not exist, does not apply, or does not exist yet. An answer vaguer than either, like "not sure yet" or "might be handy", means the column is not ready to be nullable.

The point is not to avoid nulls. It is to avoid errant ones, where a null means something the next reader would not guess. When several nullable columns together carry one fact, say so in a check constraint: if exactly one of them must be set, or at least one, enforce it, as the polymorphic rules on Tables do.

Because: a column that is nullable by accident lets someone create an invalid row, and the fault turns up months later, far from its cause. A NOT NULL column turns the same mistake into an error on the day it happens, when it is cheap to fix. A null used as a stand-in for false hides a decision nobody made, so give the column a default instead.

Good: a property's identifier in an outside system, null for properties that do not use that system, because there is none to store
Good: a booking's `confirmation_number`, null until the booking reaches its final phase, because it does not exist yet
Bad:  a hotel's room count left nullable. A hotel without one is an invalid record, so let the database refuse it.
Bad:  a lease's `end_date` left null both for "open-ended" and for "not entered yet". A reader cannot tell which, so settle on one meaning and give the other its own representation, such as a NOT NULL `is_open_ended` flag.
Bad:  a flag for whether a property shows in search, where null is treated as false. Give it a default of false.
