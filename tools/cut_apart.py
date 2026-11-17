#!/usr/bin/env python3
"""
cut_apart.py: derive an agent-loadable file set from the Groups360 database standards wiki.

The wiki pages (pages/*.md) are the ONLY place anyone edits. Everything this script writes
is a derived artifact and is rebuilt from scratch on every run. Nothing here assumes a
particular agent repo format: it produces a neutral set that an adapter can map later.

Usage:  python3 tools/cut_apart.py [pages_dir] [out_dir]
        defaults: pages  derived        (run from the folder that holds pages/)

STAGE ONE IS SAFE BY DEFAULT. A rule with no cut point is injected in full. To trim a long rule,
put the marker  <!-- brisk-end -->  on its own line after the last paragraph an agent must see
first. Everything above the marker, plus the Good, Bad, Because and Second opinion lines, is stage
one. The rest goes to the companion. The marker is an HTML comment, so it never shows to a human.

Output (out_dir):
  rules/<slug>.md          stage one: the brisk rule an agent gets injected (frontmatter + statement
                           + Good/Bad + Because), with a pointer to its companion when there is more
  companions/<slug>.md     stage two: the full rule text, then the explanation behind it (siblings
                           that share its why key, and the stories and principles that serve it)
  stories/<slug>.md        stories, one per file
  principles/<slug>.md     the Index principles, one per file
  reference/<name>.md      reference material that is not a rule (the approved acronym tables)
  groups/<page>--<g>.md    the overview paragraph that opens a group (NOT in the load hints unless
                           listed in INTRO_IN_AI_SET below)
  AGENT_GUIDE.md           the entry point for an agent: what is here, what to load, how to treat a rule
  rule_index.md            one table of every rule slug, for cross-referencing
  manifest.json            every object with its metadata, links, and sizes
  loading.json             what to load when: always-load, by scope, by page, by group
  cut_report.md            counts, sizes, checks, and the rules whose brisk form may be lossy
"""
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---- decisions kept in one place, for the maintainers to change --------------------------------
RULE_PAGES = ["global_rules", "columns", "tables", "other_objects"]   # pages that hold rule chunks
ALWAYS_LOAD_SCOPES = {"global"}                    # global rules apply to every name
INTRO_IN_AI_SET = {                                # group intros that carry real content
    ("tables", "Tables that belong to one of several parents"),   # says its chunks are read in order
}
PAGES_KEPT_OUT_OF_AI_SET = {"stock_tables"}        # living document, undecided (not parsed here)
SCOPE_WHEN = {   # one line per scope: when an agent should load its rules
    "column": "the change adds, alters, or names a column",
    "table": "the change creates, alters, or names a table",
    "index": "the change adds or names an index",
    "constraint": "the change adds or names a key or a constraint",
    "database": "the change creates or names a database",
    "schema": "the change creates or names a schema",
    "trigger": "the change adds or names a trigger",
    "function": "the change adds or names a function",
    "procedure": "the change adds or names a stored procedure",
    "view": "the change adds or names a view",
    "materialized_view": "the change adds or names a materialized view",
    "role": "the change creates or names a role",
    "user": "the change creates or names a database user or service account",
}
BRISK_MARKER = "<!-- brisk-end -->"
SENTINEL = "\u0001"                                 # stands in for the marker while comments are stripped
UNMARKED_LONG_WORDS = 120                          # an unmarked rule longer than this is a trim candidate
# ----------------------------------------------------------------------------------------------

TAG = re.compile(
    r"^### ([^\n]+)\n\[Slug: ([a-z0-9-]+) · Temperature: (Rule|Default|Judgment call)"
    r" · Origin: (house|general) · Scope: ([a-z_]+) · Why: ([a-z0-9-]+)\]\n", re.M)
