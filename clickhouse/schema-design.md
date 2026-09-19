# Schema design: compression, sort key, partitions, TTL

Default MergeTree columns use **LZ4, no codec, no dictionary**. A typical
analytics table leaves 2–5× on the floor. Diagnose with the per-column
`ratio` + `bytes_per_row` query in `SKILL.md`, then apply the below.

## Codecs (biggest disk wins)

Codecs are storage-only (insert format unchanged) and apply to **new parts only**
(`MODIFY COLUMN … CODEC` rewrites that column; or they take effect on backfill).

| column kind | codec | why |
|---|---|---|
| `DateTime`/`DateTime64` | `CODEC(Delta(8), ZSTD(1))` | sorted/near-monotonic → tiny deltas; often **5–10×** |
| monotonic / small-range ints (durations, counts) | `CODEC(T64, ZSTD(1))` or `Gorilla` | bit-packs the range |
| high-cardinality text (path, url, user_agent, ip) | `CODEC(ZSTD(1))` | ~30–50% better than LZ4 on text |
| already-tiny / low-card | prefer `LowCardinality` (below) | — |

```sql
ALTER TABLE t MODIFY COLUMN ts DateTime64(3, 'UTC') CODEC(Delta(8), ZSTD(1));
ALTER TABLE t MODIFY COLUMN duration_ms UInt32 CODEC(T64, ZSTD(1));
```

A column with **ratio ≈ 1.0** is incompressible: it's random (UUID/hash — wrong
to store sorted) or already-compressed bytes. No codec helps; reconsider the column.

## LowCardinality (dictionary encoding)

Wrap a `String`/number whose **distinct count is « ~100K**:
`domain`, `hostname`, `country_code`, `colo/region`, `city`, `referrer_domain`,
`os`, `browser`, status enums.

```sql
domain LowCardinality(String), country_code LowCardinality(String)
```

Wins twice: smaller on disk **and faster `GROUP BY`** (the dashboards group by
exactly these). **Anti-pattern** for genuinely high-cardinality columns
(`ip`, `path`, full URLs, free text) — the dictionary becomes huge and adds
overhead; keep those `String` + `ZSTD`. When unsure, `uniq(col)` (one at a time
on a small box) — under ~10⁵ ⇒ LowCardinality.

Prefer `LowCardinality(String)` over `FixedString(n)` for short codes
(e.g. country) — it GROUPs faster and avoids padding quirks.

`Enum8`/`Enum16` for a tiny fixed set (response types, states) — 1–2 bytes, validated.

## ORDER BY / primary key

The sort key drives both the sparse primary index **and** physical ordering
(hence compression locality). Rules:

- Lead with the column you filter/group by most and that has **low cardinality**
  (e.g. `domain`), then `timestamp`. `ORDER BY (domain, timestamp)`.
- **Never end the key with a random/unique column** (a `UUID` "row id"). It's
  incompressible and adds nothing — plain `MergeTree` does **not** require a
  unique sort key and does **not** dedup. (If you need dedup, that's
  `ReplacingMergeTree` keyed deliberately — not a random tiebreaker.)
- Don't over-stuff the key with high-cardinality columns; it bloats the index and
  hurts compression of trailing columns.
- Changing `ORDER BY` later is expensive (`MODIFY ORDER BY` only **appends**) → get
  it right, or plan a rebuild (`migrations.md`).

## Partitioning & TTL

- `PARTITION BY toYYYYMM(timestamp)` is the analytics default — monthly parts make
  retention drops and time-range pruning cheap. **Don't** partition by something
  high-cardinality (per-day on years of data, or by id) → too many parts.
- **Retention** via TTL: `TTL timestamp + INTERVAL 1 YEAR` — old parts auto-drop in
  background merges. Caps steady-state size; pairs with monthly partitions.
- Tiered TTL (move cold parts to cheap storage) needs an S3-backed disk; on a
  single-volume managed host, plain `DELETE` TTL is what you've got.

## Don't store what you can derive

`full_url` = `hostname || path || query_string`. Storing all four duplicates the
fattest one. Keep the parts; reconstruct on read (`concat(...)`) if ever needed.
In one real table `full_url` was ~24% of bytes for zero query use.

## Worked example (what a good analytics row looks like)

```sql
CREATE TABLE events (
    timestamp        DateTime64(3, 'UTC')   CODEC(Delta(8), ZSTD(1)),
    domain           LowCardinality(String),
    hostname         LowCardinality(String),
    path             String                 CODEC(ZSTD(1)),
    response_type    Enum8('redirect'=1,'for_sale'=2,'fallback'=3,'parked'=4),
    cache_hit        Bool DEFAULT false,
    ip               String                 CODEC(ZSTD(1)),
    country_code     LowCardinality(String) DEFAULT '',
    user_agent       String                 CODEC(ZSTD(1)),
    duration_ms      UInt32 DEFAULT 0        CODEC(T64, ZSTD(1))
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(timestamp)
ORDER BY (domain, timestamp)     -- no random id tail
TTL timestamp + INTERVAL 1 YEAR;
```

Real result of applying all of the above to an existing 82M-row table:
**3.88 GiB → 0.92 GiB (≈4.3×), overall ratio 7 → 16** — dropping a UUID `event_id`
(32%, incompressible) and a derivable `full_url` (24%) accounted for most of it,
codecs + LowCardinality the rest.
