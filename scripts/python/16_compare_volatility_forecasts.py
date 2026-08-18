from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURE_VECTOR_DIR = PROJECT_ROOT / "outputs" / "figures" / "vector"
FIGURE_PREVIEW_DIR = PROJECT_ROOT / "outputs" / "figures" / "preview"

FIGURE_VECTOR_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)


def feature_set_short(value: str) -> str:
    if value.startswith("Set A"):
        return "Set A"
    if value.startswith("Set B"):
        return "Set B"
    if value.startswith("Set C"):
        return "Set C"
    return value


def validation_selected_test_rows(comp_df: pd.DataFrame) -> pd.DataFrame:
    val_df = comp_df[comp_df["split"] == "validation"].copy()
    rank = (
        val_df.groupby(["horizon", "model", "feature_set"], as_index=False)["QLIKE"]
        .mean()
        .sort_values(["horizon", "model", "QLIKE"])
    )
    selected = rank.drop_duplicates(["horizon", "model"])[["horizon", "model", "feature_set"]]
    test_df = comp_df[comp_df["split"] == "test"].merge(
        selected, on=["horizon", "model", "feature_set"], how="inner"
    )
    test_df["model_display"] = test_df["model"] + "\n(" + test_df["feature_set"].map(feature_set_short) + ")"
    return test_df


def plot_figure_16(summary_df: pd.DataFrame) -> None:
    print("Generating Figure 16 (ML/DL model comparison)...")
    agg_df = summary_df.copy()
    agg_df["model_display"] = agg_df["model"] + "\n(" + agg_df["feature_set"].map(feature_set_short) + ")"

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for i, h in enumerate([5, 20]):
        ax = axes[i]
        plot_data = agg_df[agg_df["horizon"] == h].sort_values("QLIKE").reset_index(drop=True)
        y_pos = list(range(len(plot_data)))
        xmin = plot_data[["QLIKE", "QLIKE_ci95_low"]].min().min()
        xmax = plot_data[["QLIKE", "QLIKE_ci95_high"]].max().max()
        pad = max(0.015, 0.12 * (xmax - xmin))

        ax.hlines(y=y_pos, xmin=xmin, xmax=plot_data["QLIKE"], color="#8bb7d3", lw=2)
        ax.scatter(plot_data["QLIKE"], y_pos, color="#0072B2", s=55, zorder=3)
        ax.errorbar(
            plot_data["QLIKE"],
            y_pos,
            xerr=[
                plot_data["QLIKE"] - plot_data["QLIKE_ci95_low"],
                plot_data["QLIKE_ci95_high"] - plot_data["QLIKE"],
            ],
            fmt="none",
            ecolor="#2f2f2f",
            elinewidth=0.9,
            capsize=2.5,
            zorder=2,
        )
        ax.set_title(f"Chronological test-period QLIKE loss, horizon = {h} days")
        ax.set_xlabel("QLIKE (lower is better; 95% moving-block CI)")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(plot_data["model_display"])
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.25)
        # Reserve a value column beyond every confidence interval so that
        # numerical labels never sit on the plotted horizontal elements.
        value_x = xmax + pad * 0.25
        ax.set_xlim(xmin - pad, xmax + pad * 1.5)
        for y, value in zip(y_pos, plot_data["QLIKE"]):
            ax.text(
                value_x,
                y,
                f"{value:.3f}",
                ha="left",
                va="center",
                fontsize=8,
                zorder=4,
            )

    plt.tight_layout()
    fig.savefig(FIGURE_VECTOR_DIR / "figure_16_volatility_forecast_model_comparison.pdf", bbox_inches="tight")
    fig.savefig(FIGURE_PREVIEW_DIR / "figure_16_volatility_forecast_model_comparison.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_figure_17(comp_df: pd.DataFrame, pred_df: pd.DataFrame) -> None:
    print("Generating Figure 17 (realized vs ML/DL predictions)...")
    pred_df["date"] = pd.to_datetime(pred_df["date"])

    # Pick the validation-selected best model at the 20-day horizon.
    val_rank = (
        comp_df[(comp_df["split"] == "validation") & (comp_df["horizon"] == 20)]
        .groupby(["model", "feature_set"], as_index=False)["QLIKE"]
        .mean()
        .sort_values("QLIKE")
    )
    selected = val_rank.iloc[0]
    model = selected["model"]
    feature_set = selected["feature_set"]

    symbols = ["PETR4", "VALE3", "BBDC4"]
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    for ax, sym in zip(axes, symbols):
        sdf = pred_df[
            (pred_df["symbol"] == sym)
            & (pred_df["horizon"] == 20)
            & (pred_df["model"] == model)
            & (pred_df["feature_set"] == feature_set)
            & (pred_df["split"].isin(["validation", "test"]))
        ].sort_values("date")

        ax.plot(sdf["date"], sdf["y_true"], label="Realized volatility", color="#222222", linewidth=1.0)
        ax.plot(
            sdf["date"],
            sdf["y_pred"],
            label=f"{model} ({feature_set_short(feature_set)})",
            color="#0072B2",
            linewidth=1.25,
        )
        ax.axvline(pd.Timestamp("2021-01-01"), color="#666666", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.set_title(sym)
        ax.set_ylabel("20-day volatility")
        ax.grid(True, alpha=0.25)
        ax.legend(loc="upper right", frameon=False)

    axes[-1].set_xlabel("Date")
    plt.tight_layout()
    fig.savefig(FIGURE_VECTOR_DIR / "figure_17_realized_vs_predicted_volatility.pdf", bbox_inches="tight")
    fig.savefig(FIGURE_PREVIEW_DIR / "figure_17_realized_vs_predicted_volatility.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_figure_18(fi_df: pd.DataFrame) -> None:
    print("Generating Figure 18 (feature importance)...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, h in zip(axes, [5, 20]):
        plot_data = fi_df[fi_df["horizon"] == h].sort_values("importance", ascending=False).head(18)
        sns.barplot(data=plot_data, x="importance", y="feature", ax=ax, color="#009E73")
        ax.set_title(f"Random Forest feature importance, horizon = {h} days")
        ax.set_xlabel("Impurity-based importance")
        ax.set_ylabel("")
        ax.grid(axis="x", alpha=0.25)

    plt.tight_layout()
    fig.savefig(FIGURE_VECTOR_DIR / "figure_18_ml_feature_importance.pdf", bbox_inches="tight")
    fig.savefig(FIGURE_PREVIEW_DIR / "figure_18_ml_feature_importance.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    print("Starting ML/DL volatility plotting...")
    comp_df = pd.read_csv(OUTPUT_DIR / "volatility_model_comparison_2006_2025.csv")
    pred_df = pd.read_csv(OUTPUT_DIR / "volatility_model_predictions_2006_2025.csv")
    fi_df = pd.read_csv(OUTPUT_DIR / "ml_feature_importances_2006_2025.csv")
    summary_df = pd.read_csv(OUTPUT_DIR / "forecast_validation_selected_test_summary_2006_2025.csv")

    plot_figure_16(summary_df)
    plot_figure_17(comp_df, pred_df)
    plot_figure_18(fi_df)
    print("Done.")


if __name__ == "__main__":
    main()
