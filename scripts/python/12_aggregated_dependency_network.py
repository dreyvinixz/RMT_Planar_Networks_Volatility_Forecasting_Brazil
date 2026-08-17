from __future__ import annotations

import sys
from pathlib import Path
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgba

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
NETWORKS_DIR = PROJECT_ROOT / "outputs" / "networks" / "graphml"

# Enhanced Palette for B3 Sectors
CUSTOM_PALETTE = {
    "Financials": "#2ca02c", 
    "Basic Materials": "#ff7f0e", 
    "Oil Gas and Biofuels": "#1f77b4", 
    "Utilities": "#e377c2", 
    "Consumer Cyclical": "#8c564b", 
    "Consumer Non-Cyclical": "#17becf", 
    "Industrials": "#d62728", 
    "Real Estate": "#7f7f7f", 
    "Telecommunications": "#bcbd22", 
    "Unknown": "#aaaaaa"
}

def main() -> None:
    (FIGURES_DIR / "vector").mkdir(parents=True, exist_ok=True)
    (FIGURES_DIR / "preview").mkdir(parents=True, exist_ok=True)
    NETWORKS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Loading data for Aggregated Dependency Network...")
    
    # Load matrices
    mat_path = OUTPUT_DIR / "correlation_group_mode_core_historical_1998_2025.csv"
    C_df = pd.read_csv(mat_path, index_col=0)
    symbols = C_df.columns.tolist()
    
    # Load metadata
    sector_df = pd.read_csv(OUTPUT_DIR / "assets_sector_map.csv").set_index("symbol")
    try:
        universe_df = pd.read_csv(OUTPUT_DIR / "core_historical_universe_1998_2025.csv").set_index("symbol")
    except FileNotFoundError:
        universe_df = pd.DataFrame(index=symbols, columns=["avg_financial_volume"])
        universe_df["avg_financial_volume"] = 1.0
        
    # Map symbols to subsector and sector
    asset_to_sub = {}
    asset_to_sec = {}
    asset_to_vol = {}
    
    for sym in symbols:
        sub = "Unknown"
        sec = "Unknown"
        vol = 0.0
        
        if sym in sector_df.index:
            sub = str(sector_df.loc[sym, "subsector"])
            sec = str(sector_df.loc[sym, "sector"])
        if sym in universe_df.index:
            vol_val = universe_df.loc[sym, "avg_financial_volume"]
            vol = float(vol_val) if pd.notnull(vol_val) else 0.0
            
        # Clean nulls/nans
        if sub in ["nan", "None", ""]: sub = "Unknown"
        if sec in ["nan", "None", ""]: sec = "Unknown"
            
        asset_to_sub[sym] = sub
        asset_to_sec[sym] = sec
        asset_to_vol[sym] = vol
        
    subsectors = sorted(list(set(asset_to_sub.values())))
    n_subs = len(subsectors)
    
    print("Computing pairwise aggregated dependencies...")
    # Initialize dependency matrix
    dep_mat = pd.DataFrame(np.nan, index=subsectors, columns=subsectors)
    
    # Compute node attributes
    node_data = []
    
    for subA in subsectors:
        assets_A = [s for s in symbols if asset_to_sub[s] == subA]
        if not assets_A:
            continue
            
        secA = asset_to_sec[assets_A[0]] # Assuming all assets in subsector have same macro-sector
        n_assets = len(assets_A)
        total_vol = sum([asset_to_vol[s] for s in assets_A])
        avg_vol = total_vol / n_assets if n_assets > 0 else 0
        
        # Internal dependency
        internal_corrs = []
        if n_assets > 1:
            for i in range(len(assets_A)):
                for j in range(i+1, len(assets_A)):
                    val = C_df.loc[assets_A[i], assets_A[j]]
                    if pd.notnull(val):
                        internal_corrs.append(val)
        
        internal_mean = np.mean(internal_corrs) if internal_corrs else 0.0
        internal_median = np.median(internal_corrs) if internal_corrs else 0.0
        
        node_data.append({
            "node_id": subA,
            "subsector": subA,
            "sector": secA,
            "n_assets": n_assets,
            "avg_financial_volume": avg_vol,
            "total_financial_volume": total_vol,
            "internal_mean_correlation": internal_mean,
            "internal_median_correlation": internal_median
        })
        
        # Cross dependencies
        for subB in subsectors:
            if subA == subB:
                dep_mat.loc[subA, subB] = 1.0 # Or internal_mean, but usually diagonal is 1 for matrices
                continue
                
            assets_B = [s for s in symbols if asset_to_sub[s] == subB]
            if not assets_B:
                continue
                
            corrs = []
            for sA in assets_A:
                for sB in assets_B:
                    val = C_df.loc[sA, sB]
                    if pd.notnull(val):
                        corrs.append(val)
                        
            mean_dep = np.mean(corrs) if corrs else 0.0
            dep_mat.loc[subA, subB] = mean_dep
            
    dep_mat_path = OUTPUT_DIR / "subsector_dependency_matrix_core_historical_1998_2025.csv"
    dep_mat.to_csv(dep_mat_path)
    
    # Convert node_data to dataframe
    nodes_df = pd.DataFrame(node_data)
    
    # Top-K Filtering Strategy (k=4)
    K = 4
    print(f"Applying Top-{K} neighbors filtering strategy...")
    
    edges_set = set()
    candidate_edges_count = 0
    
    for subA in subsectors:
        row = dep_mat.loc[subA].drop(subA)
        candidate_edges_count += len(row)
        # Get top K targets
        top_k = row.nlargest(K)
        for subB, weight in top_k.items():
            if pd.notnull(weight):
                # Ensure undirected tuple (alphabetical)
                u, v = sorted([subA, subB])
                edges_set.add((u, v))
                
    n_retained = len(edges_set)
    
    G = nx.Graph()
    # Add nodes
    for _, row in nodes_df.iterrows():
        G.add_node(row["subsector"], **row.to_dict())
        
    # Add edges
    edge_data_list = []
    for u, v in edges_set:
        weight = dep_mat.loc[u, v]
        abs_weight = abs(weight)
        
        assets_u = [s for s in symbols if asset_to_sub[s] == u]
        assets_v = [s for s in symbols if asset_to_sub[s] == v]
        n_links = len(assets_u) * len(assets_v)
        
        sec_u = nodes_df[nodes_df["subsector"] == u]["sector"].iloc[0]
        sec_v = nodes_df[nodes_df["subsector"] == v]["sector"].iloc[0]
        same_sec = (sec_u == sec_v)
        
        edge_dict = {
            "source": u,
            "target": v,
            "sector_source": sec_u,
            "sector_target": sec_v,
            "subsector_source": u,
            "subsector_target": v,
            "mean_dependency": weight,
            "mean_abs_dependency": abs_weight,
            "n_pairwise_links": n_links,
            "same_sector": same_sec,
            "weight": weight # for layout
        }
        edge_data_list.append(edge_dict)
        G.add_edge(u, v, **edge_dict)
        
    # Calculate Centralities
    deg = dict(G.degree())
    weighted_deg = dict(G.degree(weight='weight'))
    betw = nx.betweenness_centrality(G, weight='weight')
    
    nodes_df["degree"] = nodes_df["subsector"].map(deg)
    nodes_df["weighted_degree"] = nodes_df["subsector"].map(weighted_deg)
    nodes_df["betweenness"] = nodes_df["subsector"].map(betw)
    
    for n in G.nodes():
        G.nodes[n]["degree"] = deg[n]
        G.nodes[n]["weighted_degree"] = weighted_deg[n]
        G.nodes[n]["betweenness"] = betw[n]
        
    nodes_path = OUTPUT_DIR / "subsector_dependency_nodes_core_historical_1998_2025.csv"
    nodes_df.to_csv(nodes_path, index=False)
    
    edges_df = pd.DataFrame(edge_data_list)
    edges_path = OUTPUT_DIR / "subsector_dependency_edges_core_historical_1998_2025.csv"
    edges_df.to_csv(edges_path, index=False)
    
    # Save GraphML
    nx.write_graphml(G, NETWORKS_DIR / "subsector_dependency_network_core_historical_1998_2025.graphml")
    
    # Summary
    deps = edges_df["mean_dependency"].values if not edges_df.empty else []
    top_deg = nodes_df.sort_values("degree", ascending=False).iloc[0]["subsector"] if not nodes_df.empty else ""
    top_bet = nodes_df.sort_values("betweenness", ascending=False).iloc[0]["subsector"] if not nodes_df.empty else ""
    top_wdeg = nodes_df.sort_values("weighted_degree", ascending=False).iloc[0]["subsector"] if not nodes_df.empty else ""
    
    density = nx.density(G)
    
    summary_df = pd.DataFrame([{
        "n_subsectors": n_subs,
        "n_edges": n_retained,
        "density": density,
        "mean_edge_dependency": np.mean(deps) if len(deps)>0 else 0,
        "median_edge_dependency": np.median(deps) if len(deps)>0 else 0,
        "mean_internal_dependency": nodes_df["internal_mean_correlation"].mean() if not nodes_df.empty else 0,
        "top_degree_subsector": top_deg,
        "top_betweenness_subsector": top_bet,
        "top_weighted_degree_subsector": top_wdeg
    }])
    sum_path = OUTPUT_DIR / "subsector_dependency_summary_core_historical_1998_2025.csv"
    summary_df.to_csv(sum_path, index=False)
    
    print("\nAggregated dependency network")
    print("  matrix source: correlation_group_mode_core_historical_1998_2025.csv")
    print("  aggregation level: subsector")
    print(f"  n_subsectors: {n_subs}")
    print(f"  n_candidate_edges: {candidate_edges_count // 2} (undirected pairs)")
    print(f"  n_retained_edges: {n_retained}")
    print(f"  density: {density:.4f}")
    print(f"  mean_edge_dependency: {np.mean(deps):.4f}" if len(deps)>0 else "  mean_edge_dependency: 0")
    print(f"  median_edge_dependency: {np.median(deps):.4f}" if len(deps)>0 else "  median_edge_dependency: 0")
    print(f"  top_degree_subsector: {top_deg}")
    print(f"  top_betweenness_subsector: {top_bet}")
    print(f"  top_weighted_degree_subsector: {top_wdeg}")
    
    # ---------------------------------------------------------
    # Visualization: Figure 15
    # ---------------------------------------------------------
    print("\nGenerating Figure 15...")
    plt.rcParams["font.family"] = "serif"
    fig, ax = plt.subplots(figsize=(18, 12), facecolor="white")

    edge_abs_weight = {(u, v): abs(d["mean_dependency"]) for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, edge_abs_weight, "abs_weight")

    # A wide, deterministic spring layout makes the subsector graph read closer
    # to the PMFG visual language used in Figure 12.
    pos = nx.spring_layout(G, seed=42, k=1.15, iterations=5000, weight="abs_weight", scale=3.4)
    xs = np.array([p[0] for p in pos.values()])
    ys = np.array([p[1] for p in pos.values()])
    x_mid, y_mid = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    x_span = xs.max() - xs.min()
    y_span = ys.max() - ys.min()
    pos = {
        n: (
            1.30 * (x - x_mid) / max(x_span, 1e-12),
            0.88 * (y - y_mid) / max(y_span, 1e-12),
        )
        for n, (x, y) in pos.items()
    }

    node_sizes = []
    node_colors = []
    for n, d in G.nodes(data=True):
        n_assets = float(d.get("n_assets", 1))
        node_sizes.append(420 + 245 * np.sqrt(n_assets))
        node_colors.append(CUSTOM_PALETTE.get(d.get("sector", "Unknown"), "#aaaaaa"))

    edge_abs = np.array([abs(d["mean_dependency"]) for _, _, d in G.edges(data=True)])
    edge_min = edge_abs.min() if len(edge_abs) else 0.0
    edge_max = edge_abs.max() if len(edge_abs) else 1.0

    edge_list = sorted(G.edges(data=True), key=lambda item: abs(item[2]["mean_dependency"]))
    for edge_idx, (u, v, d) in enumerate(edge_list):
        dep = abs(d["mean_dependency"])
        scaled = (dep - edge_min) / (edge_max - edge_min + 1e-12)
        width = 0.25 + 3.1 * scaled
        alpha = 0.12 + 0.52 * scaled

        if d["same_sector"]:
            base_col = CUSTOM_PALETTE.get(G.nodes[u].get("sector", "Unknown"), "#777777")
        else:
            base_col = "#9a9a9a"

        # Alternate mild curvature so dense local neighborhoods do not collapse
        # into a single straight bundle.
        rad = [-0.18, -0.10, 0.10, 0.18][edge_idx % 4]
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            ax=ax,
            width=width,
            edge_color=[to_rgba(base_col, alpha=alpha)],
            connectionstyle=f"arc3,rad={rad}",
            arrows=True,
            arrowstyle="-",
            min_source_margin=10,
            min_target_margin=10,
        )

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="#ffffff",
        linewidths=1.25,
        alpha=0.96,
    )

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 0.23, max(xs) + 0.23)
    ax.set_ylim(min(ys) - 0.18, max(ys) + 0.18)
    ax.axis("off")
    ax.set_aspect("equal")

    texts = []
    for n, (x, y) in pos.items():
        vec = np.array([x, y])
        norm = np.linalg.norm(vec)
        offset = np.array([0.0, 0.055]) if norm == 0 else 0.065 * vec / norm
        label = textwrap.fill(n, width=18, break_long_words=False)
        texts.append(
            ax.text(
                x + offset[0],
                y + offset[1],
                label,
                fontsize=8.4,
                color="#1f1f1f",
                ha="center",
                va="center",
                linespacing=0.95,
                bbox=dict(
                    facecolor="white",
                    edgecolor="#d0d0d0",
                    linewidth=0.25,
                    alpha=0.86,
                    pad=0.20,
                ),
            )
        )

    def repel_labels(text_artists: list[plt.Text], iterations: int = 140) -> None:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        inv = ax.transData.inverted()

        for _ in range(iterations):
            moved = False
            boxes = [text.get_window_extent(renderer=renderer).expanded(1.05, 1.18) for text in text_artists]
            for i in range(len(text_artists)):
                for j in range(i + 1, len(text_artists)):
                    if not boxes[i].overlaps(boxes[j]):
                        continue

                    ci = np.array([(boxes[i].x0 + boxes[i].x1) / 2, (boxes[i].y0 + boxes[i].y1) / 2])
                    cj = np.array([(boxes[j].x0 + boxes[j].x1) / 2, (boxes[j].y0 + boxes[j].y1) / 2])
                    direction = ci - cj
                    norm = np.linalg.norm(direction)
                    if norm == 0:
                        direction = np.array([1.0, 0.4])
                        norm = np.linalg.norm(direction)
                    direction = direction / norm

                    overlap_x = min(boxes[i].x1, boxes[j].x1) - max(boxes[i].x0, boxes[j].x0)
                    overlap_y = min(boxes[i].y1, boxes[j].y1) - max(boxes[i].y0, boxes[j].y0)
                    shift = max(1.5, min(9.0, 0.16 * min(overlap_x, overlap_y)))

                    for text, sign in ((text_artists[i], 1), (text_artists[j], -1)):
                        display_pos = ax.transData.transform(text.get_position())
                        new_pos = inv.transform(display_pos + sign * direction * shift)
                        text.set_position(new_pos)

                    moved = True

            if not moved:
                break
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()

    repel_labels(texts)

    all_sectors = sorted({d.get("sector", "Unknown") for _, d in G.nodes(data=True) if d.get("sector") != "Unknown"})
    sector_handles = [
        mpatches.Patch(color=CUSTOM_PALETTE.get(sec, "#aaaaaa"), label=sec)
        for sec in all_sectors
    ]
    edge_handles = [
        plt.Line2D([0], [0], color="#9a9a9a", lw=0.6, alpha=0.30, label="weaker dependency"),
        plt.Line2D([0], [0], color="#9a9a9a", lw=3.0, alpha=0.65, label="stronger dependency"),
    ]

    fig.legend(
        handles=sector_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.04),
        frameon=False,
        fontsize=10,
        ncol=5,
        title="Macro-sector",
        title_fontsize=10,
    )
    ax.legend(
        handles=edge_handles,
        loc="upper right",
        frameon=False,
        fontsize=10,
        title="Edge weight",
        title_fontsize=10,
    )

    plt.tight_layout(rect=[0, 0.12, 1, 1])
    
    pdf_path = FIGURES_DIR / "vector" / "figure_15_subsector_dependency_network.pdf"
    png_path = FIGURES_DIR / "preview" / "figure_15_subsector_dependency_network.png"
    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.savefig(png_path, dpi=600, bbox_inches="tight")
    plt.close()
    
    print("\nSaved outputs:")
    print(f"  {dep_mat_path.name}")
    print(f"  {edges_path.name}")
    print(f"  {nodes_path.name}")
    print(f"  {sum_path.name}")
    print("  subsector_dependency_network_core_historical_1998_2025.graphml")
    print("  figure_15_subsector_dependency_network.png")
    print("  figure_15_subsector_dependency_network.pdf")

if __name__ == "__main__":
    main()
