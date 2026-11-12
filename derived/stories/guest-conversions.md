---
slug: "guest-conversions"
title: "Where guest conversions live"
serves: ["first-assumption-correct", "clever-is-seldom-clear"]
page: "index"
---

# Where guest conversions live

Guest users are welcome in the system. But some activities, such as an RFP with its back-and-forth, require a guest to become a real user first, and a guest account has no way back by design. So the system needs to convert guests into real users. That ability existed for a long time, poorly implemented, and work began to formalize it.

Around the same time, a `user_logins` table was introduced to keep a full history of logins. The users table only held the most recent one. A conversion is, in effect, the moment a former guest logs in as a real user for the first time. So a design was proposed: add a column to `user_logins` holding the id of the guest a user was converted from. Most rows would leave it empty, and the rows that mark a conversion would carry the guest's id.

The case for that design is real. It needs no new table, it is simpler to implement, and it is sufficient, since everything about a conversion can be recovered from it.

The case against it is about who has to find it. Someone who wants to know how and why guests convert will look for something named for conversions. Nobody guesses the answer lives in the logins table. The only way to discover it is to scan the schema for a column like `converted_from_guest_user_id` and work out what it means. The design is efficient, and clever, and opaque to anyone who doesn't already know the trick. What it optimizes, one extra table, doesn't need optimizing, because data storage is cheap.

Conversions were given their own table.

This isn't a verdict. Folding one concept into another table can be the right call, for example when the concept really is just an attribute of the host row, or when the only people who will ever look for it already know where to look. The test is this: if someone who has never seen these tables went looking for the concept, where would they look first, and would they find it?
