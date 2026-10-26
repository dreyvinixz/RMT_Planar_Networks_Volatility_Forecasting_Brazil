# Registro de analise e resposta — Professor Dalmazo

| ID | Comentario consolidado | Decisao | Estado | Alteracao/evidencia |
|---|---|---|---|---|
| D1 | Inventory A/B/C, time variation, pooled scope, static identity proxies and feature selection. | accept | done | Forecast feature inventory table and adjacent text. |
| D2 | Include Ridge Set A and HAR-RV and compare structural sets against A. | accept | done | forecast_comparison and forecast_loss_test tables. |
| D3 | Purge h-day labels crossing train/validation/test boundaries and require a full horizon. | accept | done | Methodology paragraph; boundary audit CSV; recomputed downstream result tables. |
| D4 | Test block lengths longer than h for persistent losses. | accept | done | app_blocks table and forecast_block_length_sensitivity_2006_2025.csv. |
| D5 | Report model settings, search grid, seeds and neural variability. | accept | done | Methodology and app_seeds table. |
| D6 | Ask whether descriptors improve accuracy and remove unsupported positive/null claims. | accept | done | Abstract, highlights, forecast tests, Discussion, Conclusions and graphical abstract. |
| D7 | Reconcile 0.24 pairwise mean with synchronized-panel statistics. | accept | done | Results sections for correlation and RMT. |
| D8 | Extend rank tests beyond 1–5 and identify the first rank not exceeding the null. | accept | done | Circular-shift robustness subsection. |
| D9 | Distinguish four full-panel modes from two issuer modes; recompute on common dates. | accept | done | Abstract; issuer-panel robustness table and outputs/tables/issuer_panel_same_dates_* |
| D10 | Correct the narrative claiming a correlation increase absent from the plotted series. | accept | done | Updated results text and Figure 5. |
| D11 | Respect the minimum attainable p-values. | accept | done | Sector permutation and circular-shift results. |
| D12 | Align annualization, dates and schematic appearance with the metric and test period. | accept | done | Current graphical abstract in compiled PDF. |
| D13 | Check PETR, ELET and CPLE share-class retention and endpoint listing. | accept | done | Issuer-selection table and B3 BDI 2024-08-15. |
| D14 | Correct the equation/section cross-reference in the forecast table. | accept | done | Current forecast table note. |
| D15 | Correct the software citation, complete Bouchaud–Potters and remove unverified Zhang–Broadstock. | accept partially | done except DOI | Current references; official repository CITATION.cff has no DOI. |
| D16 | Soften “limited integration” claim. | accept | done | Related Work text (unchanged in this round per user instruction; wording already revised). |
| D17 | Define display precision once and remove repeated notes. | accept | done | sections/results.tex; duplicate note commands absent. |
| D18 | Reduce duplication and define Mantegna distance before use. | accept | done | Current theory and methodology sections. |
| D19 | Standardize group-mode labels and correct the Figure 7 caption. | accept | done | Current manuscript text and caption. |
| D20 | Public BovDBv2 ends in 2024; local 1998–2025 data are not redistributed. | accept partially | limitation disclosed | Data availability statement; no source-specific local license evidence. |
| D21 | Keep the research question about accuracy improvement, not an untested association. | accept | done | The Introduction, theoretical rationale and Results overview now ask whether adding structural descriptors improves forecast accuracy; the retrospective limit remains explicit. |
