from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"


def rmt_summary(returns: pd.DataFrame) -> dict[str, float | int | str]:
    """Compute a complete-case RMT summary for a return panel."""
    complete = returns.dropna(how="any")
    t_obs, n_assets = complete.shape
    q_ratio = t_obs / n_assets
    lambda_plus = 1.0 + 1.0 / q_ratio + 2.0 * np.sqrt(1.0 / q_ratio)
    eigenvalues = np.linalg.eigvalsh(complete.corr().to_numpy())[::-1]
    return {
        "assets": n_assets,
        "observations": t_obs,
        "start_date": complete.index.min().date().isoformat(),
        "end_date": complete.index.max().date().isoformat(),
        "Q": q_ratio,
        "lambda_plus": lambda_plus,
        "n_above_lambda_plus": int((eigenvalues > lambda_plus).sum()),
        "lambda_1": eigenvalues[0],
        "market_mode_trace_share": eigenvalues[0] / n_assets,
        "lambda_2": eigenvalues[1],
        "lambda_3": eigenvalues[2],
    }


def main() -> None:
    returns = pd.read_csv(
        TABLES_DIR / "core_historical_returns_wide_1998_2025.csv", parse_dates=["date"]
    ).set_index("date")
    sector_map = pd.read_csv(TABLES_DIR / "assets_sector_map.csv")
    symbols = returns.columns.tolist()
    metadata = sector_map.set_index("symbol").loc[symbols].reset_index()

    # Retain one class per issuer: maximum raw-file coverage, then ticker name.
    metadata["valid_return_observations"] = metadata["symbol"].map(returns.notna().sum())
    issuer_size = metadata.groupby("company_name")["symbol"].transform("size")
    representatives = (
        metadata.sort_values(
            ["company_name", "valid_return_observations", "symbol"],
            ascending=[True, False, True],
        )
        .drop_duplicates("company_name", keep="first")
        .sort_values("symbol")
    )

    summary = pd.DataFrame(
        [
            {"panel": "full share-class panel", **rmt_summary(returns)},
            {
                "panel": "issuer-collapsed panel",
                **rmt_summary(returns[representatives["symbol"].tolist()]),
            },
        ]
    )
    summary.to_csv(TABLES_DIR / "issuer_class_rmt_sensitivity.csv", index=False)

    duplicated = metadata.loc[issuer_size > 1].copy()
    duplicated["retained_in_issuer_panel"] = duplicated["symbol"].isin(representatives["symbol"])
    duplicated.sort_values(["company_name", "symbol"]).to_csv(
        TABLES_DIR / "issuer_class_sensitivity_selection.csv", index=False
    )

    print("Issuer/share-class RMT sensitivity")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    n_duplicated_issuers = metadata.loc[issuer_size > 1, "company_name"].nunique()
    print(f"Duplicated issuers collapsed: {n_duplicated_issuers}")


if __name__ == "__main__":
    main()