STORY_HEAD = re.compile(r"^### ([^\n]+)\n\*slug: ([a-z0-9-]+)(?: · serves: ([^*\n]+))?\*\n", re.M)
RULE_CITE = re.compile(r"\*rule: ([a-z0-9-]+)\*")
STORY_CITE = re.compile(r"\*story: ([a-z0-9-]+)\*|Story: `([a-z0-9-]+)`")
FENCE = re.compile(r"```.*?```", re.S)
LABELS = ("Because:", "Good:", "Bad:", "Second opinion:", "Story:", "Stories:", "Agent:")
AGENT_LINE = re.compile(r"^Agent:[ \t]*(.*)$", re.M)
AGENT_NONE = "none"                                 # "Agent: none" marks a rule left out of the agent set on purpose


def mask_fences(text):
    """Swap fenced code blocks for placeholders so '#' or '---' inside code never splits a chunk."""
    blocks = []
    def hold(m):
        blocks.append(m.group(0))
        return f"\u0000CODE{len(blocks) - 1}\u0000"
    return FENCE.sub(hold, text), blocks


def unmask(text, blocks):
    return re.sub(r"\u0000CODE(\d+)\u0000", lambda m: blocks[int(m.group(1))], text)


def words(s):
    return len(s.split())


def relink(s):
    """Pages sit one folder below the repo root and derived files two folders below, so a
    relative link such as ](../runbook/x.md) needs one more ../ in the derived copy."""
    return s.replace("](../", "](../../")


def clean_body(s):
    s = re.sub(r"\n-{3,}\s*\Z", "", s.strip()).strip()
    return s


def split_sections(masked):
    """Return [(group_name_or_None, text)] split on level-2 headings; the first item is the page opening."""
    parts = re.split(r"^## ", masked, flags=re.M)
    out = [(None, parts[0])]
    for p in parts[1:]:
        head, _, body = p.partition("\n")
        out.append((head.strip(), body))
    return out


def chunks(body):
    """Split a section body into [(kind, heading_match_or_None, text)] by its ### headings."""
    pos = [m.start() for m in re.finditer(r"^### ", body, flags=re.M)]
    if not pos:
        return [("intro", None, body)]
    out = [("intro", None, body[:pos[0]])]
    for i, s in enumerate(pos):
        e = pos[i + 1] if i + 1 < len(pos) else len(body)
        out.append(("chunk", None, body[s:e]))
    return out


def take_agent(full):
    """Pull the one-line "Agent:" form out of a rule body. Returns (agent_or_None, body_without_it).
    The line is for the agent-side build only, so it never reaches the neutral derived rule text.
    agent is None when the rule has no Agent line; AGENT_NONE when the rule is left out on purpose."""
    m = AGENT_LINE.search(full)
    if not m:
        return None, full
    rest = (full[:m.start()] + full[m.end():]).replace("\n\n\n", "\n\n")
    return m.group(1).strip(), clean_body(rest)


def brisk_form(body):
    """Return (brisk_text, full_text, has_marker). With no marker, stage one is the full text."""
    if SENTINEL not in body:
        return body, body, False
    before, after = body.split(SENTINEL, 1)
    full = (before.rstrip() + "\n\n" + after.lstrip()).strip()
    brisk = before.strip()
    seen = set(brisk.split("\n"))
    tail = [l for l in after.split("\n")
            if l.startswith(("Good:", "Bad:", "Because:", "Second opinion:")) and l not in seen]
    if tail:
        brisk += "\n\n" + "\n".join(tail)
    return brisk, full, True


def yaml_list(items):
    return "[" + ", ".join(f'"{x}"' for x in items) + "]"


