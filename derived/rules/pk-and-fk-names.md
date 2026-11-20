---
slug: "pk-and-fk-names"
title: "Name a primary key `pk_<table>` and a foreign key `fk_<table>_<column>`"
temperature: "Rule"
origin: "house"
scope: "constraint"
why: "object-naming"
page: "other_objects"
group: "Keys, constraints, and indexes"
second_opinion: "DBA."
companion: false
---

# Name a primary key `pk_<table>` and a foreign key `fk_<table>_<column>`

Name the constraint when you create it. A primary key left unnamed gets a default name such as `notes_pkey`, which does not follow the pattern.

A foreign key creates a constraint and no index, so there is no such thing as a foreign key index. Whether the column needs an index is a separate question, answered under Indexes on Tables.

Postgres cuts any name at 63 characters and gives only a notice, and two names cut to the same text will collide. When a pattern would run past that, keep the prefix and follow the rule on shortening long names, below.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `pk_users`, `fk_notes_user_id`
Bad:  `notes_pkey`, the default name an unnamed primary key gets

Second opinion: DBA.
