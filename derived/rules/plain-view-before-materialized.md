---
slug: "plain-view-before-materialized"
title: "Start with a plain view, and move to a materialized view only when the query has earned it"
temperature: "Default"
origin: "general"
scope: "table"
why: "derived-in-view"
page: "tables"
group: "Derived values and copies"
second_opinion: "DBA."
companion: true
---

# Start with a plain view, and move to a materialized view only when the query has earned it

A plain view is always current, and it needs nothing from operations. It pays at read time, since the query runs each time the view is read. That is the right place to start, and most views never need more.

Look at a materialized view when the query behind the view is heavy, it is read often, and the data can safely be a little behind. A materialized view stores its result and goes stale as the data underneath changes, until it is refreshed. Keeping it fresh is a plan and a commitment, and creating it is not the end of the job. It puts the object on the DBA's path, with refresh timing, load, and monitoring. That is a bigger decision than it looks.

Which kind is right depends on size. A query that is cheap on a small table may not be on a large one. See the note on scale on the Index.

Because: a plain view cannot drift. A materialized view can, and its staleness is the same kind of drift a stored copy has, so choose one deliberately and with a refresh plan in place.

Good: a view over the room and space bookings that derives a header's status when it is read
Good: a materialized view for a heavy summary that is read constantly, with a refresh plan agreed with the DBA
Bad:  a materialized view created for a cheap query, with no refresh plan, so that it goes stale unnoticed

Second opinion: DBA.

More: companions/plain-view-before-materialized.md
