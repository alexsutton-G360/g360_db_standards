# Expected findings for trial/sample_service

Planted violations. A review should flag each, with the code, and every finding should be `discuss`.
Rule line temperature decides severity (Rule High, Default Medium, Judgment call Low).

## migrations/..._rate_plans.py (and the model)

| Planted | Expected code | Slug |
|---|---|---|
| `price` as `Float` | RDBCY2 | no-float-for-money |
| `currency` instead of `currency_code`, `String(255)` | RDBCY1 | currency-code-column |
| `contact` and `contact_2` | RDBNM8 | numbered-column-names |
| `created` is `timestamp` without time zone (and not `created_at`) | RDBCL6 | no-timestamp-without-time-zone |
| no `created_at` / `updated_at` pair | RDBTB1 | created-at-updated-at-on-tables |
| `property_id` with no foreign key | RDBID4 | same-database-pointer-needs-fk |
| and no index on it | RDBRL7 (Judgment call: companion should be read) | foreign-key-index-decision |

## migrations/..._rate_plan_details.py

| Planted | Expected code | Slug |
|---|---|---|
| `website` as `Text` | RDBCL12 | url-varchar-2048 |
| `notify_emails` holds a delimited list | RDBCL14 | no-delimited-list-strings |
| `approved_on` holds a `timestamptz` | RDBCL5 | date-name-preposition-match |
| `room_count` nullable with no stated meaning | RDBCL1 | not-null-until-null-has-meaning |
| `status` open text, nullable | RDBCL15 / RDBCL16 | short-text-is-a-fixed-set, database-enforces-fixed-set |

## migrations/..._notes.py (control)

Written to follow the standards. Zero or few findings expected. Anything flagged should be a real
question (for example, whether `updated_at` has its trigger: RDBTB2 is a fair question here, since the shared function is not created in this migration), not a rule it plainly meets.

## Also check

- Judgment-call findings read the companion and name the story slug where one exists.
- The agent advises. It never says it blocks, never grades a reason, never decides for the author.
- Findings on the nullable-column and NOT NULL rules mention the overlap with `RMIG6`/`RMIG9` rather than contradicting them.
