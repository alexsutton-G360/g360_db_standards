---
slug: "no-delimited-list-strings"
title: "Never store a list of values as one delimited string"
temperature: "Rule"
origin: "general"
scope: "column"
why: "lists-or-tables"
page: "columns"
group: "Text"
companion: true
---

# Never store a list of values as one delimited string

A comma-separated string in a text or varchar column is a list that the database cannot see. It cannot check the values, count them, or tell where one ends and the next begins, so a search for one value can match part of another. If a field holds several values, use an array column or a second table. Choosing between the two is covered under Lists of values on Tables. An array column keeps the varchar rules: the limit in `varchar(254)[]` applies to each element, so the array can hold any number of values of up to 254 characters each.

Because: a delimited string only works while every value avoids the delimiter and every reader splits it the same way, and nothing in the database enforces either.

Good: `emails` as a `varchar(254)[]`, or a table of emails
Bad:  `emails varchar(500)` holding `a@example.com,b@example.com`

More: companions/no-delimited-list-strings.md
