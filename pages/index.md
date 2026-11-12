# Index

## What these docs are for

These docs exist to teach you how to think about data. If they do their job, you can handle a case nobody wrote down, because you have picked up the habit of asking the questions the rules were written to answer.

Underneath that, they do three more jobs.

**Good practice.** Some of what is here is just sound data design, true at any company. It is written down so it is not left to chance.

**Mistakes made once.** Every team makes mistakes. The aim is to make each one a single time. When something goes wrong, the lesson lands here, so the next person does not repeat it. This includes recent ones, not only old ones.

Most of what is written here was learned the hard way, by the people who wrote it. The mistakes in these pages are real ones, made by people doing their jobs with the information they had. Recognizing one of them in your own work is not a failure. It is the point of reading.

**House rules.** Some choices are not objectively right, only consistent across Groups360's systems, and the consistency is the point. Anyone who learns the choice once can rely on it everywhere, so a new variation breaks that for everyone who comes after.

None of this is a gate. The goal is for you to make these decisions yourself, with a reason you can state. A weak reason still counts, because it means a decision was made on purpose. Deviating is fine when you can say why.

## How to read a rule

Every rule on the other pages opens with a tag line, like this:

`[Slug: some-rule-name · Temperature: Rule · Origin: house · Scope: column · Why: some-key]`

The five parts name the rule, say how firm it is, say what kind of argument can overturn it, say what it governs, and say where its full explanation lives. Temperature and origin decide what you do next.

### Temperature: how firm the rule is

Every rule can be crossed. Temperature says how much a deviation owes. In every case, the reason is what matters.

**Rule.** Deviate only with a strong, specific reason, written down.

**Default.** The starting point. Deviate when you can state the reason in a sentence. A reviewer who sees a Default skipped will ask what the reason is, and if there is none, the Default stands.

**Judgment call.** There is nothing to deviate from, but a decision is owed, and the decision needs a reason. The docs supply the questions that make it easier to answer. They do not pick for you.

### Origin: what could overturn it

Origin says where a rule gets its authority, and so what kind of argument can replace it.

**house** (a house rule). A choice Groups360 has made and relies on. It is not claimed to be correct everywhere, only consistent across Groups360's systems, and it holds because the people and systems there lean on it. "Groups360 already does it" is not a defense. A better design, or a change in Groups360's own systems, can replace it. What can keep it is a real cost to changing everything that leans on it, not the fact that it exists.

**general** (a general practice). Sound data practice anywhere. It does not depend on Groups360, and it falls only to a better argument about data, not to a change in the company.

### The two are independent

Temperature says how hard a rule holds. Origin says what can defeat it. How hard a rule holds usually follows from what breaks when it bends. A choice many people rely on breaks everyone's first assumption the moment it changes. A good idea that touches only your own corner breaks nothing outside it.

| | general | house |
|---|---|---|
| **Rule** | Sound anywhere, with little room to bend. | Much leans on it, so bending it breaks things for everyone. |
| **Default** | Good practice with room to bend, where a different choice can read just as clearly. | A shared habit that varies safely where little depends on it. |

### When you deviate

Deviating is allowed at every temperature. What changes is the size of the reason.

Write the reason down, briefly, where the change is made. For most changes that means a short comment in the migration. For a larger change, add a comment on the ticket as well, so the reasoning lives somewhere a teammate would think to look. A sentence is enough. Nobody is asking for a document.

The point is the question, not the answer. Asking "why am I departing from the standard?" is the step that matters, and a written reason is the proof it was asked. A weak reason still counts, because it means the choice was made on purpose.

A written reason also protects the person who made the change. If a design later looks strange to someone, a stated reason shows it was a decision and not an accident, and shows the standards were followed.

### Slug, scope, and why

**Slug** is the rule's own name, a short phrase that points at one rule and no other. Use it to refer to a rule from another rule or from a review comment. Like a why key, it never changes, even if the rule is reworded or moved to another page. **Scope** says what the rule governs, such as a column, a table, an index, or a trigger. **Why** is a short, permanent key to the rule's full explanation, shared by every rule that explanation covers. How those explanations are found is covered next.

