---
slug: "store-utc-convert-for-display"
title: "Store timestamps in UTC and convert only for display"
temperature: "Rule"
origin: "general"
scope: "column"
why: "timestamptz-utc"
page: "columns"
group: "Dates and times"
companion: true
---

# Store timestamps in UTC and convert only for display

Store every timestamp in UTC and convert to local time in the display layer. Local time almost never belongs in storage.

There is nuance here, but not much. The one arguable case is told in `future-local-time`.

More: companions/store-utc-convert-for-display.md
