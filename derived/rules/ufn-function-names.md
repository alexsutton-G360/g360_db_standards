---
slug: "ufn-function-names"
title: "Name a function `ufn_<descriptor>`"
temperature: "Rule"
origin: "house"
scope: "function"
why: "object-naming"
page: "other_objects"
group: "Triggers, functions, procedures, and views"
second_opinion: "DBA."
companion: false
---

# Name a function `ufn_<descriptor>`

A function you write starts with `ufn_`, followed by a descriptor of what it does.

Because: the pattern is a house convention. The prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

Good: `ufn_set_updated_at`
Bad:  `set_updated_at`

Second opinion: DBA.
