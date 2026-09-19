# Deployment: making config persist on Docker / managed hosts

The lesson that wastes the most time: on managed platforms (Railway, Fly, many
Docker setups) **only the data volume `/var/lib/clickhouse` persists.**
`/etc/clickhouse-server/` lives on the container's ephemeral layer — anything you
write there (by hand or via `ssh`) **vanishes on the next redeploy/restart.**

That's why:
- `ALTER … MODIFY TTL` on system logs resets after a restart (the server
  recreates the log table from the *stock* config, which has no TTL).
- Config dropped via `ssh` into `config.d/` works until the next deploy, then is gone.

## The durable fix: bake config into a thin image

```dockerfile
# infra/clickhouse/Dockerfile
FROM clickhouse/clickhouse-server:25.12.3   # pin to the running version
COPY config.d/ /etc/clickhouse-server/config.d/
COPY users.d/  /etc/clickhouse-server/users.d/
```

Point the service at this Dockerfile (build context = this dir). On Railway:
`cd infra/clickhouse && railway up --ci --service <CHService> -e <env> -p <projectId>`
(or connect the repo + set root dir / Dockerfile path in the dashboard). A redeploy
is a ~5–30 s restart; if writers buffer (e.g. a queue/retry), there's no data loss.

Verify after boot: `SELECT version()`, then the settings/TTLs you set.

## config.d vs users.d (what goes where)

- **`config.d/*.xml`** — *server* config: system-log tables (TTL/level/disable),
  storage, merge settings, listen host.
- **`users.d/*.xml`** — *users / profiles / quotas*: query settings like the
  profiler, `max_memory_usage`, defaults per profile.

Merge attributes (essential — partial blocks otherwise *merge* with stock):
- `replace="1"` on a block → fully replace the stock definition.
- `remove="1"` on a block → delete it (e.g. disable a system log entirely).

```xml
<!-- config.d/log-tuning.xml -->
<clickhouse>
    <logger><level>information</level></logger>            <!-- merges: only overrides level -->
    <trace_log remove="1"/>                                <!-- disable profiler table entirely -->
    <text_log replace="1"><database>system</database><table>text_log</table>
        <level>warning</level><ttl>event_date + INTERVAL 3 DAY DELETE</ttl></text_log>
    <query_log replace="1"><database>system</database><table>query_log</table>
        <ttl>event_date + INTERVAL 14 DAY DELETE</ttl></query_log>
</clickhouse>
```

```xml
<!-- users.d/profiler-off.xml : stop trace_log at the source -->
<clickhouse><profiles><default>
    <query_profiler_real_time_period_ns>0</query_profiler_real_time_period_ns>
    <query_profiler_cpu_time_period_ns>0</query_profiler_cpu_time_period_ns>
</default></profiles></clickhouse>
```

## Stock-image users are XML-defined → can't `ALTER USER` them

The official image provisions the connecting user from env (`CLICKHOUSE_USER` /
`CLICKHOUSE_PASSWORD`) into `users.d/default-user.xml`. That user is **config-defined**,
so SQL like `ALTER USER … SETTINGS query_profiler_…=0` fails
(`Not enough privileges` / "cannot modify user defined in config"). Set
per-user / per-profile settings via a `users.d/*.xml` in the image instead.
(SQL-driven access control persists in `/var/lib/clickhouse/access/` only if
access management is enabled for the user — usually not on stock managed images.)

## `railway ssh` mangles `sh -c` (data-loss footgun)

`railway ssh -s X -- sh -c "cmd > file"` **word-splits the command**: `sh -c`
receives only the first token, the rest become positional params → redirections
and pipes silently no-op and you get a **0-byte file**. An empty `users.d/*.xml`
then breaks `SYSTEM RELOAD CONFIG` and can stop the server booting.

- For a one-shot command, use **direct argv**: `railway ssh -s X -- rm -f /path` (works).
- For anything with pipes/redirects/heredocs: **don't** — bake it into the image.
- If you already created a broken empty config file, remove it via direct argv and
  confirm `SYSTEM RELOAD CONFIG` parses clean before walking away.

## Quick health checks post-deploy

```sql
SELECT version();
SELECT name, value FROM system.settings WHERE name LIKE 'query_profiler%';   -- expect 0 if disabled
SELECT name FROM system.tables WHERE database='system' AND name='trace_log'; -- empty if removed
SELECT count() FROM your_table;                                              -- data intact
SELECT dateDiff('second', max(timestamp), now()) AS lag_s FROM your_table;   -- ingestion live
```
