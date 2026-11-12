---
slug: "idx-index-names"
title: "Name every other index `idx_<table>_<column>`"
temperature: "Rule"
origin: "house"
scope: "index"
why: "object-naming"
page: "other_objects"
group: "Keys, constraints, and indexes"
second_opinion: "DBA."
companion: false
---

# Name every other index `idx_<table>_<column>`

A standalone index is `idx_` followed by its table and the column or columns it covers. An index that a primary key or a unique constraint creates takes that constraint's name, and keeps it.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `idx_users_first_name`
Bad:  `users_first_name_idx`, the name Postgres would give it

Second opinion: DBA.
