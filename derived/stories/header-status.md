---
slug: "header-status"
title: "The scoreboard kept by hand"
serves: ["derived-in-view"]
page: "tables"
---

# The scoreboard kept by hand

A booking at Groups360 has a header, and beneath it sit the things that were actually booked: sleeping rooms at a hotel, and spaces such as a conference room, an event space, or a banquet hall. Rooms and spaces began as separate services and were later combined in the booking service, which holds the orchestration data that ties them together, the header among it. The header carries a status, meant to sum up the status of the room and space bookings beneath it. Sometimes only one of the two exists.

That status was kept by application code. Whatever changed a room booking or a space booking was supposed to update the header to match. That code did its work as separate steps and not as one transaction, and it handled exceptions piece by piece. So one update could succeed and commit, and then an exception in a later step was caught and handled, and the update that should have followed never ran. The room and space tables stayed accurate, and the header's status drifted away from them.

A standing weekly correction now exists to bring them back in step. The mismatch also carries into the group sync and the data warehouse, and from there into reporting, where it makes problems that had no reason to exist.

A scoreboard kept by hand makes the point. When a person writes the score on a board while the game is played somewhere else, the board is right for as long as the person sees every play. The first play that is missed, the board is wrong, and the game goes on without it. The game was never wrong, and here the game was the room and space tables. A scoreboard that reads the score from the game cannot be wrong.

The immediate bug has a fix of its own. Several changes that must succeed or fail together belong in one transaction, so that a failure part way through undoes the earlier steps instead of leaving them committed. The better answer removes the need for it.

Nothing about the status needed to be stored. It is a mapping from the statuses of the bookings below it, so it can be read through a view that derives it, with no code to keep it in step. A generated column could not do this, because it can read only its own row. The sibling case, a value derived from the same row but still kept by a separate process, is told in *derived-by-process* on Columns. The design that fits is a header table that holds only what is really stored, with a read view on top that adds the derived status. A view that sums up other rows cannot be written to, so the application writes to the table and reads through the view, and nothing writes the status. Groups360 has not built this yet. It is described here because it would remove the drift by construction, and it is worth building the first time it can be.

Nobody was at fault. This is the design most people reach for, and it looks right until the first time it drifts. The question that finds it early is whether the value could simply be derived. If a value can be made true by construction, there is no reason to store one that can differ.
