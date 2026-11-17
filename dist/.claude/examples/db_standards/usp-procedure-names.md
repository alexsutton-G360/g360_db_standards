# Name a stored procedure `usp_<descriptor>`

Rule line `RDBOB10` in `db_object_conventions.md`. Temperature: Rule. Origin: house. Second opinion: DBA.

## Full rule

A stored procedure you write starts with `usp_`, followed by a descriptor of what it does.

Because: the pattern is a house convention. The prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

Good: `usp_db_backups`
Bad:  `backup_databases`

Second opinion: DBA.
