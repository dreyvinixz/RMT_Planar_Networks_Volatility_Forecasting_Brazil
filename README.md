# RMT Planar Networks & Volatility Forecasting — Brazil

Open research code for studying the Brazilian equity market through econophysics, complex networks, and volatility forecasting.

The project analyzes daily B3 equity returns with a reproducible Python workflow: stylized facts, correlation structure, Random Matrix Theory (RMT), hierarchical clustering, financial networks, and out-of-sample volatility forecasts.

![Conceptual visualization of spectral structure, planar networks and volatility](assets/readme-hero.png)

*Conceptual visual only — it is not a result, chart or dataset from the unpublished article.*

> Research software. It is not investment advice and must not be used as the sole basis for an investment decision.

## Research questions

- How is dependence structured among Brazilian equities?
- Which correlations carry information beyond the market-wide mode?
- How do RMT filtering and network construction change the apparent market topology?
- Do structural and network features improve retrospective volatility forecasts?

## Methods

| Area | Implemented workflow |
| --- | --- |
| Returns | Adjusted prices, log returns, descriptive statistics, quality checks |
| Dependence | Pearson correlations, sector summaries, rolling and EWMA correlations |
| RMT | Marcenko-Pastur bounds, market/group modes, filtered correlation matrices |
| Networks | Mantegna distance, MST, PMFG, centrality and subsector dependency networks |
| Forecasting | Historical volatility, EWMA, GARCH, HAR-RV and machine-learning baselines |

## Repository layout

```text
.
├── config/          # Versioned, safe configuration templates and asset universes
├── docs/            # Method, data, architecture and contribution documentation
├── notebooks/       # Exploratory and figure-generation notebooks
├── scripts/python/  # Ordered research pipeline
├── src/             # Reusable analysis modules
├── outputs/         # Local generated figures, tables and networks (not versioned)
└── article/          # Local manuscript workspace (not part of the public release)
```

See the [architecture guide](docs/architecture.md) for the execution flow and [data and reproducibility guide](docs/data-and-reproducibility.md) for the data policy.

## Quick start

Requirements: Python 3.11+ and access to a local or remote ClickHouse instance containing the daily-candle table described in the configuration.

```bash
git clone https://github.com/dreyvinixz/RMT_Planar_Networks_Volatility_Forecasting_Brazil.git
cd RMT_Planar_Networks_Volatility_Forecasting_Brazil
python -m venv .venv
```

Activate the virtual environment, install the dependencies, and create your local configuration:

```bash
pip install -r requirements.txt
copy config\\clickhouse.example.toml config\\clickhouse.toml
python scripts/python/00_check_clickhouse.py
```

On macOS/Linux, replace `copy` with `cp`. Edit the newly created `config/clickhouse.toml` or set the `B3_CH_*` environment variables. This local file is intentionally ignored by Git.

## Pipeline

The numbered scripts in `scripts/python/` are the canonical execution order. A typical end-to-end run is:

```text
00 data connection → 01 universe selection → 02 returns → 03–06 correlations/RMT
→ 07–12 networks → 13–16 volatility forecasting → 17–21 robustness and appendices
```

Each stage writes its derived artefacts under `outputs/`. Generated figures, tables, GraphML/GEXF files, logs, local data and temporary PDF-review files are excluded from the public repository; regenerate them from a compatible data source.

## Data access and reproducibility

This repository contains code and universe definitions, not a redistribution of market data. Obtain B3 data through a source whose licence permits your intended use, load it into ClickHouse, and configure the table locally. See [docs/data-and-reproducibility.md](docs/data-and-reproducibility.md) before running the pipeline.

## Documentation

- [Architecture](docs/architecture.md) — modules and execution flow.
- [Data and reproducibility](docs/data-and-reproducibility.md) — required schema, provenance and output policy.
- [Contributing](CONTRIBUTING.md) — setup, pull requests and research-quality expectations.
- [Citation](CITATION.cff) — how to cite the software.

## Contributing

Contributions are welcome, especially in data-validation checks, methodological robustness, documentation and reproducible examples. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

The code is distributed under the [MIT License](LICENSE). Data, third-party research papers and any publisher templates retain their own terms and are not covered by this licence.
