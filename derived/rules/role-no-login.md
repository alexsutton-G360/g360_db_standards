---
slug: "role-no-login"
title: "Create a role with no login rights, named for what it covers and its access level"
temperature: "Rule"
origin: "house"
scope: "role"
why: "role-access"
page: "other_objects"
group: "Roles and users"
second_opinion: "DBA."
companion: false
---

# Create a role with no login rights, named for what it covers and its access level

A role is a named bundle of permissions that is granted to users, and a role created this way has no login rights, so no one connects as it. In Postgres a user is a role that is allowed to log in, and a role that is not is a group. Grant the access to the role, and then grant the role to each person or service that needs it. When access later has to grow, one role changes, and not every user. Name the role for the one thing it covers, in the singular, followed by its access level, with an underscore between.

Because: the pattern is a house convention, and consistency is what lets a reader tell an object from its name.

Good: `booking_ro`, `booking_rw`
Bad:  `bookingro`, `_bookingro`

Second opinion: DBA.
