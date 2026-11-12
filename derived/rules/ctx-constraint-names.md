---
slug: "ctx-constraint-names"
title: "Name every other constraint `ctx_<descriptor>`"
temperature: "Rule"
origin: "house"
scope: "constraint"
why: "object-naming"
page: "other_objects"
group: "Keys, constraints, and indexes"
second_opinion: "DBA."
companion: false
---

# Name every other constraint `ctx_<descriptor>`

A check, unique, or exclusion constraint is `ctx_` followed by what it enforces. A unique constraint creates an index, which takes the constraint's name, so that index keeps its `ctx_` name.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `ctx_exactly_one_parent`, `ctx_unique_note_rfp`
Bad:  `notes_body_check`, the default name an unnamed check constraint gets

Second opinion: DBA.
