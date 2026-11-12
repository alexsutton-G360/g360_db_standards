---
page: "tables"
group: "Tables that belong to one of several parents"
kind: "group-intro"
in_load_hints: true
---

# Tables that belong to one of several parents

Sometimes a table needs to belong to one of several other tables. An addresses table might hold addresses for a user or for an org. This is a polymorphic association, and there are three ways to model it. Each has a place. Wherever a table points at a row in the same database, the starting point is a real foreign key (*rule: same-database-pointer-needs-fk*). This group is about keeping that when a table has several possible parents.

The chunks in this group are one line of thought and are meant to be read in order: why the rows share one table, what Groups360 used to do and why you will still meet it, what Groups360 does now, what to reach for when that strains, and a short way to choose.
