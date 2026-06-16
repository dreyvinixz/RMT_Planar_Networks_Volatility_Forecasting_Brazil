from __future__ import annotations

import sys
from pathlib import Path

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
    fig, ax = plt.subplots(figsize=(12.5, 9.5), facecolor="white")

    # Deterministic layout with stronger separation than the previous free spring plot.
    abs_weights = {(u, v): abs(d["weight"]) for u, v, d in G.edges(data=True)}
    nx.set_edge_attributes(G, abs_weights, "abs_weight")
    pos = nx.spring_layout(G, seed=12, k=1.85, iterations=3500, weight="abs_weight")

    # Normalize coordinates to a stable plotting box.
    xs = np.array([p[0] for p in pos.values()])
    ys = np.array([p[1] for p in pos.values()])
    x_mid, y_mid = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    span = max(xs.max() - xs.min(), ys.max() - ys.min())
    pos = {n: ((x - x_mid) / span, (y - y_mid) / span) for n, (x, y) in pos.items()}

    node_sizes = []
    node_colors = []
    for n, d in G.nodes(data=True):
        n_assets = float(d.get("n_assets", 1))
        node_sizes.append(240 + 170 * np.sqrt(n_assets))
        node_colors.append(CUSTOM_PALETTE.get(d.get("sector", "Unknown"), "#aaaaaa"))

    edge_abs = np.array([abs(d["mean_dependency"]) for _, _, d in G.edges(data=True)])
    edge_min = edge_abs.min() if len(edge_abs) else 0.0
    edge_max = edge_abs.max() if len(edge_abs) else 1.0

    for u, v, d in G.edges(data=True):
        dep = abs(d["mean_dependency"])
        scaled = (dep - edge_min) / (edge_max - edge_min + 1e-12)
        width = 0.35 + 2.4 * scaled
        alpha = 0.18 + 0.45 * scaled

        if d["same_sector"]:
            base_col = CUSTOM_PALETTE.get(G.nodes[u].get("sector", "Unknown"), "#777777")
        else:
            base_col = "#8a8a8a"

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            ax=ax,
            width=width,
            edge_color=[to_rgba(base_col, alpha=alpha)],
        )

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="#ffffff",
        linewidths=1.1,
        alpha=0.95,
    )

    # Place labels just outside the node centers to reduce node-label collisions.
    for n, (x, y) in pos.items():
        vec = np.array([x, y])
        norm = np.linalg.norm(vec)
        if norm == 0:
            offset = np.array([0.0, 0.035])
        else:
            offset = 0.035 * vec / norm
        lx, ly = x + offset[0], y + offset[1]
        ax.text(
            lx,
            ly,
            n,
            fontsize=6.9,
            color="#1f1f1f",
            ha="center",
            va="center",
            bbox=dict(facecolor="white", edgecolor="#dddddd", linewidth=0.25, alpha=0.82, pad=0.18),
        )

    ax.axis("off")
    ax.set_aspect("equal")

    all_sectors = sorted({d.get("sector", "Unknown") for _, d in G.nodes(data=True) if d.get("sector") != "Unknown"})
    sector_handles = [
        mpatches.Patch(color=CUSTOM_PALETTE.get(sec, "#aaaaaa"), label=sec)
        for sec in all_sectors
    ]
    edge_handles = [
        plt.Line2D([0], [0], color="#8a8a8a", lw=0.6, alpha=0.35, label="weaker dependency"),
        plt.Line2D([0], [0], color="#8a8a8a", lw=2.4, alpha=0.65, label="stronger dependency"),
    ]

    fig.legend(
        handles=sector_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.045),
        frameon=False,
        fontsize=8,
        ncol=3,
        title="Macro-sector",
        title_fontsize=8,
    )
    ax.legend(
        handles=edge_handles,
        loc="upper right",
        frameon=False,
        fontsize=8,
        title="Edge weight",
        title_fontsize=8,
    )

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 0.13, max(xs) + 0.13)
    ax.set_ylim(min(ys) - 0.13, max(ys) + 0.13)

    plt.tight_layout(rect=[0, 0.13, 1, 1])
    
    pdf_path = FIGURES_DIR / "vector" / "figure_15_subsector_dependency_network.pdf"
    png_path = FIGURES_DIR / "preview" / "figure_15_subsector_dependency_network.png"
    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
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
