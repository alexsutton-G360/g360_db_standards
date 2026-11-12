---
slug: "image-order"
title: "Image order"
serves: ["clever-is-seldom-clear", "database-is-source-of-truth", "first-assumption-correct", "edit-in-place"]
page: "index"
---

# Image order

Hotels complained that their image carousel, the hero image plus the pictures of the lobby, the fountains, and so on, was showing pictures of toilets as the first image. By the fourth or fifth report it had reached the data team: toilets were being shown as the most important image at a hotel. The cause was a fix, made without a full picture of someone else's data model.

The image process had been built quickly, copying an existing one. It read from an image provider, worked out all the images for a hotel, and inserted them into an image table. Every run, it deleted all of that hotel's images and inserted a fresh set, whether or not anything had changed. Each day it scanned 10, 20, 30,000 hotels and replaced around 100 images for each, so the id values got very high.

Later, a complaint came in that images weren't being pulled often enough, or some other bug. While fixing it, the delete-everything behavior came to light, and the process was improved: insert a row only when there is a new image, and update the row when an existing image changes. The table stopped churning.

That is what caused the toilets. The table had no image-order column. The original programmers used the `id` as the display order. Since the rows were rebuilt every run, the id order effectively was the display order, so from their perspective it never caused a problem. But the id is a SQL identity, used for foreign keys and joins. It isn't meant to be load-bearing for what is presented to clients.

Once the rebuilding stopped, consider which pictures a hotel updates least often. The lobby gets redone at Christmas. Guest rooms get new linens, curtains, renovations. The last thing a hotel updates, and the last thing it even uploads new photos of, is the toilets. Those rows kept the lowest ids, the lowest ids were shown first, and so toilets were shown. It was a fun bug to track down.

An engineer saved maybe twenty minutes by not adding an image-order column and filling it in. It was a really clever trick, and genuinely clever. It just wasn't clever in a way that was useful.
