# Give a table that belongs to one of several parents one nullable foreign key per parent, and a check that exactly one is set

Rule line `RDBRL3` in `db_relationship_conventions.md`. Temperature: Default. Origin: general.

## Full rule

Add one column for each possible parent, each a real foreign key, and a check constraint that counts how many are filled in.

```sql
CREATE TABLE addresses (
  id      bigint GENERATED ALWAYS AS IDENTITY,
  street  varchar(200) NOT NULL,
  city    varchar(100) NOT NULL,
  user_id bigint,
  org_id  bigint,
  CONSTRAINT pk_addresses         PRIMARY KEY (id),
  CONSTRAINT fk_addresses_user_id FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT fk_addresses_org_id  FOREIGN KEY (org_id)  REFERENCES orgs (id),
  CONSTRAINT ctx_exactly_one_parent
    CHECK (num_nonnulls(user_id, org_id) = 1)
);
```

Every filled-in column is a real, enforced foreign key. A parent that does not exist is rejected, a parent that still has addresses cannot be deleted by accident, and the database knows what each column means. The check does the job that would otherwise fall to application code, on every write, whatever the application does. If a row is allowed to belong to no parent, change `= 1` to `<= 1`.

These columns are nullable for a reason the nullability rule on Columns accepts. Here null means "this address is not attached to a user", which is a real answer: that parent does not apply to this row. The check constraint keeps it honest. The nulls are there on purpose, and the constraint makes sure no row has the wrong number of them. Whatever the count is, exactly one or at most one, say it in the constraint.

Adding a new kind of parent takes an `ALTER TABLE`, a new nullable column with its foreign key, and a replacement check constraint. That is a migration on a live table and needs care, and the larger the table, the more care. See the note on scale on the Index. If the parents keep multiplying, see the junction-table chunk below.

Because: the database is the lowest level at which something can be true, and a check constraint enforces this on every write, for good.
