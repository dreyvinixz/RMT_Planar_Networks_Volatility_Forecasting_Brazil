# ROADMAP — RMT Planar Networks & Volatility Forecasting — Brazil

## Status legend

- [ ] Pending
- [~] In progress
- [x] Done
- [!] Attention / methodological risk
- [-] Deferred

---

## Phase 0 — Project setup

- [x] Create project structure
- [x] Create README.md
- [x] Fill requirements.txt
- [x] Fill config/clickhouse.toml
- [x] Configure Python import path
- [x] Test local execution from project root
- [x] Initialize Git repository
- [x] Create .gitignore
- [x] Connect repository to GitHub `dreyvinixz/RMT_Planar_Networks_Volatility_Forecasting_Brazil`

---

## Phase 1 — ClickHouse connection

- [x] Start QuantBase backend Docker stack
- [x] Confirm ClickHouse container is running
- [x] Confirm port 8123 is exposed
- [x] Test ClickHouse connection through Python client
- [x] Implement `src/db.py`
- [x] Implement `scripts/python/00_check_clickhouse.py`
- [x] Run `SELECT 1`
- [x] Run table summary for `quantbase.candles_1d`

---

## Phase 2 — Data audit

- [x] Describe `quantbase.candles_1d`
- [x] Confirm available columns
- [x] Confirm first and last date
- [x] Count total rows
- [x] Count unique symbols
- [x] Check duplicated rows by `symbol, date`
- [x] Check null values in `adj_close`
- [x] Check null values in `financial_volume`
- [x] Check invalid prices
- [x] Check invalid volume
- [~] Inspect `factor_status`
- [x] Confirm that `adj_close` is the correct price column for returns
- [x] Validate generated return table dimensions

---

## Phase 3 — Liquid universe selection

- [x] Generate clean top assets excluding BDRs
- [x] Build `core_historical` universe with `n_days >= 5000`
- [x] Build `modern_liquid` candidate universe with `n_days >= 1000`
- [x] Decide to keep Brazilian units
- [x] Decide to exclude BDRs using `specification NOT LIKE '%DR%'`
- [x] Fill `config/assets_universe.yaml`
- [x] Implement `scripts/python/01_list_liquid_assets.py`
- [x] Export universe tables to `outputs/tables`
- [x] Define `demo_assets`: PETR4, VALE3, BBDC4
- [x] Define `modern_liquid_top_50`

---

## Phase 4 — Returns

- [x] Load adjusted daily prices from ClickHouse
- [x] Compute log returns using `adj_close`
- [x] Create long returns DataFrame
- [x] Create wide returns matrix
- [x] Generate summary statistics by asset
- [x] Validate extreme returns
- [x] Approve `demo_assets` for first stylized-facts figure
- [!] Investigate extreme adjusted-return events in modern universe
- [!] Avoid full-period complete-case dropna for `modern_liquid_top_50`

---

## Phase 4.1 — Return quality control

- [ ] Create extreme-return flags
- [ ] Inspect `abs(log_return) > 0.50`
- [ ] Inspect `abs(log_return) > 1.00`
- [ ] Investigate KLBN11 December 2013 adjustment sequence
- [ ] Decide treatment for extreme corporate-action-like returns
- [~] Define modern analysis window, likely 2018-2025
- [ ] Export `extreme_returns_modern_top_50.csv`
- [ ] Export `critical_returns_modern_top_50.csv`

---

## Phase 5 — Stylized facts

- [x] Generate normalized price plot
- [x] Generate daily returns plot
- [x] Generate CCDF of absolute returns
- [x] Generate ACF of absolute returns
- [x] Add journal-style return offsets
- [x] Extend absolute-return ACF to 300 lags
- [x] Add pooled/all ACF curve
- [x] Add power-law reference line for CCDF tail
- [x] Export Figure 1 as PDF
- [x] Export Figure 1 as SVG
- [x] Export Figure 1 preview as PNG
- [x] Export Figure 1D, clean 2006-2025 main candidate
- [x] Remove obsolete Figure 1A/1B/1C variants
- [x] Visually inspect Figure 1 PNG
- [x] Visually inspect Figure 1D clean PNG
- [x] Commit and push Figure 1 artifacts
- [x] Generate Table 1 with descriptive statistics for demo_assets

---

## Phase 6 — Correlation structure

- [x] Compute Pearson correlation matrix
- [x] Export pairwise observation-count matrix
- [x] Generate correlation histogram
- [x] Create initial macro-sector classification
- [x] Preserve `Utilities` and `Real Estate` as separate sectors
- [x] Preserve `subsector` metadata for Basic Materials and other sectors
- [x] Compute within-sector correlations
- [x] Compute between-sector correlations
- [x] Run Mann-Whitney U test for within-sector vs between-sector correlations
- [x] Generate Figure 3 sector correlation distribution
- [x] Compute rolling correlations
- [x] Generate rolling average market correlation figure
- [x] Generate dynamic pairwise correlation figure
- [x] Compute EWMA correlations
- [ ] Compute Spearman correlation matrix

