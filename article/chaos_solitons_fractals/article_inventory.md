# Article Inventory — Chaos, Solitons & Fractals Draft

This inventory records the reproducible assets currently available for the full manuscript skeleton. The sector map is treated as an **initial macro-sector classification**, not a final exchange-certified taxonomy.

## Figures Available

| Candidate | Filename | Short description | Placement | Section |
|---|---|---|---|---|
| Figure 1 | `images/figure_1d_stylized_facts_demo_assets_clean_2006_2025.pdf` | Stylized facts for PETR4, VALE3 and BBDC4: normalized price, offset returns, CCDF, absolute-return ACF | Main text | Stylized facts and correlations |
| Figure 2a | `images/figure_2_correlation_histogram.pdf` | Full pairwise Pearson correlation distribution for the core historical universe | Main text | Stylized facts and correlations |
| Figure 2b | `images/figure_3_sector_correlation_distribution.pdf` | Within-sector vs between-sector correlation distribution | Main text | Stylized facts and correlations |
| Figure 3 | `images/figure_4_rolling_average_correlation.pdf` | Rolling average market correlation | Main text | Stylized facts and correlations |
| Figure 4 | `images/figure_6_rmt_eigenvalue_spectrum.pdf` | Empirical eigenvalue spectrum and Marcenko-Pastur bounds | Main text | RMT |
| Figure 5 | `images/figure_8_rmt_filtered_matrices.pdf` | Market, group, noise and filtered correlation matrices | Main text | RMT |
| Figure 6 | `images/figure_12b_pmfg_refined_comparison.pdf` | Refined PMFG comparison, original vs group-mode structure | Main text | Networks |
| Figure 7 | `images/figure_15_subsector_dependency_network.pdf` | Aggregated subsector dependency network | Main text | Networks |
| Figure 8 | `images/figure_16_volatility_forecast_model_comparison.pdf` | Volatility forecasting model comparison | Main text | Forecasting |
| Figure 9 | `images/figure_18_ml_feature_importance.pdf` | Random Forest feature importance across forecasting horizons | Main text | Forecasting |
| Appendix A1 | `images/figure_5_dynamic_pairwise_correlations.pdf` | Dynamic pairwise correlations for selected assets | Appendix candidate | Correlation dynamics |
| Appendix A2 | `images/figure_7b_rmt_top_eigenvectors_top_loadings.pdf` | Top eigenvector loadings | Appendix candidate | RMT |
| Appendix A3 | `images/figure_7a_rmt_top_eigenvectors_all_assets.pdf` | Eigenvector loadings for all assets | Appendix candidate | RMT |
| Appendix A4 | `images/figure_9_dendrograms_comparison.pdf` | Hierarchical clustering dendrograms | Appendix candidate | Clustering |
| Appendix A5 | `images/figure_10_ordered_heatmaps.pdf` | Ordered heatmaps | Appendix candidate | Clustering |
| Appendix A6 | `images/figure_11b_mst_refined_comparison.pdf` | Refined MST comparison | Appendix candidate | Networks |
| Appendix A7 | `images/figure_13_network_topology_comparison.pdf` | MST/PMFG topology comparison | Appendix candidate | Networks |
| Appendix A8 | `images/figure_14_network_hub_rank_comparison.pdf` | Hub-rank comparison across network filters | Appendix candidate | Networks |
| Appendix A9 | `images/figure_17_realized_vs_predicted_volatility.pdf` | Realized vs predicted volatility | Appendix candidate | Forecasting |

## Tables Available

| Candidate | Filename | Short description | Placement |
|---|---|---|---|
| Table 1 | `outputs/tables/table_1_descriptive_stats_2006_2025.tex` | Descriptive statistics for demo assets | Main text |
| Table 2 | `outputs/tables/core_historical_sector_correlation_summary_1998_2025.csv` | Within-sector vs between-sector correlation summary | Main text |
| Table 3 | `outputs/tables/rmt_summary_core_historical_1998_2025.csv` | RMT sample size, MP bounds and number of deviating eigenvalues | Main text |
| Table 4 | `outputs/tables/network_topology_comparison_core_historical_1998_2025.csv` | MST and PMFG topology summary | Main text |
| Table 5 | `outputs/tables/garch_parameters_2006_2025.csv` | GARCH(1,1) parameter estimates | Main text or appendix |
| Table 6 | `outputs/tables/volatility_model_comparison_2006_2025.csv` | Econometric and ML forecasting comparison | Main text |
| Appendix table | `outputs/tables/rmt_eigenvalues_core_historical_1998_2025.csv` | Full eigenvalue table | Appendix candidate |
| Appendix table | `outputs/tables/rmt_top_8_assets_per_eigenvector_core_historical_1998_2025.csv` | Top eigenvector loadings by asset | Appendix candidate |
| Appendix table | `outputs/tables/mst_summary_core_historical_1998_2025.csv` | MST-only summary | Appendix candidate |
| Appendix table | `outputs/tables/pmfg_summary_core_historical_1998_2025.csv` | PMFG-only summary | Appendix candidate |
| Appendix table | `outputs/tables/ml_feature_importances_2006_2025.csv` | Feature importance table | Appendix candidate |

## Missing or Uncertain Items

- A final author list and affiliations must be confirmed before submission.
- A final table for the asset-universe summary should be generated from `outputs/tables/core_historical_assets_1998_2025.csv`.
- The manuscript currently uses derived tables and figures; raw B3 data are not redistributed.
- Modern-universe extreme-return quality control remains open and should not be claimed as complete.
- Forecasting currently uses three demo assets; broader cross-sectional forecasting remains future work.
