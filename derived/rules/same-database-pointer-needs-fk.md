---
slug: "same-database-pointer-needs-fk"
title: "A column that points at a row in the same database needs a real foreign key"
temperature: "Rule"
origin: "general"
scope: "column"
why: "real-foreign-keys"
page: "columns"
group: "Identifiers"
companion: false
---

# A column that points at a row in the same database needs a real foreign key

If a column holds the `id` of a row in another table in the same database, declare a foreign key on it. A column that looks like a pointer but has no foreign key behind it is only a convention, and it holds only as long as every piece of code that touches the data respects it. The database cannot refuse a missing parent, cannot protect a parent that still has children, and cannot tell anyone the link exists.

When the row lives in another database, which happens often in a microservice setup, no foreign key is possible. That column is a `_guid` and not an `_id`, and having no key behind it is expected. Why a `guid` is what travels between databases is under Row identity on Tables.

One case inside a single database needs more than this rule says: a table that can belong to one of several parents. A plain pointer column and a foreign key do not fit it, and there is a good deal more to say about keeping real keys there. That is covered in the group Tables that belong to one of several parents, on Tables. It includes the pattern you will meet most often in existing tables (*rule: source-type-id-pattern*) and a short way to choose among the designs (*rule: polymorphic-decision-matrix*).

A foreign key does not index its column. Whether to add an index is a separate decision, covered under Indexes on Tables.

Because: the database is the lowest level at which something can be true. An application that knows about the link is not enough, because the link has to hold no matter what code touches the data.

Good: `property_id`, with a foreign key to `properties (id)`, and `rfp_guid`, pointing at another service, with no key
Bad:  `property_id` holding a real property id, with no foreign key declared
