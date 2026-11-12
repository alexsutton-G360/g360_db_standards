---
slug: "no-float-for-money"
title: "Never store money in float, real, or double"
temperature: "Rule"
origin: "general"
scope: "column"
why: "currency-major-units"
page: "columns"
group: "Currency"
companion: true
---

# Never store money in float, real, or double

Because: binary floating point cannot represent most decimal amounts exactly, so totals drift. Each error is tiny, but they stack when amounts are added together, and a report can end up off by a few cents with no one able to say where.

Storing an amount only to display it is not an exception in practice. A value kept for display tends to be summed, exported, or reported on later, and by then the float is already in the pipeline. A value that really is display-only, and will stay so, carries little risk, and as with any Rule it can be crossed with a strong reason written down. Be suspicious of the claim that it will stay display-only.

More: companions/no-float-for-money.md