def parse_page(name, text):
    text = text.replace(BRISK_MARKER, SENTINEL)
    masked, blocks = mask_fences(re.sub(r"<!--.*?-->", "", text, flags=re.S))
    rules, intros, refs, stories, principles = [], [], [], [], []
    for group, body in split_sections(masked):
        if group is None:
            # the page opening: the H1, a lead-in, and (on Global Rules) the rule chunks themselves
            h1, _, rest = body.partition("\n")
            pieces = chunks(rest)
            lead = unmask(clean_body(re.sub(r"\n-{3,}", "", pieces[0][2])), blocks)
            if lead:
                intros.append(dict(page=name, group="(page opening)", text=lead))
            page_group = h1.replace("#", "").strip() or name
            for _, _, seg in pieces[1:]:
                m = TAG.match(seg)
                if m:
                    full = unmask(clean_body(seg[m.end():]), blocks)
                    agent, full = take_agent(full)
                    brisk, full, marked = brisk_form(full)
                    second = next((l[len("Second opinion:"):].strip() for l in full.split("\n")
                                   if l.startswith("Second opinion:")), None)
                    rules.append(dict(page=name, group=page_group, title=m.group(1), slug=m.group(2),
                                      temperature=m.group(3), origin=m.group(4), scope=m.group(5),
                                      why=m.group(6), full=full, brisk=brisk, marked=marked,
                                      second_opinion=second, agent=agent))
            continue
        if group == "Stories":
            for m in STORY_HEAD.finditer(body):
                end = body.find("\n### ", m.end())
                seg = body[m.end(): end if end != -1 else len(body)]
                serves = [s.strip() for s in (m.group(3) or "").split(",") if s.strip()]
                stories.append(dict(page=name, title=m.group(1), slug=m.group(2), serves=serves,
                                    text=unmask(clean_body(seg), blocks)))
            continue
        if group == "Principles":
            for m in STORY_HEAD.finditer(body):
                end = body.find("\n### ", m.end())
                seg = body[m.end(): end if end != -1 else len(body)]
                principles.append(dict(page=name, title=m.group(1), slug=m.group(2),
                                       text=unmask(clean_body(seg), blocks)))
            continue
        pieces = chunks(body)
        intro_text = unmask(clean_body(re.sub(r"\n-{3,}", "", pieces[0][2])), blocks)
        if intro_text:
            intros.append(dict(page=name, group=group, text=intro_text))
        for _, _, seg in pieces[1:]:
            m = TAG.match(seg)
            if m:
                full = unmask(clean_body(seg[m.end():]), blocks)
                agent, full = take_agent(full)
                brisk, full, marked = brisk_form(full)
                second = next((l[len("Second opinion:"):].strip() for l in full.split("\n")
                               if l.startswith("Second opinion:")), None)
                rules.append(dict(page=name, group=group, title=m.group(1), slug=m.group(2),
                                  temperature=m.group(3), origin=m.group(4), scope=m.group(5),
                                  why=m.group(6), full=full, brisk=brisk, marked=marked,
                                  second_opinion=second, agent=agent))
            else:
                head, _, rest = seg.partition("\n")
                refs.append(dict(page=name, group=group, title=head.replace("### ", "").strip(),
                                 text=unmask(clean_body(rest), blocks)))
    return rules, intros, refs, stories, principles


