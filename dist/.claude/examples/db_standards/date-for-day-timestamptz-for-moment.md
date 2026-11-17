# Use `date` for a day and `timestamptz` for a moment

Rule line `RDBCL4` in `db_column_conventions.md`. Temperature: Rule. Origin: general.

## Full rule

Use `date` when what matters is the day something happens, like availability on March 4 or an arrival on April 1. Use `timestamptz` when what matters is the moment, like when a record was created.

## Why this rule exists

Rules that share this explanation (why: `timestamptz-utc`):

- `no-timestamp-without-time-zone`: Never use `timestamp` without a time zone
- `store-utc-convert-for-display`: Store timestamps in UTC and convert only for display

### Story: Which clock was that?

Early in Groupsync's history, most date-and-time columns at Groups360 were plain `timestamp`. A plain `timestamp` holds a clock reading with no time zone attached, so the column itself does not say which clock was read. The intent was to store UTC in them. In practice that was applied unevenly, and the result is a set of columns where some values are UTC, some are Central time, and nothing in the data says which. Untangling them has been slow, and it is not finished.

A quieter hazard sits on top of that, and it comes from `NOW()`. The function returns a moment with a time zone attached, and shows it in whatever zone the session is set to. That setting belongs to the connection, so two people running the same statement can get different results. When the value is written into a plain `timestamp` column, Postgres drops the zone and keeps the clock reading.

The same statement, `UPDATE ... SET updated_at = NOW()`, therefore writes UTC from a session set to UTC and local time from a session set to Chicago. In a test, the Chicago session wrote 13:11 where the UTC session wrote 19:11 for the same instant: six hours in the past, with no error and nothing to show it. A workaround exists, `NOW() AT TIME ZONE 'UTC'`, but a standard that depends on every author remembering a workaround to avoid a trap leaves the trap in place.

So the standard removes the trap and does not ask anyone to step around it: always `timestamptz`. A `timestamptz` column stores the moment itself, and the same `NOW()` writes the same value from any session. It also says what it holds. A reader never has to guess whether the column is UTC, Central time, or something else, because it holds moments and shows them in whatever zone the session asks for.

### Story: A time that is a promise, not a moment

A UTC timestamp records an instant, an exact moment on one universal clock. That is what a record of something that already happened needs, and it is why the standard stores UTC. It is not always what a person means. Someone who schedules an event for 9:00 in the morning, local time, in a given city next March means a clock reading in a place, not an instant.

For most events the two come to the same thing, and storing UTC works. The difference appears when the rules change. Governments change their daylight saving rules, sometimes with little notice. A stored instant is an answer worked out in advance under the old rules. What the organizer meant was closer to the question: 9:00 on the clock in that city. If the rules change, the question can be asked again and will give the new answer. The old answer cannot fix itself, and nothing in the database shows that it has gone wrong.

This is where `timestamptz` alone falls short. A `timestamptz` value is converted to UTC the moment it is written, and the zone it arrived in is thrown away. A value entered as 9:00 in Athens and a value entered as 7:00 UTC are identical once stored. The intent is gone at write time, so there is nothing left to work from later. Keeping it takes a pair of columns beside each other, the local clock reading and the name of the time zone, like `Europe/Athens`, with the instant calculated from them whenever it is needed.

That arrangement has costs, and they are the reason the standard does not simply recommend it.

- The local clock reading has no zone of its own, so it has to sit in a plain `timestamp`, the one type the standard otherwise forbids.
- Calculating again only helps once Postgres has caught up with the new rule. Until its time zone data is updated, every calculation for that place is wrong, stored or not. That is outside Groups360's hands, in the same way a currency changing its decimal places is.
- Not every local time exists, and not every local time is unique. When clocks jump forward, 2:30 in the morning never happens. When they fall back, 1:30 happens twice. Postgres raises no error for either and silently picks one, so the pair can hold a reading that was never a real moment.
- Postgres will accept the calculated instant in a generated column, but a stored value is a snapshot of the rules as they were when the row was written. Calculating when the value is read keeps it current.

So the case is arguable, and in most systems it does not earn its cost. A rule change that lands between scheduling and the event is rare, and many times that look like promises about a clock are perfectly well served as moments. Where the intent has to survive, as with an event that must happen at 9:00 on the wall clock whatever a government decides, the pair of columns is the way to keep it. Everywhere else, `timestamptz` and UTC. The question to ask first is whether anyone needs the intent preserved.

None of this applies to something that has already happened. A record of when something happened is a moment, and a later rule change does not move it. Storing the zone name beside a past moment, so it can be shown in that place's local time, is fine and is not an exception.
