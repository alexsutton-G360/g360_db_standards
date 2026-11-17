#!/usr/bin/env bash
# Builds a scratch copy of the guidance repo with our dist.zip unzipped into it, plus a sample service on a
# branch with the planted bad migrations. Nothing in your real checkouts is touched.
#
# Usage:  bash trial/run_trial_setup.sh [work-folder]     (default: ~/g360_trial)
# Needs: git, node, unzip. Run from the root of g360_db_standards after `python3 tools/emit_agent_tree.py --zip`.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${1:-$HOME/g360_trial}"
[ -f "$HERE/dist.zip" ] || { echo "dist.zip not found; run: python3 tools/emit_agent_tree.py --zip"; exit 1; }
[ -d "$HERE/vendor/ai_python_guidance/.claude" ] || { echo "submodule empty; run: git submodule update --init"; exit 1; }
rm -rf "$WORK"; mkdir -p "$WORK"

# 1. scratch guidance repo = their repo at the pinned commit + our dist.zip
mkdir "$WORK/guidance"
(cd "$HERE/vendor/ai_python_guidance" && tar --exclude=.git -cf - .) | (cd "$WORK/guidance" && tar xf -)
unzip -q "$HERE/dist.zip" -d "$WORK/guidance"
(cd "$WORK/guidance" && CLAUDE_SERVICE_PKG=app node .claude/scripts/check-claude.mjs >/dev/null && echo "guidance copy passes check-claude")

# 2. sample service: main has no migrations, the branch adds them, so /review has a diff
SVC="$WORK/sample_service"; mkdir "$SVC"; cd "$SVC"
git init -q -b main
git config user.name trial; git config user.email trial@example.com
echo "# sample service" > README.md; git add README.md; git commit -q -m "base"
git checkout -q -b trial/bad-migrations
cp -r "$HERE/trial/sample_service/migrations" "$HERE/trial/sample_service/app" .
git add migrations app; git commit -q -m "add rate_plans and notes"

# 3. link the guidance copy into the service the way their README describes
node "$WORK/guidance/link-into.mjs" "$SVC" app
echo; echo "Ready: $SVC  (branch trial/bad-migrations). Now follow trial/TRIAL.md step 3."
