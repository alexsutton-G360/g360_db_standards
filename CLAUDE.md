# Working in this repository

The Groups360 database standards. The pages are the corpus: the wiki and the agent files are both
rendered from them. Read this file before changing anything. Keep it short (see the last section).
Plans and status live in `NEXT_STEPS.md`.

## What is editable and what is generated

- **Edit:** `pages/`, `runbook/`, the hand-written rule file `agent/rules/db_usage_conventions.md`, the control
  file `agent/control.toml`, and the agent template `agent/agents/database_design_agent.md`.
- **Never edit by hand:** `derived/`, `dist/`, and the lock files `slugs.lock` and `codes.lock`. Lock files
  change only through the documented commands (`lint_pages.py --update-lock`, `emit_agent_tree.py --update-lock`).
  A rule code is permanent once assigned.
- After any change to `pages/`, run these in order and commit what they produce:
  1. `python3 tools/lint_pages.py`
  2. `python3 tools/cut_apart.py pages derived`
- Never point the output of `cut_apart.py` at a folder you care about. It wipes and rebuilds its output
  folder. It refuses unsafe targets, but do not rely on that.

## Handing off to the guidance repository

Pages are fixed at page level. A fix to a page is a full replacement of that wiki page, and the agent files
are re-cut from the pages and handed over again. Nobody edits a generated agent file.

1. Fix the page, then run the two commands above.
2. `python3 tools/emit_agent_tree.py --zip` (add `--update-lock` for new rules), then
   `python3 tools/run_target_validators.py`. Fix the pages until both pass.
3. Replace the wiki page, and hand `dist.zip` to the team that maintains the guidance repository (a zip or a commit).

## The Agent line

Each rule may carry one line that starts `Agent:`. It is the short form an agent is given: the rule in one
or two sentences that open with the situation they apply to, then a one-line reason when the reason is not
obvious. `Agent: none` leaves a rule out of the agent set on purpose.

**An Agent line never states a rule the page does not state.** It compresses the rule above it and takes its
reason from the Because line. Lint warns about rules that have none yet and fails on an empty or doubled one.
`cut_apart.py` removes the line from the neutral `derived/` rules and records it in `manifest.json`.

**An Agent line is about the change, never about who acts.** The pages speak to the author of a change, and the
agent is the go-between, so a line must not say the agent raises, asks, or tells anyone. Who must be consulted
lives in the page's `Second opinion:` line, and how the agent relays it lives in `agent/rules/db_usage_conventions.md`.
Every rule is a guideline that can be bent for a stated reason, and no line may suggest otherwise.

## Anatomy of a rule

- A rule is a heading, a tag line, the statement, then Because, Good and Bad, Second opinion, and Agent lines.
  The Index defines the tag line, Temperature, and Origin. Do not invent new values for them.
- A slug is unique and permanent. Never rename or delete one. To retire a rule, say so in the pull
  request, and a maintainer removes its names from `slugs.lock` in the same change.
- To add a rule: choose a slug that is distinct from every why key, story, and principle. Reuse an
  existing why key when its explanation already covers the rule. State the decision first and the reason
  as a Because line. Then run `python3 tools/lint_pages.py --update-lock`.

## Writing standards

- No em dashes. No singular first person in rules and stories. A collective "we" for Groups360 is fine.
- Stories are blameless and name no people, teams, services, or tables. Each serves a why key or principle.
- Test every SQL or Postgres claim on a real instance before it goes on a page, and say which versions.
- Keep editorial notes out of the pages. Put open questions and reasoning in the pull request. Lint
  warns on HTML comments other than the stage-one marker.

## The agent target

The agent files are built for the shared AI guidance repository for the Python services. Its validators
bind our output, and a rule or agent file that breaks them can be silently dropped.

- **Never write to the guidance repository.** It is a read-only git submodule at `vendor/ai_python_guidance`
  (after a fresh clone, `git submodule update --init`; the emitter does it when the folder is empty). Never commit
  inside it, and run its scripts only against a scratch copy. Do not copy its files into this repository.
- **Start with `agent/reference/README.md`.** It explains how the target loads files and what a file must
  look like. `agent/formats/` holds example agent files (two exist today) that pass the target's validators.
- **Prove every rule file and agent file** with the target's own validators before handing it over
  (`tools/run_target_validators.py` runs them on a scratch copy). A reading of the spec does not count.
- Copy an agent's fixed boilerplate from the target's `data_migration_agent.md`. Do not retype it.
- **Every concern file is scoped by `paths` only** (migrations and models), with no `whenPaths` or `when`.
  The target's hook loads a file whenever a `paths` glob matches, so a file cannot be both path-scoped and
  content-gated. Claude Code reads only `paths`, so a gated file with none loads in every session.
- **Err on the side of loading.** Every concern file loads on every migration and model edit. A rule that
  loads when it does not apply costs tokens. A rule that fails to load costs a standard nobody sees applied.
  Revisit only with suppression counts and spend numbers, never with a guessed list of trigger words.
- **Do not settle the Decisions in `NEXT_STEPS.md` step 2 that are still open yourself.** Ask the data architect.

## Keeping this file lean

A line earns a place here only if all three hold:

1. It is an instruction or a fact someone must act on. History does not count.
2. Forgetting it causes a mistake that nothing else would catch. CI, the pages, and the scripts count
   as catching it.
3. It cannot live closer to the thing, such as a rule's Because line, a script's docstring, or a lint
   check.

Stories, rationale, and "we considered X and declined" do not belong here. If a declined idea is
proposed a second time, pin it in a new section named Pins, with the reason.
