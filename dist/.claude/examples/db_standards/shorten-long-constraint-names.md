# When a constraint or index name would pass 63 characters, shorten it from the table of short forms

Rule line `RDBOB15` in `db_object_conventions.md`. Temperature: Default. Origin: house. Second opinion: DBA or Data Architect.

## Full rule

Postgres cuts any name at 63 characters and gives only a notice, and two names cut to the same text collide. This happens to constraints and indexes on a table that already has a long name, because every key repeats the table name and then adds column names. A unique constraint on two columns of a table with a five-word name can pass the limit on its own.

Spell every word out whenever the name fits. When it does not, work through these steps in order, and stop at the first one that makes the name fit:

1. Use the short form of any term on the approved acronym tables.
2. Use the short forms on the Short forms for names at the limit table. Start with the word that saves the most characters, and shorten every occurrence of a word at once, until the name fits.
3. If it still does not fit, rename the table, or consult the DBA and Data Architect before going further.

Decide once per table, using its longest constraint or index name, and then use the same short forms in every constraint and index on that table, so a word is never spelled out in one name and shortened in the next. The table's own name and its columns stay spelled out.

Because: a name Postgres has to cut can collide with another cut name without any error. A fixed order and a fixed table give every author the same short name for the same words, so the result is consistent across databases.

Good: `ctx_rfp_template_agenda_rsvtn_parts_rsvtn_id_day_idx` (52 characters, where the full name is 66) and `fk_rfp_template_agenda_rsvtn_parts_space_configuration_id` (57, spelled out where it fits)
Bad:  `ctx_rfp_tmplt_agnd_rsvtn_parts_rsvtn_id_day_idx`, which shortens words that did not need it, and the same table using `reservation` in one name and `rsvtn` in the next

Second opinion: DBA or Data Architect.
