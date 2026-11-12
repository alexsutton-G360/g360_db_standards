---
slug: "columns-in-positive-voice"
title: "Name columns in the positive voice"
temperature: "Default"
origin: "general"
scope: "column"
why: "positive-voice"
page: "columns"
group: "Naming"
companion: true
---

# Name columns in the positive voice

Name a flag for what is true, not for what is not. Avoid negations. Pairs that differ only by a negating verb lean the same way, less strictly.

Because: code that tests a negated name reads as a double negative, and the extra words add nothing.

Good: `is_active`, `has_attachments`
Bad:  `is_not_active`, `does_not_have_attachments`

This one bends when another name reads more clearly. Story: `hidden-vs-displayed`.

More: companions/columns-in-positive-voice.md
