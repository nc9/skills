# Migrations: ALTER limits & the zero-downtime rebuild

## What ALTER can and can't do

| change | how | cost |
|---|---|---|
| add column | `ALTER … ADD COLUMN IF NOT EXISTS c T DEFAULT d` | metadata, cheap |
| drop column | `ALTER … DROP COLUMN IF EXISTS c` | metadata + bg file removal, cheap |
| change codec | `ALTER … MODIFY COLUMN c T CODEC(...)` | **rewrites that column** (mutation) |
| change type | `ALTER … MODIFY COLUMN c NewT` | mutation if not bit-compatible |
| **extend** sort key | `ALTER … MODIFY ORDER BY (old…, newcol)` | only **appends**; column must already exist & be in PK-compatible position |
| **shrink/reorder** sort key | ❌ not possible in place | → **full rebuild** |
| change `PARTITION BY` | ❌ not possible in place | → **full rebuild** |

So: dropping a column that's *in* `ORDER BY`, removing/reordering sort-key
columns, or re-partitioning all require building a new table and swapping.

Mutations (`MODIFY`/`DELETE`) run in background and can OOM on a small box —
watch `system.mutations`; `KILL MUTATION WHERE NOT is_done` to abort a stuck one.
Note: a mutation triggered by `ALTER MODIFY TTL` on a *populated* table tries to
rewrite everything at once (can OOM); set TTL on an **empty** table, or via config.

## The zero-downtime rebuild recipe

Use to change `ORDER BY`, drop sort-key columns, re-partition, or apply
codecs/LowCardinality across the whole table — while it's being written to.

**Key fact that makes it safe: materialized views bind to their source table by
NAME.** After `EXCHANGE TABLES a AND b`, inserts into (the now-swapped) `a` fire
the MVs that targeted `a`, and the MVs keep their existing rollup/inner tables —
**no POPULATE, no recreation, no rollup loss.** Verify on throwaway tables for
your version before trusting it on prod (recipe at the bottom).

```sql
-- 0) (optional) confirm no MV references the columns you're dropping
SELECT name, multiSearchAnyCaseInsensitive(create_table_query, ['col_to_drop'])
FROM system.tables WHERE database='DB' AND engine='MaterializedView';

-- 1) new table with the target schema (new ORDER BY / codecs / LowCardinality)
CREATE TABLE events_new ( … ) ENGINE=MergeTree PARTITION BY toYYYYMM(timestamp)
ORDER BY (domain, timestamp) TTL timestamp + INTERVAL 1 YEAR;

-- 2) stop merges so the backfill doesn't contend with merges (small-box OOM guard)
SYSTEM STOP MERGES;

-- 3) backfill in CHUNKS (per month/day). Big single INSERT…SELECT OOMs; chunk it.
--    list the EXACT columns (omit dropped ones, cast changed types, e.g. toString(country_code)).
INSERT INTO events_new (c1,c2,…) SELECT c1,c2,… FROM events
WHERE toYYYYMM(timestamp)=202601;
-- … repeat per partition; if a month still OOMs, split by toDayOfMonth ranges …

-- 4) watermark = newest row that made it into the copy
SELECT max(timestamp) FROM events_new;     -- call it W

-- 5) atomic swap (metadata-only, no downtime)
EXCHANGE TABLES events AND events_new;      -- now events=new, events_new=old data

-- 6) tail-copy rows that arrived in the old table during the backfill
INSERT INTO events (c1,c2,…) SELECT c1,c2,… FROM events_new WHERE timestamp > 'W';

-- 7) resume merges
SYSTEM START MERGES;
```

Then verify, keep the old table as a rollback net, and drop it later:

```sql
SELECT (SELECT count() FROM events) AS new, (SELECT count() FROM events_new) AS old_backup;
SELECT max(timestamp), dateDiff('second', max(timestamp), now()) AS lag_s FROM events;  -- ingestion live?
SELECT max(bucket) FROM some_mv;                                                        -- MVs still firing?
RENAME TABLE events_new TO events_pre_rebuild_bak;   -- clarity; DROP when confident
```

### Caveats / gotchas

- **`INSERT … SELECT` is not atomic across blocks.** A mid-statement OOM leaves
  *partial* parts in the target partition (and possibly partial-row dupes if you
  retry the same range). Recover: `ALTER TABLE events_new DROP PARTITION 202603`
  then re-run that month (ideally with merges stopped + smaller chunks).
- **Tail-copy boundary**: `> W` may miss a handful of rows whose event-time ≤ W
  but which were inserted after the snapshot (out-of-order/late). For analytics
  that's negligible; the MVs saw every insert at insert-time so **rollups stay
  exact** regardless of the few raw rows.
- **Type changes in the backfill SELECT**: cast explicitly
  (`toString(country_code)` for FixedString→LowCardinality(String)); JSONEachRow
  inserts coerce, but `INSERT…SELECT` is stricter.
- **Update the schema source-of-truth** (your app's `CREATE TABLE` DDL / migration
  list). If a startup migration still does `ADD COLUMN full_url`, it silently
  re-adds the column you just dropped — replace it with `DROP COLUMN IF EXISTS`.

### Verify MV-after-EXCHANGE on your version first (cheap throwaway test)

```sql
CREATE TABLE _t (d String, x UInt32) ENGINE=MergeTree ORDER BY d;
CREATE MATERIALIZED VIEW _tmv ENGINE=SummingMergeTree ORDER BY d AS SELECT d,count() c FROM _t GROUP BY d;
INSERT INTO _t VALUES ('a',1),('a',2),('b',3);                 -- _tmv: a=2, b=1
CREATE TABLE _t2 (d String, x UInt32) ENGINE=MergeTree ORDER BY (d,x);
INSERT INTO _t2 SELECT * FROM _t;
EXCHANGE TABLES _t AND _t2;
INSERT INTO _t VALUES ('a',9);                                 -- into swapped-in table
SELECT d, sum(c) FROM _tmv GROUP BY d;                         -- a=3 ⇒ MV FIRED (good); a=2 ⇒ broke
DROP VIEW _tmv; DROP TABLE _t; DROP TABLE _t2;
```
