from __future__ import annotations

"""Temporal stability of MST and PMFG edges, hubs and communities.

The complete 58-asset RMT panel is divided into three consecutive equal-sized
trading-day windows.  Each window re-estimates its correlation and RMT group
component before constructing the graph, so overlap measures quantify temporal
rather than layout stability.
"""

from itertools import combinations
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TABLES = PROJECT_ROOT / "outputs" / "tables"
RETURNS_PATH = TABLES / "core_historical_returns_wide_1998_2025.csv"
WINDOW_SUMMARY_PATH = TABLES / "network_temporal_stability_window_summary.csv"
PAIRWISE_PATH = TABLES / "network_temporal_stability_pairwise.csv"
HUB_PATH = TABLES / "network_temporal_stability_hub_frequency.csv"


def group_mode(correlation: np.ndarray, n_obs: int) -> np.ndarray:
    n_assets = correlation.shape[0]
    q_ratio = n_obs / n_assets
    lambda_plus = (1 + np.sqrt(1 / q_ratio)) ** 2
    eigenvalues, eigenvectors = np.linalg.eigh(correlation)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    matrix = np.zeros_like(correlation)
    for rank in range(1, n_assets):
        if eigenvalues[rank] > lambda_plus:
            vector = eigenvectors[:, rank]
            matrix += eigenvalues[rank] * np.outer(vector, vector)
    np.fill_diagonal(matrix, 1.0)
    return matrix


def edge_candidates(matrix: np.ndarray, symbols: list[str]):
    distance_matrix = np.sqrt(2 * (1 - np.clip(matrix, -1, 1)))
    return sorted(
        (
            float(distance_matrix[i, j]),
            symbols[i],
            symbols[j],
            float(matrix[i, j]),
        )
        for i in range(len(symbols))
        for j in range(i + 1, len(symbols))
    )


def construct_mst(matrix: np.ndarray, symbols: list[str]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(symbols)
    graph.add_weighted_edges_from((u, v, distance) for distance, u, v, _ in edge_candidates(matrix, symbols))
    return nx.minimum_spanning_tree(graph, weight="weight")


def construct_pmfg(matrix: np.ndarray, symbols: list[str]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(symbols)
    target_edges = 3 * len(symbols) - 6
    for distance, source, target, correlation in edge_candidates(matrix, symbols):
        graph.add_edge(source, target, weight=distance, correlation=correlation)
        if not nx.check_planarity(graph)[0]:
            graph.remove_edge(source, target)
        if graph.number_of_edges() == target_edges:
            break
    if graph.number_of_edges() != target_edges:
        raise RuntimeError("PMFG did not reach its planar edge count")
    return graph


def graph_features(graph: nx.Graph) -> tuple[set[tuple[str, str]], set[str], np.ndarray]:
    edges = {tuple(sorted(edge)) for edge in graph.edges()}
    betweenness = nx.betweenness_centrality(graph, weight="weight")
    top_hubs = {symbol for symbol, _ in sorted(betweenness.items(), key=lambda item: (-item[1], item[0]))[:5]}
    communities = list(nx.algorithms.community.greedy_modularity_communities(graph, weight=None))
    labels: dict[str, int] = {}
    for label, community in enumerate(communities):
        labels.update({symbol: label for symbol in community})
    return edges, top_hubs, np.array([labels[symbol] for symbol in sorted(graph.nodes())])


def main() -> None:
    returns = pd.read_csv(RETURNS_PATH)
    returns["date"] = pd.to_datetime(returns["date"])
    complete = returns.drop(columns="date").dropna(how="any")
    dates = returns.loc[complete.index, "date"].reset_index(drop=True)
    symbols = complete.columns.tolist()
    windows = np.array_split(np.arange(len(complete)), 3)

    records: list[dict[str, object]] = []
    features: dict[tuple[str, str, int], tuple[set[tuple[str, str]], set[str], np.ndarray]] = {}

    for window_id, positions in enumerate(windows, start=1):
        window_returns = complete.iloc[positions]
        original = window_returns.corr().to_numpy()
        matrices = {"original": original, "group_mode": group_mode(original, len(window_returns))}
        for matrix_type, matrix in matrices.items():
            for network_type, constructor in {"MST": construct_mst, "PMFG": construct_pmfg}.items():
                graph = constructor(matrix, symbols)
                edges, hubs, communities = graph_features(graph)
                features[(network_type, matrix_type, window_id)] = (edges, hubs, communities)
                records.append(
                    {
                        "window": window_id,
                        "start_date": dates.iloc[positions[0]].date().isoformat(),
                        "end_date": dates.iloc[positions[-1]].date().isoformat(),
                        "n_observations": len(window_returns),
                        "network": network_type,
                        "matrix": matrix_type,
                        "n_edges": len(edges),
                        "top5_betweenness_hubs": "|".join(sorted(hubs)),
                    }
                )

    pairwise: list[dict[str, object]] = []
    for network_type in ["MST", "PMFG"]:
        for matrix_type in ["original", "group_mode"]:
            for left, right in combinations([1, 2, 3], 2):
                edges_l, hubs_l, communities_l = features[(network_type, matrix_type, left)]
                edges_r, hubs_r, communities_r = features[(network_type, matrix_type, right)]
                pairwise.append(
                    {
                        "network": network_type,
                        "matrix": matrix_type,
                        "window_left": left,
                        "window_right": right,
                        "edge_jaccard": len(edges_l & edges_r) / len(edges_l | edges_r),
                        "top5_hub_overlap": len(hubs_l & hubs_r) / 5,
                        "community_adjusted_rand_index": adjusted_rand_score(communities_l, communities_r),
                    }
                )

    hubs: list[dict[str, object]] = []
    for network_type in ["MST", "PMFG"]:
        for matrix_type in ["original", "group_mode"]:
            counts: dict[str, int] = {}
            for window in [1, 2, 3]:
                for symbol in features[(network_type, matrix_type, window)][1]:
                    counts[symbol] = counts.get(symbol, 0) + 1
            for symbol, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
                hubs.append(
                    {
                        "network": network_type,
                        "matrix": matrix_type,
                        "symbol": symbol,
                        "top5_betweenness_window_count": count,
                        "top5_betweenness_window_share": count / 3,
                    }
                )

    pd.DataFrame(records).to_csv(WINDOW_SUMMARY_PATH, index=False)
    pd.DataFrame(pairwise).to_csv(PAIRWISE_PATH, index=False)
    pd.DataFrame(hubs).to_csv(HUB_PATH, index=False)
    print(f"Saved {WINDOW_SUMMARY_PATH}")
    print(f"Saved {PAIRWISE_PATH}")
    print(f"Saved {HUB_PATH}")
    print(pd.DataFrame(pairwise).groupby(["network", "matrix"], as_index=False).mean(numeric_only=True).to_string(index=False))


if __name__ == "__main__":
    main()
