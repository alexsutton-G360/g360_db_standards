---
slug: "derive-major-from-minor"
title: "Derive major units from minor units instead of storing a second copy"
temperature: "Default"
origin: "general"
scope: "column"
why: "currency-major-units"
page: "columns"
group: "Currency"
companion: true
---

# Derive major units from minor units instead of storing a second copy

When dollars, euros, and the like are needed, calculate them from the minor-unit column. The type is `numeric(23,4)`, or `decimal(23,4)` in Redshift. Store a major-unit column directly only when the value needs fractions of a minor unit, like half a cent.

More: companions/derive-major-from-minor.md
