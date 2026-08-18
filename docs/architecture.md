# Architecture

## Overview

The repository separates reusable research logic from numbered pipeline stages:

```text
ClickHouse daily candles
        ↓
config/assets_universe.yaml
        ↓
scripts/python/00–02  →  validation, universe selection and log returns
        ↓
scripts/python/03–06  →  stylized facts, correlation structure and RMT
        ↓
scripts/python/07–12  →  clustering and financial networks
        ↓
scripts/python/13–21  →  volatility forecasts, robustness and appendices
        ↓
outputs/              →  local figures, tables and network files
```

## Reusable modules

| Module | Responsibility |
| --- | --- |
| `src/db.py` | Loads local ClickHouse configuration and creates database clients. |
| `src/data_loader.py` | Loads validated daily prices for a selected universe. |
| `src/returns.py` | Computes and summarizes log returns. |
| `src/correlations.py` | Correlation and rolling-dependence calculations. |
| `src/rmt.py` | Random Matrix Theory decomposition and filtering. |
| `src/networks.py` | MST, PMFG and network-statistics utilities. |
| `src/plotting.py` | Shared plotting configuration and figure helpers. |
| `src/utils.py` | General research utilities. |

## Configuration

`config/assets_universe.yaml` is versioned because it records the sample definitions used by the research. `config/clickhouse.toml` is local-only because connection details and table locations depend on the researcher’s environment. Start from `config/clickhouse.example.toml`.

The database configuration can be overridden through `B3_ECONOPHYSICS_CONFIG`. Individual connection values can be overridden by `B3_CH_HOST`, `B3_CH_PORT`, `B3_CH_USERNAME`, `B3_CH_PASSWORD`, and `B3_CH_DATABASE`.

## Output contract

Scripts may consume outputs from earlier stages and write derived data below `outputs/`. This directory is intentionally untracked: it can be large, depends on licensed market data, and is reproducible from the configured source data. A release or paper-specific archive can be published separately with a versioned data manifest.
