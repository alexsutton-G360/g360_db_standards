---
slug: "by-column-when-no-user"
title: "What a `_by` column holds when no user acted is an open decision"
temperature: "Judgment call"
origin: "house"
scope: "column"
why: "system-actors"
page: "columns"
group: "Identifiers"
second_opinion: "Data Architect."
companion: false
---

# What a `_by` column holds when no user acted is an open decision

This question is open on purpose, and your design may be the reason to close it. The platform has no settled answer for what a `_by` column holds when the actor is a machine or an anonymous person, and this page does not guess.

If a design needs it, that is the signal the question is due. Bring it to the Data Architect, so it can be decided together with the other architects and directors and not by one team on its own.

Until it is decided, do not use null for it, since a null there could be read as unknown or as "no user acted" and the platform has not said which, and do not make up a stand-in value on your own.

Open since: October 2026.

Second opinion: Data Architect.
