# Stock tables

**This is a living document.** It holds boilerplate tables that can be lifted straight into a design, along with the reasons they are shaped as they are. It is only beginning. For now there is one.

## How to read a stock table

Every column and constraint is marked as a pillar or a suggestion. A pillar holds the design up, and taking it out stops the table from doing its job. A suggestion is useful, and it can be changed or dropped without bringing the design down. Where a choice follows a rule elsewhere in these docs, the note names the rule, so the reason is one step away.

A stock table is a starting point and not a mold. Copy it, then check it against the case in front of you.

---

## User uploads

### What this table is for

This table records files that a person uploads on behalf of an organization. It is not about how an upload is processed, with the bucket, the virus scan, and the move to a clean bucket. It is only the record that follows a file along the way.

Two columns carry the assumption that a person did the uploading on behalf of an organization: `org_guid` and `uploaded_by`. If files can also arrive from a machine, or only from a machine, rethink those two first, because a system has no organization and no user in the usual sense. Talk to the data architect before copying the table. What `uploaded_by` should hold when no user acted is an open question on Columns, and this table is not the place to improvise an answer.

### The table

```sql
CREATE TABLE uploads (
    id              bigint GENERATED ALWAYS AS IDENTITY,
    guid            uuid NOT NULL,
    org_guid        uuid NOT NULL,
    uploaded_by     uuid NOT NULL,
    filename        varchar(255) NOT NULL,
    content_type    varchar(255) NOT NULL,
    size_bytes      bigint NOT NULL,
    file_hash       varchar(64) NOT NULL,
    s3_uri          varchar(255) NOT NULL,
    status          varchar(20) NOT NULL DEFAULT 'pending',
    status_detail   varchar(255),
    created_at      timestamptz NOT NULL DEFAULT now(),
    updated_at      timestamptz NOT NULL DEFAULT now(),
    deleted_at      timestamptz,
    CONSTRAINT pk_uploads PRIMARY KEY (id),
    CONSTRAINT ctx_uploads_guid_unique UNIQUE (guid),
    CONSTRAINT ctx_uploads_status
        CHECK (status IN ('pending', 'clean', 'rejected', 'failed'))
);

-- Dedupe within an org. Files that never cleared a scan, or that were deleted, don't block a retry.
CREATE UNIQUE INDEX idx_uploads_org_guid_file_hash
    ON uploads (org_guid, file_hash)
    WHERE status IN ('pending', 'clean')
      AND deleted_at IS NULL;

-- updated_at is owned by the database, not the application. The function is the shared
-- ufn_set_updated_at, defined once per database (see Row lifecycle on Tables).
CREATE TRIGGER trg_uploads_set_updated_at
    BEFORE UPDATE ON uploads
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION ufn_set_updated_at();
```

### Column by column

| Column or constraint | Role | Why |
|---|---|---|
| `id` | Pillar | The identity every table carries. It never leaves the database. See Row identity on Tables. |
| `guid` | Pillar | What anything outside the database uses to refer to an upload. It is declared unique, which also gives it its index. The application generates it before the upload, so it can go into the S3 key and whatever consumes the scan result can find the row directly. The database does not generate it. It enforces that the value is present and unique. See Row identity on Tables. |
| `org_guid` | Pillar | The organization the file belongs to. It points at another service's data, so it is a guid with no foreign key. See the foreign key rule under Identifiers on Columns. |
| `uploaded_by` | Pillar | The user who uploaded the file, as a guid. See the `_by` rule on Columns. |
| `filename` | Suggestion | The name the file had when it was uploaded, kept for people to read. |
| `content_type` | Suggestion | The kind of file, such as `application/pdf`. |
| `size_bytes` | Suggestion | The size of the file, with the unit in the name so nobody has to guess. It is a `bigint` because a file can be larger than an `integer` holds. |
| `file_hash` | Pillar | A hash of the file's contents, used to recognize the same file twice. The dedupe index depends on it. Sixty-four characters is the length of a SHA-256 hash written in hex. If you are not using SHA-256, you may need to extend the limit. |
| `s3_uri` | Suggestion | Where the file lives. Some form of location is required, and the URI is the recommended form. If you store a key instead, you are making a deliberate choice, so know why you are not storing the URI. See why it is a URI below. |
| `status` | Pillar | Where the upload is on its path. It is one of four values: pending until the file is processed, clean once it has passed the scan, rejected if it did not, and failed if processing broke. A check constraint enforces the set and the default is `pending`. See Values from a fixed set on Columns. |
| `status_detail` | Suggestion | The most trimmable column in the table. See below. |
| `created_at`, `updated_at` | Pillar | The standard pair. The database keeps `updated_at` current through the shared trigger. See Row lifecycle on Tables. |
| `deleted_at` | Suggestion | Marks an upload as deleted without removing it, so the record of what was uploaded, and what happened to it, survives. It is null while the upload is live. An upload is forensic evidence, so the record is worth keeping. See soft delete under Row lifecycle on Tables. |
| `pk_uploads` | Pillar | The primary key, named by the pattern on Other objects and tools. |
| `ctx_uploads_guid_unique` | Pillar | Keeps every `guid` different. |
| `ctx_uploads_status` | Pillar | Keeps `status` inside its four values, at the lowest level where that can be true. |
| `idx_uploads_org_guid_file_hash` | Suggestion | Stops an organization from uploading the same file twice while an upload is still pending or clean. A file that was rejected, failed, or deleted does not count, so it can be uploaded again. Drop it if duplicates are fine. |
| `trg_uploads_set_updated_at` | Pillar | Keeps `updated_at` honest. It is the shared function and the trigger form from Row lifecycle on Tables, so an update that changes nothing leaves `updated_at` alone. |

### Why it is built this way

**A URI and not a key.** The table first stored an S3 key, with the bucket set for each environment. That made lower environments easy, and it also tied the table to one bucket. Storing the full URI means operations can place files in as many buckets as they like, for their own reasons, and the table does not care, because the only thing that matters is the value that whatever writes the row sets. Nothing should have permission to read from the bucket that holds files before they are scanned anyway, so a URI that points there is not a leak. This was argued back and forth for a while and is not a slam dunk, so treat it as a considered choice and not a rule.

**Why 255 for the URI.** The rule on Columns for a URL is `varchar(2048)`, which is about as big as a URL should be, and it says a smaller field is fine when the URL comes from something you control. Here Groups360 sets the value, so a tighter limit is a deliberate choice, set at a defensible low end. Going past 255 is allowed, and it should be a decision someone makes on purpose and not something that drifts. For reference, the largest legal S3 URI is 1,093 characters: 5 for `s3://`, up to 63 for the bucket name, 1 for the slash, and up to 1,024 bytes for the key. Raising the limit to 1,100 would hold any of them.

**`status_detail`.** The most trimmable column in the table, and kept on purpose as a challenge to it. It records, in a short sentence, how a row came to be in its status, in case someone needs to know. It is not a home for a stack trace, and 255 characters is enough for a reason. The database refuses a longer value, so whatever writes it truncates the message to the limit first, and an overlong message can never block a status update. A null means no detail was recorded. If it never earns its place, it is the first thing to cut.
