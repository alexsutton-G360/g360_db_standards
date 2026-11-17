# Next steps

From where this repository is now to rendering the corpus into the shared AI guidance repository.
Work the steps in order. Each says what done looks like. Decisions belong to the data architect, with the
owner of the AI guidance repository for anything that lands there and the DBA for the objects and tools page.

## Where things stand

- [x] The pages are drafted and reviewed (Index, Global Rules, Columns, Tables, Other objects and tools, Stock tables), plus the currency runbook.
- [x] `tools/lint_pages.py`, `tools/cut_apart.py`, CI, and `slugs.lock` are in place.
- [x] `derived/` holds a neutral per-rule set, a manifest, load hints, a rule index, and `AGENT_GUIDE.md`.
- [x] The target repository is known. It is an existing shared `.claude/` of 20 concern files, 16 review
  agents, and a rule-injection hook that links whole files. See "The agent target" in `CLAUDE.md`.

The key consequence: per-rule files are the wrong shape for that repository. It wants concern files with
numbered rule lines, and a review agent that owns them. The neutral `derived/rules/` set is an
intermediate, not the deliverable.

## 1. Foundation

- [x] Repository `CLAUDE.md` (what is editable, the handoff steps, the Agent line, rule anatomy, writing standards, the agent target, the bar for adding to it).
- [x] This file.
- [x] Loose agent-side files moved into `agent/reference/` and `agent/formats/examples/`, and the original `README.md` restored.
- [ ] Add `agent/control.toml` (grouping, codes, globs, gating) and put the hand-written agent definition in `agent/agents/`.
- [ ] Update `README.md` so its layout table and "derived set" section describe the target above.

Done when: a new contributor, or a fresh Claude session, can say what to edit, what is generated, and where agent-side material goes, from `CLAUDE.md` alone.

## 2. Decisions

Settle these before building. Each has a recommendation to react to.

Settled:

- [x] **Where the agent form lives.** One `Agent:` line per rule, on the page (see "The Agent line" in `CLAUDE.md`). No overlay folder and no hash check. A fix to a page is a re-cut and a re-handoff.
- [x] **What reaches the agent.** Every rule, unless it says `Agent: none`. Concern files are scoped by `paths` to migrations and models, with no content gating at all. The target's hook treats `paths` as unconditional, so a file cannot be both path-scoped and gated, and a file gated with `whenPaths` alone loads in every Claude Code session. Currency detection is therefore never needed. Revisit with suppression counts and spend numbers, not guesses. Tell the guidance team this is deliberate, since their RRC6 prefers narrow scopes.
- [x] **Delivery.** A zip or a commit handed to the team that maintains the guidance repository. This repository never writes to it. Their validators run on a scratch copy.
- [x] **Reuse.** Nothing is copied. Their repo is a read-only submodule at `vendor/ai_python_guidance`, pinned to a commit, and we reuse their validators and agent boilerplate from it.

- [x] **Guidelines, not laws.** Any rule can be bent for a stated reason, and the agent never grades the reason or writes it for the author. The agent relays advice to the author and never acts on a rule's "ask" or "tell" itself. Drafted in `agent/rules/db_usage_conventions.md` (code `RDBUS`), which passes the target's validators on a scratch copy.

- [x] **Rule code family.** Every code is `RDB` plus two letters for the concern file (`RDBCL`, `RDBCY`, and so on), then a number. The maintainer of the guidance repository agreed. The target has no `RDB` code today, and a duplicate code fails its `check-claude.mjs`. Keep our acronyms the same length, so none is a prefix of another, and state in the handoff note that `RDB*` is ours.

- [x] **Severity and recommendation.** Every finding is `discuss`, so nothing is ever rewritten without the author, and the review never stops the coding process. In the target nothing stops a commit anyway: `/review` only prints a verdict, and `/review-loop` auto-applies fixes only for non-`discuss` findings. Firmness shows in severity: Rule High, Default Medium, Judgment call Low. This is a dial: raise severity or use `fix-suggested` later if more intensity is wanted. Record it in the agent definition.

Open:

- [ ] **Codes are permanent in the wild.** Suppression markers in service code name a rule by code (for example `RDBCL1`), so `codes.lock` is essential and a code is never reused or renumbered.
- [ ] **See the reasons.** A scanner that reads a service checkout and lists every `claude-allow: RDB...` reason by rule, so the data architect can see which guidelines get bent and why. The target only warns its own rule-review agent when one rule passes 10 markers.
- [ ] **Concern files and their codes.** Group the 20 page groups into 8 to 10 concern files of 3 to 15 KB each, and choose the two letters after `RDB` for each. Their largest existing file is 24 KB, and a whole file loads at once. Proposed: naming (`RDBNM`), identifiers (`RDBID`), columns (`RDBCL`), currency (`RDBCY`), tables (`RDBTB`), relationships and indexes (`RDBRL`), other objects (`RDBOB`), and the usage file (`RDBUS`).
- [ ] **Agent.** A new database design agent that owns the family, beside the existing migration agent, which keeps migration mechanics. Recommended over extending the migration agent.
- [ ] **Origin.** Decide whether `house` and `general` appear in the rule line or stay wiki-only.
- [ ] **Numbering gaps.** The target's authoring rules are silent on whether a retired line may leave a gap. Ask, then record the answer.
- [ ] **Generated header.** Which header marks a generated file, so their review agents leave it alone.

