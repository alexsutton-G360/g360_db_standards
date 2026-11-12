---
slug: "no-flat-divide-by-100"
title: "Never turn minor units into major units with a flat divide by 100"
temperature: "Rule"
origin: "general"
scope: "column"
why: "currency-major-units"
page: "columns"
group: "Currency"
companion: true
---

# Never turn minor units into major units with a flat divide by 100

How many minor units make a major unit depends on the currency. Most use two decimal places, a few use none, like the yen, some use three, like the Kuwaiti dinar, and two use four. A flat divide by 100 is right for most currencies and wrong for the rest, and the error is easy to miss because testing rarely covers every currency.

Because: the number of decimal places is a property of the currency, not a constant.

Good: the standard block below
Bad:  `amount_minor_units / 100` for every currency

Story: `major-units-by-paste`.

More: companions/no-flat-divide-by-100.md
