# Name every other constraint `ctx_<descriptor>`

Rule line `RDBOB6` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A check, unique, or exclusion constraint is `ctx_` followed by what it enforces. A unique constraint creates an index, which takes the constraint's name, so that index keeps its `ctx_` name.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `ctx_exactly_one_parent`, `ctx_unique_note_rfp`
Bad:  `notes_body_check`, the default name an unnamed check constraint gets

Second opinion: DBA.
