---
slug: "varchar-over-char-and-text"
title: "Use varchar, not char or text"
temperature: "Rule"
origin: "general"
scope: "column"
why: "varchar-vs-text"
page: "columns"
group: "Text"
companion: true
---

# Use varchar, not char or text

Use varchar, with a limit. Do not use char. Text is almost never right either, but there are a few narrow situations where it is, mainly data with no honest upper limit, covered below.

Because: text can outgrow the warehouse and crash billing views, while char pads values with whitespace for no benefit.

More: companions/varchar-over-char-and-text.md
