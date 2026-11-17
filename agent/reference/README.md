# How the target loads and checks files

Read this first, then the vendored files in the order below. `SOURCE.md` records where they came from.

## How a rule file reaches the model

1. A hook runs before every Read, Edit, or Write. It matches the file being touched against the frontmatter of
   every rule file in the target's `.claude/rules/`.
2. It injects an **index of links** to the matching rule files, and Claude Code expands each link into the
   **whole file**. Each rule file is injected at most once per session.
3. So the unit of cost is a whole concern file. The target's largest is 24 KB. Keep a concern file to one
   concern (`RRC5`) and a few KB.

## What a file must look like

- **Frontmatter.** `description` (one line, shortened to about 140 characters in the index), and `paths`, or
  `whenPaths` plus `when`. Each is a **bracketed list of quoted strings**. Block-style YAML lists are ignored.
  A glob cannot contain a quote.
- **Globs.** `<pkg>` stands for the service package and may be used only for paths inside it (`RRC19`).
  Root-anchored globs such as `migrations/**` stay literal.
- **Content gating.** A `when` entry is a regular expression matched against the change's content. It is
  taken as written, so a single backslash is a regex escape. The target's own files use plain substrings.
- **Rule lines.** `^R[A-Z]{2,6}\d+:` at the start of a line. One acronym per file. Codes are unique across
  files and stable once assigned.
- **Authoring rules.** `RRC1` through `RRC19` in `rule_conventions.md` bind every rule file.
- **Agent files.** `name` equals the filename with underscores replaced by hyphens, `tools` is read-only,
  `triggers` is required for a specialty agent, and `Read first` must list `suppression_conventions.md`.
  The `Guardrails`, `Suppression handling`, and `Output format` sections are fixed boilerplate. `RAGT1`
  through `RAGT17` in `agent_conventions.md` bind every agent file.

## Reading order

1. `target/rules/rule_conventions.md`, the rule authoring spec.
2. `target/rules/agent_conventions.md`, the agent authoring spec.
3. `target/rules/migration_conventions.md`, an exemplar rule file and the rules ours overlap with.
4. `target/agents/data_migration_agent.md`, an exemplar agent and the source of the boilerplate.
5. The header comment of `target/hooks/inject-rules.cjs`, for the loading behavior above.

## Checking your work

`python3 tools/run_target_validators.py <file...>` builds a scratch tree from these files plus your
candidates and runs the target's own validators on it. See `../formats/README.md` for what they catch.

## One thing to raise with the target's owner

The rule files also sit under the native `.claude/rules/` folder, so Claude Code may load them itself in
addition to the hook. Two of the target's files have no `paths` at all, which natively means they load every
session. This does not affect how we write files, but it affects how much context they cost.
