---
slug: "junction-table-per-parent"
title: "When the parents are many or keep growing and integrity still matters, use one junction table per parent"
temperature: "Judgment call"
origin: "general"
scope: "table"
why: "polymorphic-associations"
page: "tables"
group: "Tables that belong to one of several parents"
companion: false
---

# When the parents are many or keep growing and integrity still matters, use one junction table per parent

Keep the core table lean and give each kind of parent a small table of its own that joins the two.

```sql
CREATE TABLE addresses (
  id     bigint GENERATED ALWAYS AS IDENTITY,
  street varchar(200) NOT NULL,
  city   varchar(100) NOT NULL,
  CONSTRAINT pk_addresses PRIMARY KEY (id)
);

CREATE TABLE user_addresses (
  id         bigint GENERATED ALWAYS AS IDENTITY,
  address_id bigint NOT NULL,
  user_id    bigint NOT NULL,
  CONSTRAINT pk_user_addresses            PRIMARY KEY (id),
  CONSTRAINT fk_user_addresses_address_id FOREIGN KEY (address_id) REFERENCES addresses (id),
  CONSTRAINT fk_user_addresses_user_id    FOREIGN KEY (user_id)    REFERENCES users (id),
  CONSTRAINT ctx_unique_address_user      UNIQUE (address_id, user_id)
);
```

Every foreign key is real. A new kind of parent is a new table, and nothing that already exists has to change, so there is no migration on a live table. If the link itself carries data, such as a timestamp, an order, or a status, that data has a natural home on the junction row. Name each junction table for the two things it joins, as under Naming tables on this page. Like every table it carries an `id`, and the unique constraint on the pair keeps the same link from being made twice, as under Row identity.

The cost is more tables. Finding out what a row is attached to means checking several of them and not reading one row. For a small, stable set of parents that is more infrastructure than the problem needs, which is why this is not the default.

Because: when there are many parents and a dangling reference would do real harm, the extra tables are what it costs to keep the database enforcing the relationship.
