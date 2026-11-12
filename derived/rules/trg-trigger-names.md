---
slug: "trg-trigger-names"
title: "Name a trigger `trg_<table>_<descriptor>`"
temperature: "Rule"
origin: "house"
scope: "trigger"
why: "object-naming"
page: "other_objects"
group: "Triggers, functions, procedures, and views"
second_opinion: "DBA."
companion: false
---

# Name a trigger `trg_<table>_<descriptor>`

A trigger name starts with `trg_`, then the table it sits on, then a descriptor of what it does. The shared trigger that keeps `updated_at` current is under Row lifecycle on Tables.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `trg_bookings_set_updated_at`
Bad:  `bookings_trigger`, `update_bookings`

Second opinion: DBA.
