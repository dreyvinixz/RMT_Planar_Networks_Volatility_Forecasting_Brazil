# Contributing to RMT Planar Networks & Volatility Forecasting — Brazil

Thank you for helping improve the project. Contributions to code, documentation, validation and methodological robustness are welcome.

## Before opening a pull request

1. Open an issue for substantial changes so the research question and scope are clear.
2. Keep changes focused; avoid combining refactors, new methods and generated results in one pull request.
3. Do not add credentials, raw market data, downloaded papers, local logs, `outputs/`, `tmp/` or manuscript drafts.
4. Describe data sources, sample windows, preprocessing, random seeds and evaluation splits whenever the change affects an empirical result.

## Local checks

Run the relevant script or notebook for the changed stage. At a minimum, ensure the edited Python files compile:

```bash
python -m compileall -q src scripts/python
```

Database-dependent checks require a locally configured ClickHouse instance; see the README and the data guide.

## Research standards

- State assumptions and limitations explicitly.
- Prefer deterministic runs and record random seeds.
- Keep the original and derived data paths distinct.
- Do not present backtests as investment advice or as evidence of future performance.
- Add or update documentation when a configuration, data contract or pipeline stage changes.

## Pull-request description

Explain the problem, the method, validation performed, expected impact on outputs, and any remaining caveats. Follow the repository’s [Code of Conduct](CODE_OF_CONDUCT.md).
