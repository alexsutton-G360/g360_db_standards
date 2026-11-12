---
slug: "date-name-preposition-match"
title: "If a date or timestamp name ends in a preposition, make it match the type"
temperature: "Default"
origin: "general"
scope: "column"
why: "date-prepositions"
page: "columns"
group: "Dates and times"
companion: false
---

# If a date or timestamp name ends in a preposition, make it match the type

End a name with `_on` only when the column is a date, and with `_at` only when it is a timestamp. Never put `_on` on a timestamp or `_at` on a date. A name with no preposition, like `arrival_date`, is always fine.

Because: a thing happens on a day and at a moment, so the preposition tells a reader the type before they look it up. A mismatch gives the reader a wrong first assumption.

Good: `created_at` holding a `timestamptz`, `arrival_date` holding a `date`
Bad:  `approved_on` holding a `timestamptz`, `arrival_at` holding a `date`

This is mostly a prohibition. It does not require a preposition, and it does not require `_on` for dates.