## How the pieces link

Every rule carries a **why** key, a short name such as `hidden-vs-displayed`. The key points to the explanation behind the rule, not to another rule. To point at another rule, use its slug. A why key never changes, even if the rule is reworded, split, or moved to another page, so a reference to it stays good.

An explanation can be a short reason written under the rule, or a story. Stories are short accounts of something that went wrong, or nearly did, and they sit at the end of the page whose rules they explain. A story that bears on rules on more than one page is told in full in one place, and the other pages point to it by its key. The links are many to many. A rule can point to several stories, and one story can explain several rules.

### When to read the story

When a rule is clear and fits your case, there is nothing more to read. When you are unsure the rule applies, or you are thinking of deviating, follow the rule's why key to the story behind it. The story shows what the rule was written to protect. Compare your case to it. If your case is far from that situation, deviating is probably fine. If it is close, the reason you write down should speak to it.

### How to read the stories

These stories are accounts of choices other engineers made, on their own judgment and with the information they had at the time. They are evidence, not rulings. Beware of reading one and seeing a foolish engineer behind it. Many of these stories are not cut-and-dry, and even where they are, every engineer who has been at this long enough, and looked honestly, has a story of their own where something they did looked foolish later, to them or to someone else. It is a hazard of the trade.

The principles below work the same way. Each one points to the story that shows it in practice.

## When to ask for help

Some rules name someone to ask. At the bottom of the rule, you'll see a line labeled Second opinion, followed by the person or role to check with, and it marks where a rule most wants another pair of eyes.

That doesn't make those the only times to ask. Ask for help whenever you want it. Explaining a decision to anyone, a teammate, a friend, or a rubber duck, often shows you the problem, and the data architect is always glad to be asked, about anything, however small.

## These docs are meant to be edited

These docs are not set in stone, and they are not here to be followed just because they were written down. They are here so we have something to edit.

That asks something of you beyond deviating for a good reason. You may find a rule that is flat wrong. You may meet a case nobody thought of, where the rules do not fit, or fit badly. Either one is welcome news, and we would count it a gift to hear it. It is how these pages get better. Tell the data architect what you found and why. A rough note is plenty.

You are on the hook for this, dear reader, and that includes an agent reading these rules. If a rule seems wrong for the case in front of you, say so plainly and say why. Do not apply it only because it is there.

## Where to look

The rules are split across pages by what you are doing. Start with the task, not with the object.

**Storing a piece of data.** Go to Columns. It covers how to name a column, how a column that points at another row is named, when a value may be null, how to store dates and times, how long a text column should be, how to store a value that comes from a fixed set, how to store money, and which values the database should maintain for you.

**Designing or changing a table.** Go to Tables. It covers how a table manages its rows (`created_at`, `updated_at`, and deleting), how to name a table, what identity a table needs (an `id`, and sometimes a `guid`), when a list belongs in an array and when in a second table, how to avoid storing a value that a view can derive, what to do when a table belongs to one of several parents, and when to add an index.

**Naming something that is not a table or a column.** Go to Other objects and tools. It covers databases and schemas, keys, constraints, and indexes, triggers, functions, procedures, and views, and roles and users.

**Naming anything at all.** Global Rules apply to every name: lowercase, underscores between words, no special characters, and the list of short forms Groups360 has approved. Every other page assumes them.

**Wanting a starting point for a standard table.** Stock tables holds the boilerplate tables Groups360 has settled on, starting with user uploads. It is a living page, and it has only begun to fill.

When what you are doing touches two pages, read both. The name of a column is on Columns, but the table it sits on and the index that may follow it are on Tables. Some topics are split on purpose, and the page that is not the home leaves a signpost. The standard columns every table carries are one example: Columns points to Tables, where the rule lives.

If someone points you to a rule by its slug, search the pages for it. And when nothing here fits your case, see When to ask for help.

## A note on scale

These rules grew up in an environment where our tables are modest in size, well within what Postgres handles easily. That is partly good fortune, and it shapes the advice. Some of it is comfortable at this size and may not be at much larger ones, and a few of our tables are already big enough to change the answer.

