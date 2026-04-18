---
name: modern-data-stack
description: "Modern OLAP/analytics data stack: DuckDB (embedded OLAP), Apache Arrow (columnar format), Apache Iceberg / Delta Lake / Apache Hudi (table formats), ClickHouse, Polars, dbt, Parquet. Zero-copy interop, lakehouse patterns. Triggers on DuckDB, Arrow, Iceberg, Delta Lake, Hudi, ClickHouse, Parquet, lakehouse, columnar analytics."
category: databases
tags: [duckdb, arrow, iceberg, delta-lake, clickhouse, parquet, lakehouse]
---

# Modern Data Stack

## Stack map

| Layer | Tools |
|-------|-------|
| **In-process OLAP** | DuckDB |
| **Columnar format** | Apache Arrow, Parquet |
| **Table format** | Apache Iceberg, Delta Lake, Apache Hudi |
| **Distributed OLAP** | ClickHouse, StarRocks, Pinot |
| **DataFrames** | Polars, pandas 2 (PyArrow-backed), Dask |
| **Transformation** | dbt, SQLMesh |
| **Streaming** | Apache Flink, RisingWave, Materialize |

## DuckDB

In-process SQL OLAP. "SQLite for analytics." Single binary / Python / R / Node.

```python
import duckdb
con = duckdb.connect("db.duckdb")
# Query Parquet / CSV / JSON / Postgres / Iceberg directly
con.sql("SELECT name, SUM(price) FROM 's3://bucket/*.parquet' GROUP BY name").df()
# Arrow zero-copy
arrow_table = con.sql("SELECT * FROM big_table").arrow()
# Attach another DB
con.sql("ATTACH 'postgres://...' AS pg")
```

Features:
- Vectorized engine, multi-threaded
- Reads Parquet, CSV, JSON, Arrow, Postgres, MySQL, SQLite, Iceberg, Delta, S3
- Full SQL (window fns, CTEs, recursive, Postgres-compatible)
- Export formats: Parquet, Arrow, pandas, Polars
- `httpfs` for direct cloud reads without download

Typical use: replaces pandas for >1 GB data, replaces BigQuery/Snowflake for single-node.

## Apache Arrow

In-memory columnar format — zero-copy between languages and tools.

```python
import pyarrow as pa, pyarrow.parquet as pq
t = pa.table({"x": [1,2,3], "y": ["a","b","c"]})
pq.write_table(t, "out.parquet", compression="zstd")
# Zero-copy to pandas / Polars / DuckDB
df = t.to_pandas()
pl_df = pl.from_arrow(t)
```

Arrow Flight: high-speed RPC for Arrow data (replaces ODBC for columnar use).

## Parquet

Columnar on-disk format. 5-20× smaller than CSV, 10-100× faster scans. Default for all lakehouse tools.

Column chunk → row group → file. Predicate pushdown + column pruning → read only needed bytes.

## Lakehouse table formats

Metadata layer on top of Parquet files providing ACID, schema evolution, time travel, partitioning.

| Feature | Iceberg | Delta Lake | Hudi |
|---------|---------|------------|------|
| Origin | Netflix / Apache | Databricks | Uber / Apache |
| Transactions | snapshot isolation | optimistic | MVCC |
| Schema evolution | yes | yes | yes |
| Partition evolution | yes | no | no |
| Time travel | yes | yes | yes |
| Catalog | REST, Glue, Hive, Nessie | Unity, Glue, Hive | Hive |

### Iceberg quick
```sql
-- Via DuckDB, Trino, Spark, Flink, Athena
CREATE TABLE events (ts TIMESTAMP, user_id BIGINT, ...)
PARTITIONED BY (days(ts));
SELECT * FROM events VERSION AS OF 12345;
```

### Delta Lake
```python
from deltalake import write_deltalake, DeltaTable
write_deltalake("s3://bucket/events", df)
dt = DeltaTable("s3://bucket/events")
dt.vacuum(retention_hours=168)
df_v5 = DeltaTable("s3://bucket/events", version=5).to_pandas()
```

## ClickHouse

Distributed columnar OLAP for real-time analytics. ~100× faster than Postgres on aggregations.

```bash
docker run -p 9000:9000 clickhouse/clickhouse-server
```

```sql
CREATE TABLE events (
  ts DateTime, user_id UInt64, event LowCardinality(String)
) ENGINE = MergeTree ORDER BY (ts, user_id);
```

Typical query latency: sub-second on billions of rows. Excellent for: product analytics, telemetry, time-series.

## Polars

Rust-backed dataframes. 10-100× faster than pandas, lazy evaluation.

```python
import polars as pl
df = pl.scan_parquet("s3://bucket/*.parquet")    # lazy
result = (
  df.filter(pl.col("price") > 100)
    .group_by("category")
    .agg(pl.col("qty").sum())
    .collect(streaming=True)
)
```

## When what

| Need | Pick |
|------|------|
| Single-file / single-node analytics | DuckDB |
| Cross-language in-memory data | Arrow |
| Efficient on-disk columnar storage | Parquet |
| Data lake with ACID | Iceberg (vendor-neutral) |
| Databricks shop | Delta Lake |
| Streaming upserts | Hudi |
| Real-time user-facing analytics | ClickHouse |
| Python dataframes replacement | Polars |

## Zero-copy interop

```python
import polars as pl, duckdb, pandas as pd, pyarrow as pa
pl_df = pl.read_parquet("f.parquet")       # Rust arrow under hood
arrow = pl_df.to_arrow()                    # zero-copy
pd_df = arrow.to_pandas(types_mapper=pd.ArrowDtype)   # PyArrow-backed pandas
duckdb.sql("SELECT * FROM arrow").show()
```

## References
- duckdb.org/docs
- arrow.apache.org
- iceberg.apache.org
- delta.io
- clickhouse.com/docs
- pola.rs
