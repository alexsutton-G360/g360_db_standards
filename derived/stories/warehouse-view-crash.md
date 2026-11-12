---
slug: "warehouse-view-crash"
title: "The text field that took down the views"
serves: ["varchar-vs-text", "redshift-varchar-ceiling"]
page: "columns"
---

# The text field that took down the views

Groups360 runs two kinds of database. The operational databases sit under Groupsync and the private label apps, and run PostgreSQL (version 17.11 as of November 2026, which may have changed since). Downstream is a data warehouse in Amazon Redshift, which is built differently and has a different toolkit. A sync tool, currently Stitch, copies flagged tables from one to the other and reshapes the data to fit.

Postgres allows far longer values than the warehouse does. Redshift has no `text` type at all, and its `varchar` stops at 65,535. A `text` column is where the mismatch bites, and the same sequence has played out more than once:

1. A field in Groupsync is defined as `text`.
2. The sync tool keeps up, raising the `varchar` size on the warehouse copy each time a longer value arrives.
3. A value arrives that is longer than any before it. The sync tool pulls it into the source table in the warehouse and updates that table's definition to fit.
4. The views built on top of that table do not follow. A materialized view fixes its column sizes when it is created and does not inherit later changes to the table underneath.
5. The next time a view tries to pull in the new value, it fails, and stays unavailable until someone finds the offending value and widens the column in the warehouse by hand.

Those views are critical infrastructure for billing and revenue recognition, so a column type chosen at design time becomes an outage in finance reporting. That is the whole case for `varchar` over `text`, and for never going above 65,535.
