from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
VECTOR_FIGURES_DIR = FIGURES_DIR / "vector"
PREVIEW_FIGURES_DIR = FIGURES_DIR / "preview"

RETURNS_LONG_PATH = TABLES_DIR / "demo_assets_returns_long_1998_2025.csv"
RETURNS_WIDE_PATH = TABLES_DIR / "demo_assets_returns_wide_1998_2025.csv"

FIGURE_SLUG = "figure_1d_stylized_facts_demo_assets_clean_2006_2025"
START_DATE = "2006-01-01"
END_DATE = "2025-12-31"

ASSET_ORDER = ["PETR4", "VALE3", "BBDC4"]
ASSET_COLORS = {
    "PETR4": "#1f77b4",
    "VALE3": "#2ca02c",
    "BBDC4": "#d62728",
}
def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 300,
            "text.usetex": True,
            "font.family": "serif",
            "mathtext.fontset": "cm",
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.linewidth": 0.7,
            "axes.grid": False,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "legend.frameon": False,
        }
    )


def style_axes(axes: np.ndarray) -> None:
    for ax in axes.ravel():
        ax.grid(False)
        ax.spines["top"].set_visible(True)
        ax.spines["right"].set_visible(True)
        ax.tick_params(width=0.7, length=3.5)


def load_returns() -> tuple[pd.DataFrame, pd.DataFrame]:
    returns_long = pd.read_csv(RETURNS_LONG_PATH, parse_dates=["date"])
    returns_wide = pd.read_csv(RETURNS_WIDE_PATH, parse_dates=["date"])
    returns_wide = returns_wide.set_index("date").sort_index()

    start_date = pd.Timestamp(START_DATE)
    end_date = pd.Timestamp(END_DATE)
    symbols = [symbol for symbol in ASSET_ORDER if symbol in returns_wide.columns]

    returns_wide = returns_wide.loc[start_date:end_date, symbols].copy()
    returns_long = returns_long[
        (returns_long["date"] >= start_date)
        & (returns_long["date"] <= end_date)
        & returns_long["symbol"].isin(symbols)
    ].copy()

    return returns_long, returns_wide


def normalized_price_from_prices(returns_long: pd.DataFrame) -> pd.DataFrame:
    prices = returns_long.pivot(index="date", columns="symbol", values="price")
    prices = prices[[symbol for symbol in ASSET_ORDER if symbol in prices.columns]].sort_index()
    return prices / prices.iloc[0]


