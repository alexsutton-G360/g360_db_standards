---
slug: "choose-fixed-set-mechanism"
title: "Choose how to enforce a fixed set by asking what each value carries"
temperature: "Judgment call"
origin: "general"
scope: "column"
why: "constrained-values"
page: "columns"
group: "Values from a fixed set"
companion: false
---

# Choose how to enforce a fixed set by asking what each value carries

Start with one question: does each value carry anything with it, such as a display label, a sort order, an active flag, or a description, or is it only a string that must be one of the set?

- Use a lookup table with a foreign key when the values carry something, or when the set is likely to expand regularly. Adding a value is then an insert and not a change to the table's structure. The code stays stable, the label can change, and a value is retired by marking it inactive.
- Use a check constraint on a varchar, or an enum, when each value is only a string and the set rarely changes. Booking statuses are the standard example.

A booking shows both. It has a status, and it can have a cancellation reason.

A cancellation reason carries things with it. Staff pick from a dropdown, so each reason has a label and a place in the order. An old reason has to be retired without breaking the bookings that used it, so each has an active flag. And support will keep asking for new ones. That is a lookup table.

```sql
CREATE TABLE cancellation_reasons (
  id         bigint GENERATED ALWAYS AS IDENTITY,
  code       varchar(30)  NOT NULL,
  label      varchar(100) NOT NULL,
  sort_order integer      NOT NULL,
  is_active  boolean      NOT NULL DEFAULT true,
  CONSTRAINT pk_cancellation_reasons PRIMARY KEY (id),
  CONSTRAINT ctx_unique_cancellation_reason_code UNIQUE (code)
);

ALTER TABLE bookings
  ADD COLUMN cancellation_reason_id bigint,
  ADD CONSTRAINT fk_bookings_cancellation_reason_id
    FOREIGN KEY (cancellation_reason_id) REFERENCES cancellation_reasons (id);
```

Adding a reason is an insert, and retiring one is an update. Neither changes the structure of any table, and neither needs a deploy.

```sql
INSERT INTO cancellation_reasons (code, label, sort_order)
VALUES ('weather', 'Weather event', 40);

UPDATE cancellation_reasons SET is_active = false WHERE code = 'duplicate_booking';
```

The label can be reworded at any time, because a booking holds only the `id`. The `code` is the stable handle for people and queries, and the unique constraint keeps it that way. The column on `bookings` is nullable because a booking that was not cancelled has no reason, which is a real answer (*rule: not-null-until-null-has-meaning*).

A booking status is only a string. There are a few values, the set rarely changes, and none of them carries anything else. A check constraint is enough.

```sql
ALTER TABLE bookings
  ADD COLUMN status varchar(20) NOT NULL DEFAULT 'draft',
  ADD CONSTRAINT ctx_status_values
    CHECK (status IN ('draft', 'hold', 'confirmed', 'cancelled'));
```

A value outside the set, such as a misspelled `'confrimed'`, is refused. No second table or join is needed to make that true.

The check constraint and the enum cost different things. A check constraint leaves the column an ordinary varchar, and changing the set means replacing the constraint. An enum is its own type. A value can be added or renamed but not dropped. A new value cannot be used until the transaction that adds it commits. `LIKE` needs a cast to text, and values sort in the order they were declared, not alphabetically. Moving a column onto an enum, or from one enum type to another, rewrites the table. Costs like these grow with the size of the table. See the note on scale on the Index.

For a column that has three states only because one of them means unknown, see the nullable boolean rule under Nullability.
