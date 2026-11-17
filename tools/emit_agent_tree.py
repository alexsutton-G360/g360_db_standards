#!/usr/bin/env python3
"""
emit_agent_tree.py: build the handoff tree for the AI guidance repository from the wiki pages.

Usage:  python3 tools/emit_agent_tree.py [--update-lock] [--no-agent] [--out DIR]
        run from the repository root. Needs Python 3.11+ (or `pip install tomli`).

What it reads
  pages/*.md            the rules, each with an Agent: line (see CLAUDE.md, "The Agent line")
  agent/control.toml    how rules are bundled, what each bundle is called, where companions go
  agent/rules/          the hand-written usage rule file, copied as is
  agent/agents/         the agent template, filled in here
  codes.lock            rule code -> slug. A code is assigned once and never reused.
  vendor/ai_python_guidance   a read-only git submodule of the guidance repository. Its data_migration_agent.md
                        supplies the fixed agent sections (Guardrails, Suppression handling, Output format)
                        word for word. Initialized automatically when empty. The commit is recorded in
                        dist/.generated. Nobody commits inside it.

What it writes (default dist/, wiped and rebuilt every run)
  dist/.claude/rules/db_*_conventions.md   one bundle per concern, numbered rule lines, `paths` only
  dist/.claude/rules/db_usage_conventions.md
  dist/.claude/examples/db_standards/      one companion per rule (the full rule and its stories)
                                           plus approved-acronyms.md
  dist/.claude/agents/database_design_agent.md
  dist/HANDOFF.md                          what to tell the team that maintains the guidance repository
  dist/.generated                          marks the folder as safe to wipe

It never writes to the guidance repository. Prove the result with tools/run_target_validators.py.

A rule line is: CODE: <Agent line> [Second opinion: X.] [Temperature; slug: s; full rule: path]
A rule with `Agent: none` is left out. A rule with no Agent line stops the build.
Adding a rule needs `--update-lock`, which only adds codes and never removes one.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 and older
    import tomli as tomllib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import cut_apart as ca  # noqa: E402

RULE_LINE = re.compile(r"^R[A-Z]{2,6}\d+:")
FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
LOCAL_LINK = re.compile(r"\[([^\]]*)\]\((?:\.\./)+[^)]*\)")
GENERATED_MARK = ".generated"
PLACEHOLDERS = ("READ_FIRST", "GUARDRAILS", "SUPPRESSION", "SECTIONS", "OUTPUT_FORMAT")


def die(msg):
    sys.exit(f"emit_agent_tree: {msg}")


def sentence(s):
    s = s.strip()
    return s if s.endswith((".", "!", "?")) else s + "."


# ---- reading --------------------------------------------------------------------------------

def load_control(path):
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    for key in ("output", "loading", "agent", "bundle"):
        if key not in cfg:
            die(f"{path} has no [{key}] section")
    acronyms = [b["acronym"] for b in cfg["bundle"]]
    files = [b["file"] for b in cfg["bundle"]]
    if len(set(acronyms)) != len(acronyms) or len(set(files)) != len(files):
        die("control file: two bundles share an acronym or a file name")
    for a in acronyms:
        if not re.fullmatch(r"R[A-Z]{2,6}", a):
            die(f"acronym {a} must match R plus 2 to 6 capital letters")
        for o in acronyms:
            if a != o and o.startswith(a):
                die(f"acronym {a} is a prefix of {o}; the target's check-claude.mjs would blur them")
    return cfg


def load_rules(pages_dir):
    rules = []
    for name in ca.RULE_PAGES:
        r = ca.parse_page(name, (pages_dir / f"{name}.md").read_text())[0]
        rules += r
    return rules


def bundle_rules(rules, bundles):
    """Return {acronym: [rules]} in bundle order, checking that every group is placed exactly once."""
    where = {}
    for b in bundles:
        for page, group in b["groups"]:
            if (page, group) in where:
                die(f"group {page}: {group} is listed in two bundles")
            where[(page, group)] = b["acronym"]
    present = {(r["page"], r["group"]) for r in rules}
    for key in sorted(present - set(where)):
        die(f"no bundle takes the group {key[0]}: {key[1]}")
    for key in sorted(set(where) - present):
        die(f"control file lists the group {key[0]}: {key[1]}, which has no rules on the pages")
    for r in rules:
        if r["agent"] is None:
            die(f"rule {r['slug']} has no Agent: line (add one, or 'Agent: none')")
    out = {}
    for b in bundles:
        picked = []
        for page, group in b["groups"]:
            picked += [r for r in rules if (r["page"], r["group"]) == (page, group) and r["agent"] != ca.AGENT_NONE]
        out[b["acronym"]] = picked
    skipped = [r["slug"] for r in rules if r["agent"] == ca.AGENT_NONE]
    return out, skipped


# ---- codes ----------------------------------------------------------------------------------

def load_lock(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return dict(data.get("codes", {}))


def assign_codes(bundled, lock, update):
    slug_to_code = {s: c for c, s in lock.items()}
    new = {}
    for acr, rs in bundled.items():
        pat = re.compile(re.escape(acr) + r"(\d+)")
        used = [int(m.group(1)) for c in lock if (m := pat.fullmatch(c))]
        nxt = max(used, default=0) + 1
        for r in rs:
            code = slug_to_code.get(r["slug"])
            if code is None:
                code = f"{acr}{nxt}"
                nxt += 1
                new[code] = r["slug"]
                slug_to_code[r["slug"]] = code
            elif not pat.fullmatch(code):
                die(f"{r['slug']} holds the code {code} but now sits in the {acr} bundle. Moving a rule "
                    f"between bundles needs a decision about its old code, which may be in use in service code.")
    if new and not update:
        die(f"{len(new)} rule(s) have no code in codes.lock yet; run with --update-lock to assign them")
    live = {r["slug"] for rs in bundled.values() for r in rs}
    reserved = {c: s for c, s in lock.items() if s not in live}
    return slug_to_code, new, reserved


def write_lock(path, lock, new):
    merged = {**lock, **new}
    def key(c):
        m = re.fullmatch(r"([A-Z]+)(\d+)", c)
        return (m.group(1), int(m.group(2)))
    ordered = {c: merged[c] for c in sorted(merged, key=key)}
    path.write_text(json.dumps({"version": 1, "codes": ordered}, indent=2) + "\n")


# ---- rendering ------------------------------------------------------------------------------

def companion_text(r, code, bundle_file, tmp):
    slug = r["slug"]
    comp = tmp / "companions" / f"{slug}.md"
    rule = tmp / "rules" / f"{slug}.md"
    has = comp.exists()
    body = FRONT.sub("", (comp if has else rule).read_text(), count=1).strip()
    head, _, rest = body.partition("\n\n")
    if not has:
        rest = re.sub(r"\n+More: companions/[^\n]*\s*$", "", rest).strip()
        rest = "## Full rule\n\n" + rest
    meta = f"Rule line `{code}` in `{bundle_file}`. Temperature: {r['temperature']}. Origin: {r['origin']}."
    if r["second_opinion"]:
        meta += f" Second opinion: {sentence(r['second_opinion'])}"
    text = f"{head}\n\n{meta}\n\n{rest}\n"
    return LOCAL_LINK.sub(r"\1", text)


def render_bundle(b, rules, codes, cfg):
    comp_dir = cfg["output"]["companions_dir"]
    notice = cfg["output"]["generated_notice"]
    lines = ["---", f"description: {b['description']}",
             f"paths: {json.dumps(cfg['loading']['paths'])}", "---", "",
             f"All {b['title'].lower()} rules are enumerated using the {b['acronym']} ({b['meaning']}) code.", "",
             f"> {notice}", ""]
    if b.get("note"):
        lines += [b["note"], ""]
    seen_groups = []
    for r in rules:
        if r["group"] not in seen_groups:
            seen_groups.append(r["group"])
            lines += [f"## {r['group']}", ""]
        so = f" Second opinion: {sentence(r['second_opinion'])}" if r["second_opinion"] else ""
        tail = f"[{r['temperature']}; slug: {r['slug']}; full rule: {comp_dir}/{r['slug']}.md]"
        line = f"{codes[r['slug']]}: {sentence(r['agent'])}{so} {tail}"
        if "\n" in line or not RULE_LINE.match(line):
            die(f"bad rule line for {r['slug']}")
        lines += [line, ""]
    return "\n".join(lines).rstrip() + "\n"


def sections_of(text):
    """Split markdown on level-2 headings, ignoring anything inside a fenced block."""
    out, cur, buf, fence = {}, None, [], None
    for line in text.split("\n"):
        m = re.match(r"(`{3,}|~{3,})", line)
        if m:
            tick = m.group(1)
            if fence is None:
                fence = tick
            elif tick[0] == fence[0] and len(tick) >= len(fence) and line.strip() == tick:
                fence = None
        if fence is None and line.startswith("## "):
            if cur:
                out[cur] = "\n".join(buf).rstrip() + "\n"
            cur, buf = line[3:].strip(), [line]
        else:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).rstrip() + "\n"
    return out


SUBMODULE = ROOT / "vendor" / "ai_python_guidance"


def guidance_checkout():
    """Return (folder, commit) of the read-only guidance submodule, initializing it when it is empty."""
    if not (SUBMODULE / ".claude").is_dir():
        print("vendor/ai_python_guidance is empty; running: git submodule update --init vendor/ai_python_guidance")
        r = subprocess.run(["git", "-C", str(ROOT), "submodule", "update", "--init", "vendor/ai_python_guidance"],
                           capture_output=True, text=True)
        if r.returncode != 0 or not (SUBMODULE / ".claude").is_dir():
            die("could not initialize the guidance submodule. Check your git access to the Groups360 "
                "ai_python_guidance repository, then run: git submodule update --init\n" + r.stderr.strip())
    sha = subprocess.run(["git", "-C", str(SUBMODULE), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    return SUBMODULE, sha


def render_agent(cfg, bundled, codes, target):
    template = (ROOT / cfg["agent"]["template"]).read_text()
    exemplar_path = target / cfg["agent"]["boilerplate_from"]
    if not exemplar_path.exists():
        die(f"{exemplar_path} not found; run: git submodule update --init")
    secs = sections_of(exemplar_path.read_text())
    for name in ("Guardrails", "Suppression handling", "Output format"):
        if name not in secs:
            die(f"the target's {exemplar_path.name} has no '## {name}' section; its layout changed")
    bundles = cfg["bundle"]
    read_first = [f"- `.claude/rules/{b['file']}`" for b in bundles]
    read_first.append(f"- `.claude/rules/{Path(cfg['agent']['usage_rules']).name}`")
    read_first.append("- `.claude/rules/suppression_conventions.md`")
    read_first += ["", "If a rule's reasoning is not enough to judge a boundary case, follow the path at the end of its "
                       "line to the companion for that rule before deciding."]
    sections = []
    for b in bundles:
        rs = bundled[b["acronym"]]
        if not rs:
            continue
        block = [f"## {b['title']}", "", b["skip"], ""]
        for r in rs:
            extra = ", Judgment call" if r["temperature"] == "Judgment call" else ""
            block.append(f"- [ ] {r['title']} ({codes[r['slug']]}{extra})")
        sections.append("\n".join(block))
    fill = {"READ_FIRST": "\n".join(read_first), "GUARDRAILS": secs["Guardrails"].rstrip(),
            "SUPPRESSION": secs["Suppression handling"].rstrip(), "SECTIONS": "\n\n".join(sections),
            "OUTPUT_FORMAT": secs["Output format"].rstrip()}
    for k in PLACEHOLDERS:
        template = template.replace("{{" + k + "}}", fill[k])
    if "{{" in template:
        die("the agent template still has an unfilled {{placeholder}}")
    return template.rstrip() + "\n"


def render_handoff(cfg, bundled, codes, sizes, skipped):
    comp = cfg["output"]["companions_dir"]
    rows = []
    for b in cfg["bundle"]:
        rs = bundled[b["acronym"]]
        nums = sorted(int(re.search(r"\d+$", codes[r["slug"]]).group()) for r in rs)
        span = f"{b['acronym']}{nums[0]} to {b['acronym']}{nums[-1]}" if nums else "none"
        rows.append(f"| `{b['file']}` | `{b['acronym']}` | {len(rs)} | {span} | {sizes[b['file']] / 1024:.1f} KB |")
    total = sum(sizes[b["file"]] for b in cfg["bundle"])
    skipped_note = (f"{len(skipped)} rule(s) are marked `Agent: none` and left out." if skipped
                    else "No rule is left out.")
    return f"""# Handoff: Groups360 database standards for the AI guidance repository