def index_section(text, heading, level):
    """Return the body of a heading in the Index, comments removed, or None if the heading is gone."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    m = re.search(rf"^{'#' * level} {re.escape(heading)}\n(.*?)(?=^#{{1,{level}}} |\Z)", text, flags=re.S | re.M)
    return m.group(1).strip() if m else None


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    pages_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "pages")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "derived")
    # The output folder is wiped and rebuilt on every run, so refuse to wipe anything that is not
    # clearly a previous output of this script: never the pages folder, a folder that contains it
    # (such as the repository root), the current folder, or any non-empty folder with no manifest.json.
    out_r, pages_r = out.resolve(), pages_dir.resolve()
    unsafe = (out_r == pages_r or out_r in pages_r.parents or pages_r in out_r.parents
              or out_r == Path.cwd().resolve() or out_r == Path(out_r.anchor))
    if out.exists() and not unsafe:
        unsafe = any(out.iterdir()) and not (out / "manifest.json").exists()
    if unsafe:
        sys.exit(f"Refusing to use '{out}' as the output folder: it would be wiped on every run, and it is "
                 f"not an empty folder or a previous output of this script. Use a path such as 'derived'.")
    if out.exists():
        shutil.rmtree(out)
    for d in ("rules", "companions", "stories", "principles", "reference", "groups"):
        (out / d).mkdir(parents=True)

    rules, intros, refs, stories, principles = [], [], [], [], []
    for name in RULE_PAGES:
        r, i, f, s, p = parse_page(name, (pages_dir / f"{name}.md").read_text())
        rules += r; intros += i; refs += f; stories += s; principles += p
    # the Index holds principles and the stories that serve them
    _, _, _, s, p = parse_page("index", (pages_dir / "index.md").read_text())
    stories += s; principles += p

    problems = []
    slugs = [r["slug"] for r in rules]
    for d in [k for k, v in Counter(slugs).items() if v > 1]:
        problems.append(f"duplicate rule slug: {d}")
    why_keys = {r["why"] for r in rules}
    by_why = defaultdict(list)
    for r in rules:
        by_why[r["why"]].append(r)
    story_by_slug = {s["slug"]: s for s in stories}
    prin_by_slug = {p["slug"]: p for p in principles}
    for k in set(slugs) & (why_keys | set(story_by_slug) | set(prin_by_slug)):
        problems.append(f"rule slug collides with a why key, story or principle: {k}")

    serves_by_key = defaultdict(list)
    for s in stories:
        for t in s["serves"]:
            serves_by_key[t].append(s)
            if t not in why_keys and t not in prin_by_slug:
                problems.append(f"story {s['slug']} serves '{t}', which is not a why key or principle")

    # ---- write rules and companions ----
    for r in rules:
        cites_rules = sorted(set(RULE_CITE.findall(r["full"])))
        cites_stories = sorted({a or b for a, b in STORY_CITE.findall(r["full"])})
        for c in cites_rules:
            if c not in slugs:
                problems.append(f"{r['slug']} cites unknown rule {c}")
        for c in cites_stories:
            if c not in story_by_slug:
                problems.append(f"{r['slug']} cites unknown story {c}")
        r["cites_rules"], r["cites_stories"] = cites_rules, cites_stories
        siblings = [x for x in by_why[r["why"]] if x["slug"] != r["slug"]]
        stories_for = list(serves_by_key.get(r["why"], []))
        for c in cites_stories:
            if story_by_slug.get(c) and story_by_slug[c] not in stories_for:
                stories_for.append(story_by_slug[c])
        r["stories"] = [s["slug"] for s in stories_for]
        has_more = r["brisk"].strip() != r["full"].strip() or bool(stories_for)
        r["has_companion"] = has_more

        fm = ["---", f'slug: "{r["slug"]}"', f'title: "{r["title"]}"',
              f'temperature: "{r["temperature"]}"', f'origin: "{r["origin"]}"',
              f'scope: "{r["scope"]}"', f'why: "{r["why"]}"', f'page: "{r["page"]}"',
              f'group: "{r["group"]}"']
        if r["second_opinion"]:
            fm.append(f'second_opinion: "{r["second_opinion"]}"')
        fm.append(f"companion: {'true' if has_more else 'false'}")
        fm.append("---")
        brisk = "\n".join(fm) + f"\n\n# {r['title']}\n\n{relink(r['brisk'])}\n"
        if has_more:
            brisk += f"\nMore: companions/{r['slug']}.md\n"
        (out / "rules" / f"{r['slug']}.md").write_text(brisk)

        comp = ["---", f'slug: "{r["slug"]}"', f'why: "{r["why"]}"', "---", "",
                f"# {r['title']}", "", "## Full rule", "", relink(r["full"]), ""]
        if siblings or stories_for:
            comp += ["## Why this rule exists", ""]
            if siblings:
                comp += [f"Rules that share this explanation (why: `{r['why']}`):", ""]
                comp += [f"- `{x['slug']}`: {x['title']}" for x in siblings] + [""]
            for s in stories_for:
                comp += [f"### Story: {s['title']}", "", relink(s["text"]), ""]
        if has_more:
            (out / "companions" / f"{r['slug']}.md").write_text("\n".join(comp))

    for s in stories:
        (out / "stories" / f"{s['slug']}.md").write_text(
            f'---\nslug: "{s["slug"]}"\ntitle: "{s["title"]}"\nserves: {yaml_list(s["serves"])}\npage: "{s["page"]}"\n---\n\n# {s["title"]}\n\n{relink(s["text"])}\n')
    for p in principles:
        (out / "principles" / f"{p['slug']}.md").write_text(
            f'---\nslug: "{p["slug"]}"\ntitle: "{p["title"]}"\n---\n\n# {p["title"]}\n\n{relink(p["text"])}\n')

    # ---- reference blocks (the approved acronym tables) ----
    ref_files = []
    acr_intro = next((i for i in intros if i["page"] == "global_rules" and i["group"] == "Approved acronyms"), None)
    acr = [r for r in refs if r["page"] == "global_rules"]
    if acr:
        body = "# Approved acronyms\n\n" + (acr_intro["text"] + "\n\n" if acr_intro else "")
        for r in acr:
            body += f"## {r['title']}\n\n{r['text']}\n\n"
        (out / "reference" / "approved-acronyms.md").write_text(body)
        ref_files.append("reference/approved-acronyms.md")

    # ---- group intros ----
    intro_files = []
    for i in intros:
        if i["group"] in ("(page opening)",) or (i["page"], i["group"]) == ("global_rules", "Approved acronyms"):
            continue
        fn = f"groups/{i['page']}--{slugify(i['group'])}.md"
        (out / fn).write_text(f'---\npage: "{i["page"]}"\ngroup: "{i["group"]}"\nkind: "group-intro"\n'
                              f'in_load_hints: {"true" if (i["page"], i["group"]) in INTRO_IN_AI_SET else "false"}\n---\n\n'
                              f'# {i["group"]}\n\n{i["text"]}\n')
        i["file"] = fn
        intro_files.append(i)

    # ---- rule index: one table of every slug, for people who are cross-referencing ----
    idx = ["# Rule index", "",
           f"{len(rules)} rules. A slug points at exactly one rule and never changes. Generated by tools/cut_apart.py, do not edit.", ""]
    for n in RULE_PAGES:
        idx += [f"## {n}", "", "| slug | rule | temperature | origin | scope | group |", "|---|---|---|---|---|---|"]
        for r in [r for r in rules if r["page"] == n]:
            idx.append(f"| `{r['slug']}` | {r['title']} | {r['temperature']} | {r['origin']} | {r['scope']} | {r['group']} |")
        idx.append("")
    (out / "rule_index.md").write_text("\n".join(idx))

    # ---- manifest and loading hints ----
    manifest = dict(
        generated_from="pages/*.md",
        counts=dict(rules=len(rules), stories=len(stories), principles=len(principles),
                    reference=len(ref_files), group_intros=len(intro_files)),
        rules=[{k: r[k] for k in ("slug", "title", "page", "group", "temperature", "origin", "scope",
                                  "why", "second_opinion", "cites_rules", "cites_stories", "stories",
                                  "has_companion")}
               | dict(words_full=words(r["full"]), words_brisk=words(r["brisk"]),
                      agent=r["agent"],
                      brisk_file=f"rules/{r['slug']}.md",
                      companion_file=f"companions/{r['slug']}.md" if r["has_companion"] else None)
               for r in rules],
        stories=[dict(slug=s["slug"], title=s["title"], serves=s["serves"], page=s["page"],
                      file=f"stories/{s['slug']}.md") for s in stories],
        principles=[dict(slug=p["slug"], title=p["title"], file=f"principles/{p['slug']}.md") for p in principles],
        why_keys={k: dict(rules=[x["slug"] for x in v], stories=[s["slug"] for s in serves_by_key.get(k, [])])
                  for k, v in sorted(by_why.items())},
    )
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    def rf(r): return f"rules/{r['slug']}.md"
    loading = dict(
        always=[rf(r) for r in rules if r["scope"] in ALWAYS_LOAD_SCOPES] + ref_files,
        by_scope={k: [rf(r) for r in rules if r["scope"] == k] for k in sorted({r["scope"] for r in rules})
                  if k not in ALWAYS_LOAD_SCOPES},
        by_page={n: [rf(r) for r in rules if r["page"] == n] for n in RULE_PAGES},
        by_group={f"{n}:{g}": [rf(r) for r in rules if r["page"] == n and r["group"] == g]
                  for n in RULE_PAGES for g in sorted({r["group"] for r in rules if r["page"] == n})},
        group_intros_in_ai_set=[i["file"] for i in intro_files if (i["page"], i["group"]) in INTRO_IN_AI_SET],
        left_out_of_ai_set=dict(pages=sorted(PAGES_KEPT_OUT_OF_AI_SET),
                                group_intros=[i["file"] for i in intro_files if (i["page"], i["group"]) not in INTRO_IN_AI_SET]),
    )
    (out / "loading.json").write_text(json.dumps(loading, indent=2))

    # ---- agent guide: hand-written orientation plus definitions copied verbatim from the Index ----
    index_text = (pages_dir / "index.md").read_text()
    pulled = {}
    for heading, level in (("Temperature: how firm the rule is", 3), ("Origin: what could overturn it", 3),
                           ("When you deviate", 3), ("These docs are meant to be edited", 2)):
        body = index_section(index_text, heading, level)
        if body is None:
            problems.append(f"the Index no longer has the heading '{heading}', which AGENT_GUIDE.md copies")
        pulled[heading] = relink(body or "")
    scope_rows = [f"| `{k}` | {len([r for r in rules if r['scope'] == k])} | {SCOPE_WHEN.get(k, 'the change touches a ' + k)} |"
                  for k in sorted({r["scope"] for r in rules}) if k not in ALWAYS_LOAD_SCOPES]
    guide = f"""# Groups360 database standards: guide for agents