When a table is, or is about to become, far larger than the ones these rules were written around, stop and think twice before applying a rule as written, especially one that keeps rows around or adds work to every row. This is not a line to cross. It is a prompt to check the rule against your table, and to ask for help when the two do not fit.

---

## Principles

One idea sits underneath every rule in these docs, and four principles follow from it. When a rule's explanation says "see consistency is clarity", this is where it points.

### The first assumption should be correct
*slug: first-assumption-correct*

Here's a shortcut for making life easy: design around what is intuitive. When you misplace something new and finally find it, put it back in the first place you thought to look. That's empirically the most intuitive spot for it.

Data design works the same way. Wherever it is practical, the assumptions a newcomer makes on first looking at your data model should be correct.

*Evidence:* a concept that works fine, but lives somewhere nobody would think to look. (*story: guest-conversions*)

### Consistency is clarity
*slug: consistency-is-clarity*

Some of our paradigms may not be the best, but be careful when you decide to introduce a new one. Many people learn our structures once and then expect them everywhere. A new name or shape in one place makes everyone's first assumption wrong somewhere else, and that creates tribal knowledge.

**Consistency. is. clarity.**

*Evidence:* one renamed field, and every reader after it has to learn two answers. (*story: renamed-field*)

### Bend or break the rules in the name of clarity
*slug: bend-or-break*

The job of data conventions and naming conventions is to make our data more consistent and more readable. In every circumstance you can afford to, your data types, naming, and so on should be **intuitive** and easy to understand. The first thing someone thinks when looking at your data should be the truth, as much as you can afford for it to be.

So when do the rules we lay out in these documents get to be bent or broken? When doing so will make the data (or the code using the data) easier to read.

So bend the rules, even break them, if you are doing so in the name of clarity. Gut-check your choice with another engineer to make sure it really reads the way you think it does, and write down your reason.

*Evidence:* one bend that earned its keep (*story: hidden-vs-displayed*) and one that cost more than it gained (*story: renamed-field*).

### The database is the source of truth
*slug: database-is-source-of-truth*

At the end of the day, the database is our source of truth for our data. If the database doesn't enforce a constraint, then the constraint is only really an opinion delivered by other parts of our system, and it will stop existing when we change front end code, API code, anything else. Database constraints are true at the lowest level a thing can be true, and they are true forever.

If the database layer doesn't enforce something, it's not a standard, it's just a convention.

This is why so many of our rules are constraints and not advice: varchar limits, `NOT NULL`, real foreign keys, check constraints. We always end up adding the constraint at the database layer eventually. The only thing you do by not doing the work up front is pass the buck to someone else and multiply the number of man-hours required to fix it.

Database structures should also reflect the truth of your data. If an address has the same structure whether it belongs to a user or an org, the design should say so, and not hold two copies of the same table.

### Clever is seldom clear
*slug: clever-is-seldom-clear*

Engineers are smart, and smart people go looking for places to apply it. Reusing one column for a second job feels clever, and it usually is. But a clever trick saves its author a little effort and leaves the bill with whoever comes after, who never saw the trade. If a column means one thing on its face and another in practice, do not leave the second meaning hidden. If it is new information, give it a column of its own. If it can be worked out from what the table already holds, do not store it as a second copy: derive it, with a generated column when it depends only on the same row (*rule: same-row-value-generated-column*), or with a view when it depends on other tables (*rule: no-second-copy-use-a-view*).

*Evidence:* an image table used its `id` as the display order, and when the sync stopped rebuilding rows, photos of toilets became the first image at several hotels (*story: image-order*). A table saved by folding one concept into another was efficient, and hard for anyone to find (*story: guest-conversions*).

### When principles collide

Sometimes two of these pull against each other, and bending a rule for clarity can cost you consistency. Choose the option that keeps a newcomer's first assumption correct, and write down your reason.

---

## Stories

*hidden-vs-displayed* is told in full on the Columns page, beside the naming rule it explains.

