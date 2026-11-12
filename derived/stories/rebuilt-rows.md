---
slug: "rebuilt-rows"
title: "Labels on the bags"
serves: ["created-updated", "soft-deletes", "edit-in-place"]
page: "tables"
---

# Labels on the bags

Reporting in the data warehouse went out of step with the operational system. Rows were turning up there for a booking's room types that did not exist in the operational databases at all.

A booking at Groups360 is one record, the roll-up: when it was created, the total cost, the arrival and departure dates. The room types booked sit in a child table, with one row for each room type on each day, so a five-night booking with five room types is 25 rows. The booking carried `created_at` and `updated_at`. The child table did not. From the application's side that looked reasonable. The booking already says when it was created and when it last changed, and the rows inside it could simply inherit that.

The warehouse does not see it that way. To the sync, every table is just a table. It does not know that these rows belong to a booking, and it cannot borrow the booking's timestamps. Each row is a package that is moved around on its own, long before anything opens the box it belongs to. A package with no label gives the sync nothing to go on, and the only thing left to follow was the `id`.

Then the way the application "updated" those rows came into it. It deleted the old rows and created new ones. The old rows had often been copied to the warehouse already. Deleting them in the operational database told the warehouse nothing, because a hard delete leaves nothing behind to notice. The new rows arrived with new ids and were copied as new. The old rows stayed, and reporting counted both.

Three things were weak at once, and each is a layer that was missing:

- **Rows were rebuilt when they should have been edited.** Changing the row that exists keeps its id and leaves nothing behind.
- **Rows were hard-deleted.** A deleted row leaves nothing for a sync to find. A `deleted_at` timestamp on a soft-deleted row turns a deletion into a change that can be seen.
- **The sync followed `id` and not `updated_at`.** An id can say that a row exists. It cannot say that the row has changed.

An `updated_at` on the table would not have fixed this on its own, since the rebuilt rows would still have been strays. It is one of the pillars the design should have stood on. A sync that follows `updated_at`, together with a `deleted_at` on soft-deleted rows, sees every change, deletions included, even when application code rebuilds rows it should have edited. Each layer covers a gap the others leave, which is the case for supplying all of them.

The lesson underneath is about whose point of view a table is designed from. In the application, a timestamp answers a question the application asks. In the warehouse, the same column has another job: it is how a row is tracked. A table that leaves the columns off has quietly taken itself out of that.
