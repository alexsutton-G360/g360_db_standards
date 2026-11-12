---
slug: "by-column-is-user-guid"
title: "A column ending in `_by` holds a user guid from identity_service"
temperature: "Rule"
origin: "house"
scope: "column"
why: "by-columns"
page: "columns"
group: "Identifiers"
second_opinion: "Data Architect."
companion: true
---

# A column ending in `_by` holds a user guid from identity_service

If a column ends in `_by`, it holds a guid that points to a user in identity_service. Never a name, an email, or free text.

Use `_by` without further conversation when all three of these are true:

1. It is always a user guid pointing at identity_service.
2. It is never unknown, so it is `NOT NULL`.
3. There is no extra texture: no anonymous users, no automated actors, nobody it could be besides a logged-in person.

Everything else is an engineering question, so here are the questions:

- Is it really a user guid? If not, do not call it `_by`. Name it for what it holds.
- Can it genuinely be unknown or not applicable? Then it is nullable, and the author must be able to say in one sentence what null means.
- Can a machine or an anonymous person do this? That is a platform decision. See the next rule.

Null never means "a machine did it" or "anonymous". Null means unknown or not applicable, as everywhere else on these pages.

Because: enough columns already end in `_by` and mean this that it has become a default, so keeping one meaning costs less than a second dialect.

Second opinion: Data Architect.

More: companions/by-column-is-user-guid.md
