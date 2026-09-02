# Implementation Plan — Full Article Draft for Chaos, Solitons & Fractals

## Project

**Repository:** `b3-econophysics-ai`  
**Target journal:** `Chaos, Solitons & Fractals`  
**Article folder:**  
`C:\quantbase-services\services\b3-econophysics-ai\article\chaos_solitons_fractals`

## Objective

Write the first complete LaTeX draft of the article.

This draft is not expected to be final. It should be a strong academic skeleton/casca that the author will later refine, rewrite, shorten, expand, validate and polish.

The goal is to transform the completed computational project into a coherent journal-style manuscript for **Chaos, Solitons & Fractals**, with the central narrative:

> A complex-systems and econophysics framework for analyzing Brazilian stock-market dependencies, combining stylized facts, Random Matrix Theory, financial networks, MST/PMFG topology and volatility forecasting with econometric and machine-learning benchmarks.

---

# General Instructions for the AI Writer

You have full permission to use the project structure, generated results, figures, tables, roadmaps, walkthroughs and implementation plans as the basis for drafting the article.

However:

- Do **not** fabricate numerical results.
- Do **not** invent citations.
- Do **not** copy text verbatim from reference papers.
- Use reference papers as methodological and stylistic inspiration only.
- Use cautious academic wording:
  - “suggests”
  - “indicates”
  - “is consistent with”
  - “provides evidence”
  - “we find”
- Avoid exaggerated claims:
  - “proves definitively”
  - “irrefutable”
  - “perfect”
  - “revolutionary”
  - “unprecedented” unless carefully justified.

The user will later refine the entire manuscript manually. Your task is to create a coherent, complete and technically grounded first version.

---

# Main Reference Article

Use the following paper as the **main methodological and writing reference**:

```text
C:\quantbase-services\services\b3-econophysics-ai\article\literature_review\docs\2302.08208v1_copy.pdf
```

This paper is:

```text
A Look at Financial Dependencies by Means of Econophysics and Financial Economics
M. Raddant and T. Di Matteo
arXiv:2302.08208v1
```

Use it as inspiration for:

* how to introduce financial dependencies;
* how to connect financial economics and econophysics;
* how to discuss correlations, networks and RMT;
* how to explain the bridge between factor models, volatility and financial networks;
* how to structure the motivation for studying asset comovement.

Important:

```text
Do not copy the text.
Do not paraphrase too closely.
Use the paper only as a conceptual and stylistic reference.
```

---

# Additional Literature Review Material

There are several articles from the target journal and related literature in:

```text
C:\quantbase-services\services\b3-econophysics-ai\article\literature_review\docs
```

Use these papers as inspiration for:

* writing style;
* section organization;
* figure captions;
* methodological framing;
* terminology used in complex systems and econophysics;
* how Chaos, Solitons & Fractals papers present results.

When using any specific claim from a paper, add a citation placeholder in the LaTeX file and include a corresponding BibTeX placeholder in `references.bib`.

If the exact citation is not yet known, use a placeholder such as:

```latex
\cite{raddant_dimatteo_2023}
```

or:

```latex
\cite{placeholder_pmfg_reference}
```

Then mark with:

```latex
% TODO: verify citation
```

---

# Target Journal Requirements

The manuscript should be written for:

```text
Chaos, Solitons & Fractals
```

Use the Elsevier `elsarticle` template already organized in:

```text
C:\quantbase-services\services\b3-econophysics-ai\article\chaos_solitons_fractals
```

Recommended document class:

```latex
\documentclass[preprint,12pt]{elsarticle}
```

The journal requires:

* editable source files;
* single-column LaTeX style for submission;
* abstract up to 250 words;
* 1 to 7 keywords;
* 3 to 5 highlights, each up to 85 characters;
* all figures cited in order;
* data availability statement;
* declaration of competing interests;
* funding statement;
* declaration of generative AI use if applicable;
* references in Elsevier numerical style.

Use:

```latex
\bibliographystyle{elsarticle-num}
```

---

# Proposed Article Title

Use this as the working title:

```text
Random Matrix Filtering and Planar Financial Networks for Volatility Forecasting in the Brazilian Stock Market
```

Alternative titles to mention in comments:

```text
Econophysics, Financial Networks and Machine Learning Volatility Forecasting in the Brazilian Stock Market

Complex Network Topology and Random Matrix Filtering of Brazilian Stock Market Dependencies

Random Matrix Filtering, Planar Financial Networks and Risk Forecasting in B3 Equities
```