---

## Phase 7 — Random Matrix Theory and PCA

- [x] Compute eigenvalues of correlation matrix
- [x] Compute Marcenko-Pastur bounds
- [x] Identify market mode
- [x] Identify eigenvalues outside the random-matrix noise band
- [x] Analyze eigenvectors above the noise band
- [x] Generate top-eigenvector loading figure
- [x] Reconstruct market-mode matrix
- [x] Reconstruct group/sector-mode matrix
- [x] Reconstruct filtered correlation matrix
- [x] Compare original and filtered matrices

---

## Phase 8 — Heatmap and dendrogram

- [x] Compute Mantegna distance matrix
- [x] Run hierarchical clustering
- [x] Reorder correlation matrix
- [x] Generate ordered heatmap
- [x] Generate dendrogram
- [x] Export vector figure

---

## Phase 9 — Financial networks

- [x] Build MST from original correlation matrix
- [x] Build MST from Group/Sector Mode matrix
- [x] Export MST edges, centralities and GraphML files
- [x] Generate MST comparison figure (Figure 11 / 11B Refined)
- [x] Build PMFG from original correlation matrix
- [x] Build PMFG from Group/Sector Mode matrix
- [x] Build PMFG from Filtered Market+Group matrix
- [x] Export PMFG edges, centralities, cliques and GraphML files
- [x] Generate PMFG comparison figure (Figure 12 / 12B Refined)
- [x] Compare MST and PMFG topology quantitatively (Phase 9.3)
- [x] Generate network topology comparison table
- [x] Generate hub-rank comparison table
- [x] Generate network topology comparison figures (Figure 13 and 14)
- [x] Build aggregated dependency network at subsector level (Phase 9.4)
- [x] Export subsector dependency matrix, edges and GraphML
- [x] Generate subsector dependency network figure (Figure 15)
- [ ] Community Detection Algorithms (Phase 9.5)
- [ ] Export MST as GEXF

---

## Phase 10 — Volatility Forecasting: Econometric Benchmarks vs Machine Learning

- [x] Prepare volatility forecasting dataset
- [x] Create forward realized-volatility targets
- [x] Implement Historical Volatility baseline
- [x] Implement EWMA baseline
- [x] Implement GARCH(1,1) benchmark
- [x] Implement HAR-RV benchmark
- [x] Implement Ridge Regression
- [x] Implement Random Forest
- [x] Implement XGBoost/LightGBM or HistGradientBoosting
- [x] Compare classical features vs RMT/network features
- [x] Evaluate models using MAE, RMSE, QLIKE and out-of-sample R²
- [x] Generate model-comparison figure
- [x] Generate realized-vs-predicted volatility figure
- [x] Generate ML feature-importance figure
- [ ] Compute dynamic correlation matrices
- [ ] Compute largest eigenvalue over time
- [ ] Compute average correlation over time
- [ ] Compute network metrics over time
- [ ] Compare crisis and non-crisis periods

---

## Phase 11 — Econometric benchmarks

- [ ] Estimate GARCH(1,1) for selected assets
- [ ] Compare EWMA and GARCH volatility
- [ ] Test DCC-GARCH on selected pairs/subsample
- [ ] Evaluate Granger causality network
- [ ] Evaluate variance decomposition / spillover network

---

## Phase 12 — AI models

- [ ] Define predictive task
- [ ] Implement PCA baseline
- [ ] Implement Autoencoder
- [ ] Compare Autoencoder latent factors with PCA
- [ ] Choose LSTM, Transformer, or GNN extension
- [ ] Train first AI model
- [ ] Compare AI model with classical baseline

---

## Critical priority — Revision from three professor reports (blocking)

### Canonical source and revision controls

- [x] Use only `outputs/overleaf/_Andrey___Preprint_submitted_to_Elsevier___RMT_filtered_networks__retrospective_volatility_assessment.zip` as manuscript source and final destination. Do not use `article/mode_title_2_revision`, `article/mode_title_2_professor_structure` or another package as canonical source/destination.
- [x] Review sources: `outputs/review_package/reviewer_1/Review_berri.txt` (Professor Berri), `outputs/review_package/reviewer_2/Review_gean.txt` (Professor Gean), and `outputs/review_package/reviewer_3/Reviewer_dalmazo.txt` (Professor Dalmazo).
- [x] Initial ZIP SHA-256 verified before editing: `fe40fa80c4ca4bc1d94a0d686971e81ff14a1d52992d9fbb88182b423a6f6f08` (65 entries; archive read check passed). The original remained byte-for-byte unchanged during staging work.
- [x] Extract to `tmp/revision_staging`; preserve all 65 original archive paths and submission files unrelated to the revisions. New compilation byproducts remain outside the final archive inventory.
- [x] Repack to the canonical ZIP only after the staged LaTeX compilation, citation/resource checks, visual PDF inspection and archive integrity/content checks pass.

