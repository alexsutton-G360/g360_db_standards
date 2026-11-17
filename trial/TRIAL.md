# Trial: does the database design agent flag what it should?

`sample_service/` is a tiny fake service with planted violations. `EXPECTED.md` lists what a review
should flag. `RESULTS.md` records the stand-in runs. This file is the real run, about 10 minutes.

You need: git, node, unzip, and Claude Code. Nothing in your real checkouts is touched.

## 1. Build the scratch setup

From the root of this repository:

    python3 tools/emit_agent_tree.py --zip
    bash trial/run_trial_setup.sh

It builds `~/g360_trial/` with a scratch copy of the guidance repo (their pinned commit plus our
`dist.zip`) and a sample service on the branch `trial/bad-migrations`, linked to the scratch copy.
It prints `guidance copy passes check-claude`. The "dormant rule" warnings above that line are normal.

## 2. Open Claude Code in the sample service

    cd ~/g360_trial/sample_service
    export CLAUDE_SERVICE_PKG=app
    claude

Do not use direnv here. The `export` does the same job.

## 3. Run the review

Type `/review`. It diffs `main` against the branch and launches every agent whose triggers match.

## 4. What to look for

1. **Routing.** Near the top of the output, `database-design-agent` should be in the set of agents invoked,
   next to `data-migration-agent`. If it is missing, the routing is broken. Stop and send me the output.
2. **Findings.** Compare against `EXPECTED.md`. Every planted violation should appear with its `RDB` code.
3. **Tone.** Every finding says `discuss`. Nothing says a change is blocked. Nothing grades the author's reason.
4. **Companions.** For Judgment-call rules (`RDBRL7`, `RDBNM8`, `RDBCL17`, `RDBTB5`), the finding names a story
   or asks the rule's questions. If it never mentions a story where one exists, the companion lookup is not
   happening, which is the thing we most want to know.
5. **Verdict.** `/review` prints `Needs discussion`, not `Needs changes`.

## 4b. Check what the database agent actually read

After the review finishes, run this in any terminal. It lists every rule and companion file that was opened.
The seven `db_*_conventions.md` files and `db_usage_conventions.md` should each appear, and so should the
`examples/db_standards/` files for any finding that carries a story or is a Judgment call.

    grep -rhoE '"file_path": ?"[^"]*(\.claude/(rules|examples)/)[^"]*"' ~/.claude/projects/*sample*service* | sed 's/.*\.claude\///' | sort | uniq -c | sort -rn

## 5. Report back

Paste the full `/review` output to me, or tell me which of the five checks failed. If all five pass, the
handoff is ready to send.

## Cleaning up

    rm -rf ~/g360_trial
