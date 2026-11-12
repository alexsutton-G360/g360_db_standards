---
slug: "currency-code-column"
title: "Store a currency's code in `currency_code`"
temperature: "Rule"
origin: "general"
scope: "column"
why: "currency-major-units"
page: "columns"
group: "Currency"
companion: true
---

# Store a currency's code in `currency_code`

Name the column `currency_code`, make it `varchar(3)`, and store the ISO-4217 three-letter code in uppercase: `USD`, `EUR`. The uppercase applies to the values. The column name stays lowercase. Any column that holds a currency code has `currency_code` in its name, in exactly that form.

A row has one currency code unless it truly spans currencies. Before adding a second currency column to a table, ask whether the row holds money in more than one currency, or one currency and several amounts. It is almost always the second. A property with a resort fee, a parking fee, and a Wi-Fi fee is the usual way this goes wrong: each fee gets its own currency column, but all of them hold the same currency. That is one fact stored three times, and the copies can drift apart. One `currency_code` covers every amount in the row.

Where a row really does span currencies, such as a payment charged in one currency and settled in another, name each column for its role: `charged_currency_code` and `settlement_currency_code`.

Good: `resort_fee_minor_units` and `parking_fee_minor_units`, with one `currency_code` on the row
Bad:  `resort_fee_currency_code` and `parking_fee_currency_code`, where the two always hold the same value
Bad:  `currency`, `ccy`, or `curr_cd` for a column that holds the code

Because: the name is how copies of the standard major-unit block are found later. The block reads the code column by this name, and the currency runbook searches for it, so a column that holds a currency code under any other name is the one that gets missed when a currency changes.

More: companions/currency-code-column.md
