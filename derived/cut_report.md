# Cut-apart report

Rules: 73 | stories: 20 | principles: 5 | reference files: 1 | group intros written: 11

Words: full rule text 10618, stage one 10618 (100% of full). Rules with a cut point (<!-- brisk-end -->): 0 of 73.

## Words by scope (what loading that scope would inject)

| scope | rules | stage one words | full words |
|---|---|---|---|
| column | 36 | 4853 | 4853 |
| constraint | 2 | 202 | 202 |
| database | 1 | 70 | 70 |
| function | 1 | 53 | 53 |
| global | 4 | 243 | 243 |
| index | 1 | 67 | 67 |
| materialized_view | 1 | 64 | 64 |
| procedure | 1 | 54 | 54 |
| role | 1 | 133 | 133 |
| schema | 3 | 392 | 392 |
| table | 19 | 4262 | 4262 |
| trigger | 1 | 60 | 60 |
| user | 1 | 103 | 103 |
| view | 1 | 62 | 62 |

## Checks

- no problems: slugs unique and distinct from why keys, stories and principles; every citation and every story target resolves

## Trim candidates: unmarked rules over 120 words (36)

These are injected in full until someone places a cut point. Each one needs a judgment about where
the statement ends and the elaboration begins.

- `choose-fixed-set-mechanism` (554 words)
- `shared-updated-at-trigger` (372 words)
- `source-type-id-pattern` (365 words)
- `not-null-until-null-has-meaning` (339 words)
- `exclusive-arc-default` (308 words)
- `same-database-pointer-needs-fk` (306 words)
- `index-when-a-lookup-exists` (267 words)
- `junction-table-per-parent` (265 words)
- `guid-not-null-unique-generated-anywhere` (261 words)
- `currency-code-column` (257 words)
- `no-second-copy-use-a-view` (251 words)
- `plain-view-before-materialized` (250 words)
- `plan-for-existing-rows` (239 words)
- `array-or-second-table` (235 words)
- `major-units-standard-block` (234 words)
- `soft-delete-default` (228 words)
- `no-honest-limit-decide-where` (227 words)
- `guid-for-externally-referenced-tables` (219 words)
- `change-row-in-place` (218 words)
- `same-row-value-generated-column` (207 words)
- `by-column-is-user-guid` (205 words)
- `polymorphic-decision-matrix` (179 words)
- `foreign-key-index-decision` (174 words)
- `id-on-every-table-including-junctions` (169 words)
- `id-internal-guid-external` (165 words)
- `trigger-for-change-dependent-value` (162 words)
- `short-text-is-a-fixed-set` (159 words)
- `money-in-minor-units` (152 words)
- `schema-for-real-divisions` (146 words)
- `url-varchar-2048` (142 words)
- `no-delimited-list-strings` (142 words)
- `name-junction-tables-for-both-sides` (140 words)
- `pk-and-fk-names` (135 words)
- `schema-never-named-for-database` (134 words)
- `by-column-when-no-user` (133 words)
- `role-no-login` (133 words)

## Group intros

- global_rules: Approved acronyms (51 words): written out, not in the load hints
- columns: Standard columns (46 words): written out, not in the load hints
- columns: Currency (10 words): written out, not in the load hints
- tables: Row lifecycle (22 words): written out, not in the load hints
- tables: Naming tables (19 words): written out, not in the load hints
- tables: Row identity (55 words): written out, not in the load hints
- tables: Lists of values (46 words): written out, not in the load hints
- tables: Derived values and copies (38 words): written out, not in the load hints
- tables: Tables that belong to one of several parents (129 words): IN the load hints
- tables: Indexes (25 words): written out, not in the load hints
- other_objects: Keys, constraints, and indexes (47 words): written out, not in the load hints
- other_objects: Roles and users (27 words): written out, not in the load hints

## Decisions in this script (top of cut_apart.py)

- always-load scopes: ['global']
- group intros in the AI set: [('tables', 'Tables that belong to one of several parents')]
- pages kept out of the AI set: ['stock_tables']