### A field renamed in one place
*slug: renamed-field · serves: consistency-is-clarity, bend-or-break*

In the properties table, the `image_url` field probably should have been called `default_image_url` when it was created, since it stores the property's default image.

That naming exists across both an upstream database and a downstream one, and it works the same in both places. When the downstream one was created, the field was renamed `default_image_url` in that database and only that database. The change was almost certainly well-meant, an attempt to make things clearer than they were. But the structure of the properties table is something many, many people in the organization understand, and those who learn it for the first time are likely to learn it from the upstream database first and then discover it everywhere else.

That one naming change means the statement "the hero image of a property is stored on the `image_url` field" must continue "unless you are looking at the downstream database, in which case the name is different". This creates tribal knowledge. It makes people's first assumption wrong. That costs time and effort, and creates unnecessary frustration.

### Image order
*slug: image-order · serves: clever-is-seldom-clear, database-is-source-of-truth, first-assumption-correct, edit-in-place*

Hotels complained that their image carousel, the hero image plus the pictures of the lobby, the fountains, and so on, was showing pictures of toilets as the first image. By the fourth or fifth report it had reached the data team: toilets were being shown as the most important image at a hotel. The cause was a fix, made without a full picture of someone else's data model.

The image process had been built quickly, copying an existing one. It read from an image provider, worked out all the images for a hotel, and inserted them into an image table. Every run, it deleted all of that hotel's images and inserted a fresh set, whether or not anything had changed. Each day it scanned 10, 20, 30,000 hotels and replaced around 100 images for each, so the id values got very high.

Later, a complaint came in that images weren't being pulled often enough, or some other bug. While fixing it, the delete-everything behavior came to light, and the process was improved: insert a row only when there is a new image, and update the row when an existing image changes. The table stopped churning.

That is what caused the toilets. The table had no image-order column. The original programmers used the `id` as the display order. Since the rows were rebuilt every run, the id order effectively was the display order, so from their perspective it never caused a problem. But the id is a SQL identity, used for foreign keys and joins. It isn't meant to be load-bearing for what is presented to clients.

Once the rebuilding stopped, consider which pictures a hotel updates least often. The lobby gets redone at Christmas. Guest rooms get new linens, curtains, renovations. The last thing a hotel updates, and the last thing it even uploads new photos of, is the toilets. Those rows kept the lowest ids, the lowest ids were shown first, and so toilets were shown. It was a fun bug to track down.

An engineer saved maybe twenty minutes by not adding an image-order column and filling it in. It was a really clever trick, and genuinely clever. It just wasn't clever in a way that was useful.

### Where guest conversions live
*slug: guest-conversions · serves: first-assumption-correct, clever-is-seldom-clear*

Guest users are welcome in the system. But some activities, such as an RFP with its back-and-forth, require a guest to become a real user first, and a guest account has no way back by design. So the system needs to convert guests into real users. That ability existed for a long time, poorly implemented, and work began to formalize it.

Around the same time, a `user_logins` table was introduced to keep a full history of logins. The users table only held the most recent one. A conversion is, in effect, the moment a former guest logs in as a real user for the first time. So a design was proposed: add a column to `user_logins` holding the id of the guest a user was converted from. Most rows would leave it empty, and the rows that mark a conversion would carry the guest's id.

The case for that design is real. It needs no new table, it is simpler to implement, and it is sufficient, since everything about a conversion can be recovered from it.

The case against it is about who has to find it. Someone who wants to know how and why guests convert will look for something named for conversions. Nobody guesses the answer lives in the logins table. The only way to discover it is to scan the schema for a column like `converted_from_guest_user_id` and work out what it means. The design is efficient, and clever, and opaque to anyone who doesn't already know the trick. What it optimizes, one extra table, doesn't need optimizing, because data storage is cheap.

Conversions were given their own table.

This isn't a verdict. Folding one concept into another table can be the right call, for example when the concept really is just an attribute of the host row, or when the only people who will ever look for it already know where to look. The test is this: if someone who has never seen these tables went looking for the concept, where would they look first, and would they find it?
