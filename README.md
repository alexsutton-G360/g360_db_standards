# Groups360 database standards

How Groups360 designs PostgreSQL databases, written to be read by people and loaded by AI agents.

The pages try to teach how to think about data first and to state rules second. If they do their job,
you can handle a case nobody wrote down.

## Start here

Read [`pages/index.md`](pages/index.md). It explains what these docs are for, how to read a rule, the
principles behind them, and where to look for what.

## What is in this repository

| Path | What it is |
|---|---|
| `pages/` | The standards. **This is the only place to edit.** Index, Global Rules, Columns, Tables, Other objects and tools, Stock tables. |
| `runbook/` | The currency runbook. It is separate from the standards and covers what to do when a currency is added or changed. |
| `derived/` | Generated from `pages/` by `tools/cut_apart.py`. **Never edit by hand.** One file per rule for agents, plus companions, stories, principles, a manifest, load hints and a rule index. |
| `tools/` | `cut_apart.py` builds `derived/`. `lint_pages.py` checks the pages. `emit_agent_tree.py` builds the handoff zip. `run_target_validators.py` proves it. Standard-library Python 3 (3.11+, or `pip install tomli`). The validators need Node. |
| `agent/` | Hand-written inputs to the handoff: `control.toml` (which rules go in which bundle), the agent template, and the usage rules. |
| `vendor/ai_python_guidance/` | Read-only git submodule of the AI guidance repository. Nobody edits or commits inside it. |
| `dist/`, `dist.zip` | Generated handoff for the guidance repository. **Never edit by hand.** |
| `codes.lock` | The permanent code (for example `RDBCL3`) of every rule in the handoff. |
| `slugs.lock` | Every stable name (rule slugs, why keys, story and principle slugs). Names listed here are never removed or renamed. |
| `.github/` | The CI check, and a template for review ownership. |

## How a rule looks

Every rule has a heading and a tag line:

```
### Use lowercase for every name
[Slug: lowercase-every-name · Temperature: Rule · Origin: general · Scope: global · Why: lowercase-only]
```

- **Slug** points at exactly one rule. Use it to refer to the rule. It never changes.
- **Temperature** says how firm the rule is: Rule, Default, or Judgment call.
- **Origin** says what could overturn it: `house` (a Groups360 choice) or `general` (how Postgres or good practice works).
- **Scope** says what the rule governs: a column, a table, an index, and so on.
- **Why** is a key to the explanation behind the rule, shared by every rule that explanation covers.

After the tag line come the rule, a Because line, Good and Bad examples, and a Second opinion line.
The Index explains all of this in full.

## Setup

After cloning, fetch the submodule once (`git clone --recurse-submodules`, or afterwards
`git submodule update --init`). The handoff build reads one file from it, and does that for you if you forget.

## Building the handoff

```
python3 tools/emit_agent_tree.py --zip     # writes dist/ and dist.zip
python3 tools/run_target_validators.py     # runs the guidance repository's own checks on a scratch copy
```

Add `--update-lock` to the first command when a rule is new, so it receives its permanent code. Hand
`dist.zip` to the team that maintains the guidance repository.

## Editing the standards

These docs are meant to be edited. If a rule is wrong, or you hit a case nobody thought of, say so.

1. Edit files in `pages/` (or `runbook/`) on a branch and open a pull request. Say why in the description.
2. Run the checks, and commit what they produce:
   ```
   python3 tools/lint_pages.py
   python3 tools/cut_apart.py pages derived
   ```
   CI runs both and fails if `derived/` is out of date.
3. Never rename or delete a slug, a why key, or a story or principle slug. Other rules and outside
   documents point at them. If a rule really has to go, say so in the pull request, and a maintainer
   removes the name from `slugs.lock` in the same change.
4. New names are added to `slugs.lock` with `python3 tools/lint_pages.py --update-lock`.

House style, enforced where it can be: no em dashes, no singular first person in rules and stories
(a collective "we" for Groups360 is fine), stories are blameless and name no people, and a new rule
needs a unique slug.

Questions and second opinions go to the data architect. The DBA is the second opinion for the objects
and tools page.

## The derived set for agents

`tools/cut_apart.py` turns the pages into a neutral set of files that an agent can load:

- `derived/rules/<slug>.md`: stage one, the rule an agent is given first.
- `derived/companions/<slug>.md`: stage two, the full rule and the explanation behind it, read when the agent is unsure.
- `derived/AGENT_GUIDE.md`: the entry point for an agent. What is in the set, what to load and when, and how to treat a rule. The definitions in it are copied from the Index, so they cannot drift.
- `derived/manifest.json`, `derived/loading.json`, `derived/rule_index.md`: what exists and when to load it.
- `derived/cut_report.md`: sizes, checks, and the rules that could still be trimmed.

Stage one is safe by default: a rule with no cut point is given in full. To trim a long rule, put
`<!-- brisk-end -->` on its own line after the last paragraph an agent must see first. Everything above
it, plus the Good, Bad, Because and Second opinion lines, is stage one. The rest goes to the companion.
Humans never see the marker.

No rule has a cut point yet. The output is also not yet mapped to the format of any particular agent
repository. That adapter comes after the loading design is agreed.

## Status

- All pages are drafted and have been through a full review by the data architect.
- The DBA's review of `pages/other_objects.md` is pending. His comments will be handled like any other update.
- `pages/stock_tables.md` is a living page. It is not parsed into `derived/` and is not yet in the agent set.
- The pages were written and tested against PostgreSQL 15 and 17. Production is on 17.11.
