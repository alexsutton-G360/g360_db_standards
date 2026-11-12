---
slug: "array-or-second-table"
title: "Before using an array column, check that it is not a second table you have not made"
temperature: "Judgment call"
origin: "general"
scope: "table"
why: "lists-or-tables"
page: "tables"
group: "Lists of values"
companion: true
---

# Before using an array column, check that it is not a second table you have not made

An array column is the right home for a list when each value is bare: a plain value that belongs to the row and has nothing else attached to it, such as the tags on a record. It is simple, it keeps one fact in one place, and a search can match whole values.

It is a second table you have not made when any of these is true:

- A value carries something of its own, such as a flag, a date, or a status.
- A value points at another table. A foreign key cannot be placed on the elements of an array.
- A value must be unique across the rows of the table. A unique constraint on an array column compares whole arrays and not their elements.

If none of these is true, use the array. If one is, make the table, however much easier the array feels today. The easy moment to ask is when the column is created, and the question to ask is what each value might come to carry.

Because: an array looks like a column and behaves like one until the first time a value needs a fact or a link of its own, and by then the data is already in the wrong shape.

Good: `tags varchar(50)[]`, where a tag is only a word
Bad:  `contact_emails text[]`, where each address will need its own flag

More: companions/array-or-second-table.md
