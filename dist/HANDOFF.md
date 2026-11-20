# Handoff: Groups360 database standards for the AI guidance repository

This folder is generated from the Groups360 database standards wiki pages. Nobody edits these files by
hand. A change to a page is a full replacement of that wiki page, and these files are re-cut from the pages
and handed over again.

## What is here

| Path | What it is |
|---|---|
| `.claude/rules/db_*_conventions.md` | Seven concern files of numbered rule lines, scoped by `paths` to `migrations/**` and `<pkg>/data/models/**` |
| `.claude/rules/db_usage_conventions.md` | How to apply the rules: they are guidelines the author may bend for a stated reason, and the agent never decides for the author |
| `.claude/agents/database_design_agent.md` | A specialty review agent that owns the family. Its Guardrails, Suppression handling, and Output format sections are copied word for word from `data_migration_agent.md` |
| `.claude/examples/db_standards/` | One companion per rule (the full rule and the stories behind it), plus `approved-acronyms.md` |

Nothing existing is overwritten. Every file is new.

## How to install

Unzip `dist.zip` at the root of the guidance repository. **Almost everything is inside a hidden `.claude/` folder, so
Finder and most zip previews show only `HANDOFF.md`.** To see the rest, run `unzip -l dist.zip`, or press
`Cmd+Shift+.` in Finder. Everything lands under `.claude/`, next to the
existing rules and agents, and no existing file is replaced. `HANDOFF.md` and `.generated` also land at the root;
this note can be deleted once read, and `.generated` records which commit of your repository the agent's
fixed sections were copied from. Then run `node .claude/scripts/check-claude.mjs` as usual.

## The rules

No rule is left out. Together the rule files come to about 43 KB, about 10k tokens if all of them load.

| File | Acronym | Rules | Codes | Size |
|---|---|---|---|---|
| `db_naming_conventions.md` | `RDBNM` | 9 | RDBNM1 to RDBNM9 | 4.4 KB |
| `db_identifier_conventions.md` | `RDBID` | 10 | RDBID1 to RDBID10 | 5.9 KB |
| `db_column_conventions.md` | `RDBCL` | 19 | RDBCL1 to RDBCL19 | 10.4 KB |
| `db_currency_conventions.md` | `RDBCY` | 7 | RDBCY1 to RDBCY7 | 3.9 KB |
| `db_table_conventions.md` | `RDBTB` | 7 | RDBTB1 to RDBTB7 | 4.9 KB |
| `db_relationship_conventions.md` | `RDBRL` | 7 | RDBRL1 to RDBRL7 | 5.0 KB |
| `db_object_conventions.md` | `RDBOB` | 15 | RDBOB1 to RDBOB15 | 8.0 KB |

The `RDB` prefix is reserved for these files, and the maintainer of the guidance repository has agreed to it.
A code, once assigned, is permanent: suppression markers in service code name a rule by its code. The codes
are recorded in `codes.lock` in the standards repository and are never reused or renumbered.

## Decisions for the maintainers of the guidance repository

1. **Companions live under `.claude/examples/`, not `.claude/rules/`.** Claude Code loads every file under
   `rules/` that has no `paths`, and the companions have none. If you prefer another location, tell us.
2. **Every file is path-scoped only, with no `whenPaths` or `when`.** Your hook treats `paths` as
   unconditional, so a file cannot be both scoped and gated, and a file with only `whenPaths` loads in every
   Claude Code session. We deliberately load all of these rules on every migration and model edit, so a rule is
   never missed, and will narrow the load only with suppression counts and spend numbers to go on.
3. **Every finding from the new agent is `discuss`.** Nothing is applied without the author, and `/review-loop`
   never rewrites a design on its own. Severity follows the rule's Temperature: Rule is High, Default is
   Medium, Judgment call is Low.
4. **Suppression reasons.** The standards treat any specific reason as enough, and the agent never grades it.
   `check-markers.mjs` already behaves this way. The wording in `suppression_conventions.md` RSUP2 ("a reason an
   unfamiliar reader could evaluate") is a little stricter than the script, so please confirm which governs.
5. **Overlaps to reconcile.** `RMIG6` and `RMIG9` (new columns must be nullable or carry a default) conflict
   with the Default "make every column NOT NULL until you can say what a null in it would mean" (`RDBCL`).
   `RMIG4` and `RMIG19` overlap the id, guid, and constraint naming rules. The agent file cross-links them.
6. **A mismatch in your agent file.** `data_migration_agent.md` calls `RMIG15` "DDL-to-data-model parity", but in
   `migration_conventions.md` `RMIG15` is "migrations must not import ORM models". Parity is only a cross-layer
   check in `review.md`.
7. **Observing companion lookups.** The agent is told to read a rule's companion before reporting a Judgment-call
   finding. A hook that logs reads of `.claude/examples/db_standards/` would show whether it does.
8. **Rule injection is once per session.** `inject-rules.cjs` injects each rule file at most once per session, and
   subagents appear to share the session. A review agent that reads a migration after another agent has done so may
   receive none of the injected rules. Our agent therefore reads its bundles with explicit Read calls and does not
   rely on injection. Other agents that depend on injection may be getting less than they appear to.
9. **Overlap with `code-reviewer`.** In a trial review, `code-reviewer` reported floating-point money and naive
   timestamps independently of our agent, so each was reported two or three times. Our rule codes make the
   duplicates easy to spot, but the orchestrator does not merge them.
10. **Constraint name prefixes.** `RMIG19` asks for a project-wide naming convention but names no prefixes. In a trial
   review, `data-migration-agent` told the author to rename `ctx_notes_guid_unique` to `uq_notes_guid`, which
   contradicts `RDBOB6` (`ctx_` for check, unique, and exclusion constraints). The `uq_` prefix appears nowhere in
   your repository. We suggest `RMIG19` point at `RDBOB5` to `RDBOB7` for the prefixes, and that the migration agent
   defer to them.
11. **Model and effort.** Every agent in your repository sets both fields, so we set ours to `opus` and `high`, which
   is what most of them use (`data-migration-agent`, `architecture-layering-agent`, and nine others). In our first
   trial run, before the other fixes, the agent inherited the session setting and skimmed its rule files. Retune
   them under `RAGT17` as you see fit. The value is recorded on its own commit so it can be reverted alone.
12. **The generated notice** at the top of each bundle is our wording. If you use a standard header for generated
   files, tell us and we will switch.

## How these were checked

The files were validated against `validate-rule.mjs` and `check-claude.mjs` on a scratch copy of the
guidance repository. The repository itself was not written to.