This folder is generated from the Groups360 database standards wiki pages. Nobody edits these files by
hand. A change to a page is a full replacement of that wiki page, and these files are re-cut from the pages
and handed over again.

## What is here

| Path | What it is |
|---|---|
| `.claude/rules/db_*_conventions.md` | Seven concern files of numbered rule lines, scoped by `paths` to `migrations/**` and `<pkg>/data/models/**` |
| `.claude/rules/db_usage_conventions.md` | How to apply the rules: they are guidelines the author may bend for a stated reason, and the agent never decides for the author |
| `.claude/agents/database_design_agent.md` | A specialty review agent that owns the family. Its Guardrails, Suppression handling, and Output format sections are copied word for word from `data_migration_agent.md` |
| `{comp}/` | One companion per rule (the full rule and the stories behind it), plus `approved-acronyms.md` |

Nothing existing is overwritten. Every file is new.

## How to install

Unzip `dist.zip` at the root of the guidance repository. Everything lands under `.claude/`, next to the
existing rules and agents, and no existing file is replaced. `HANDOFF.md` and `.generated` also land at the root;
this note can be deleted once read, and `.generated` records which commit of your repository the agent's
fixed sections were copied from. Then run `node .claude/scripts/check-claude.mjs` as usual.

## The rules

{skipped_note} Together the rule files come to about {total / 1024:.0f} KB, about {total // 4000}k tokens if all of them load.

| File | Acronym | Rules | Codes | Size |
|---|---|---|---|---|
{chr(10).join(rows)}

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
   finding. A hook that logs reads of `{comp}/` would show whether it does.
8. **The generated notice** at the top of each bundle is our wording. If you use a standard header for generated
   files, tell us and we will switch.

## How these were checked

The files were validated against `validate-rule.mjs` and `check-claude.mjs` on a scratch copy of the
guidance repository. The repository itself was not written to.
"""


# ---- main -----------------------------------------------------------------------------------

def check_out_dir(out):
    out_r = out.resolve()
    protected = [ROOT, ROOT / "pages", ROOT / "agent", ROOT / "tools", ROOT / "derived", ROOT / "runbook"]
    if any(out_r == p.resolve() or out_r in p.resolve().parents for p in protected):
        die(f"refusing to use '{out}' as the output folder: it would be wiped")
    if out.exists() and any(out.iterdir()) and not (out / GENERATED_MARK).exists():
        die(f"refusing to wipe '{out}': it is not empty and is not a previous output of this script")


def main():
    ap = argparse.ArgumentParser(description="Build the handoff tree for the AI guidance repository.")
    ap.add_argument("--update-lock", action="store_true", help="assign codes to new rules in codes.lock")
    ap.add_argument("--zip", action="store_true", help="also write <out>.zip, the file to hand over")
    ap.add_argument("--no-agent", action="store_true", help="skip the agent file (no target needed)")
    ap.add_argument("--out", default=None, help="output folder (default: output.dir in the control file)")
    args = ap.parse_args()

    cfg = load_control(ROOT / "agent" / "control.toml")
    out = Path(args.out or cfg["output"]["dir"])
    if not out.is_absolute():
        out = ROOT / out
    check_out_dir(out)
    target, target_sha = (None, None) if args.no_agent else guidance_checkout()

    rules = load_rules(ROOT / "pages")
    bundled, skipped = bundle_rules(rules, cfg["bundle"])
    lock_path = ROOT / "codes.lock"
    lock = load_lock(lock_path)
    codes, new, reserved = assign_codes(bundled, lock, args.update_lock)
    if args.update_lock and new:
        write_lock(lock_path, lock, new)
        print(f"codes.lock: {len(new)} new code(s) assigned, {len(lock) + len(new)} in total")
    for c, s in sorted(reserved.items()):
        print(f"  NOTE: {c} ({s}) is no longer emitted. The code stays reserved and is never reused.")

    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name) / "derived"
        res = subprocess.run([sys.executable, str(HERE / "cut_apart.py"), str(ROOT / "pages"), str(tmp)],
                             capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if res.returncode != 0:
            die("cut_apart.py failed:\n" + res.stdout + res.stderr)

        if out.exists():
            shutil.rmtree(out)
        rules_dir = out / ".claude" / "rules"
        comp_dir = out / cfg["output"]["companions_dir"]
        rules_dir.mkdir(parents=True)
        comp_dir.mkdir(parents=True)

        sizes = {}
        file_of = {}
        for b in cfg["bundle"]:
            text = render_bundle(b, bundled[b["acronym"]], codes, cfg)
            (rules_dir / b["file"]).write_text(text)
            sizes[b["file"]] = len(text.encode())
            for r in bundled[b["acronym"]]:
                file_of[r["slug"]] = (b["file"], codes[r["slug"]])
        usage = ROOT / cfg["agent"]["usage_rules"]
        shutil.copy(usage, rules_dir / usage.name)

        for acr, rs in bundled.items():
            for r in rs:
                bundle_file, code = file_of[r["slug"]]
                (comp_dir / f"{r['slug']}.md").write_text(companion_text(r, code, bundle_file, tmp))
        acro = tmp / "reference" / "approved-acronyms.md"
        if acro.exists():
            (comp_dir / "approved-acronyms.md").write_text(LOCAL_LINK.sub(r"\1", acro.read_text()))

        if not args.no_agent:
            agents_dir = out / ".claude" / "agents"
            agents_dir.mkdir(parents=True)
            (agents_dir / Path(cfg["agent"]["template"]).name).write_text(render_agent(cfg, bundled, codes, target))

        (out / "HANDOFF.md").write_text(render_handoff(cfg, bundled, codes, sizes, skipped))
        (out / GENERATED_MARK).write_text("This folder is rebuilt by tools/emit_agent_tree.py. Do not edit it.\n"
                                          + (f"Agent boilerplate copied from vendor/ai_python_guidance at {target_sha}.\n" if target_sha else ""))

    # a duplicate code across the generated and hand-written files would fail the target's gate
    seen = {}
    for f in sorted(rules_dir.glob("*.md")):
        for line in f.read_text().split("\n"):
            m = re.match(r"^(R[A-Z]{2,6}\d+):", line)
            if m:
                if m.group(1) in seen:
                    die(f"code {m.group(1)} appears in {seen[m.group(1)]} and {f.name}")
                seen[m.group(1)] = f.name
    total = sum(sizes.values())
    print(f"rules emitted {sum(len(v) for v in bundled.values())} in {len(cfg['bundle'])} bundles, "
          f"{len(skipped)} left out | {total / 1024:.1f} KB of rule lines (about {total // 4000}k tokens)")
    for b in cfg["bundle"]:
        print(f"  {b['file']:34} {b['acronym']}  {len(bundled[b['acronym']]):3} rules  {sizes[b['file']] / 1024:5.1f} KB")
    print(f"wrote {out}")
    if args.zip:
        base = out.parent / out.name
        shutil.make_archive(str(base), "zip", root_dir=out)
        print(f"wrote {base}.zip (hand this file over)")


if __name__ == "__main__":
    main()
