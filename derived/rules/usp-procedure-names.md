---
slug: "usp-procedure-names"
title: "Name a stored procedure `usp_<descriptor>`"
temperature: "Rule"
origin: "house"
scope: "procedure"
why: "object-naming"
page: "other_objects"
group: "Triggers, functions, procedures, and views"
second_opinion: "DBA."
companion: false
---

# Name a stored procedure `usp_<descriptor>`

A stored procedure you write starts with `usp_`, followed by a descriptor of what it does.

Because: the pattern is a house convention. The prefix tells a reader that the object is user-defined and which kind it is, and that holds only if every one carries it.

Good: `usp_db_backups`
Bad:  `backup_databases`

Second opinion: DBA.
