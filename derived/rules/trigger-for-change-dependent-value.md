---
slug: "trigger-for-change-dependent-value"
title: "When a value depends on how a row changed, let a trigger maintain it"
temperature: "Default"
origin: "general"
scope: "column"
why: "calculated-columns"
page: "columns"
group: "Values the database maintains"
companion: true
---

# When a value depends on how a row changed, let a trigger maintain it

When a value cannot be worked out from the other columns of the same row, because it depends on when or how the row changed, let a trigger maintain it and do not leave it to application code. A generated column cannot do this job, since its formula has to give the same answer every time. A timestamp stamped at the moment of a change is the standard case, and the shared trigger for `updated_at` is the worked example (*rule: shared-updated-at-trigger*, on Tables). That function maintains `updated_at` and nothing else, so a different value gets a function of its own, written in the same shape. Name the trigger and the function by the rules on Other objects and tools (*rule: trg-trigger-names*, *rule: ufn-function-names*).

Because: a trigger maintains the value for every writer, whichever application or script touched the row.

Good: a trigger that sets `updated_at` on every real change
Bad:  every piece of application code that writes the row setting `updated_at` itself

More: companions/trigger-for-change-dependent-value.md
