# Server operations: logs, memory, disk

## System-log bloat (the #1 "why is it huge" cause)

ClickHouse writes its own observability into `system.*_log` MergeTree tables. On
the stock image several ship with **no TTL** and the logger at `trace`, so they
grow forever and can be 10–100× your real data.

The usual offenders, worst first:

| table | what it is | typical fix |
|---|---|---|
| `trace_log` | query/memory **profiler** stack samples (flamegraphs) | **disable** unless profiling |
| `text_log` | the server log mirrored into a table | level → `warning`, short TTL |
| `asynchronous_metric_log` | ~hundreds of metrics every few seconds (huge row count) | short TTL |
| `part_log`, `query_log`, `query_views_log`, `metric_log`, `processors_profile_log` | merges / queries / MV / metrics | TTL 7–14d |

Check which logs lack retention:

```sql
SELECT name, engine, (position(create_table_query,'TTL')>0) AS has_ttl
FROM system.tables WHERE database='system' AND name LIKE '%_log%' ORDER BY name;
```

Get their sizes from metadata (don't scan — these can be billions of rows and
will OOM on `count()`):

```sql
SELECT table, formatReadableSize(sum(bytes_on_disk)) AS disk, sum(rows) AS rows
FROM system.parts WHERE active AND database='system' AND table LIKE '%_log'
GROUP BY table ORDER BY sum(bytes_on_disk) DESC;
```

### Reclaiming the space NOW

`TRUNCATE TABLE system.trace_log` is instant (drops parts, no RAM). But ClickHouse
guards big drops:

```
TABLE_SIZE_EXCEEDS_MAX_DROP_SIZE_LIMIT … max_table_size_to_drop (50 GB)
```

Override **per-query** (HTTP URL param or `SETTINGS`) — no server config change:

```
curl ".../?max_table_size_to_drop=0&max_partition_size_to_drop=0" --data-binary 'TRUNCATE TABLE system.trace_log'
```

(Other escapes: raise the setting in config, or `touch /var/lib/clickhouse/flags/force_drop_table`.)

### Stopping regrowth (durable)

`ALTER TABLE system.trace_log MODIFY TTL event_date + INTERVAL 3 DAY` works **but
resets on restart** if the server recreates the log table from config (schema
mismatch → it renames yours to `trace_log_0`/`_1` and makes a fresh no-TTL one;
those `_N` shadow tables are the tell). The durable fix lives in **config** —
see `deployment.md`. Pattern:

```xml
<clickhouse>
  <trace_log remove="1"/>                                   <!-- disable entirely -->
  <text_log replace="1"><database>system</database><table>text_log</table>
    <level>warning</level><ttl>event_date + INTERVAL 3 DAY DELETE</ttl></text_log>
  <asynchronous_metric_log replace="1">…<ttl>event_date + INTERVAL 3 DAY DELETE</ttl></asynchronous_metric_log>
</clickhouse>
```

Notes:
- **`trace_log` is profiler-only** — flamegraph data for debugging a slow query,
  read by nothing in normal operation. If you don't profile, `remove="1"` it.
  Caveat: it fills even with the *query* profiler off, because **background
  merge/mutation threads still get sampled** — disabling the table is the airtight fix.
- After `remove="1"`, drop the now-orphaned table once to reclaim: `DROP TABLE system.trace_log`.
- `text_log` huge ⇒ the server is logging at `trace`/`debug`. Gate the **table** to
  `warning` and/or lower `<logger><level>` to `information`.

## Memory-limited instances (queries OOM)

Symptom: `Code 241 … MEMORY_LIMIT_EXCEEDED … OvercommitTracker`. The whole-server
RAM ceiling (often 2–4 GB on managed tiers) is shared across queries **and**
background merges. Even a bare `count()` over 80M rows can fail.

Tactics, cheapest first:
- **Read metadata, not data.** Sizes/row-counts/date-ranges live in
  `system.parts`, `system.parts_columns`, `system.tables.total_bytes`,
  `system.disks` — zero scan.
- **`max_threads=1`** (URL param or `SETTINGS`) — fewer parallel read buffers.
  Often the single thing that turns an OOM into a result.
- **`uniq()` not `uniqExact()`** — HLL uses ~KB; exact builds a full hash set.
  Running many `uniq()` in one SELECT still OOMs — split into separate queries.
- **Prune via the sort-key prefix.** A `WHERE` on the leading `ORDER BY` column
  reads almost nothing; a `WHERE` on a non-indexed column scans everything.
- **Window the scan**: `WHERE timestamp >= now() - INTERVAL 7 DAY` for estimates.
- **Smaller blocks**: `max_block_size=16384` lowers per-block memory.

## Insert-vs-merge contention (bulk loads OOM)

A large `INSERT … SELECT` **plus** a background merge firing mid-insert exceeds
the ceiling together — even modest chunks fail intermittently while the box looks
idle between them. For any bulk backfill on a small box:

```sql
SYSTEM STOP MERGES;     -- pause merges for the whole load
-- … chunked INSERT … SELECT (parts just accumulate harmlessly) …
SYSTEM START MERGES;    -- compaction catches up afterwards
```

Short-term part accumulation is fine (watch `parts_to_throw_insert`, default
3000 — you won't get near it). See `migrations.md` for the full chunked recipe.

## Cheap, safe inspectors

```sql
SELECT metric, formatReadableSize(value) FROM system.metrics WHERE metric='MemoryTracking';
SELECT count() AS merges, formatReadableSize(sum(memory_usage)) AS mem FROM system.merges;
SELECT database, table, mutation_id, latest_fail_reason FROM system.mutations WHERE NOT is_done;
-- kill a stuck/ OOMing mutation:
KILL MUTATION WHERE database='DB' AND table='T' AND NOT is_done;
```
