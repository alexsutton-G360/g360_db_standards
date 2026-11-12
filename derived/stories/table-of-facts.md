---
slug: "table-of-facts"
title: "A table is a ledger, not a to-do list"
serves: ["declarative-names"]
page: "columns"
---

# A table is a ledger, not a to-do list

A table in a database is almost always a store of facts. The properties table is a collection of what properties exist in the world: which ones are hidden, and which are not. It is not a set of requests about how property data should be displayed. It is the property data. The same goes for "this RFP was created at such a time" and "this brand contains these hotels". Each row is a statement that is true.

A ledger and a to-do list make a useful pair. A ledger records what happened, and a reader can trust every line as a fact. A to-do list asks someone to do something, and a reader cannot tell whether the thing has been done, will be done, or was dropped. A column named `is_hidden` is a ledger line. A column named `hide` is a to-do item, and reading it raises questions the table cannot answer: whether the property is hidden now, or someone has asked for it to be.

This does not hold for every table. A table that really holds instructions, such as jobs waiting to run, is a to-do list on purpose, and its columns can be named that way. For most tables the facts framing is the right one, and column names that follow it need no explanation.
