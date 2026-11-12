---
slug: "unlabeled-timestamps"
title: "Which clock was that?"
serves: ["timestamptz-utc"]
page: "columns"
---

# Which clock was that?

Early in Groupsync's history, most date-and-time columns at Groups360 were plain `timestamp`. A plain `timestamp` holds a clock reading with no time zone attached, so the column itself does not say which clock was read. The intent was to store UTC in them. In practice that was applied unevenly, and the result is a set of columns where some values are UTC, some are Central time, and nothing in the data says which. Untangling them has been slow, and it is not finished.

A quieter hazard sits on top of that, and it comes from `NOW()`. The function returns a moment with a time zone attached, and shows it in whatever zone the session is set to. That setting belongs to the connection, so two people running the same statement can get different results. When the value is written into a plain `timestamp` column, Postgres drops the zone and keeps the clock reading.

The same statement, `UPDATE ... SET updated_at = NOW()`, therefore writes UTC from a session set to UTC and local time from a session set to Chicago. In a test, the Chicago session wrote 13:11 where the UTC session wrote 19:11 for the same instant: six hours in the past, with no error and nothing to show it. A workaround exists, `NOW() AT TIME ZONE 'UTC'`, but a standard that depends on every author remembering a workaround to avoid a trap leaves the trap in place.

So the standard removes the trap and does not ask anyone to step around it: always `timestamptz`. A `timestamptz` column stores the moment itself, and the same `NOW()` writes the same value from any session. It also says what it holds. A reader never has to guess whether the column is UTC, Central time, or something else, because it holds moments and shows them in whatever zone the session asks for.
