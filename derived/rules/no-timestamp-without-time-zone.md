---
slug: "no-timestamp-without-time-zone"
title: "Never use `timestamp` without a time zone"
temperature: "Rule"
origin: "general"
scope: "column"
why: "timestamptz-utc"
page: "columns"
group: "Dates and times"
companion: true
---

# Never use `timestamp` without a time zone

Use `timestamptz`. If something truly forces a plain `timestamp`, store only UTC in it, with no exceptions.

Because: a plain timestamp drops the time zone when a value is inserted, so a value that looks the same can mean different times depending on the session that wrote it, and a column of mixed zones cannot be untangled afterward.

More: companions/no-timestamp-without-time-zone.md
