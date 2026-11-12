---
slug: "contact-list"
title: "The contact list that grew up"
serves: ["lists-or-tables"]
page: "tables"
---

# The contact list that grew up

This is an illustration and not a real case. It shows how a series of reasonable choices ends at the wrong shape.

A property needs a few contact emails. The simplest thing is one field, `contact_emails`, holding them separated by commas. For a while that is enough. The screen shows the field, and nobody needs more from it.

Then someone asks to find the property that an address belongs to. A search for `ann@example.com` returns a property that holds `joann@example.com`, because the search is matching pieces of text and the database has no idea where one address ends and the next begins. The fix is a sensible one: make the field an array. The same search now matches whole addresses, and the column is better for it.

Then someone asks which of the addresses should receive invoices. There is nowhere to put that. A flag belongs to one address, and an array element is only a value, with nothing to hang a flag on. The addresses were never a list of values that belonged to the property. Each one was a thing with facts of its own, and the property had a collection of them. That is a table, and it was a table from the start.

Each earlier step was a reasonable answer to the question in front of it. The question that would have found this at the first step is what each value might come to carry, and whether anyone will ever need to say something about one address and not about all of them together.
