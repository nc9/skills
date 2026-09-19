---
name: clickhouse
description: Operate and evolve ClickHouse - disk/memory forensics, runaway trace_log/text_log cleanup and retention, codecs and LowCardinality, MergeTree ORDER BY/partition/TTL design, zero-downtime rebuilds with EXCHANGE TABLES, persistent config on Docker/Railway. Use when an instance is large or OOMing, or when designing or migrating a schema.
allowed-tools: Bash, Read, Write, Edit
---

# ClickHouse: operations, schema & migrations

Generic, battle-tested lessons for running and evolving ClickHouse — especially
MergeTree analytics tables on small or managed (Railway/Fly/Docker) instances,
where RAM is tight and you don't control the host config directly.

Connect however the project does. Two equivalent forms used throughout:
- **HTTP** (works anywhere, lets you pass per-query settings as URL params):
  `curl -s "https://HOST:PORT/?database=DB&SETTING=VAL" -H 'X-ClickHouse-User: U' -H 'X-ClickHouse-Key: P' --data-binary 'SELECT 1'`
- **client**: `clickhouse-client --host H --user U --password P -q 'SELECT 1'`

Append `FORMAT PrettyCompact` (human) or `FORMAT JSON`/`TSV` (parsing) to SELECTs.

## When to use

- An instance's disk is unexpectedly large / a volume is filling up.
- Queries fail with `MEMORY_LIMIT_EXCEEDED` / OvercommitTracker.
- Designing or optimizing a MergeTree table (compression, sort key, partition, TTL).
- Changing `ORDER BY`, dropping a column, or any table migration.
- Configuring system-log retention (trace_log / text_log / metric_log / …).
- Running ClickHouse on Docker or a managed host and config won't stick.

## Golden rules (the ones that bite hardest)

1. **"The DB is 500 GB" is usually not your data.** ClickHouse's own system logs
   (`trace_log`, `text_log`, `asynchronous_metric_log`, `part_log`, …) ship with
   weak/zero retention and grow unbounded; they routinely dwarf real tables.
   **Measure per-database/table before assuming.** → `server-ops.md`
2. **On a small box, aggregations OOM.** `count()`/`GROUP BY`/`uniqExact()` over
   tens of millions of rows blow the memory ceiling. Use `max_threads=1`,
   `uniq()` (HLL) not `uniqExact()`, filter on the sort-key prefix, or read
   **metadata** (`system.parts`) instead of scanning. → `server-ops.md`
3. **No codecs = default LZ4 = leaving 2–5× on the table.** `timestamp` →
   `Delta+ZSTD`; monotonic ints → `T64/Gorilla+ZSTD`; text → `ZSTD`;
   low-cardinality strings → `LowCardinality`. → `schema-design.md`
4. **Never put a random/high-entropy column (UUID) in `ORDER BY`.** It's
   incompressible and a unique tiebreaker buys nothing on plain MergeTree (it
   doesn't dedup). → `schema-design.md`
5. **You cannot shrink/reorder a sort key in place** (`MODIFY ORDER BY` only
   *appends*). Changing it = full table rebuild. → `migrations.md`
6. **Materialized views bind to their source by NAME** → `EXCHANGE TABLES` swaps
   the table under them and they keep firing *and* keep their rollups. This makes
   zero-downtime rebuilds possible. → `migrations.md`
7. **On managed hosts only the data volume persists.** `/etc/clickhouse-server`
   is ephemeral; config written there (or via `ssh`) vanishes on redeploy. Bake
   it into a thin image. → `deployment.md`

## First move when "ClickHouse is too big": measure, don't assume

All metadata — **no data scan, safe on an OOMing box**:

```sql
-- size per database (system vs your data)
SELECT database, formatReadableSize(sum(data_compressed_bytes)) AS comp,
       formatReadableSize(sum(data_uncompressed_bytes)) AS uncomp, sum(rows) AS rows
FROM system.parts WHERE active GROUP BY database ORDER BY sum(data_compressed_bytes) DESC;

-- top tables across all databases
SELECT database, table, formatReadableSize(sum(data_compressed_bytes)) AS comp, sum(rows) AS rows
FROM system.parts WHERE active GROUP BY database, table
ORDER BY sum(data_compressed_bytes) DESC LIMIT 20;

-- actual volume usage
SELECT name, formatReadableSize(total_space - free_space) AS used,
       formatReadableSize(free_space) AS free FROM system.disks;

-- per-column for one table: where the bytes are + compression ratio
SELECT column, formatReadableSize(sum(column_data_compressed_bytes)) AS comp,
       round(sum(column_data_uncompressed_bytes)/sum(column_data_compressed_bytes),1) AS ratio,
       round(sum(column_data_compressed_bytes)/(SELECT sum(rows) FROM system.parts
         WHERE active AND database='DB' AND table='T'),1) AS bytes_per_row
FROM system.parts_columns WHERE active AND database='DB' AND table='T'
GROUP BY column ORDER BY sum(column_data_compressed_bytes) DESC;
```

`ratio` near **1.0** = incompressible (random data — wrong codec or a UUID);
combine with bytes_per_row + % of table to pick what to fix first.

## Reference files

- **server-ops.md** — system-log bloat & retention, memory-limited query tuning,
  the `max_table_size_to_drop` guard, insert-vs-merge OOM, reclaiming space.
- **schema-design.md** — codecs, LowCardinality, ORDER BY / primary key,
  partitioning, TTL, type choices, what *not* to store.
- **migrations.md** — ALTER limits, the zero-downtime rebuild recipe
  (create → STOP MERGES → chunked backfill → watermark → EXCHANGE → tail-copy),
  materialized-view behavior, partial-insert recovery.
- **deployment.md** — config persistence on Docker/managed platforms, config.d vs
  users.d, disabling a system log, XML-defined users, the `railway ssh` footgun.
