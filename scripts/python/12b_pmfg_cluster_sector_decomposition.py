from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgba
import networkx as nx
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
NETWORKS_DIR = PROJECT_ROOT / "outputs" / "networks" / "graphml"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"

SECTOR_PALETTE = {
    "Financials": "#2ca02c",
    "Basic Materials": "#ff7f0e",
    "Oil Gas and Biofuels": "#1f77b4",
    "Utilities": "#e377c2",
    "Consumer Cyclical": "#8c564b",
    "Consumer Non-Cyclical": "#17becf",
    "Industrials": "#d62728",
    "Real Estate": "#7f7f7f",
    "Telecommunications": "#bcbd22",
    "Unknown": "#aaaaaa",
}

CLUSTER_PALETTE = [
    "#0b4ea2",
    "#16b6b1",
    "#2daf5f",
    "#b66b7a",
    "#c81f63",
    "#f28e2b",
    "#6f63c6",
    "#8cc63f",
    "#d4a017",
    "#7f7f7f",
]

NETWORK_KIND = "group_mode"
COMMUNITY_RESOLUTION = 1.5


def normalize_positions(pos: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    coords = np.array(list(pos.values()), dtype=float)
    center = coords.mean(axis=0)
    coords = coords - center
    span = max(coords[:, 0].max() - coords[:, 0].min(), coords[:, 1].max() - coords[:, 1].min(), 1e-12)
    nodes = list(pos.keys())
    return {node: coords[i] / span for i, node in enumerate(nodes)}


def main() -> None:
    (FIGURES_DIR / "vector").mkdir(parents=True, exist_ok=True)
    (FIGURES_DIR / "preview").mkdir(parents=True, exist_ok=True)

    graph_path = NETWORKS_DIR / f"pmfg_{NETWORK_KIND}_core_historical_1998_2025.graphml"
    if not graph_path.exists():
        raise FileNotFoundError(f"Missing {graph_path}. Run 10_pmfg_network.py first.")

    G = nx.read_graphml(graph_path)
    for _, _, data in G.edges(data=True):
        data["abs_corr"] = abs(float(data.get("correlation", 0.0)))

    communities = list(
        nx.algorithms.community.louvain_communities(
            G,
            weight="abs_corr",
            resolution=COMMUNITY_RESOLUTION,
            seed=42,
        )
    )
    communities = sorted(communities, key=lambda group: (-len(group), sorted(group)[0]))

    cluster_by_node = {}
    for idx, community in enumerate(communities, start=1):
        for node in community:
            cluster_by_node[node] = idx
            G.nodes[node]["cluster"] = idx

    cluster_graph = nx.Graph()
    for idx, community in enumerate(communities, start=1):
        cluster_graph.add_node(idx, size=len(community))

    for u, v, data in G.edges(data=True):
        cu, cv = cluster_by_node[u], cluster_by_node[v]
        if cu == cv:
            continue
        weight = data["abs_corr"]
        current = cluster_graph.get_edge_data(cu, cv, default={}).get("weight", 0.0)
        cluster_graph.add_edge(cu, cv, weight=current + weight)

    cluster_pos = nx.spring_layout(cluster_graph, seed=9, k=1.6, iterations=3000, weight="weight", scale=4.0)
    cluster_pos = normalize_positions(cluster_pos)

    # Wide stretched cluster map; this keeps the airy chain-like structure that
    # makes the decomposition easy to read.
    for key, val in cluster_pos.items():
        cluster_pos[key] = np.array([1.65 * val[0], 1.15 * val[1]])

    pos: dict[str, np.ndarray] = {}
    for idx, community in enumerate(communities, start=1):
        subgraph = G.subgraph(community)
        local_scale = 0.12 + 0.055 * np.sqrt(len(community))
        if len(community) == 1:
            local = {next(iter(community)): np.array([0.0, 0.0])}
        else:
            local = nx.spring_layout(
                subgraph,
                seed=100 + idx,
                k=0.42,
                iterations=2000,
                weight="abs_corr",
                scale=local_scale,
            )
        local = normalize_positions({node: np.array(value) for node, value in local.items()})
        for node, value in local.items():
            pos[node] = cluster_pos[idx] + local_scale * value

    plt.rcParams["font.family"] = "serif"
    fig = plt.figure(figsize=(9.2, 10.6), facecolor="white")
    grid = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[4.8, 1.25], hspace=0.08)
    ax_net = fig.add_subplot(grid[0])
    ax_bar = fig.add_subplot(grid[1])

    # Draw inter-cluster edges first, then intra-cluster edges on top.
    edge_items = sorted(G.edges(data=True), key=lambda item: item[2]["abs_corr"])
    for edge_idx, (u, v, data) in enumerate(edge_items):
        cu, cv = cluster_by_node[u], cluster_by_node[v]
        corr = data["abs_corr"]
        width = 0.18 + 1.7 * corr
        rad = [-0.23, -0.15, -0.08, 0.08, 0.15, 0.23][edge_idx % 6]

        if cu == cv:
            base = CLUSTER_PALETTE[(cu - 1) % len(CLUSTER_PALETTE)]
            alpha = 0.25 + 0.42 * min(corr, 0.8)
        else:
            base = "#8f8f8f"
            alpha = 0.10 + 0.24 * min(corr, 0.8)

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            ax=ax_net,
            width=width,
            edge_color=[to_rgba(base, alpha)],
            connectionstyle=f"arc3,rad={rad}",
            arrows=True,
            arrowstyle="-",
            min_source_margin=2,
            min_target_margin=2,
        )

    node_colors = [CLUSTER_PALETTE[(cluster_by_node[node] - 1) % len(CLUSTER_PALETTE)] for node in G.nodes()]
    node_sizes = [
        10 + 65 * float(G.nodes[node].get("betweenness_centrality", 0.0)) ** 0.5
        for node in G.nodes()
    ]
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax_net,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="#1f1f1f",
        linewidths=0.22,
        alpha=0.96,
    )

    # Cluster numbers at community centroids.
    for idx, community in enumerate(communities, start=1):
        coords = np.array([pos[node] for node in community])
        centroid = coords.mean(axis=0)
        ax_net.text(
            centroid[0],
            centroid[1],
            str(idx),
            ha="center",
            va="center",
            fontsize=15,
            color="black",
            path_effects=[pe.withStroke(linewidth=3.0, foreground="white", alpha=0.82)],
        )

    coords = np.array(list(pos.values()))
    ax_net.set_xlim(coords[:, 0].min() - 0.14, coords[:, 0].max() + 0.14)
    ax_net.set_ylim(coords[:, 1].min() - 0.18, coords[:, 1].max() + 0.14)
    ax_net.axis("off")
    ax_net.set_aspect("equal")

    sector_rows = []
    for idx, community in enumerate(communities, start=1):
        counts: dict[str, int] = {}
        for node in community:
            sector = G.nodes[node].get("sector", "Unknown")
            counts[sector] = counts.get(sector, 0) + 1
        total = sum(counts.values())
        for sector, count in counts.items():
            sector_rows.append({"cluster": idx, "sector": sector, "share": count / total, "count": count})

    sector_df = pd.DataFrame(sector_rows)
    table_path = TABLES_DIR / f"pmfg_{NETWORK_KIND}_cluster_sector_decomposition.csv"
    sector_df.to_csv(table_path, index=False)

    sectors = [sector for sector in SECTOR_PALETTE if sector_df["sector"].eq(sector).any()]
    y_positions = np.arange(1, len(communities) + 1)
    for idx in y_positions:
        left = 0.0
        row = sector_df[sector_df["cluster"] == idx].set_index("sector")
        for sector in sectors:
            share = float(row.loc[sector, "share"]) if sector in row.index else 0.0
            if share <= 0:
                continue
            ax_bar.barh(
                idx,
                share,
                left=left,
                height=0.72,
                color=SECTOR_PALETTE.get(sector, "#aaaaaa"),
                edgecolor="none",
            )
            left += share

    ax_bar.set_xlim(0, 1)
    ax_bar.set_ylim(0.35, len(communities) + 0.65)
    ax_bar.set_yticks(y_positions)
    ax_bar.set_ylabel("Cluster", fontsize=8)
    ax_bar.set_title("cluster decomposition by sector", fontsize=8, pad=5)
    ax_bar.tick_params(axis="both", labelsize=7, length=2)
    ax_bar.grid(axis="x", color="#e6e6e6", linewidth=0.5)
    for spine in ax_bar.spines.values():
        spine.set_color("#777777")
        spine.set_linewidth(0.5)

    handles = [mpatches.Patch(color=SECTOR_PALETTE[sector], label=sector) for sector in sectors]
    ax_bar.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
        fontsize=6.5,
        borderaxespad=0,
    )

    pdf_path = FIGURES_DIR / "vector" / "figure_15b_pmfg_cluster_sector_decomposition.pdf"
    png_path = FIGURES_DIR / "preview" / "figure_15b_pmfg_cluster_sector_decomposition.png"
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    fig.savefig(png_path, dpi=600, bbox_inches="tight")
    plt.close(fig)

    print("Saved clustered PMFG sector-decomposition figure:")
    print(f"  {pdf_path}")
    print(f"  {png_path}")
    print(f"  {table_path}")


if __name__ == "__main__":
    main()
