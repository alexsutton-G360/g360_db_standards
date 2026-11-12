---
slug: "database-name-form"
title: "Name a database in the singular, short and descriptive"
temperature: "Rule"
origin: "house"
scope: "database"
why: "object-naming"
page: "other_objects"
group: "Databases and schemas"
second_opinion: "DBA."
companion: false
---

# Name a database in the singular, short and descriptive

A database name is lowercase and singular, short, and descriptive. Use underscores between words where it has more than one, though one word is preferred. A test copy takes the same name with a suffix. Abbreviate only as Global Rules allows.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `booking_service`, `booking_service_test`
Bad:  `bookings`, `booking_services`

Second opinion: DBA.
