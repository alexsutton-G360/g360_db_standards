# Store money as minor units in a bigint

Rule line `RDBCY3` in `db_currency_conventions.md`. Temperature: Default. Origin: general.

## Full rule

Store an amount as a count of the currency's smallest unit in a `bigint`. In US dollars that is cents, so $5.00 is stored as 500. A currency with no minor unit, like yen, stores ¥10,000 as 10000.

Why not `numeric`, which is exact? Nothing is wrong with it, and it is what the derived major-unit column below uses. The case against it as the stored form is scale. A `numeric` column has to be given a number of decimal places, and the right number depends on the currency: none for yen, three for the Kuwaiti dinar. One scale cannot be right for every currency. A count of minor units in a `bigint` needs no scale, stays exact in every tool and language, and has no decimal type for anything downstream to mishandle. Using `numeric` instead is a deviation from this Default, and it needs a reason written down like any other.

## Why this rule exists

Rules that share this explanation (why: `currency-major-units`):

- `currency-code-column`: Store a currency's code in `currency_code`
- `no-float-for-money`: Never store money in float, real, or double
- `money-column-minor-units-name`: Name each money column for what it holds, ending in `_minor_units`
- `derive-major-from-minor`: Derive major units from minor units instead of storing a second copy
- `no-flat-divide-by-100`: Never turn minor units into major units with a flat divide by 100
- `major-units-standard-block`: Calculate major units in a generated column with the standard block

### Story: Why a copied block, and why that is worth it

A major-units column was once built by dividing the minor units by 100 for every currency. It is right for most currencies and wrong for the rest, and the yen is the one that exposed it. The wrong values reached financial reporting, where some bookings showed costs that made no sense. The cause was nowhere near the place the symptom showed up, and it was found only by tracing the numbers backwards, step by step, to the column that produced them. A wrong value that surfaces far from its source takes a long time to trace, and that is the cost the rule exists to avoid. Whatever the standard recommends has to make the correct version at least as easy as the wrong one.

Three ways of doing it were weighed.

A reference table of currencies and their decimal places, joined in a view, is the cleanest. It keeps the data in one place. It was set aside because it is a table to build, fill, and keep in every database that needs it, and the path that takes real setup is the path people skip. The flat divide takes none.

A shared function that holds the lists is tidier than a copied block, since a change means editing one place. It was set aside as the default because it is one more thing to find or create before first use, and the change it protects against, a currency's decimal places shifting, is expected almost never to happen.

A block copied into each generated column was chosen. It takes the least effort, so it is the version people will actually use. Its costs are real and accepted. A change means finding every copy, which is a text search because every copy is identical, and then updating each one, which also recomputes the stored values. An unlisted currency is treated as two decimal places, which is right for nearly all of them.

A shared function is the better choice once a database has many such columns and its authors want one place to edit, and moving to one at that point is reasonable. Copying the block is a shortcut taken on purpose, in the cheapest place, to avoid a worse mistake that is easy to make.
