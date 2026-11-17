# File formats for the agent side

One synthetic example for every kind of file this repository will make for the agent side. The examples are
in `examples/`. **They show the shape of each file, not decided content.** Every prefix, grouping, severity
value, and rule-line syntax in them is illustrative until the decisions in `NEXT_STEPS.md` step 2 are made.
The two rule files and the agent file pass the target's real validators (see "Checking", below).

| Entity | Who writes it | Where it goes | Example | Checked by |
|---|---|---|---|---|
| Concern rule file | Generated from the overlay short forms and the control file | The target's `.claude/rules/` | `examples/db_columns_conventions.md` | `validate-rule.mjs`, `check-claude.mjs` |
| Content-gated rule file | Generated, as above | The target's `.claude/rules/` | `examples/db_currency_conventions.md` | the same |
| Agent definition | By hand, with the fixed boilerplate copied from the target | The target's `.claude/agents/` | `examples/database_design_agent.md` | `check-claude.mjs` |
| Overlay entry | By hand | `agent/overlay/<slug>.md` | `examples/overlay_not-null-until-null-has-meaning.md` | the staleness check (planned) |
| Control file | By hand | `agent/control.toml` | `examples/control.toml` | the emitter (planned) |
| Companion | Generated from the page and the overlay | The target (location undecided) | `examples/companion_money-in-minor-units.md` | link checks (planned) |
| Code lock | Generated; never edited by hand | `codes.lock` | `examples/codes.lock.json` | the emitter (planned) |
| Type mapping | By hand | `agent/type_mapping.md` | `examples/type_mapping_reference.md` | review |

## How to read each example

- **Rule file.** Frontmatter, one intro line naming the acronym, a generated-file notice, then sections of
  numbered lines. Each line is a statement, then a one-line reason, then the slug. The statement opens with
  its trigger when it is conditional (`RRC10`), and a prohibition or a demand needs none. The first example
  loads whenever a matching file is edited (`paths`). The second loads only when the change also mentions one
  of its `when` terms (`whenPaths` plus `when`).
- **Agent.** The sections `Guardrails`, `Suppression handling`, and `Output format` are copied verbatim from
  the target's exemplar and must stay in step with it (`RAGT15`). The opening statement, the co-owned rules
  table, `Read first`, and the domain sections are written by hand. Each domain section opens with a skip
  condition and cites rule codes. The file contains the target's own em dashes, which come from the copied
  boilerplate and from the suppression marker syntax.
- **Overlay entry.** Keyed by slug. `rule_hash` records which version of the page's rule the short form was
  written against. The hash is the first 16 hex characters of the SHA-256 of
  `### <title> [Slug: … · Temperature: … · Origin: … · Scope: … · Why: …] <body>`, where the body has
  HTML comments removed and every run of whitespace collapsed to one space. The build must implement this
  exact function. The short form is needed because some rules cannot be cut mechanically: for example, the
  body of `no-float-for-money` opens with its Because line, and its statement is only the page heading.
- **Control file.** TOML, because the Python standard library can read it. It holds the grouping of page
  groups into concern files, one acronym per file, the globs and content-gating terms, which groups reach the
  agent, and the severity mapping.
- **Companion.** The stage-two file: the full rule, why it exists, and the engine-specific examples that the
  engine-neutral pages leave out.
- **Code lock.** Maps each rule code to its slug so a code is assigned once and never reused.
- **Type mapping.** Spellings only. The pages stay engine-neutral.

## What is deliberately undecided

The split into concern files and the letters after `RDB` (`RDBCL` and `RDBCY` are examples), whether temperature and origin appear in a rule
line, the `[slug: …]` syntax, where companions live in the target, and every value in `[severity]`.

## Checking

```
python3 tools/run_target_validators.py              # the examples
python3 tools/run_target_validators.py <file...>    # any candidate rule or agent files
```

Observed behavior of the target's validators, tested by breaking the examples on purpose:

| Mistake | Result |
|---|---|
| `paths:` written as a block-style YAML list instead of `["a", "b"]` | Error. The hook silently ignores such a list, so the rule would never load. |
| A rule file with no frontmatter | Error. The hook silently skips it. |
| An agent whose `name` is not its filename with underscores turned into hyphens | Error (`RAGT2`). |
| A specialty agent with no `triggers` | Error (`RAGT5`). |
| The same rule code in two files that own the same acronym | Error (`RRC1`). |
| A file that mixes two acronyms | Its minority-prefix lines are treated as citations of other files' codes, not definitions, so a duplicate under the minority prefix is not caught. Give each file exactly one acronym. |
