---
slug: "lowercase-every-name"
title: "Use lowercase for every name"
temperature: "Rule"
origin: "general"
scope: "global"
why: "lowercase-only"
page: "global_rules"
group: "Global Rules"
companion: true
---

# Use lowercase for every name

Write every database object name in lowercase, with no capital letters anywhere.

Because: Postgres folds unquoted names to lowercase, so a name with capitals has to be wrapped in double quotes every time anyone refers to it.

Good: `booking_service`
Bad:  `BookingService`

Applies to every object unless its own page says otherwise.

More: companions/lowercase-every-name.md
