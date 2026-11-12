---
slug: "money-in-minor-units"
title: "Store money as minor units in a bigint"
temperature: "Default"
origin: "general"
scope: "column"
why: "currency-major-units"
page: "columns"
group: "Currency"
companion: true
---

# Store money as minor units in a bigint

Store an amount as a count of the currency's smallest unit in a `bigint`. In US dollars that is cents, so $5.00 is stored as 500. A currency with no minor unit, like yen, stores ¥10,000 as 10000.

Why not `numeric`, which is exact? Nothing is wrong with it, and it is what the derived major-unit column below uses. The case against it as the stored form is scale. A `numeric` column has to be given a number of decimal places, and the right number depends on the currency: none for yen, three for the Kuwaiti dinar. One scale cannot be right for every currency. A count of minor units in a `bigint` needs no scale, stays exact in every tool and language, and has no decimal type for anything downstream to mishandle. Using `numeric` instead is a deviation from this Default, and it needs a reason written down like any other.

More: companions/money-in-minor-units.md