### P0 — Method and forecasting validity (Dalmazo)

- [x] Inventory every feature in Sets A/B/C, its source and time variation, pooled-versus-asset-specific model scope, and network-feature inclusion rule. The staged feature table lists all predictors; the text identifies static asset descriptors as pooled-model identity proxies, including `subsector_Mining` for VALE3. Set C uses a fixed list of ten network predictors; importance rankings do not select them.
- [x] Audit 5- and 20-day targets at every split boundary, purge labels whose forward window crosses a boundary, require a full horizon, and recompute downstream results. The revised Methodology now states the `t+1...t+h` target window, boundary purge and valid pooled counts. Audit: `outputs/tables/forecast_target_boundary_audit_2006_2025.csv`; h=5 totals train/validation/test 8,880/2,211/3,723; h=20 totals 8,835/2,166/3,678.
- [x] Compare Ridge Set A with HAR-RV and validation-selected Set B/C; test Set B versus A and Set C versus A; state the validation-only selection rule. Results are in the revised forecast tables and `outputs/tables/forecast_feature_set_hac_tests_2006_2025.csv`.
- [x] Report fixed model configurations, no hyperparameter search grid, seed 42 for the primary run, and five-seed MLP/CNN sensitivity (seeds 11, 23, 42, 77, 101); results in `outputs/tables/neural_seed_sensitivity_2006_2025.csv` and its summary.
- [x] Document circular moving-block bootstrap construction, 2,000 repetitions, seed 42 and horizon-length blocks; assess 2h and 4h blocks. Results in `outputs/tables/forecast_block_length_sensitivity_2006_2025.csv`.
- [x] Frame the question as whether descriptors improve forecast accuracy. Report the supported result: Ridge Set B/C have higher test QLIKE than Ridge Set A at both horizons; all four paired HAC contrasts remain significant after Holm adjustment. HAR-RV has the lowest aggregate QLIKE mean, but its paired comparison with Ridge A is not significant at either horizon. No nonsignificance is described as proof of a zero effect.
- [x] Align abstract, graphical abstract, highlights, discussion and conclusions with the revised results. The graphical abstract labels its volatility chart illustrative, uses the 2021–2025 test period and non-annualized 20-day RV, and reports the Ridge Set B/C result.

### P1 — RMT, panels, results, and data (Dalmazo)

- [x] Distinguish the full-panel result (four non-market modes beyond the market mode) from issuer collapse (two additional modes), on the same dates.
- [x] Recompute issuer-collapsed `C_group`, MST/PMFG and robustness tables on the main panel's 1,527 dates (23 Aug 2006–15 Aug 2024), separating the effect of N from T. See `outputs/tables/issuer_panel_same_dates_c_group.csv`, `outputs/tables/issuer_panel_network_sensitivity_same_dates.csv`, and the staged RMT/network tables.
- [x] Extend the circular-shift rank test through rank 58. Ranks 1–5 exceed their rank-matched 95th percentile; rank 6 is the first not to exceed it; ranks 6–58 have p=1 under the plus-one estimate.
- [x] Reconcile the broad unbalanced pairwise mean (~0.24), same-panel mean off-diagonal correlation (0.3350), and leading spectral share `lambda_1/N` (0.3733), explicitly distinguishing their populations and definitions.
- [x] Recalculate/report the 10,000 sector-label and 1,000 circular-shift simulation counts and attainable p-value floors (1/10,001 and 1/1,001); remove claims below those floors.
- [x] Correct the 2015–16 correlation description to match Figure 5: the 252/504-day rolling measure remains near 0.2 and shows no comparable jump in that interval.
- [x] Apply deterministic share-class retention by common-panel coverage, mean financial volume over those dates, then ticker only as a final tie-break. PETR4 is retained over PETR3, ELET3 over ELET6, and CPLE6 over CPLE3. The common-panel selection table records 1,527 observations per share class. The official B3 bulletin for the panel's final date (15 Aug 2024) includes PETR3/PETR4, ELET3/ELET6 and CPLE3/CPLE6, confirming these symbols were listed in the market data on the endpoint itself (official BDI: `https://arquivos.b3.com.br/bdi/download/bdi/2024-08-15/BDI_00_20240815.pdf`).
- [ ] Prepare a versioned release of the 2025 daily data used in the study for the research-software repository. Record source provenance, adjustment details, checksums and applicable licensing/redistribution terms before release; keep this reproducibility item open until the dataset is actually published and independently accessible.

### P1 — Figures and readability (Berri; Gean; Dalmazo)

