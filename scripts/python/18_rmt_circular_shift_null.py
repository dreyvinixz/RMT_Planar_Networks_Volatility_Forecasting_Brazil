from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
N_SURROGATES = 1000
RANDOM_SEED = 42
N_RANKS = 5


def main() -> None:
    returns = pd.read_csv(TABLES_DIR / "core_historical_returns_wide_1998_2025.csv")
    returns = returns.drop(columns="date").dropna(how="any").to_numpy(dtype=float)
    n_obs, n_assets = returns.shape
    empirical = np.linalg.eigvalsh(np.corrcoef(returns, rowvar=False))[::-1]

    rng = np.random.default_rng(RANDOM_SEED)
    surrogate_eigenvalues = np.empty((N_SURROGATES, N_RANKS))
    for replicate in range(N_SURROGATES):
        shifts = rng.integers(0, n_obs, size=n_assets)
        shifted = np.column_stack(
            [np.roll(returns[:, column], shifts[column]) for column in range(n_assets)]
        )
        surrogate_eigenvalues[replicate] = np.linalg.eigvalsh(
            np.corrcoef(shifted, rowvar=False)
        )[::-1][:N_RANKS]

    rows = []
    for rank in range(N_RANKS):
        exceedances = int((surrogate_eigenvalues[:, rank] >= empirical[rank]).sum())
        rows.append(
            {
                "eigen_rank": rank + 1,
                "empirical_eigenvalue": empirical[rank],
                "surrogate_q95": np.quantile(surrogate_eigenvalues[:, rank], 0.95),
                "surrogate_max": surrogate_eigenvalues[:, rank].max(),
                "exceedances": exceedances,
                "monte_carlo_p": (exceedances + 1) / (N_SURROGATES + 1),
                "n_surrogates": N_SURROGATES,
                "null": "independent circular shifts by asset",
            }
        )

    output = pd.DataFrame(rows)
    output.to_csv(TABLES_DIR / "rmt_circular_shift_null_1000.csv", index=False)
    print("Circular-shift RMT null summary")
    print(output.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()
