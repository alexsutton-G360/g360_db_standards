# Stand-in trial results (2026-11-17)

The generated `database-design-agent` was run as a subagent against each sample file, in a scratch copy of the
guidance repo with `dist/` overlaid. This tests content and wording. It does not test `/review` routing.
Run `TRIAL.md` for that.

| Sample | Planted violations caught | Extra findings | Notes |
|---|---|---|---|
| rate_plans migration + model | 7 of 7 (RDBCY1, RDBCY2, RDBCL6, RDBID4, RDBTB1, RDBNM8, plus RDBRL7 only in passing) | RDBID9, RDBTB3, RDBOB5, RDBCL1 | RDBRL7 (FK index, a Judgment call) was mentioned inside the RDBID4 finding, not raised on its own, and its companion was not read. |
| rate_plan_details migration | 5 of 5 (RDBCL12, RDBCL14, RDBCL5, RDBCL1, RDBCL15/16) | RDBCL8, RDBCL11, RDBCL17, RDBTB5 | Judgment calls asked the rule's questions in order and picked no answer. Deferred deploy mechanics to RMIG6/RMIG9. |
| notes migration (control) | n/a | RDBTB2, RDBOB5, RDBNM9 (first draft) | The control was not clean: an unnamed primary key and a two-noun table name. Both were fixed in the sample. The remaining RDBTB2 question is fair. |

What held up: every finding was `discuss`, severity followed Temperature, the agent said it contacted no
one when a second opinion applied, no reason was graded, and companions were read for Judgment calls
in two of three runs.

Cost: each run used roughly 80k to 105k subagent tokens, mostly reading all seven bundles plus companions.
That is the price of loading everything on every change, and it is the number to watch.

Open: the agent did not raise RDBRL7 as its own finding. A real run will show whether that repeats.

## Real `/review` runs (2026-11-17)

Run 1 (before the read fixes): routing passed and all 12 planted problems were found. The agent opened only
three of its nine files, with `cat | head`, and no companion at all. Findings named no stories.

Run 2 (after requiring full Reads, adding `story:` markers, and pinning `opus` / `high`): all seven bundles and
the usage rules were opened with Read, plus 17 companions, including the Judgment-call and story-bearing ones.
Which of the three changes mattered was not isolated. To isolate the model and effort pin, revert the commit that
adds it and rerun.

Other agents in the fleet reported the same float price and naive timestamp. The verdict was `Needs changes`
because of `RLAY8`, `RMIG18` and `RMIG25`/`RMIG28` findings, none of them ours. Every database-design finding
was `discuss`.
