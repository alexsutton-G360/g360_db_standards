# Name a function `ufn_<descriptor>`

Rule line `RDBOB9` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A function you write starts with `ufn_`, followed by a descriptor of what it does.

Because: the pattern is a house convention. The prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

Good: `ufn_set_updated_at`
Bad:  `set_updated_at`

Second opinion: DBA.