Read this first. These are the Groups360 PostgreSQL database standards, cut into one file per rule so an
agent can load only what a change needs. This set is generated from the wiki pages. Do not edit it by hand.

## What is in this set

| Path | What it holds |
|---|---|
| `rules/<slug>.md` | One rule. This is what you are given first (stage one). |
| `companions/<slug>.md` | The full rule and the explanation behind it, including stories. Only some rules have one. |
| `loading.json` | What to load and when: always-load files, and rules grouped by scope, page and group. |
| `manifest.json` | Every rule, story and principle with its metadata and links. |
| `rule_index.md` | Every rule slug in one table. |
| `reference/approved-acronyms.md` | The approved short forms for names. Needed whenever you name something. |
| `stories/`, `principles/`, `groups/` | Explanation for people. You do not need them to apply a rule. |

## How to use it

1. **Always load** the files listed under `always` in `loading.json`: the global naming rules and the approved acronyms. They apply to every name.
2. **Then load by scope.** Load the rules whose scope matches each kind of object the change creates or alters. A change that touches several kinds of object loads each scope.

| scope | rules | load when |
|---|---|---|
{chr(10).join(scope_rows)}

3. **Each rule file stands alone.** Its frontmatter gives the slug, temperature, origin and scope, and the `why` key shared by related rules.
4. **If a rule is not enough, read its companion.** A rule file ends with `More: companions/<slug>.md` when there is more to read. Follow it when you are unsure how a rule applies, then decide again.
5. **Refer to a rule by its slug.** Write `rule: <slug>`. A slug points at exactly one rule and never changes.
6. **Temperature is not a severity score.** It says how much a deviation owes, as defined below.

