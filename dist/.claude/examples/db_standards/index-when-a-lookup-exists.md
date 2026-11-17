# Add an index when something looks the column up, in the same change that adds the lookup

Rule line `RDBRL6` in `db_relationship_conventions.md`. Temperature: Default. Origin: general.

## Full rule

An index is a cost paid in advance. It takes space, and every insert, update, and delete on the table has to maintain it too. An index that nothing uses pays that cost for nothing. So add one when a query that exists needs it, whether that is a lookup, a join, or a sort the table is genuinely asked to do, and add it in the same change that introduces the query. Do not add one in case it is needed someday.

The other direction fails quietly. A lookup with no index works on a small table and slows as the table grows, with no error to say why. That is the reason the index belongs in the same change as the lookup and not in a follow-up.

A unique constraint creates an index, so it carries the same cost. When the constraint enforces something true about the data, as a `guid` being unique does, the index is a consequence of that guarantee and not a guess about future queries.

We do this badly today. Many of our databases carry indexes that no query has ever used, and every one of them is still maintained on every write.

Because: every index slows every write to the table and takes space whether or not a query ever uses it, so an index should be able to name the query it serves.

Good: an index on `check_in_date`, added in the same change as the report that filters bookings by it
Bad:  indexes put on three columns when the table is created, in case someone searches by them later
