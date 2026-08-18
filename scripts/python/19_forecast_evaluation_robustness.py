from __future__ import annotations

"""Uncertainty and loss-difference checks for the retrospective forecast study.

The analysis uses the already saved daily predictions.  Moving-block bootstrap
intervals retain serial dependence induced by overlapping realized-volatility
horizons.  The formal comparison is a HAC loss-difference test between the
validation-selected best structural specification and the validation-selected
Set A baseline; it does not turn the ex-post structural descriptors into
point-in-time features.
"""

from math import erfc, sqrt
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"

COMPARISON_PATH = TABLES_DIR / "volatility_model_comparison_2006_2025.csv"
PREDICTIONS_PATH = TABLES_DIR / "volatility_model_predictions_2006_2025.csv"
BY_ASSET_PATH = TABLES_DIR / "forecast_validation_selected_test_metrics_by_asset_2006_2025.csv"
SUMMARY_PATH = TABLES_DIR / "forecast_validation_selected_test_summary_2006_2025.csv"
LOSS_TEST_PATH = TABLES_DIR / "forecast_hac_loss_difference_tests_2006_2025.csv"

N_BOOTSTRAP = 2_000
SEED = 42


def qlike_observations(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    epsilon = 1e-12
    realized_variance = np.maximum(np.asarray(y_true, dtype=float) ** 2, epsilon)
    predicted_variance = np.maximum(np.asarray(y_pred, dtype=float) ** 2, epsilon)
    return np.log(predicted_variance) + realized_variance / predicted_variance


def moving_block_indices(n_obs: int, block_length: int, rng: np.random.Generator) -> np.ndarray:
    n_blocks = int(np.ceil(n_obs / block_length))
    starts = rng.integers(0, n_obs, size=n_blocks)
    offsets = np.arange(block_length)
    return ((starts[:, None] + offsets) % n_obs).ravel()[:n_obs]


def qlike_bootstrap_interval(
    losses: np.ndarray,
    block_length: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    boot_means = np.empty(N_BOOTSTRAP, dtype=float)
    for replicate in range(N_BOOTSTRAP):
        indices = moving_block_indices(len(losses), block_length, rng)
        boot_means[replicate] = losses[indices].mean()
    return tuple(np.quantile(boot_means, [0.025, 0.975]))


def validation_selected_configurations(comparison: pd.DataFrame) -> pd.DataFrame:
    validation = comparison[comparison["split"] == "validation"]
    ranking = (
        validation.groupby(["horizon", "model", "feature_set"], as_index=False)["QLIKE"]
        .mean()
        .sort_values(["horizon", "model", "QLIKE"])
    )
    return ranking.drop_duplicates(["horizon", "model"])[["horizon", "model", "feature_set"]]


def validation_champion(comparison: pd.DataFrame, horizon: int, set_a_only: bool) -> pd.Series:
    validation = comparison[(comparison["split"] == "validation") & (comparison["horizon"] == horizon)]
    if set_a_only:
        validation = validation[validation["feature_set"] == "Set A (Classical)"]
    ranking = (
        validation.groupby(["model", "feature_set"], as_index=False)["QLIKE"]
        .mean()
        .sort_values("QLIKE")
        .reset_index(drop=True)
    )
    if ranking.empty:
        raise ValueError(f"No validation candidate found for horizon={horizon}, set_a_only={set_a_only}")
    return ranking.iloc[0]


def selected_test_metrics(predictions: pd.DataFrame, selected: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    test = predictions[predictions["split"] == "test"].merge(
        selected, on=["horizon", "model", "feature_set"], how="inner"
    )
    rng = np.random.default_rng(SEED)
    rows: list[dict[str, object]] = []

    for keys, frame in test.groupby(["horizon", "model", "feature_set", "symbol"], sort=True):
        horizon, model, feature_set, symbol = keys
        frame = frame.sort_values("date")
        y_true = frame["y_true"].to_numpy(dtype=float)
        y_pred = frame["y_pred"].to_numpy(dtype=float)
        losses = qlike_observations(y_true, y_pred)
        ci_low, ci_high = qlike_bootstrap_interval(losses, int(horizon), rng)
        rows.append(
            {
                "horizon": horizon,
                "model": model,
                "feature_set": feature_set,
                "symbol": symbol,
                "n_test_observations": len(frame),
                "MAE": np.mean(np.abs(y_true - y_pred)),
                "RMSE": np.sqrt(np.mean((y_true - y_pred) ** 2)),
                "QLIKE": losses.mean(),
                "QLIKE_ci95_low": ci_low,
                "QLIKE_ci95_high": ci_high,
            }
        )

    by_asset = pd.DataFrame(rows).sort_values(["horizon", "model", "symbol"])

    # Aggregate at the date level before bootstrapping so each date, rather than
    # each asset-date, is the resampling unit and cross-asset co-movement remains.
    summary_rows: list[dict[str, object]] = []
    for keys, frame in test.groupby(["horizon", "model", "feature_set"], sort=True):
        horizon, model, feature_set = keys
        frame = frame.copy()
        frame["qlike_loss"] = qlike_observations(frame["y_true"].to_numpy(), frame["y_pred"].to_numpy())
        date_losses = frame.groupby("date", as_index=False)["qlike_loss"].mean().sort_values("date")
        ci_low, ci_high = qlike_bootstrap_interval(
            date_losses["qlike_loss"].to_numpy(), int(horizon), rng
        )
        asset_rows = by_asset[
            (by_asset["horizon"] == horizon)
            & (by_asset["model"] == model)
            & (by_asset["feature_set"] == feature_set)
        ]
        summary_rows.append(
            {
                "horizon": horizon,
                "model": model,
                "feature_set": feature_set,
                "n_assets": asset_rows["symbol"].nunique(),
                "n_test_dates": len(date_losses),
                "MAE": asset_rows["MAE"].mean(),
                "RMSE": asset_rows["RMSE"].mean(),
                "QLIKE": date_losses["qlike_loss"].mean(),
                "QLIKE_ci95_low": ci_low,
                "QLIKE_ci95_high": ci_high,
                "bootstrap_replicates": N_BOOTSTRAP,
                "bootstrap_block_length_days": int(horizon),
                "bootstrap_seed": SEED,
            }
        )
    return by_asset, pd.DataFrame(summary_rows).sort_values(["horizon", "QLIKE"])


def hac_loss_difference_tests(comparison: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    """One-sided HAC tests of baseline loss minus structural loss by horizon."""
    test = predictions[predictions["split"] == "test"].copy()
    output: list[dict[str, object]] = []

    for horizon in [5, 20]:
        structural = validation_champion(comparison, horizon, set_a_only=False)
        baseline = validation_champion(comparison, horizon, set_a_only=True)

        def configuration_losses(choice: pd.Series, label: str) -> pd.DataFrame:
            frame = test[
                (test["horizon"] == horizon)
                & (test["model"] == choice["model"])
                & (test["feature_set"] == choice["feature_set"])
            ][["date", "symbol", "y_true", "y_pred"]].copy()
            frame[label] = qlike_observations(frame["y_true"].to_numpy(), frame["y_pred"].to_numpy())
            return frame[["date", "symbol", label]]

        structural_losses = configuration_losses(structural, "structural_loss")
        baseline_losses = configuration_losses(baseline, "baseline_loss")
        merged = baseline_losses.merge(structural_losses, on=["date", "symbol"], how="inner")
        date_difference = (
            merged.assign(loss_difference=lambda x: x["baseline_loss"] - x["structural_loss"])
            .groupby("date", as_index=False)["loss_difference"]
            .mean()
            .sort_values("date")
        )
        differences = date_difference["loss_difference"].to_numpy()
        n_obs = len(differences)
        lag = int(horizon) - 1
        centered = differences - differences.mean()
        long_run_variance = np.mean(centered**2)
        for autocovariance_lag in range(1, lag + 1):
            weight = 1 - autocovariance_lag / (lag + 1)
            autocovariance = np.mean(centered[autocovariance_lag:] * centered[:-autocovariance_lag])
            long_run_variance += 2 * weight * autocovariance
        standard_error = sqrt(max(long_run_variance, 0.0) / n_obs)
        statistic = differences.mean() / standard_error if standard_error > 0 else np.nan
        one_sided_p = 0.5 * erfc(statistic / sqrt(2)) if np.isfinite(statistic) else np.nan
        output.append(
            {
                "horizon": horizon,
                "structural_model": structural["model"],
                "structural_feature_set": structural["feature_set"],
                "baseline_model": baseline["model"],
                "baseline_feature_set": baseline["feature_set"],
                "n_assets": merged["symbol"].nunique(),
                "n_test_dates": n_obs,
                "newey_west_lag": lag,
                "mean_baseline_minus_structural_QLIKE": differences.mean(),
                "hac_standard_error": standard_error,
                "loss_difference_statistic": statistic,
                "one_sided_p_baseline_loss_gt_structural_loss": one_sided_p,
            }
        )
    return pd.DataFrame(output)


def main() -> None:
    comparison = pd.read_csv(COMPARISON_PATH)
    predictions = pd.read_csv(PREDICTIONS_PATH)
    predictions["date"] = pd.to_datetime(predictions["date"])

    selected = validation_selected_configurations(comparison)
    by_asset, summary = selected_test_metrics(predictions, selected)
    loss_tests = hac_loss_difference_tests(comparison, predictions)

    by_asset.to_csv(BY_ASSET_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)
    loss_tests.to_csv(LOSS_TEST_PATH, index=False)

    print(f"Saved {BY_ASSET_PATH}")
    print(f"Saved {SUMMARY_PATH}")
    print(f"Saved {LOSS_TEST_PATH}")
    print("\nValidation-selected structural versus Set A loss checks")
    print(loss_tests.to_string(index=False))


if __name__ == "__main__":
    main()
