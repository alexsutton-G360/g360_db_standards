#!/usr/bin/env python3
"""
lint_pages.py: check the wiki pages before they are merged.

Usage:  python3 tools/lint_pages.py [--update-lock]
        run from the repository root. Exit code 1 if any ERROR is found.

ERRORS (fail the check)
  - a rule chunk without a valid tag line, or with an unknown scope
  - a duplicate rule slug, or a slug that collides with a why key, story or principle
  - a (*rule: x*) or (*story: x*) citation that points at nothing
  - a story that serves a key that does not exist
  - a slug, why key, story or principle listed in slugs.lock that has disappeared
  - an em dash or en dash anywhere in page text
  - a relative markdown link that points at a file that is not there
  - a rule with more than one Agent: line, or an empty one

WARNINGS (reported, do not fail)
  - rules with no Agent: line yet (one summary line), and an Agent: line over 600 characters
  - singular first person (I, my, me) in rule or story text. The Index may quote the reader.
  - an HTML comment other than the stage-one marker. Editorial notes belong in pull requests.
  - a slug or why key that is new and not yet in slugs.lock

slugs.lock records every stable name. Names in it may never be removed or renamed, because other
rules, stories and outside documents point at them. --update-lock adds new names to it and never
removes any.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cut_apart as ca  # noqa: E402

ROOT = Path(".")
PAGES = ROOT / "pages"
LOCK = ROOT / "slugs.lock"
SCOPES = {"global", "column", "table", "database", "schema", "constraint", "index", "trigger",
          "function", "procedure", "view", "materialized_view", "role", "user"}
AGENT_MAX_CHARS = 600
TEXT_FILES =sorted(PAGES.glob("*.md")) + sorted((ROOT / "runbook").glob("*.md"))

errors, warnings = [], []


def vis(t):
    return re.sub(r"<!--.*?-->", "", t, flags=re.S)


def main():
    update = "--update-lock" in sys.argv
    rules, stories, principles, refs = [], [], [], []
    for name in ca.RULE_PAGES:
        r, _, f, s, p = ca.parse_page(name, (PAGES / f"{name}.md").read_text())
        rules += r; refs += [(name, x) for x in f]; stories += s; principles += p
    _, _, _, s, p = ca.parse_page("index", (PAGES / "index.md").read_text())
    stories += s; principles += p

    # chunks that are neither rules nor stories nor the acronym tables
    for name, f in refs:
        if name != "global_rules":
            errors.append(f"{name}: heading '{f['title']}' is not a rule (no valid tag line) and not a story")

    slugs = [r["slug"] for r in rules]
    why_keys = {r["why"] for r in rules}
    story_slugs = {s["slug"] for s in stories}
    prin_slugs = {p["slug"] for p in principles}
    for r in rules:
        if r["scope"] not in SCOPES:
            errors.append(f"{r['slug']}: unknown scope '{r['scope']}'")
    for d in sorted({s for s in slugs if slugs.count(s) > 1}):
        errors.append(f"duplicate rule slug: {d}")
    for k in sorted(set(slugs) & (why_keys | story_slugs | prin_slugs)):
        errors.append(f"rule slug collides with a why key, story or principle: {k}")
    for r in rules:
        for c in ca.RULE_CITE.findall(r["full"]):
            if c not in slugs:
                errors.append(f"{r['slug']} cites unknown rule '{c}'")
        for a, b in ca.STORY_CITE.findall(r["full"]):
            if (a or b) not in story_slugs:
                errors.append(f"{r['slug']} cites unknown story '{a or b}'")
    for s in stories:
        for t in s["serves"]:
            if t not in why_keys and t not in prin_slugs:
                errors.append(f"story {s['slug']} serves '{t}', which is not a why key or principle")

    # Agent lines: the one-sentence form an agent is given. "Agent: none" leaves a rule out on purpose.
    for r in rules:
        if ca.AGENT_LINE.search(r["full"]):
            errors.append(f"{r['slug']}: more than one Agent: line")
        a = r["agent"]
        if a is not None and not a:
            errors.append(f"{r['slug']}: empty Agent: line (write the rule, or 'Agent: none')")
        elif a and a != ca.AGENT_NONE and len(a) > AGENT_MAX_CHARS:
            warnings.append(f"{r['slug']}: Agent: line is {len(a)} characters (over {AGENT_MAX_CHARS}); the agent form should be short")
    missing = [r["slug"] for r in rules if r["agent"] is None]
    if missing:
        warnings.append(f"{len(missing)} of {len(rules)} rules have no Agent: line yet "
                        f"(add one, or 'Agent: none' to leave a rule out on purpose)")

    # slug lock
    current = dict(rule_slugs=sorted(slugs), why_keys=sorted(why_keys),
                   story_slugs=sorted(story_slugs), principle_slugs=sorted(prin_slugs))
    locked = json.loads(LOCK.read_text()) if LOCK.exists() else {k: [] for k in current}
    for kind, names in locked.items():
        for n in names:
            if n not in current.get(kind, []):
                errors.append(f"slugs.lock: {kind[:-1].replace('_', ' ')} '{n}' has disappeared. Stable names are never removed or renamed.")
    for kind, names in current.items():
        for n in names:
            if n not in locked.get(kind, []) and not update:
                warnings.append(f"new {kind[:-1].replace('_', ' ')} '{n}' is not in slugs.lock yet (run with --update-lock)")
    if update:
        merged = {k: sorted(set(locked.get(k, [])) | set(v)) for k, v in current.items()}
        LOCK.write_text(json.dumps(merged, indent=2) + "\n")
        print(f"slugs.lock updated: " + ", ".join(f"{len(v)} {k}" for k, v in merged.items()))

    # text checks
    for f in TEXT_FILES:
        raw = f.read_text()
        t = vis(raw)
        for ch, nm in (("\u2014", "em dash"), ("\u2013", "en dash")):
            if ch in t:
                errors.append(f"{f}: contains an {nm}")
        for c in re.findall(r"<!--(.*?)-->", raw, flags=re.S):
            if c.strip() != "brisk-end":
                warnings.append(f"{f}: editorial HTML comment: {c.strip()[:60]!r}")
        for m in re.finditer(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", t):
            target = m.group(1)
            if "://" in target or target.startswith("mailto:"):
                continue
            if not (f.parent / target).resolve().exists():
                errors.append(f"{f}: broken relative link '{target}'")
        if f.name != "index.md":
            body = re.sub(r"```.*?```", "", t, flags=re.S)
            for i, line in enumerate(body.split("\n"), 1):
                if re.search(r"\b(I|I'm|I've|I'd|my|me|mine|myself)\b", line):
                    warnings.append(f"{f}: singular first person: {line.strip()[:60]!r}")

    print(f"{len(rules)} rules, {len(stories)} stories, {len(principles)} principles checked")
    for w in warnings:
        print("  WARNING:", w)
    for e in errors:
        print("  ERROR:", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
