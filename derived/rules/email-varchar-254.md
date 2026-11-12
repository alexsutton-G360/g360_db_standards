---
slug: "email-varchar-254"
title: "Email addresses: varchar(254)"
temperature: "Default"
origin: "general"
scope: "column"
why: "email-limits"
page: "columns"
group: "Text"
companion: true
---

# Email addresses: varchar(254)

Use `varchar(254)` for an email address. Use 320 only with a very good reason.

Because: 320 is the RFC maximum, but 254 is the practical limit that mail servers along the way enforce.

More: companions/email-varchar-254.md
