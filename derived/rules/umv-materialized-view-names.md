---
slug: "umv-materialized-view-names"
title: "Name a materialized view `umv_<table>_<descriptor>`"
temperature: "Rule"
origin: "house"
scope: "materialized_view"
why: "object-naming"
page: "other_objects"
group: "Triggers, functions, procedures, and views"
second_opinion: "DBA."
companion: false
---

# Name a materialized view `umv_<table>_<descriptor>`

A materialized view starts with `umv_`, followed by the table it reads from and a descriptor of what it does. A materialized view that an application creates, and not a person, is not covered by this rule.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `umv_bookings_monthly_totals`
Bad:  `monthly_totals`

Second opinion: DBA.
