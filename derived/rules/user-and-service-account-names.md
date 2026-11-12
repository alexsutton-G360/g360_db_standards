---
slug: "user-and-service-account-names"
title: "Name a user for the person or service it stands for, and describe a service account in its comment"
temperature: "Rule"
origin: "house"
scope: "user"
why: "role-access"
page: "other_objects"
group: "Roles and users"
second_opinion: "DBA."
companion: false
---

# Name a user for the person or service it stands for, and describe a service account in its comment

A user is a personal account or a service account. A personal account is named `<name>_<team>_<access>`. A service account begins with `svc`, followed by the database and the access type. Describe what a service account is for in the object's comment.

Because: the pattern is a house convention, and the comment is what lets someone who finds a service account later learn what it is for.

Good: `svcbooking_ro`, a read-only service account for the booking database
Good: `svcroom_rw`, a read and write service account for the room database
Bad:  a service account with no comment saying what it is for

Second opinion: DBA.