- [x] Redraw the main group-mode dendrogram with a narrower page footprint and larger leaf labels; inspect the compiled page.
- [x] Keep the Random Forest feature-importance figure in the main text because it is cited and interpreted as descriptive split importance, not incremental forecast evidence. The full dendrogram comparison is supplementary and is cited from the main discussion of hierarchical fit.
- [x] Simplify and enlarge the graphical-abstract typography; reduce dense labels and decorative elements while retaining the polished visual style.
- [x] Align graphical-abstract wording with the actual 20-day RV metric and 2021–2025 test interval; label schematic network views and the illustrative volatility series explicitly.
- [x] Integrate the Figure 2/3 interpretation and the supporting descriptive table into the surrounding results narrative before the corresponding callouts.

### P2 — Text and organization (Berri; Gean)

- [x] Correct abstract capitalization and transitions, state the forecast-accuracy question, and avoid requiring “We study” as a mandatory grammar correction.
- [x] Check the RMT citations and add explicit MST and PMFG references; soften the literature-gap claim to match the review.
- [x] Reduce duplicated theory/method exposition while retaining cited definitions of QLIKE and `R^2_OOS`; remove explanatory subsubsections that repeated the forecasting design.
- [!] Related Work's four topic subsections are retained unchanged at the user's explicit direction, although Professor Gean preferred a less segmented discussion.
- [x] Use the clear section title “Methods: Integrated Empirical Framework”; explain the sequence without inventing a promotional algorithm name or unsupported algorithm novelty.
- [x] Merge short methodology/theory subheadings into their parent sections and integrate limitations into the Discussion without removing their content. The former standalone source file is no longer included in `main.tex`; its content is integrated into the Discussion.
- [x] Use the chosen contribution-item editorial voice consistently and title the final section “Conclusions”.
- [x] At the user's explicit instruction, add CNPq 318141/2025-6 and remove joint FAPERGS/CNPq 23/2551-0000126-8 from Acknowledgements and Funding; keep the other listed support unchanged. The public dataset sources remain cited to their published authors. No separate personal data-provision role is asserted for Rafael beyond the manuscript's existing authorship/CRediT record. [Official CNPq result](https://www.gov.br/cnpq/pt-br/chamadas/todas-as-chamadas/chamadas-2025/chamada-no-23-2025/resultado-preliminar-da-chamada-23-2025-3a-retificacao/%40%40download/file).

### P2 — References, terminology, and consistency (Berri; Dalmazo)

- [x] Audit references [16], [17], [54], [55]: update software author to Andrey V. S. Souza and retain its versioned GitHub URL; complete Bouchaud–Potters book details; connect Hansen–Lunde to the GARCH discussion; and remove the unverified/misidentified Zhang–Broadstock entry. The official repository citation metadata has no DOI, so none is invented.
- [x] Standardize manuscript terminology on “group mode” / “group-mode”; update theory, methods diagram and supplementary caption. The unchanged Related Work section retains its existing “group-mode” wording.
- [x] Correct Figure 7's caption (“component RMT components”).
- [x] State numerical precision and Monte Carlo resolution once at the start of Results; remove repeated empty precision-note commands. Correct the forecast-metrics cross-reference and QLIKE equation reference.
- [x] Recompile and audit cross-references, citations, captions, inputs and graphics after the section changes; the latest log has no unresolved citation/reference warnings and all 10 inputs/20 graphics resolve.

### Completion gate

- [x] Map each substantive reviewer comment to a revised manuscript passage, recalculation, figure/table, or an explicit accepted editorial decision. A fresh comparison record and populated reviewer tracker are stored under `outputs/review_package/`.
- [x] Recompute and record all affected split, panel, feature-set, bootstrap and seed results in the referenced CSV outputs.
- [x] Compile the staged LaTeX and visually inspect the graphical abstract, dendrogram, forecast figure, forecast tables and supplementary figures. The PDF is 44 pages; the latest build has no unresolved citations/references. The class emits non-blocking caption/hypersetup warnings and an existing title-page overfull-box diagnostic.
- [x] Verify the final ZIP's original 65-entry inventory, required LaTeX/bibliography/resources and archive CRC after repacking.
- [x] Close the previously open grant item following the user's explicit instruction. Related Work remains unchanged at the user's direction. No software API/interface was changed by this manuscript revision.
- [ ] Publish the versioned 2025 daily-data release promised in the manuscript, after documenting its provenance, adjustment method and redistribution terms; then update the Data Availability statement and close the reproducibility gate.

---

## Phase 13 — Article writing

- [x] Write abstract
- [x] Write introduction
- [x] Write related work
- [x] Write data section
- [x] Write methodology
- [x] Write results
- [x] Write discussion
- [x] Write conclusion
- [x] Format references
- [x] Compile LaTeX
