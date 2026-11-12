---
slug: "no-second-copy-use-a-view"
title: "Do not keep a second copy of data that a view can derive"
temperature: "Default"
origin: "general"
scope: "table"
why: "derived-in-view"
page: "tables"
group: "Derived values and copies"
companion: true
---

# Do not keep a second copy of data that a view can derive

When data already exists in one place and another place needs a different view of it, derive it with a view. Do not store a copy that application code keeps in step. That covers a whole second table filled by copying from the first, and it covers a stored column whose value is worked out from rows in other tables, such as a header's status that sums up the bookings beneath it.

A stored copy can differ from its source, and it is only as reliable as every run of the code that maintains it. A view cannot differ, because it is the source, read a different way. If a value must be stored in a table at all, store only what cannot be derived, and put the derived part in a read view on top.

A generated column does not fit here, because it can read only the row it sits in. Anything that needs other tables is a view. See Values the database maintains on Columns.

Because: a value that can differ from its source will, sooner or later, and everything downstream of it, including the warehouse and reporting, inherits the difference. A value that can be made true by construction should not be left to stay true by effort.

Good: a parent's status read through a view that derives it from the child rows
Bad:  a status column on a parent, filled in by application code from its child rows, with a standing clean-up to correct the drift

More: companions/no-second-copy-use-a-view.md