---

# Core Contribution

The paper should make three main contributions:

1. It constructs a long-run empirical dependency study of Brazilian B3 equities using adjusted daily prices from 1998 to 2025.

2. It applies econophysics tools — stylized facts, correlation structure, Random Matrix Theory, eigenvector analysis, hierarchical clustering, MST and PMFG — to separate market-wide, sectoral and noisy components of financial dependencies.

3. It evaluates whether RMT/network-derived structural features add predictive information to realized-volatility forecasting when compared with classical econometric benchmarks such as EWMA, HAR-RV and GARCH(1,1).

---

# Main Empirical Pipeline

The article should follow the actual computational pipeline of the project:

```text
Data audit
→ Liquid universe selection
→ Adjusted log returns
→ Stylized facts
→ Descriptive statistics
→ Static correlations
→ Sectoral correlations
→ Rolling correlations
→ RMT/PCA
→ RMT-filtered matrices
→ Heatmaps and dendrograms
→ MST and PMFG networks
→ Aggregated subsector dependency network
→ Econometric volatility benchmarks
→ Machine-learning volatility forecasting
```

---

# Data and Universe

Use the following facts:

* Data source: QuantBase ClickHouse database built from B3 daily data.
* Main table: `quantbase.candles_1d`.
* Main price column: `adj_close`.
* Main return definition: adjusted log returns.
* Period available: approximately 1998 to 2025.
* Main research universe: `core_historical`, 58 liquid long-history B3 assets.
* Demo assets for stylized facts and volatility forecasting:

  * `PETR4`
  * `VALE3`
  * `BBDC4`
* Benchmarks/index instruments such as `BOVA11`, `SMAL11`, `IVVB11` are treated separately and not included in the main equity network.
* BDRs, ETFs, funds and non-equity instruments are excluded from the main network universe.
* Brazilian units are retained when they represent relevant liquid domestic securities.

Methodological filter:

```text
adj_close > 0
cod_bdi = '02'
specification NOT LIKE '%DR%'
```

Mention that adjusted prices are used to account for corporate actions and construct economically meaningful return series.

---

# Article Structure

Generate the manuscript using the following structure.

## 1. Introduction

Write a strong introduction explaining:

* financial markets as complex systems;
* why dependencies between assets matter;
* why emerging markets such as Brazil are interesting;
* why B3 provides a meaningful case study;
* why raw correlations are noisy;
* why RMT and filtered networks are useful;
* why volatility forecasting is a natural extension.

The introduction should end with clear contributions.

Suggested contribution paragraph:

```text
The contribution of this paper is threefold. First, we document the long-run dependency structure of Brazilian equities using adjusted daily B3 prices from 1998 to 2025. Second, we combine Random Matrix Theory and planar financial networks to separate market-wide, sectoral and noisy components of stock-market comovement. Third, we investigate whether features extracted from these econophysics-based structures improve realized-volatility forecasting relative to classical econometric benchmarks.
```

## 2. Related Work

Use the main reference paper `2302.08208v1_copy.pdf` as a conceptual guide.

Discuss:

* financial dependencies;
* stylized facts;
* correlation-based networks;
* Random Matrix Theory in finance;
* Mantegna distance;
* MST;
* PMFG;
* GARCH and volatility clustering;
* machine learning for financial volatility forecasting.

Add citations placeholders where needed.

Potential subsections:

```text
2.1 Financial dependencies and asset comovement
2.2 Econophysics, RMT and financial networks
2.3 Volatility modeling and machine learning
```

## 3. Data and Asset Universe

Describe:

* ClickHouse data source;
* daily B3 adjusted prices;
* asset filters;
* construction of `core_historical`;
* construction of `demo_assets`;
* exclusion criteria;
* treatment of benchmarks;
* return definition.

Include a table placeholder for universe summary if available.

Mention that all computations use adjusted closing prices.

## 4. Methodology

This is the most important technical section.

Suggested subsections:

```text
4.1 Log returns and realized volatility
4.2 Correlation matrices and Mantegna distance
4.3 Random Matrix Theory and Marcenko-Pastur bounds
4.4 Eigenvector interpretation and RMT filtering
4.5 Hierarchical clustering
4.6 MST and PMFG network construction
4.7 Aggregated subsector dependency network
4.8 Econometric volatility benchmarks
4.9 Machine-learning volatility models
4.10 Evaluation metrics
```

