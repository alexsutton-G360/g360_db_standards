---
slug: "array-or-second-table"
why: "lists-or-tables"
---

# Before using an array column, check that it is not a second table you have not made

## Full rule

An array column is the right home for a list when each value is bare: a plain value that belongs to the row and has nothing else attached to it, such as the tags on a record. It is simple, it keeps one fact in one place, and a search can match whole values.

It is a second table you have not made when any of these is true:

- A value carries something of its own, such as a flag, a date, or a status.
- A value points at another table. A foreign key cannot be placed on the elements of an array.
- A value must be unique across the rows of the table. A unique constraint on an array column compares whole arrays and not their elements.

If none of these is true, use the array. If one is, make the table, however much easier the array feels today. The easy moment to ask is when the column is created, and the question to ask is what each value might come to carry.

Because: an array looks like a column and behaves like one until the first time a value needs a fact or a link of its own, and by then the data is already in the wrong shape.

Good: `tags varchar(50)[]`, where a tag is only a word
Bad:  `contact_emails text[]`, where each address will need its own flag

## Why this rule exists

Rules that share this explanation (why: `lists-or-tables`):

- `no-delimited-list-strings`: Never store a list of values as one delimited string

### Story: The contact list that grew up

This is an illustration and not a real case. It shows how a series of reasonable choices ends at the wrong shape.

A property needs a few contact emails. The simplest thing is one field, `contact_emails`, holding them separated by commas. For a while that is enough. The screen shows the field, and nobody needs more from it.

Then someone asks to find the property that an address belongs to. A search for `ann@example.com` returns a property that holds `joann@example.com`, because the search is matching pieces of text and the database has no idea where one address ends and the next begins. The fix is a sensible one: make the field an array. The same search now matches whole addresses, and the column is better for it.

Then someone asks which of the addresses should receive invoices. There is nowhere to put that. A flag belongs to one address, and an array element is only a value, with nothing to hang a flag on. The addresses were never a list of values that belonged to the property. Each one was a thing with facts of its own, and the property had a collection of them. That is a table, and it was a table from the start.

Each earlier step was a reasonable answer to the question in front of it. The question that would have found this at the first step is what each value might come to carry, and whether anyone will ever need to say something about one address and not about all of them together.