def empirical_ccdf(values: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    clean = values.dropna().to_numpy()
    clean = clean[clean >= 1e-4]
    clean.sort()

    n_obs = len(clean)
    ccdf = (n_obs - np.arange(n_obs)) / n_obs

    return clean, ccdf


def tail_reference_line(x_values: np.ndarray, y_values: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    tail_mask = (x_values >= np.quantile(x_values, 0.95)) & (y_values > 0)
    tail_x = x_values[tail_mask]
    tail_y = y_values[tail_mask]

    if len(tail_x) < 5:
        return np.array([]), np.array([]), np.nan

    slope, intercept = np.polyfit(np.log(tail_x), np.log(tail_y), 1)
    reference_x = np.linspace(tail_x.min(), tail_x.max(), 80)
    reference_y = np.exp(intercept) * reference_x**slope

    return reference_x, reference_y, -slope


def absolute_return_acf(series: pd.Series, nlags: int) -> np.ndarray:
    clean = series.abs().dropna()
    if len(clean) <= nlags + 1:
        return np.full(nlags + 1, np.nan)
    return acf(clean, nlags=nlags, fft=True, missing="drop")


def plot_stylized_facts(returns_long: pd.DataFrame, returns_wide: pd.DataFrame) -> plt.Figure:
    configure_matplotlib()

    fig = plt.figure(figsize=(9.6, 6.3), constrained_layout=True)
    grid = fig.add_gridspec(2, 2)
    ax_price = fig.add_subplot(grid[0, 0])
    return_grid = grid[0, 1].subgridspec(3, 1, hspace=0.08)
    return_axes = [fig.add_subplot(return_grid[i, 0]) for i in range(3)]
    ax_ccdf = fig.add_subplot(grid[1, 0])
    ax_acf = fig.add_subplot(grid[1, 1])
    style_axes(np.array([ax_price, *return_axes, ax_ccdf, ax_acf]))
    price_index = normalized_price_from_prices(returns_long)

    ax = ax_price
    for symbol in price_index.columns:
        ax.plot(
            price_index.index,
            price_index[symbol],
            label=symbol,
            color=ASSET_COLORS[symbol],
            linewidth=0.8,
        )
    ax.set_title("normalized price")
    ax.set_ylabel(r"$P_t/P_0$")
    ax.legend(loc="upper left", ncols=3, handlelength=2.0, columnspacing=1.3)

    return_limit = 0.40
    for index, (ax, symbol) in enumerate(zip(return_axes, returns_wide.columns)):
        ax.plot(
            returns_wide.index,
            returns_wide[symbol],
            color=ASSET_COLORS[symbol],
            linewidth=0.35,
            alpha=0.85,
        )
        ax.axhline(0.0, color="black", linewidth=0.45, alpha=0.7)
        ax.set_ylim(-return_limit, return_limit)
        ax.set_ylabel(r"$r_t$")
        ax.text(
            0.02,
            0.74,
            symbol,
            transform=ax.transAxes,
            color=ASSET_COLORS[symbol],
            fontsize=8,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="0.75", alpha=0.9),
        )
        if index == 0:
            ax.set_title("daily log returns")
        if index < len(return_axes) - 1:
            ax.tick_params(labelbottom=False)
    return_axes[-1].set_xlabel("time")

    ax = ax_ccdf
    for symbol in returns_wide.columns:
        x_values, y_values = empirical_ccdf(returns_wide[symbol].abs())
        ax.loglog(
            x_values,
            y_values,
            label=symbol,
            color=ASSET_COLORS[symbol],
            linewidth=0.9,
        )

    pooled_x, pooled_y = empirical_ccdf(returns_long["log_return"].abs())
    ref_x, ref_y, alpha = tail_reference_line(pooled_x, pooled_y)
    ax.loglog(pooled_x, pooled_y, label="all", color="black", linewidth=1.0)
    if len(ref_x):
        ax.loglog(ref_x, ref_y, color="black", linewidth=0.8, linestyle="--", label=rf"$x^{{-{alpha:.2f}}}$")
    ax.set_title("complementary CDF of returns")
    ax.set_xlabel(r"$|r_t|$")
    ax.set_ylabel(r"$P(|r_t| > x)$")
    ax.legend(loc="lower left", handlelength=2.0)

    ax = ax_acf
    max_lag = 150
    lags = np.arange(1, max_lag + 1)
    acf_by_asset = []
    for symbol in returns_wide.columns:
        acf_values = absolute_return_acf(returns_wide[symbol], nlags=max_lag)[1:]
        acf_by_asset.append(acf_values)
        ax.plot(
            lags,
            acf_values,
            label=symbol,
            color=ASSET_COLORS[symbol],
            linewidth=0.55,
            alpha=0.55,
        )

    all_acf = np.nanmean(np.vstack(acf_by_asset), axis=0)
    ax.plot(lags, all_acf, label="all", color="0.25", linewidth=1.0, alpha=0.9)
    ax.axhline(0.0, color="black", linewidth=0.6)
    ax.set_xlim(0, max_lag)
    ax.set_title("autocorrelations")
    ax.set_xlabel("lag, trading days")
    ax.set_ylabel(r"$\mathrm{ACF}(|r_t|)$")
    ax.legend(loc="upper right", handlelength=2.0)

    return fig


def save_figure(fig: plt.Figure) -> None:
    VECTOR_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    output_paths = (
        VECTOR_FIGURES_DIR / f"{FIGURE_SLUG}.pdf",
        VECTOR_FIGURES_DIR / f"{FIGURE_SLUG}.svg",
        PREVIEW_FIGURES_DIR / f"{FIGURE_SLUG}.png",
    )
    for output_path in output_paths:
        fig.savefig(output_path, bbox_inches="tight")
        print(f"Saved {output_path}")


def main() -> None:
    returns_long, returns_wide = load_returns()
    fig = plot_stylized_facts(returns_long, returns_wide)
    save_figure(fig)
    plt.close(fig)


if __name__ == "__main__":
    main()
