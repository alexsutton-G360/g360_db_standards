---
slug: "database-enforces-fixed-set"
title: "Have the database enforce a fixed set of values"
temperature: "Rule"
origin: "general"
scope: "column"
why: "constrained-values"
page: "columns"
group: "Values from a fixed set"
companion: false
---

# Have the database enforce a fixed set of values

When a column holds one of a fixed set of values, the database enforces the set. A check in application code alone does not count, because anything that writes to the table without going through that code can still write a value outside the set.

Because: a limit kept in application code is an opinion. A limit in the database is true for every writer.
