# Groups360 database standards: guide for agents

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
| `column` | 36 | the change adds, alters, or names a column |
| `constraint` | 3 | the change adds or names a key or a constraint |
| `database` | 1 | the change creates or names a database |
| `function` | 1 | the change adds or names a function |
| `index` | 1 | the change adds or names an index |
| `materialized_view` | 1 | the change adds or names a materialized view |
| `procedure` | 1 | the change adds or names a stored procedure |
| `role` | 1 | the change creates or names a role |
| `schema` | 3 | the change creates or names a schema |
| `table` | 19 | the change creates, alters, or names a table |
| `trigger` | 1 | the change adds or names a trigger |
| `user` | 1 | the change creates or names a database user or service account |
| `view` | 1 | the change adds or names a view |

3. **Each rule file stands alone.** Its frontmatter gives the slug, temperature, origin and scope, and the `why` key shared by related rules.
4. **If a rule is not enough, read its companion.** A rule file ends with `More: companions/<slug>.md` when there is more to read. Follow it when you are unsure how a rule applies, then decide again.
5. **Refer to a rule by its slug.** Write `rule: <slug>`. A slug points at exactly one rule and never changes.
6. **Temperature is not a severity score.** It says how much a deviation owes, as defined below.

## How to treat a rule

### Temperature: how firm the rule is

Every rule can be crossed. Temperature says how much a deviation owes. In every case, the reason is what matters.

**Rule.** Deviate only with a strong, specific reason, written down.

**Default.** The starting point. Deviate when you can state the reason in a sentence. A reviewer who sees a Default skipped will ask what the reason is, and if there is none, the Default stands.

**Judgment call.** There is nothing to deviate from, but a decision is owed, and the decision needs a reason. The docs supply the questions that make it easier to answer. They do not pick for you.

### Origin: what could overturn it

Origin says where a rule gets its authority, and so what kind of argument can replace it.

**house** (a house rule). A choice Groups360 has made and relies on. It is not claimed to be correct everywhere, only consistent across Groups360's systems, and it holds because the people and systems there lean on it. "Groups360 already does it" is not a defense. A better design, or a change in Groups360's own systems, can replace it. What can keep it is a real cost to changing everything that leans on it, not the fact that it exists.

**general** (a general practice). Sound data practice anywhere. It does not depend on Groups360, and it falls only to a better argument about data, not to a change in the company.

### When you deviate

Deviating is allowed at every temperature. What changes is the size of the reason.

Write the reason down, briefly, where the change is made. For most changes that means a short comment in the migration. For a larger change, add a comment on the ticket as well, so the reasoning lives somewhere a teammate would think to look. A sentence is enough. Nobody is asking for a document.

The point is the question, not the answer. Asking "why am I departing from the standard?" is the step that matters, and a written reason is the proof it was asked. A weak reason still counts, because it means the choice was made on purpose.

A written reason also protects the person who made the change. If a design later looks strange to someone, a stated reason shows it was a decision and not an accident, and shows the standards were followed.

## When a rule seems wrong

These docs are not set in stone, and they are not here to be followed just because they were written down. They are here so we have something to edit.

That asks something of you beyond deviating for a good reason. You may find a rule that is flat wrong. You may meet a case nobody thought of, where the rules do not fit, or fit badly. Either one is welcome news, and we would count it a gift to hear it. It is how these pages get better. Tell the data architect what you found and why. A rough note is plenty.

You are on the hook for this, dear reader, and that includes an agent reading these rules. If a rule seems wrong for the case in front of you, say so plainly and say why. Do not apply it only because it is there.

## What is not in this set

- The Stock tables page is a living document and is not in this set yet.
- The currency runbook is separate from the standards and is not in this set.
- Rule files are currently given in full. Where a rule has a companion, the companion adds the story or explanation behind it.
- `cut_report.md` is for the people who maintain this set. You do not need it.
