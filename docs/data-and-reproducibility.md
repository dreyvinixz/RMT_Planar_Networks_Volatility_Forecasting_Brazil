# Data and reproducibility

## Data policy

The public repository distributes no raw B3 price data. Market data can be subject to contractual, exchange, vendor, or database-specific terms. Before reproducing an analysis, obtain the data from an authorised source and retain its provenance, licence, retrieval date, and adjustment methodology.

The tracked `config/assets_universe.yaml` defines the intended asset universes and study windows. It is a methodological specification, not a data redistribution.

## Expected daily-candle schema

The scripts expect the configured ClickHouse table to provide at least:

| Column | Use |
| --- | --- |
| `date` | Trading date |
| `symbol` | B3 ticker/symbol |
| `company_name` | Issuer label used in tables and figures |
| `adj_close` | Adjusted closing price used for return calculations |
| `close` | Unadjusted close used in validation |
| `volume` | Trading volume |
| `financial_volume` | Financial-volume field used for liquidity selection |

The universe-selection stage also uses source metadata such as `cod_bdi` and `specification`; adapt that query if your provider uses different column names.

## Reproduction checklist

1. Record the source, retrieval date, adjustment rules, timezone and corporate-action treatment.
2. Load a compatible table into ClickHouse and create `config/clickhouse.toml` from the example file.
3. Run `python scripts/python/00_check_clickhouse.py` and resolve any schema or quality differences.
4. Run the numbered scripts in order, retaining the generated outputs with the code commit and configuration used.
5. Report sample dates, assets, preprocessing choices, model splits and random seeds alongside any result.

## Output and release policy

`outputs/`, `logs/`, `tmp/`, downloaded literature and manuscript workspaces are local working artefacts. Do not commit them by default. When results must be shared, publish a deliberate release archive with:

- the Git commit or tagged version;
- the exact configuration and asset-universe version;
- a data-provenance statement;
- checksums for any sharable derived artefacts; and
- the licences or permissions that allow redistribution.

Never commit credentials, proprietary data, access tokens, or unlicensed research papers.