Done when: each decision is written into the control file or `CLAUDE.md`, whichever it belongs in.

## 3. Reconcile with the existing data rules

The target already has rules that overlap ours. Go through them one at a time. The boundary: the pages
own what the schema should be, and the target's migration rules own how migrations are written.

- [ ] The rules on nullable new columns and on adding NOT NULL (`RMIG6`, `RMIG9`) against "not nullable by default". The pages replace them. First carry the deploy-safety content (Expand and Contract, a completed backfill, a staged deploy) into the Nullability section.
- [ ] The identity and UUID default rule (`RMIG4`) against the `id` and `guid` rules. Decide who owns it.
- [ ] The data seeder, which sets `created_at` in application code, against database-managed `created_at` and the `updated_at` trigger.
- [ ] DDL-to-model parity, since our column rules touch the same files. In the target it is a cross-layer check in `review.md`, and its migration agent file calls it `RMIG15`. In `migration_conventions.md`, `RMIG15` is "migrations must not import ORM models". Cite the real rule text in our co-owned table, and tell the target's owner about the mismatch in their agent file.

Done when: no rule in either place contradicts the other, and the target's owner has agreed to every replacement.

## 4. Build

- [x] (Built: `tools/emit_agent_tree.py`, `agent/control.toml`, `codes.lock`, `tools/run_target_validators.py`. Validators pass on a scratch copy.) An emitter in `tools/` that writes a `.claude/`-shaped tree into `dist/`: concern files with the target's frontmatter (`description`, `paths`, and `whenPaths` plus `when` only where a gate is justified), numbered rule lines built from the Agent lines and carrying the slug, and companions. Companions go under the target's `examples/`, never under `rules/`, because Claude Code loads everything under `rules/` that has no `paths`. Confirm the location with the target's owner.
- [ ] `codes.lock`, so a rule's number is assigned once and never reused.
- [ ] `tools/run_target_validators.py`: copies the target's `.claude/` to a scratch folder, overlays `dist/`, and runs its `check-claude.mjs` and `validate-rule.mjs` there. It never writes to the target. The path to the target comes from an argument or an environment variable.
- [ ] A self-match test: every `Good:` and `Bad:` example in a gated group must match that group's own `when` patterns, and the build fails if one does not.
- [ ] Sample migrations built from a few `Bad:` examples, to check that the agent flags them. This is the only way to see a silent miss.
- [ ] Decide whether the neutral per-rule set is retired. Keep `manifest.json` and `rule_index.md` either way.

Done when: one command regenerates `dist/`, and the target's validators pass on it in a scratch copy.

## 5. Author the agent side

This replaces the earlier plan to place trim markers in the pages.

- [x] An `Agent:` line on every rule (73 of 73), written for review of the wording. Each line opens with its trigger, and a rule that is a prohibition may open with the prohibition.
- [x] The database design agent definition in `agent/agents/`, with `triggers:` on migrations and models. Its boilerplate is copied from the target. Its co-owned rules table cites real rule text.
- [ ] Make companion lookups reliable and visible. In the agent definition, require reading the rule's companion before reporting a Judgment-call finding or a departure, and require the finding to name what the rule protects (the story slug). Put the companion path, not just the slug, on each bundle line. Then run trial reviews on sample migrations built from `Bad:` examples, and check the transcripts for those Reads before handoff. Ask the target's owner about a hook that logs Reads of companion files.
- [ ] Deferred: a Postgres type to SQLAlchemy mapping reference and Alembic examples. They are code, and the pages stay engine-neutral. If wanted later, the target's `examples/` folder is the home.

Done when: every rule has an Agent line or an explicit `none`, and a trial review of a sample migration cites slugs correctly.

## 6. Integrate

- [ ] Hand `dist/` to the guidance team as a zip or a commit. Do not write to their repository from here.
- [ ] Tell them that wider default loading is deliberate (see the settled decision on what reaches the agent), and that suppression counts are the signal for narrowing it.
- [ ] Teach that repository's own review agents that files with the generated header are edited here, not there.
- [ ] Raise one observation with its owner: the rules also sit under native `.claude/rules/`, so Claude Code may load them itself. Two files with no `paths` would load every session.

Done when: a service that links the guidance repository gets the database rules on a migration edit, and the review agents leave generated files alone.

## Alongside, not blocking

- [x] The DBA's review of `pages/other_objects.md` is treated as approval. His comments, when he is back, are practice for editing a page and re-running the handoff steps.
- [ ] A wiki publish step: render the pages to the wiki, turning each `(*rule: slug*)` citation into a link. The wiki target is undecided.
- [ ] Held stories: for each, either write it up anonymized into the pages or let it go.
- [ ] Fill in `.github/CODEOWNERS`, choose a license, and tag the first release.
- [ ] One Index sentence saying how to propose an edit (a pull request, or tell the data architect).
- [ ] The runbook's open edges: the "Not covered here" list and the Step 0 cases need confirming.