Include equations for:

### Log returns

```latex
r_{i,t} = \log(P_{i,t}) - \log(P_{i,t-1})
```

### Mantegna distance

```latex
d_{ij} = \sqrt{2(1-\rho_{ij})}
```

### Marcenko-Pastur bounds

```latex
\lambda_{\pm} = \sigma^2 \left(1 + \frac{1}{Q} \pm 2\sqrt{\frac{1}{Q}}\right)
```

or the equivalent standard formulation, with careful notation.

### GARCH(1,1)

```latex
\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2
```

### Realized volatility target

```latex
RV_{t,h} = \sqrt{\sum_{k=1}^{h} r_{t+k}^2}
```

### QLIKE

```latex
QLIKE = \log(\hat{\sigma}_t^2) + \frac{\sigma_t^2}{\hat{\sigma}_t^2}
```

Explain all terms for interdisciplinary readers.

## 5. Empirical Results

Organize results in a logical progression.

Suggested subsections:

```text
5.1 Stylized facts of selected B3 stocks
5.2 Static and sectoral correlation structure
5.3 Dynamic market synchronization
5.4 Random Matrix Theory and market mode
5.5 RMT-filtered matrices and hierarchical clustering
5.6 Financial networks: MST and PMFG
5.7 Aggregated subsector dependency network
5.8 Volatility forecasting: econometrics vs machine learning
```

Use cautious claims.

Do not overstate results.

---

# Figures and Tables

The article currently has many figures. Do not insert all of them in the main body unless necessary.

The recommended main-body figures are:

## Main figures

```text
Figure 1 — Stylized facts for PETR4, VALE3 and BBDC4
Figure 2 — Correlation distribution and/or sectoral correlation comparison
Figure 3 — Rolling average market correlation
Figure 4 — RMT eigenvalue spectrum
Figure 5 — RMT-filtered matrices / ordered heatmap
Figure 6 — PMFG refined original vs group mode
Figure 7 — Aggregated subsector dependency network
Figure 8 — Volatility forecasting comparison
Figure 9 — Feature importance
```

Optional appendix/supplementary:

```text
RMT eigenvector loadings
Full dendrogram comparison
MST refined comparison
MST vs PMFG topology comparison
Hub-rank comparison
Dynamic pairwise correlations
Additional forecasting plots
```

The AI should inspect the figure files available in:

```text
C:\quantbase-services\services\b3-econophysics-ai\article\chaos_solitons_fractals
```

and use the actual filenames.

If filenames are not obvious, insert placeholders like:

```latex
\includegraphics[width=\textwidth]{Figure_1.pdf}
```

and add:

```latex
% TODO: verify figure filename
```

---

# Results to Mention

Use the following validated results.

## Stylized facts

* B3 demo assets exhibit fat-tailed returns.
* Volatility clustering is visible.
* ACF of absolute returns decays slowly.
* Stylized facts are consistent with classical financial time-series behavior.

## Descriptive statistics

Mention:

* high excess kurtosis;
* negative or asymmetric tails depending on asset;
* PETR4 shows high volatility and heavy tails;
* BBDC4 is comparatively less volatile;
* VALE3 is strongly tied to commodity cycles.

## Correlation structure

Validated results:

```text
N = 58 assets
N_pairs = 1653
mean historical Pearson correlation ≈ 0.24
median historical Pearson correlation ≈ 0.23
```

Within-sector vs between-sector:

```text
Within-sector mean = 0.3433
Within-sector median = 0.3082
Between-sector mean = 0.2249
Between-sector median = 0.2076
Mann-Whitney U p-value = 1.33389e-24
```

Interpretation:

```text
Same-sector stock pairs are significantly more correlated than cross-sector pairs.
```

## Rolling correlations

Mention:

* average market correlation is time-varying;
* correlations increase during crises;
* 2008 and 2020 are major synchronization periods;
* COVID shock produced very high rolling average correlations.

## RMT

Validated RMT results:

```text
N = 58
T = 1527 complete-case observations
Q = T/N ≈ 26.33
lambda_max ≈ 1.4278
largest eigenvalue ≈ 21.6505
number of eigenvalues above lambda_max = 5
market mode share ≈ 37.3%
```

Interpretation:

```text
The largest eigenvalue is far beyond the Marcenko-Pastur noise band, indicating a strong market-wide mode.
```

