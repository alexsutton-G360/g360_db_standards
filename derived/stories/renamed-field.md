---
slug: "renamed-field"
title: "A field renamed in one place"
serves: ["consistency-is-clarity", "bend-or-break"]
page: "index"
---

# A field renamed in one place

In the properties table, the `image_url` field probably should have been called `default_image_url` when it was created, since it stores the property's default image.

That naming exists across both an upstream database and a downstream one, and it works the same in both places. When the downstream one was created, the field was renamed `default_image_url` in that database and only that database. The change was almost certainly well-meant, an attempt to make things clearer than they were. But the structure of the properties table is something many, many people in the organization understand, and those who learn it for the first time are likely to learn it from the upstream database first and then discover it everywhere else.

That one naming change means the statement "the hero image of a property is stored on the `image_url` field" must continue "unless you are looking at the downstream database, in which case the name is different". This creates tribal knowledge. It makes people's first assumption wrong. That costs time and effort, and creates unnecessary frustration.
