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
FEATURE_SET_TEST_PATH = TABLES_DIR / "forecast_feature_set_hac_tests_2006_2025.csv"
BLOCK_SENSITIVITY_PATH = TABLES_DIR / "forecast_block_length_sensitivity_2006_2025.csv"
ECON_COMPARISON_PATH = TABLES_DIR / "econometric_model_comparison_2006_2025.csv"
HAR_PREDICTIONS_PATH = TABLES_DIR / "har_rv_predictions_2006_2025.csv"

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


def har_test_metrics(
    predictions: pd.DataFrame, econometric_comparison: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    test = predictions[predictions["split"] == "test"].copy()
    rng = np.random.default_rng(SEED)
    per_asset: list[dict[str, object]] = []
    summary: list[dict[str, object]] = []
    for (horizon, symbol), frame in test.groupby(["horizon", "symbol"], sort=True):
        frame = frame.sort_values("date")
        y = frame["y_true"].to_numpy(dtype=float)
        yhat = frame["y_pred"].to_numpy(dtype=float)
        losses = qlike_observations(y, yhat)
        low, high = qlike_bootstrap_interval(losses, int(horizon), rng)
        score = econometric_comparison[
            (econometric_comparison["model"] == "HAR-RV")
            & (econometric_comparison["horizon"] == horizon)
            & (econometric_comparison["symbol"] == symbol)
            & (econometric_comparison["split"] == "test")
        ]["R2_oos"].iloc[0]
        per_asset.append({
            "horizon": horizon, "model": "HAR-RV", "feature_set": "HAR-RV benchmark",
            "symbol": symbol, "n_test_observations": len(frame),
            "MAE": np.mean(np.abs(y-yhat)), "RMSE": np.sqrt(np.mean((y-yhat)**2)),
            "QLIKE": losses.mean(), "QLIKE_ci95_low": low, "QLIKE_ci95_high": high,
            "R2_oos": score,
        })
    by_asset = pd.DataFrame(per_asset)
    for horizon, frame in test.groupby("horizon", sort=True):
        frame = frame.copy()
        frame["loss"] = qlike_observations(frame["y_true"].to_numpy(), frame["y_pred"].to_numpy())
        date_losses = frame.groupby("date", as_index=False)["loss"].mean().sort_values("date")
        low, high = qlike_bootstrap_interval(date_losses["loss"].to_numpy(), int(horizon), rng)
        by_h = by_asset[by_asset["horizon"] == horizon]
        summary.append({
            "horizon": horizon, "model": "HAR-RV", "feature_set": "HAR-RV benchmark",
            "n_assets": by_h["symbol"].nunique(), "n_test_dates": len(date_losses),
            "MAE": by_h["MAE"].mean(), "RMSE": by_h["RMSE"].mean(),
            "QLIKE": date_losses["loss"].mean(), "QLIKE_ci95_low": low,
            "QLIKE_ci95_high": high, "bootstrap_replicates": N_BOOTSTRAP,
            "bootstrap_block_length_days": int(horizon), "bootstrap_seed": SEED,
            "R2_oos": by_h["R2_oos"].mean(),
        })
    return by_asset, pd.DataFrame(summary)


def ridge_set_a_test_metrics(
    predictions: pd.DataFrame, comparison: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Add the direct Ridge Set A benchmark even if another Set A model wins validation."""
    test = predictions[
        (predictions["split"] == "test")
        & (predictions["model"] == "Ridge")
        & (predictions["feature_set"] == "Set A (Classical)")
    ].copy()
    rng = np.random.default_rng(SEED)
    asset_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    for (horizon, symbol), frame in test.groupby(["horizon", "symbol"], sort=True):
        frame = frame.sort_values("date")
        y, yhat = frame["y_true"].to_numpy(float), frame["y_pred"].to_numpy(float)
        loss = qlike_observations(y, yhat)
        low, high = qlike_bootstrap_interval(loss, int(horizon), rng)
        r2 = comparison[
            (comparison["split"] == "test")
            & (comparison["horizon"] == horizon)
            & (comparison["model"] == "Ridge")
            & (comparison["feature_set"] == "Set A (Classical)")
            & (comparison["symbol"] == symbol)
        ]["R2_oos"].iloc[0]
        asset_rows.append({
            "horizon": horizon, "model": "Ridge", "feature_set": "Set A (Classical)",
            "symbol": symbol, "n_test_observations": len(frame),
            "MAE": np.mean(np.abs(y-yhat)), "RMSE": np.sqrt(np.mean((y-yhat)**2)),
            "QLIKE": loss.mean(), "QLIKE_ci95_low": low, "QLIKE_ci95_high": high,
            "R2_oos": r2,
        })
    by_asset = pd.DataFrame(asset_rows)
    for horizon, frame in test.groupby("horizon", sort=True):
        frame = frame.copy()
        frame["loss"] = qlike_observations(frame["y_true"].to_numpy(), frame["y_pred"].to_numpy())
        date_loss = frame.groupby("date", as_index=False)["loss"].mean().sort_values("date")
        low, high = qlike_bootstrap_interval(date_loss["loss"].to_numpy(), int(horizon), rng)
        per_asset = by_asset[by_asset["horizon"] == horizon]
        summary_rows.append({
            "horizon": horizon, "model": "Ridge", "feature_set": "Set A (Classical)",
            "n_assets": per_asset["symbol"].nunique(), "n_test_dates": len(date_loss),
            "MAE": per_asset["MAE"].mean(), "RMSE": per_asset["RMSE"].mean(),
            "QLIKE": date_loss["loss"].mean(), "QLIKE_ci95_low": low,
            "QLIKE_ci95_high": high, "bootstrap_replicates": N_BOOTSTRAP,
            "bootstrap_block_length_days": int(horizon), "bootstrap_seed": SEED,
            "R2_oos": per_asset["R2_oos"].mean(),
        })
    return by_asset, pd.DataFrame(summary_rows)


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


def validation_selected_by_feature_set(comparison: pd.DataFrame) -> pd.DataFrame:
    validation = comparison[
        (comparison["split"] == "validation")
        & comparison["feature_set"].isin(
            ["Set A (Classical)", "Set B (+Market/RMT)", "Set C (+Network)"]
        )
    ]
    ranked = (
        validation.groupby(["horizon", "feature_set", "model"], as_index=False)["QLIKE"]
        .mean()
        .sort_values(["horizon", "feature_set", "QLIKE", "model"])
    )
    return ranked.drop_duplicates(["horizon", "feature_set"])


def hac_pair_test(
    baseline: pd.DataFrame, candidate: pd.DataFrame, horizon: int, contrast: str
) -> dict[str, object]:
    """Test baseline minus candidate QLIKE; positive values favor candidate."""
    merged = baseline.merge(candidate, on=["date", "symbol"], suffixes=("_base", "_candidate"))
    merged["loss_difference"] = merged["loss_base"] - merged["loss_candidate"]
    date_diff = merged.groupby("date", as_index=False)["loss_difference"].mean().sort_values("date")
    differences = date_diff["loss_difference"].to_numpy(dtype=float)
    n_obs = len(differences)
    lag = int(horizon) - 1
    numerically_identical = bool(np.max(np.abs(differences)) <= 1e-12)
    if numerically_identical:
        differences = np.zeros_like(differences)
    centered = differences - differences.mean()
    long_run_variance = np.mean(centered**2)
    for k in range(1, min(lag, n_obs - 1) + 1):
        weight = 1 - k / (lag + 1)
        long_run_variance += 2 * weight * np.mean(centered[k:] * centered[:-k])
    se = sqrt(max(long_run_variance, 0.0) / n_obs)
    statistic = differences.mean() / se if se > 0 else (0.0 if numerically_identical else np.nan)
    p_value = 0.5 if numerically_identical else (0.5 * erfc(statistic / sqrt(2)) if np.isfinite(statistic) else np.nan)
    p_two_sided = min(1.0, 2.0 * min(p_value, 1.0 - p_value)) if np.isfinite(p_value) else np.nan
    return {
        "horizon": horizon,
        "contrast": contrast,
        "n_assets": merged["symbol"].nunique(),
        "n_test_dates": n_obs,
        "newey_west_lag": lag,
        "mean_baseline_minus_candidate_QLIKE": differences.mean(),
        "hac_standard_error": se,
        "statistic": statistic,
        "one_sided_p_candidate_better": p_value,
        "one_sided_p_candidate_worse": 1.0 - p_value if np.isfinite(p_value) else np.nan,
        "two_sided_p": p_two_sided,
        "numerically_identical_forecasts": numerically_identical,
    }


def forecast_feature_set_tests(
    comparison: pd.DataFrame, predictions: pd.DataFrame, econ_comparison: pd.DataFrame,
    har_predictions: pd.DataFrame,
) -> pd.DataFrame:
    selected = validation_selected_by_feature_set(comparison)
    ml_test = predictions[predictions["split"] == "test"].copy()
    har_test = har_predictions[har_predictions["split"] == "test"].copy()
    output: list[dict[str, object]] = []

    def chosen_ml(frame: pd.DataFrame, horizon: int, label: str) -> pd.DataFrame:
        rows = frame[frame["horizon"] == horizon]
        return rows[
            (rows["model"] == label.split("|")[0])
            & (rows["feature_set"] == label.split("|")[1])
        ][["date", "symbol", "y_true", "y_pred"]].assign(
            loss=lambda x: qlike_observations(x["y_true"].to_numpy(), x["y_pred"].to_numpy())
        )[["date", "symbol", "loss"]]

    for horizon in (5, 20):
        hsel = selected[selected["horizon"] == horizon].set_index("feature_set")
        labels = {
            "A": "Set A (Classical)",
            "B": "Set B (+Market/RMT)",
            "C": "Set C (+Network)",
        }
        choices: dict[str, str] = {}
        losses: dict[str, pd.DataFrame] = {}
        for key, feature_set in labels.items():
            row = hsel.loc[feature_set]
            choices[key] = f"{row['model']}|{feature_set}"
            losses[key] = chosen_ml(ml_test, horizon, choices[key])

        for challenger in ("B", "C"):
            result = hac_pair_test(
                losses["A"], losses[challenger], horizon,
                f"validation-selected Set {challenger} vs Set A ({choices['A']} baseline; {choices[challenger]} candidate)",
            )
            output.append(result)

    # A direct Ridge Set A comparator is retained even if validation selects a
    # different Set A learner for the family-level comparisons above.
    ridge_rows = ml_test[
        (ml_test["model"] == "Ridge") & (ml_test["feature_set"] == "Set A (Classical)")
    ].copy()
    ridge_rows["loss"] = qlike_observations(ridge_rows["y_true"].to_numpy(), ridge_rows["y_pred"].to_numpy())
    for horizon in (5, 20):
        har = har_test[har_test["horizon"] == horizon][["date", "symbol", "y_true", "y_pred"]].copy()
        har["loss"] = qlike_observations(har["y_true"].to_numpy(), har["y_pred"].to_numpy())
        ridge = ridge_rows[ridge_rows["horizon"] == horizon][["date", "symbol", "loss"]]
        output.append(hac_pair_test(har[["date", "symbol", "loss"]], ridge, horizon, "HAR-RV vs Ridge Set A"))

    result = pd.DataFrame(output)
    structural = result["contrast"].str.startswith("validation-selected Set ")
    p_values = result.loc[structural, "two_sided_p"].to_numpy(dtype=float)
    order = np.argsort(p_values)
    adjusted = np.empty_like(p_values)
    running_max = 0.0
    count = len(p_values)
    for rank, index in enumerate(order):
        running_max = max(running_max, min(1.0, (count - rank) * p_values[index]))
        adjusted[index] = running_max
    result["holm_adjusted_p_two_sided"] = np.nan
    result.loc[structural, "holm_adjusted_p_two_sided"] = adjusted
    return result


def block_length_sensitivity(predictions: pd.DataFrame) -> pd.DataFrame:
    """Date-level circular moving-block CIs at h, 2h, and 4h block lengths."""
    test = predictions[predictions["split"] == "test"].copy()
    rng = np.random.default_rng(SEED)
    rows: list[dict[str, object]] = []
    for (horizon, model, feature_set), frame in test.groupby(
        ["horizon", "model", "feature_set"], sort=True
    ):
        frame["loss"] = qlike_observations(frame["y_true"].to_numpy(), frame["y_pred"].to_numpy())
        losses = frame.groupby("date", as_index=False)["loss"].mean().sort_values("date")["loss"].to_numpy()
        for block_length in (int(horizon), 2 * int(horizon), 4 * int(horizon)):
            low, high = qlike_bootstrap_interval(losses, block_length, rng)
            rows.append({
                "horizon": horizon, "model": model, "feature_set": feature_set,
                "n_test_dates": len(losses), "block_length_days": block_length,
                "bootstrap_replicates": N_BOOTSTRAP, "bootstrap_seed": SEED,
                "QLIKE": losses.mean(), "ci95_low": low, "ci95_high": high,
            })
    return pd.DataFrame(rows)


def main() -> None:
    comparison = pd.read_csv(COMPARISON_PATH)
    predictions = pd.read_csv(PREDICTIONS_PATH)
    predictions["date"] = pd.to_datetime(predictions["date"])

    selected = validation_selected_configurations(comparison)
    by_asset, summary = selected_test_metrics(predictions, selected)
    ridge_a_by_asset, ridge_a_summary = ridge_set_a_test_metrics(predictions, comparison)
    by_asset = pd.concat([by_asset, ridge_a_by_asset], ignore_index=True)
    summary = pd.concat([summary, ridge_a_summary], ignore_index=True)
    loss_tests = hac_loss_difference_tests(comparison, predictions)
    econ_comparison = pd.read_csv(ECON_COMPARISON_PATH)
    har_predictions = pd.read_csv(HAR_PREDICTIONS_PATH, parse_dates=["date"])
    har_by_asset, har_summary = har_test_metrics(har_predictions, econ_comparison)
    by_asset = pd.concat([by_asset, har_by_asset], ignore_index=True)
    summary = pd.concat([summary, har_summary], ignore_index=True)
    selected_r2 = (
        comparison[comparison["split"] == "test"]
        .merge(selected, on=["horizon", "model", "feature_set"], how="inner")
        .groupby(["horizon", "model", "feature_set"], as_index=False)["R2_oos"].mean()
    )
    summary = summary.merge(selected_r2, on=["horizon", "model", "feature_set"], how="left", suffixes=("", "_selected"))
    if "R2_oos_selected" in summary.columns:
        summary["R2_oos"] = summary["R2_oos"].combine_first(summary["R2_oos_selected"])
        summary = summary.drop(columns="R2_oos_selected")
    feature_set_tests = forecast_feature_set_tests(
        comparison, predictions, econ_comparison, har_predictions
    )
    block_sensitivity = block_length_sensitivity(pd.concat([predictions, har_predictions], ignore_index=True))

    by_asset.to_csv(BY_ASSET_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)
    loss_tests.to_csv(LOSS_TEST_PATH, index=False)
    feature_set_tests.to_csv(FEATURE_SET_TEST_PATH, index=False)
    block_sensitivity.to_csv(BLOCK_SENSITIVITY_PATH, index=False)

    print(f"Saved {BY_ASSET_PATH}")
    print(f"Saved {SUMMARY_PATH}")
    print(f"Saved {LOSS_TEST_PATH}")
    print("\nValidation-selected structural versus Set A loss checks")
    print(loss_tests.to_string(index=False))
    print("\nFeature-set and benchmark HAC comparisons")
    print(feature_set_tests.to_string(index=False))


if __name__ == "__main__":
    main()
