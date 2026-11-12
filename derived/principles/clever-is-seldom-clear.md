---
slug: "clever-is-seldom-clear"
title: "Clever is seldom clear"
---

# Clever is seldom clear

Engineers are smart, and smart people go looking for places to apply it. Reusing one column for a second job feels clever, and it usually is. But a clever trick saves its author a little effort and leaves the bill with whoever comes after, who never saw the trade. If a column means one thing on its face and another in practice, do not leave the second meaning hidden. If it is new information, give it a column of its own. If it can be worked out from what the table already holds, do not store it as a second copy: derive it, with a generated column when it depends only on the same row (*rule: same-row-value-generated-column*), or with a view when it depends on other tables (*rule: no-second-copy-use-a-view*).

*Evidence:* an image table used its `id` as the display order, and when the sync stopped rebuilding rows, photos of toilets became the first image at several hotels (*story: image-order*). A table saved by folding one concept into another was efficient, and hard for anyone to find (*story: guest-conversions*).