Eigenvectors:

```text
Eigenvector 1 = Market Mode
Eigenvector 2 = commodities/basic materials vs domestic/utilities structure
Eigenvector 3 = financials vs industrial/heavy sectors
Eigenvector 4 = localized telecommunications component
Eigenvector 5 = utilities-related structure
```

## RMT matrix reconstruction

Validated:

```text
Frobenius reconstruction error = 2.74e-14
Max abs reconstruction error = 3.99e-15
C_filtered diagonal = 1.0
```

Interpretation:

```text
The spectral reconstruction is numerically stable.
```

## Hierarchical clustering

Cophenetic correlations:

```text
Original = 0.9500
Filtered = 0.9340
Group Mode = 0.8705
```

Interpretation:

```text
The dendrograms preserve pairwise distance structure well, and the Group Mode reveals clearer sectoral blocks after removing the market component.
```

## MST

MST summary:

```text
Original:
mean edge correlation = 0.5796
same-sector edge ratio = 0.7193
top betweenness node = ITSA4

Group Mode:
mean edge correlation = 0.1388
same-sector edge ratio = 0.6316
top betweenness node = ALPA4
```

Interpretation:

```text
Original MST is dominated by strongly correlated blue-chip and dual-share relationships.
Group Mode MST reveals weaker but more sector-specific bridges.
```

## PMFG

PMFG topological validation:

```text
N = 58
edges = 168 = 3N - 6
triangles = 166 = 3N - 8
4-cliques = 55 = N - 3
planar = true
```

PMFG summary:

```text
Original:
mean edge correlation = 0.5177
average clustering = 0.5273
top betweenness = GGBR4

Group Mode:
mean edge correlation = 0.1109
average clustering = 0.6653
top betweenness = GUAR3
```

Interpretation:

```text
The Group Mode PMFG has lower average correlation but higher clustering, suggesting localized sectoral communities after market-mode removal.
```

## Volatility forecasting

GARCH persistence:

```text
PETR4: alpha + beta = 0.9911
VALE3: alpha + beta = 0.9946
BBDC4: alpha + beta = 0.9827
```

Interpretation:

```text
Volatility shocks are highly persistent in B3 equities.
```

Forecasting results:

```text
At 5-day horizon, GARCH and HAR-RV remain very competitive.
At 20-day horizon, Ridge Regression competes with or slightly outperforms GARCH in QLIKE.
Random Forest with network features approaches classical benchmarks.
PMFG-derived features appear among the top 20 feature importances.
```

Important cautious statement:

```text
Network features do not replace classical volatility predictors, but they provide incremental structural information.
```

---

# Tables to Include

Recommended main tables:

```text
Table 1 — Descriptive statistics for PETR4, VALE3 and BBDC4
Table 2 — Dataset and universe summary
Table 3 — RMT eigenvalue summary
Table 4 — Network topology comparison
Table 5 — Volatility forecasting model comparison
```

Optional appendix tables:

```text
GARCH parameters
Top PMFG/MST hubs
Eigenvector loadings
Feature importance ranking
Clique summary
```

---

# Writing Style

Use an academic, precise, non-promotional tone.

Good style:

```text
The results indicate...
This pattern is consistent with...
The evidence suggests...
The filtered network reveals...
The forecasting results show...
```

Avoid:

```text
This proves...
Unprecedented...
Perfect...
The model dominates everything...
```

---

# Required LaTeX Files

Generate or update the following files:

```text
main.tex
sections/introduction.tex
sections/related_work.tex
sections/data.tex
sections/methodology.tex
sections/results.tex
sections/forecasting.tex
sections/discussion.tex
sections/conclusion.tex
sections/declarations.tex
references.bib
highlights.tex
```

If the project currently uses a single `main.tex`, it is acceptable to keep all sections in one file for the first draft. However, modular section files are preferred.

---

# Main LaTeX Structure

Use this structure in `main.tex`:

