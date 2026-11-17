#!/usr/bin/env python3
"""
run_target_validators.py: prove dist/ against the guidance repository's own validators, on a scratch copy.

Usage:  python3 tools/run_target_validators.py [--target PATH] [--dist DIR]
        --target defaults to the vendor/ai_python_guidance submodule. Needs `node`.

What it does
  1. Copies the guidance repository's .claude/ folder to a temporary folder (the repository is only read).
  2. Overlays dist/.claude/ on the copy. It refuses to overwrite a file the target already has.
  3. Creates empty migrations/ and app/data/models/ folders so the path globs match, and sets
     CLAUDE_SERVICE_PKG=app.
  4. Runs validate-rule.mjs on our rule files, then check-claude.mjs and agent-triggers.mjs on the whole copy.
  5. Checks that the target's git status is unchanged by the run.

Exit 0 only when every validator passes. A pass here is the only proof that counts (see CLAUDE.md).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def die(msg):
    sys.exit(f"run_target_validators: {msg}")


def git_state(repo):
    r = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def run(cmd, cwd, env):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    ap = argparse.ArgumentParser(description="Run the guidance repository's validators on dist/ in a scratch copy.")
    ap.add_argument("--target", default=str(ROOT / "vendor" / "ai_python_guidance"))
    ap.add_argument("--dist", default=str(ROOT / "dist"))
    args = ap.parse_args()
    if not shutil.which("node"):
        die("node is not installed")
    target, dist = Path(args.target).expanduser(), Path(args.dist)
    if not (target / ".claude").is_dir():
        die(f"{target} has no .claude/ folder; run: git submodule update --init")
    if not (dist / ".claude").is_dir():
        die(f"{dist} has no .claude/ folder; run tools/emit_agent_tree.py first")

    before = git_state(target)
    failed = False
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp)
        shutil.copytree(target / ".claude", scratch / ".claude", symlinks=True)
        for f in sorted((dist / ".claude").rglob("*")):
            if f.is_dir():
                continue
            dest = scratch / f.relative_to(dist)
            if dest.exists():
                die(f"{f.relative_to(dist)} already exists in the target; dist/ must only add files")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, dest)
        (scratch / "migrations").mkdir()
        (scratch / "app" / "data" / "models").mkdir(parents=True)
        env = {**os.environ, "CLAUDE_SERVICE_PKG": "app"}
        scripts = scratch / ".claude" / "scripts"
        ours = sorted(str(Path(".claude/rules") / p.name) for p in (dist / ".claude" / "rules").glob("*.md"))

        steps = [("validate-rule (our rule files)", ["node", str(scripts / "validate-rule.mjs"), *ours]),
                 ("check-claude (whole copy)", ["node", str(scripts / "check-claude.mjs")]),
                 ("agent-triggers (routing map)", ["node", str(scripts / "agent-triggers.mjs")])]
        for label, cmd in steps:
            code, out = run(cmd, scratch, env)
            print(f"[{'ok' if code == 0 else 'FAIL'}] {label}")
            if code != 0:
                failed = True
            if code != 0 or label.startswith("check-claude"):
                for line in out.splitlines()[-25:]:
                    print("    " + line)
            if label.startswith("agent-triggers") and code == 0:
                print(f"    database-design-agent routed: {'database-design-agent' in out or 'database_design_agent' in out}")

    after = git_state(target)
    if before != after:
        print("[FAIL] the target's git status changed during the run")
        failed = True
    else:
        print("[ok] the target repository is untouched")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
