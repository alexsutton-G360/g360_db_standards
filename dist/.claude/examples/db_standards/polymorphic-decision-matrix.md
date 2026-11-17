# Choose among the three by how many parents there are and how much integrity matters

Rule line `RDBRL5` in `db_relationship_conventions.md`. Temperature: Judgment call. Origin: general. Second opinion: Data Architect.

## Full rule

Two questions decide it: how many kinds of parent the table can belong to, and how much a dangling reference would hurt.

| | Few parents (five or six or fewer) | Many parents |
|---|---|---|
| **Integrity matters** | Nullable foreign keys, one per parent | Junction tables |
| **Integrity is low-stakes** | Nullable foreign keys, still the easy choice | `source_type` and `source_id`, acceptable here |

Start with nullable foreign keys. For most tables that is the right default, with real referential integrity that is easy to join against and easy to understand. Reach for junction tables when the fan-out is large or growing and the data still needs protecting: the schema gets busier and the data stays safe. Consider `source_type` and `source_id` only when the fan-out is large and the table is one where an orphan truly causes no harm.

When in doubt, talk to the Data Architect before building. This is one of the places where the decision made on day one is hard to undo on day three hundred.

Second opinion: Data Architect.
