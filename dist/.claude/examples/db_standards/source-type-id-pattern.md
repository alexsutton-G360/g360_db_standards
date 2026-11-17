# Recognize `source_type` and `source_id`, and use it only when the fan-out is large and an orphan is harmless

Rule line `RDBRL2` in `db_relationship_conventions.md`. Temperature: Judgment call. Origin: general. Second opinion: Data Architect.

## Full rule

You will find this pattern in many existing Groups360 tables. One column holds a string naming the parent's table, such as `'user'` or `'org'`, and another holds the id of a row in that table. It is appealing because it is narrow, and a new kind of parent needs no change to the schema.

The cost is that the database cannot know what the two columns mean. To it they are two values, as unrelated as a first name and a street address, so it cannot hold a real foreign key on them. That makes it the exception to the rule that a pointer to a row in the same database gets a real foreign key (*rule: same-database-pointer-needs-fk*). Deleting a parent leaves its children behind. A misspelled type is accepted. An id can point at a row that never existed. Every guarantee falls to application code, and joins across the pattern are awkward to write.

Both of these must be true before the pattern is acceptable:

- The fan-out is large. The table may point at many kinds of parent, enough that the other two approaches, one nullable foreign key per parent (*rule: exclusive-arc-default*) and one junction table per parent (*rule: junction-table-per-parent*), would generate serious schema overhead.
- Orphans genuinely do not matter. The data is historical, ephemeral, or low-stakes, so a dangling reference harms nothing.

An activity log is the standard example. Entries about an RFP that was later deleted still have historical value, and logging a new kind of event needs no migration. If only one of the two is true, one of the other approaches is the better call. If you are not certain the second is true, it probably is not. An addresses table for users and orgs is not such a case: two parents is a small fan-out, so one of the other approaches is the better call.

A `source_type` column is itself a set of allowed values, so the rule on fixed sets applies to it (*rule: database-enforces-fixed-set*, on Columns).

Because: a rule the database does not enforce is a convention and not a standard, and conventions stop holding when the code around them changes.

Second opinion: Data Architect.
