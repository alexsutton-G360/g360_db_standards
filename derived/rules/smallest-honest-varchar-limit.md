---
slug: "smallest-honest-varchar-limit"
title: "Give every varchar the smallest limit your data honestly allows"
temperature: "Default"
origin: "general"
scope: "column"
why: "varchar-limits"
page: "columns"
group: "Text"
companion: true
---

# Give every varchar the smallest limit your data honestly allows

Understand your data and constrain it as far as you practically can.

Because: a limit the database does not enforce is only an opinion, and raising a limit later is lossless while lowering one is not.

Good: `varchar(3)` for an ISO currency code, `varchar(50)` for a free-form event name
Bad:  `text` or `varchar(255)` for a currency code, `varchar(65535)` for an event name

More: companions/smallest-honest-varchar-limit.md
