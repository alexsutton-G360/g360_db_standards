---
slug: "multibyte-text"
title: "When characters and bytes disagree"
serves: ["redshift-varchar-ceiling", "unbounded-data"]
page: "columns"
---

# When characters and bytes disagree

Postgres counts the length of a varchar in characters. The warehouse counts it in bytes. For plain English text the two are the same, because every character takes one byte. For other text they are not. In UTF-8, accented European letters and Greek, Cyrillic, and Hebrew letters take two bytes, most Chinese, Japanese, and Korean characters take three, and emoji take four.

So a `varchar(65535)` in Postgres can hold a value that does not fit under the warehouse's 65,535-byte ceiling. A column of Greek text can need up to twice the room, and one of Chinese text or emoji three or four times as much. The result is the failure the ceiling rule exists to prevent: one oversized value reaches the warehouse, and every view built on that column can fail.

In practice this is a corner case on top of a corner case. A column near the ceiling is rare, because 65,000 characters is a lot of text for almost any field, and a column near the ceiling that also holds non-Latin text is rarer still. Names, codes, and URLs never come close.

When it does apply, set the limit lower, so that the worst case in bytes still fits. Dividing 65,535 by the widest character expected gives the ceiling: 32,767 characters for text that is at most two bytes per character, 21,845 for three, and 16,383 for four.

To check a value that is misbehaving, compare `char_length(value)` with `octet_length(value)` in Postgres. If the second is much larger than the first, the text is multibyte, and that is probably the reason.
