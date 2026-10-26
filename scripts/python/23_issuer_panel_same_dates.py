from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "outputs" / "tables"
MAIN_START = pd.Timestamp("2006-08-23")
MAIN_END = pd.Timestamp("2024-08-15")


def rmt_components(returns: pd.DataFrame) -> tuple[dict[str, object], pd.DataFrame, np.ndarray]:
    corr = returns.corr().to_numpy(dtype=float).copy()
    eigenvalues, eigenvectors = np.linalg.eigh(corr)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    n_assets, n_obs = returns.shape[1], returns.shape[0]
    q = n_obs / n_assets
    lambda_plus = 1 + 1 / q + 2 * np.sqrt(1 / q)
    n_above = int(np.sum(eigenvalues > lambda_plus))
    group = np.zeros_like(corr)
    for k in range(1, n_above):
        vec = eigenvectors[:, k:k + 1]
        group += eigenvalues[k] * (vec @ vec.T)
    np.fill_diagonal(corr, 1.0)
    off_diagonal = corr[np.triu_indices(n_assets, k=1)]
    summary: dict[str, object] = {
        "assets": n_assets,
        "observations": n_obs,
        "start_date": returns.index.min().date().isoformat(),
        "end_date": returns.index.max().date().isoformat(),
        "Q": q,
        "lambda_plus": lambda_plus,
        "eigenvalues_above_lambda_plus": n_above,
        "non_market_modes_above_lambda_plus": max(0, n_above - 1),
        "lambda_1": eigenvalues[0],
        "lambda_1_over_N": eigenvalues[0] / n_assets,
        "mean_pairwise_correlation": float(off_diagonal.mean()),
        "group_eigenvalues": ";".join(f"{value:.8f}" for value in eigenvalues[1:n_above]),
    }
    eigen_table = pd.DataFrame({"rank": np.arange(1, n_assets + 1), "eigenvalue": eigenvalues})
    return summary, eigen_table, group


def graph_summary(
    corr: np.ndarray,
    symbols: list[str],
    metadata: pd.DataFrame,
    matrix_type: str,
    panel: str,
    observations: int,
) -> list[dict[str, object]]:
    clipped = np.clip(corr.copy(), -1, 1)
    np.fill_diagonal(clipped, 1)
    distance = np.sqrt(2 * (1 - clipped))
    sector = metadata.set_index("symbol")["sector"].to_dict()
    subsector = metadata.set_index("symbol")["subsector"].to_dict()
    candidates = []
    complete = nx.Graph()
    complete.add_nodes_from(symbols)
    for i, source in enumerate(symbols):
        for j in range(i + 1, len(symbols)):
            target = symbols[j]
            edge = {
                "weight": float(distance[i, j]),
                "distance": float(distance[i, j]),
                "correlation": float(corr[i, j]),
                "same_sector": sector[source] == sector[target],
                "same_subsector": subsector[source] == subsector[target],
            }
            complete.add_edge(source, target, **edge)
            candidates.append((edge["distance"], source, target, edge))

    mst = nx.minimum_spanning_tree(complete, weight="weight")
    pmfg = nx.Graph()
    pmfg.add_nodes_from(symbols)
    expected_edges = 3 * len(symbols) - 6
    for _, source, target, data in sorted(candidates, key=lambda item: item[0]):
        pmfg.add_edge(source, target, **data)
        is_planar, _ = nx.check_planarity(pmfg)
        if not is_planar:
            pmfg.remove_edge(source, target)
        if pmfg.number_of_edges() == expected_edges:
            break

    rows = []
    for network_name, graph in (("MST", mst), ("PMFG", pmfg)):
        edges = list(graph.edges(data=True))
        betweenness = nx.betweenness_centrality(graph, weight="weight")
        degree = dict(graph.degree())
        clustering = nx.clustering(graph, weight="weight") if network_name == "PMFG" else {}
        edge_corr = np.array([data["correlation"] for _, _, data in edges])
        same_sector = sum(bool(data["same_sector"]) for _, _, data in edges)
        same_subsector = sum(bool(data["same_subsector"]) for _, _, data in edges)
        row: dict[str, object] = {
            "panel": panel,
            "network": network_name,
            "matrix": matrix_type,
            "assets": len(symbols),
            "observations": observations,
            "edges": len(edges),
            "expected_edges": expected_edges if network_name == "PMFG" else len(symbols) - 1,
            "planar": nx.check_planarity(graph)[0] if network_name == "PMFG" else True,
            "mean_edge_correlation": float(edge_corr.mean()),
            "same_sector_edge_ratio": same_sector / len(edges),
            "same_subsector_edge_ratio": same_subsector / len(edges),
            "average_clustering": float(np.mean(list(clustering.values()))) if clustering else 0.0,
            "top_degree_node": max(degree, key=degree.get),
            "top_betweenness_node": max(betweenness, key=betweenness.get),
        }
        rows.append(row)
    return rows