## How to treat a rule

### Temperature: how firm the rule is

{pulled["Temperature: how firm the rule is"]}

### Origin: what could overturn it

{pulled["Origin: what could overturn it"]}

### When you deviate

{pulled["When you deviate"]}

## When a rule seems wrong

{pulled["These docs are meant to be edited"]}

## What is not in this set

- The Stock tables page is a living document and is not in this set yet.
- The currency runbook is separate from the standards and is not in this set.
- Rule files are currently given in full. Where a rule has a companion, the companion adds the story or explanation behind it.
- `cut_report.md` is for the people who maintain this set. You do not need it.
"""
    (out / "AGENT_GUIDE.md").write_text(guide)
    loading["guide"] = "AGENT_GUIDE.md"
    (out / "loading.json").write_text(json.dumps(loading, indent=2))

    # ---- report ----
    tf = sum(words(r["full"]) for r in rules)
    tb = sum(words(r["brisk"]) for r in rules)
    marked = [r for r in rules if r["marked"]]
    unmarked_long = sorted([r for r in rules if not r["marked"] and words(r["full"]) > UNMARKED_LONG_WORDS],
                           key=lambda r: -words(r["full"]))
    rep = ["# Cut-apart report", "",
           f"Rules: {len(rules)} | stories: {len(stories)} | principles: {len(principles)} | "
           f"reference files: {len(ref_files)} | group intros written: {len(intro_files)}", "",
           f"Words: full rule text {tf}, stage one {tb} ({round(100 * tb / tf)}% of full). "
           f"Rules with a cut point (<!-- brisk-end -->): {len(marked)} of {len(rules)}.", "",
           "## Words by scope (what loading that scope would inject)", "",
           "| scope | rules | stage one words | full words |", "|---|---|---|---|"]
    for k in sorted({r["scope"] for r in rules}):
        rs = [r for r in rules if r["scope"] == k]
        rep.append(f"| {k} | {len(rs)} | {sum(words(r['brisk']) for r in rs)} | {sum(words(r['full']) for r in rs)} |")
    rep += ["", "## Checks", ""]
    rep += [f"- PROBLEM: {p}" for p in problems] or ["- no problems: slugs unique and distinct from why keys, stories and principles; every citation and every story target resolves"]
    rep += ["", f"## Trim candidates: unmarked rules over {UNMARKED_LONG_WORDS} words ({len(unmarked_long)})", "",
            "These are injected in full until someone places a cut point. Each one needs a judgment about where",
            "the statement ends and the elaboration begins.", ""]
    rep += [f"- `{r['slug']}` ({words(r['full'])} words)" for r in unmarked_long]
    rep += ["", "## Group intros", ""]
    for i in intros:
        if i["group"] == "(page opening)":
            continue
        inset = (i["page"], i["group"]) in INTRO_IN_AI_SET
        rep.append(f"- {i['page']}: {i['group']} ({words(i['text'])} words): {'IN the load hints' if inset else 'written out, not in the load hints'}")
    rep += ["", "## Decisions in this script (top of cut_apart.py)", "",
            f"- always-load scopes: {sorted(ALWAYS_LOAD_SCOPES)}",
            f"- group intros in the AI set: {sorted(INTRO_IN_AI_SET)}",
            f"- pages kept out of the AI set: {sorted(PAGES_KEPT_OUT_OF_AI_SET)}"]
    (out / "cut_report.md").write_text("\n".join(rep) + "\n")

    print(f"rules {len(rules)} | stories {len(stories)} | principles {len(principles)} | "
          f"reference {len(ref_files)} | intros {len(intro_files)} | problems {len(problems)}")
    for p in problems:
        print("  PROBLEM:", p)


if __name__ == "__main__":
    main()
