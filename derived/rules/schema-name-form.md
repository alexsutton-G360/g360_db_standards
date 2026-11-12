---
slug: "schema-name-form"
title: "Name a schema in the singular with no underscores"
temperature: "Rule"
origin: "house"
scope: "schema"
why: "object-naming"
page: "other_objects"
group: "Databases and schemas"
second_opinion: "DBA."
companion: false
---

# Name a schema in the singular with no underscores

A schema name is lowercase and singular, with no underscores and no special characters. Postgres allows underscores in a schema name, so this is a convention and not a limit. It is the one place where the underscore rule on Global Rules gives way, because a schema name has no underscores at all.

Because: a schema is a division of the database that you can name in a word. If the name needs an underscore, the schema is probably too specific, and that is the moment to ask what it really is. Consistency also lets a reader tell an object from its name.

Good: `extraction`, `public`
Bad:  `booking_service_test`, `bookings`

Second opinion: DBA.
