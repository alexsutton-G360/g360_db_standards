---
description: Currency and money conventions: currency_code, minor units, and major-unit columns. Apply when a change adds or alters an amount of money or a currency code.
paths: ["migrations/**", "<pkg>/data/models/**"]
---

All currency rules are enumerated using the RDBCY (Rules DataBase CurrencY conventions) code.

> Generated from the Groups360 database standards repository. Edit the pages there, not this file.

## Currency

RDBCY1: when a migration or model adds a column that holds a currency code, name it `currency_code` exactly, make it `varchar(3)`, and store the uppercase ISO-4217 code (`USD`, `EUR`). Use one `currency_code` per row for all its amounts, because a second currency column on a row that holds one currency stores one fact several times. Only where a row really spans currencies, name each column for its role (`charged_currency_code`, `settlement_currency_code`). Reason: the standard major-unit block and the currency runbook find currency codes by this name. [Rule; slug: currency-code-column; full rule: .claude/examples/db_standards/currency-code-column.md]

RDBCY2: never store money in `float`, `real`, or `double`. A value kept for display tends to be summed, exported, or reported on later, so be suspicious of a claim that it will stay display-only; crossing this rule needs a strong written reason. Reason: binary floating point cannot represent most decimal amounts exactly, so totals drift. [Rule; slug: no-float-for-money; full rule: .claude/examples/db_standards/no-float-for-money.md]

RDBCY3: when a migration or model adds an amount of money, store it as a count of the currency's smallest unit in a `bigint` (5.00 US dollars is 500; a currency with no minor unit, like yen, stores 10,000 yen as 10000). Using `numeric` as the stored form is a deviation and needs a written reason. Reason: `numeric` needs a scale, and the right number of decimal places depends on the currency, none for yen and three for the Kuwaiti dinar. [Default; slug: money-in-minor-units; full rule: .claude/examples/db_standards/money-in-minor-units.md]

RDBCY4: when a migration or model adds a money column, name it for what it holds and end it in `_minor_units`: a single amount is `amount_minor_units`, and several are `base_price_minor_units`, `service_charge_minor_units`. [Default; slug: money-column-minor-units-name; full rule: .claude/examples/db_standards/money-column-minor-units-name.md]

RDBCY5: when a migration or model needs dollars, euros, or other major units, calculate them from the minor-unit column as `numeric(23,4)` (`decimal(23,4)` in Redshift) instead of storing a second copy. Store a major-unit column directly only when the value needs fractions of a minor unit, like half a cent. [Default; slug: derive-major-from-minor; full rule: .claude/examples/db_standards/derive-major-from-minor.md]

RDBCY6: never turn minor units into major units with a flat divide by 100; use the standard block (`major-units-standard-block`). Reason: the number of decimal places is a property of the currency: most use two, a few use none (yen), some use three (Kuwaiti dinar), and two use four. [Rule; slug: no-flat-divide-by-100; full rule: .claude/examples/db_standards/no-flat-divide-by-100.md]

RDBCY7: when a migration or model adds a generated major-unit column, copy the standard block from the full rule (`major-units-standard-block`) exactly as written and change only the column names, so every copy can be found and compared. A currency not on the block's list is treated as two decimal places, and a change to a currency's decimal places means every copy must be found and updated (see the currency runbook). Reason: identical copies can all be found and compared. [Default; slug: major-units-standard-block; full rule: .claude/examples/db_standards/major-units-standard-block.md]
