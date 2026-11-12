---
slug: "change-row-in-place"
why: "edit-in-place"
---

# Change a row in place, and do not delete it and create it again

## Full rule

When the data in a row changes, update the row that exists. An updated row keeps its `id`, and anything downstream, like a warehouse sync, can see that it changed. A row that is deleted and created again gets a new `id`, and whatever already saw the old row is left holding a stray.

If what you need is "insert this row, or update it if it is already there", that is an upsert, and it is a different thing from rebuilding. Postgres does it directly with `INSERT ... ON CONFLICT DO UPDATE`. It needs a unique key to conflict on, such as the unique constraint on a junction table's pair of foreign keys. The habit of deleting and re-creating rows made sense once, when Postgres had no upsert. It does now.

There may be times when rebuilding is right. If you think yours is one, say why in writing, and ask someone before you do it.

Because: an updated row keeps its identity and leaves nothing behind. In Groups360's tables, each time rebuilding rows has been looked at, it has turned out to be the wrong choice.

Good: a child row updated where it stands when its booking changes
Bad:  all of a booking's child rows deleted and inserted again on every save

Second opinion: any teammate.

## Why this rule exists

### Story: Labels on the bags

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

### Story: Image order

Hotels complained that their image carousel, the hero image plus the pictures of the lobby, the fountains, and so on, was showing pictures of toilets as the first image. By the fourth or fifth report it had reached the data team: toilets were being shown as the most important image at a hotel. The cause was a fix, made without a full picture of someone else's data model.

The image process had been built quickly, copying an existing one. It read from an image provider, worked out all the images for a hotel, and inserted them into an image table. Every run, it deleted all of that hotel's images and inserted a fresh set, whether or not anything had changed. Each day it scanned 10, 20, 30,000 hotels and replaced around 100 images for each, so the id values got very high.

Later, a complaint came in that images weren't being pulled often enough, or some other bug. While fixing it, the delete-everything behavior came to light, and the process was improved: insert a row only when there is a new image, and update the row when an existing image changes. The table stopped churning.

That is what caused the toilets. The table had no image-order column. The original programmers used the `id` as the display order. Since the rows were rebuilt every run, the id order effectively was the display order, so from their perspective it never caused a problem. But the id is a SQL identity, used for foreign keys and joins. It isn't meant to be load-bearing for what is presented to clients.

Once the rebuilding stopped, consider which pictures a hotel updates least often. The lobby gets redone at Christmas. Guest rooms get new linens, curtains, renovations. The last thing a hotel updates, and the last thing it even uploads new photos of, is the toilets. Those rows kept the lowest ids, the lowest ids were shown first, and so toilets were shown. It was a fun bug to track down.

An engineer saved maybe twenty minutes by not adding an image-order column and filling it in. It was a really clever trick, and genuinely clever. It just wasn't clever in a way that was useful.