def main() -> None:
    wide = pd.read_csv(TABLES / "core_historical_returns_wide_1998_2025.csv", parse_dates=["date"]).set_index("date")
    main_panel = wide.loc[MAIN_START:MAIN_END].dropna(how="any").sort_index()
    if main_panel.shape != (1527, 58):
        raise RuntimeError(f"Unexpected main panel shape {main_panel.shape}; expected (1527, 58)")

    metadata = pd.read_csv(TABLES / "assets_sector_map.csv")
    if set(main_panel.columns) != set(metadata["symbol"]):
        raise RuntimeError("Main panel and sector-map symbols do not match")

    long = pd.read_csv(
        TABLES / "core_historical_returns_long_1998_2025.csv",
        usecols=["date", "symbol", "financial_volume"],
        parse_dates=["date"],
    )
    common_dates = set(main_panel.index)
    common_liquidity = (
        long[long["date"].isin(common_dates)]
        .groupby("symbol", as_index=False)["financial_volume"]
        .mean()
        .rename(columns={"financial_volume": "mean_financial_volume_common_panel"})
    )
    selection = metadata.merge(common_liquidity, on="symbol", how="left")
    selection["full_sample_valid_return_observations"] = selection["symbol"].map(wide.notna().sum())
    selection["common_panel_observations"] = selection["symbol"].map(main_panel.notna().sum())
    selection = selection.sort_values(
        ["company_name", "common_panel_observations", "mean_financial_volume_common_panel", "symbol"],
        ascending=[True, False, False, True],
    ).drop_duplicates("company_name", keep="first")
    selected_symbols = selection["symbol"].tolist()
    issuer_panel = main_panel[selected_symbols].copy()

    selection_out = metadata.merge(common_liquidity, on="symbol", how="left")
    selection_out["full_sample_valid_return_observations"] = selection_out["symbol"].map(wide.notna().sum())
    selection_out["common_panel_observations"] = selection_out["symbol"].map(main_panel.notna().sum())
    selection_out["retained_in_issuer_panel"] = selection_out["symbol"].isin(selected_symbols)
    selection_out["selection_rule"] = "max common-panel observations, then max mean financial volume in common panel, then ticker"
    duplicated_names = metadata.groupby("company_name")["symbol"].transform("size") > 1
    selection_out.loc[duplicated_names].sort_values(["company_name", "symbol"]).to_csv(
        TABLES / "issuer_class_sensitivity_selection.csv", index=False
    )

    summaries = []
    network_rows: list[dict[str, object]] = []
    for panel_name, frame in (("full share-class panel", main_panel), ("issuer-collapsed panel", issuer_panel)):
        summary, eigen_table, group = rmt_components(frame)
        summaries.append({"panel": panel_name, **summary})
        if panel_name == "issuer-collapsed panel":
            eigen_table.to_csv(TABLES / "issuer_panel_same_dates_eigenvalues.csv", index=False)
            pd.DataFrame(group, index=frame.columns, columns=frame.columns).to_csv(
                TABLES / "issuer_panel_same_dates_c_group.csv"
            )
        else:
            pd.DataFrame(group, index=frame.columns, columns=frame.columns).to_csv(
                TABLES / "full_panel_same_dates_c_group.csv"
            )
        meta = metadata.loc[metadata["symbol"].isin(frame.columns)].copy()
        corr = frame.corr().to_numpy(dtype=float)
        network_rows += graph_summary(corr, frame.columns.tolist(), meta, "original", panel_name, len(frame))
        network_rows += graph_summary(group, frame.columns.tolist(), meta, "group_mode", panel_name, len(frame))

    pd.DataFrame(summaries).to_csv(TABLES / "issuer_class_rmt_sensitivity.csv", index=False)
    pd.DataFrame(network_rows).to_csv(TABLES / "issuer_panel_network_sensitivity_same_dates.csv", index=False)
    print(pd.DataFrame(summaries).to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    print(pd.DataFrame(network_rows).to_string(index=False))
    print("Issuer representatives:", ", ".join(selected_symbols))


if __name__ == "__main__":
    main()
