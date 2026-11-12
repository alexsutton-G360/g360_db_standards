---
slug: "one-table-for-same-shape-rows"
title: "When rows have the same shape whatever they belong to, keep one table and not one per parent"
temperature: "Default"
origin: "general"
scope: "table"
why: "polymorphic-associations"
page: "tables"
group: "Tables that belong to one of several parents"
companion: false
---

# When rows have the same shape whatever they belong to, keep one table and not one per parent

If an address has the same structure whether it belongs to a user or an org, give addresses one table. Two separate address tables, each with its own `street` and its own copy of every rule about an address, mean that any change to what an address is has to be made in two places. Someone working on one of them may never learn the other exists.

When the rows really do differ in shape, separate tables are the honest design, and this default does not apply.

Because: the structure of the database should say what is true about the data. If an address is the same thing everywhere, one table says so.
