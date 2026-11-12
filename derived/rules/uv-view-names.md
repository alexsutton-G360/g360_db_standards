---
slug: "uv-view-names"
title: "Name a view `uv_<table>_<descriptor>`"
temperature: "Rule"
origin: "house"
scope: "view"
why: "object-naming"
page: "other_objects"
group: "Triggers, functions, procedures, and views"
second_opinion: "DBA."
companion: false
---

# Name a view `uv_<table>_<descriptor>`

A view starts with `uv_`, followed by the table it reads from and a descriptor of what it does. When to choose a view, and which kind, is under Derived values and copies on Tables.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `uv_bookings_status`
Bad:  `bookings_status`

Second opinion: DBA.