```latex
\documentclass[preprint,12pt]{elsarticle}

\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{lineno}

\journal{Chaos, Solitons \& Fractals}

\begin{document}

\begin{frontmatter}

\title{Random Matrix Filtering and Planar Financial Networks for Volatility Forecasting in the Brazilian Stock Market}

\author[inst1]{Author Name}
\author[inst1]{Author Name}

\affiliation[inst1]{
  organization={Federal University of Rio Grande},
  city={Rio Grande},
  country={Brazil}
}

\begin{abstract}
% Abstract up to 250 words.
\end{abstract}

\begin{keyword}
Econophysics \sep Random matrix theory \sep Financial networks \sep
Planar maximally filtered graph \sep Volatility forecasting \sep
Machine learning \sep Brazilian stock market
\end{keyword}

\end{frontmatter}

\linenumbers

\input{sections/introduction}
\input{sections/related_work}
\input{sections/data}
\input{sections/methodology}
\input{sections/results}
\input{sections/forecasting}
\input{sections/discussion}
\input{sections/conclusion}
\input{sections/declarations}

\bibliographystyle{elsarticle-num}
\bibliography{references}

\end{document}
```

---

# Highlights

Create `highlights.tex` or `highlights.txt`.

Initial draft:

```text
RMT separates market, sector and noise components in B3 equities.
Planar financial networks reveal hidden sectoral market topology.
PMFG centralities add information for volatility forecasting.
Small ML models compete with GARCH and HAR-RV benchmarks.
```

Before final submission, ensure each bullet has at most 85 characters.

---

# Declarations Section

Create `sections/declarations.tex`.

Include placeholders for:

## Funding

If no specific funding:

```latex
\section*{Funding}
This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.
```

## Competing interests

```latex
\section*{Declaration of competing interest}
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
```

## Data availability

Draft:

```latex
\section*{Data availability}
The raw market data used in this study were obtained from B3 daily price records processed through the QuantBase data infrastructure. Due to data redistribution restrictions, raw data are not redistributed with this manuscript. Derived tables, scripts and reproducibility materials will be made available in a public repository upon publication.
```

## Generative AI disclosure

If applicable:

```latex
\section*{Declaration of generative AI and AI-assisted technologies in the writing process}
During the preparation of this work, the authors used ChatGPT for language refinement, structural organization and code-review support. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.
```

Important:

```text
Do not claim that AI generated or altered manuscript figures.
Figures must be generated from reproducible computational scripts.
```

---

# References

Create or update `references.bib`.

Mandatory reference placeholders:

```bibtex
@article{raddant_dimatteo_2023,
  title={A Look at Financial Dependencies by Means of Econophysics and Financial Economics},
  author={Raddant, M. and Di Matteo, T.},
  journal={arXiv preprint arXiv:2302.08208},
  year={2023}
}
```

Also include placeholders for:

```text
Mantegna financial networks
Random Matrix Theory in finance
Marcenko-Pastur distribution
MST in financial markets
PMFG in financial markets
GARCH
HAR-RV
QLIKE / volatility forecast evaluation
Machine learning for volatility forecasting
```

If exact BibTeX is unknown, insert placeholder entries with `% TODO: verify`.

---

# Captions

Write captions in academic style.

Captions should:

* describe what the figure shows;
* define important symbols;
* mention period and universe;
* avoid overly long interpretation.

Example caption style:

```latex
\caption{
Planar maximally filtered graphs constructed from the original and RMT-filtered correlation matrices of the B3 core historical universe. Node colors indicate macro-sector classification and node sizes are proportional to network centrality. The original PMFG is dominated by market-mode hubs, whereas the Group/Sector Mode PMFG reveals a more localized sectoral topology after removing the dominant market component.
}
```

---

# Final Writing Goal

The draft should be complete enough that the user can:

```text
1. compile the article in LaTeX;
2. inspect the full narrative;
3. manually refine claims and citations;
4. decide which figures stay in the main text;
5. move extra figures to appendix;
6. prepare the final submission package for Chaos, Solitons & Fractals.
```

---

# Output Expected From the AI Writer

When executing this plan, the AI should:

1. Generate the article skeleton in LaTeX.
2. Fill all major sections with coherent academic prose.
3. Insert figure/table placeholders.
4. Insert citation placeholders.
5. Insert TODO comments where exact numbers, filenames or citations need verification.
6. Create `references.bib` with initial entries.
7. Create `highlights.txt`.
8. Create `sections/declarations.tex`.

The first draft should prioritize coherence, completeness and structure over final polishing.

---

# Final Instruction

Write the article as a serious first draft for an A1 journal target.

The manuscript should sound like a complex-systems/econophysics paper with a financial-risk forecasting extension, not like a generic data-science report.

The user will later revise the paper deeply, improve the English, verify citations, adjust figures and refine the final contribution.
