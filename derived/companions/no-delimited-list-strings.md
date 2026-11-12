---
slug: "no-delimited-list-strings"
why: "lists-or-tables"
---

# Never store a list of values as one delimited string

## Full rule

A comma-separated string in a text or varchar column is a list that the database cannot see. It cannot check the values, count them, or tell where one ends and the next begins, so a search for one value can match part of another. If a field holds several values, use an array column or a second table. Choosing between the two is covered under Lists of values on Tables. An array column keeps the varchar rules: the limit in `varchar(254)[]` applies to each element, so the array can hold any number of values of up to 254 characters each.

Because: a delimited string only works while every value avoids the delimiter and every reader splits it the same way, and nothing in the database enforces either.

Good: `emails` as a `varchar(254)[]`, or a table of emails
Bad:  `emails varchar(500)` holding `a@example.com,b@example.com`

## Why this rule exists

Rules that share this explanation (why: `lists-or-tables`):

- `array-or-second-table`: Before using an array column, check that it is not a second table you have not made

### Story: The contact list that grew up

This is an illustration and not a real case. It shows how a series of reasonable choices ends at the wrong shape.

A property needs a few contact emails. The simplest thing is one field, `contact_emails`, holding them separated by commas. For a while that is enough. The screen shows the field, and nobody needs more from it.

Then someone asks to find the property that an address belongs to. A search for `ann@example.com` returns a property that holds `joann@example.com`, because the search is matching pieces of text and the database has no idea where one address ends and the next begins. The fix is a sensible one: make the field an array. The same search now matches whole addresses, and the column is better for it.

Then someone asks which of the addresses should receive invoices. There is nowhere to put that. A flag belongs to one address, and an array element is only a value, with nothing to hang a flag on. The addresses were never a list of values that belonged to the property. Each one was a thing with facts of its own, and the property had a collection of them. That is a table, and it was a table from the start.

Each earlier step was a reasonable answer to the question in front of it. The question that would have found this at the first step is what each value might come to carry, and whether anyone will ever need to say something about one address and not about all of them together.
