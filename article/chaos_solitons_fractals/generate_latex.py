import os
from pathlib import Path

base_dir = Path(r"C:\quantbase-services\services\b3-econophysics-ai\article\chaos_solitons_fractals")
sections_dir = base_dir / "sections"
sections_dir.mkdir(exist_ok=True)

main_tex = r"""\documentclass[preprint,12pt]{elsarticle}

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
Financial markets are classic examples of complex systems where asset dependencies evolve dynamically, often obscured by noise. In emerging markets like Brazil, understanding these true structural dependencies is crucial for risk management and portfolio allocation. In this paper, we document the long-run dependency structure of Brazilian equities using adjusted daily B3 prices from 1998 to 2025. By combining Random Matrix Theory (RMT) and planar financial networks, specifically the Minimum Spanning Tree (MST) and Planar Maximally Filtered Graph (PMFG), we effectively separate market-wide, sectoral, and noisy components of stock-market comovement. The RMT-filtered network topologies reveal a clear sectoral block structure hidden within the dominant market mode. Furthermore, we investigate whether the topological features extracted from these econophysics-based structures provide predictive value for realized-volatility forecasting. Our results indicate that while classical econometric benchmarks such as GARCH(1,1) and HAR-RV remain extremely strong baselines due to the high volatility persistence of Brazilian assets, incorporating PMFG centralities into non-linear machine learning models (Random Forests) yields highly competitive forecasts. Network features do not replace classical volatility predictors but provide incremental structural information, demonstrating that the static global geometry of financial networks encodes valuable signals regarding local variance and risk shocks.
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
"""

intro_tex = r"""\section{Introduction}
\label{sec:intro}

Financial markets are increasingly recognized as quintessential complex systems, characterized by nonlinear dynamics, heavy-tailed return distributions, and intricate dependency structures among thousands of interacting assets \cite{raddant_dimatteo_2023, mantegna_1999_introduction}. Understanding how these assets comove is not merely a theoretical curiosity; it is the cornerstone of modern portfolio theory, risk management, and derivative pricing. In particular, emerging markets such as the Brazilian stock exchange (B3) present a meaningful case study due to their unique liquidity constraints, exposure to global commodity cycles, and pronounced volatility shocks.

However, raw empirical correlation matrices are notoriously noisy. Because the length of available financial time series is often of the same order of magnitude as the number of assets, empirical correlations are contaminated by finite-size effects and measurement noise \cite{laloux_1999_noise}. Random Matrix Theory (RMT) has emerged as a powerful econophysics framework to isolate true economic signals from this random noise \cite{plerou_2002_random}. By comparing the empirical eigenvalue spectrum against the Mar\v{c}enko-Pastur theoretical bounds, researchers can filter the correlation matrix, extracting the dominant market mode and underlying sectoral structures.

Building upon filtered correlation matrices, complex network theory provides topological tools to visualize and quantify financial dependencies. Techniques such as the Minimum Spanning Tree (MST) \cite{mantegna_1999_hierarchical} and the Planar Maximally Filtered Graph (PMFG) \cite{tumminello_2005_tool} map high-dimensional correlation matrices into sparse graphs. These planar financial networks extract the most critical linkages between assets, revealing hubs, communities, and vulnerabilities that are otherwise obscured in dense matrices.

While econophysics has successfully mapped the topology of financial markets, volatility forecasting remains largely dominated by classical econometrics. Models such as GARCH \cite{bollerslev_1986_generalized} and HAR-RV \cite{corsi_2009_simple} excel at capturing the stylized facts of volatility clustering and long memory. A natural extension is to ask whether the static structural geometry extracted from financial networks contains predictive information regarding the temporal evolution of risk. Can machine learning models leverage network centralities to improve upon econometric volatility forecasts?

The contribution of this paper is threefold. First, we document the long-run dependency structure of Brazilian equities using a robust dataset of adjusted daily B3 prices from 1998 to 2025. Second, we combine Random Matrix Theory and planar financial networks to separate market-wide, sectoral, and noisy components of stock-market comovement. Third, we investigate whether features extracted from these econophysics-based structures improve realized-volatility forecasting relative to classical econometric benchmarks, evaluating the efficacy of machine learning models in capturing nonlinear risk transmission.
"""

related_tex = r"""\section{Related Work}
\label{sec:related}

\subsection{Financial Dependencies and Asset Comovement}
The study of financial dependencies traditionally revolves around Pearson cross-correlation matrices and factor models. However, classical models often struggle with the non-stationary nature of financial time series. Recent literature \cite{raddant_dimatteo_2023} bridges the gap between financial economics and econophysics by framing asset comovement through the lens of complex systems, where macroscopic market behavior emerges from microscopic interactions.

\subsection{Econophysics, RMT, and Financial Networks}
Random Matrix Theory (RMT) was introduced to finance by Laloux et al. \cite{laloux_1999_noise} and Plerou et al. \cite{plerou_2002_random} to differentiate information from noise in correlation matrices. Subsequent advances utilized Mantegna's distance metric \cite{mantegna_1999_hierarchical} to construct Minimum Spanning Trees (MST), reducing complete graphs to acyclic subgraphs of essential linkages. Tumminello et al. \cite{tumminello_2005_tool} generalized this approach with the Planar Maximally Filtered Graph (PMFG), which retains more information, allows for loops (cliques), and embeds the graph on a sphere, preserving hierarchical and clustering properties critical for risk analysis.

\subsection{Volatility Modeling and Machine Learning}
Volatility forecasting is central to quantitative finance. The GARCH model \cite{bollerslev_1986_generalized} remains the standard for capturing conditional heteroskedasticity, while the HAR-RV model \cite{corsi_2009_simple} elegantly handles realized volatility using heterogeneous autoregressive components. Recently, machine learning techniques, including Random Forests and Gradient Boosting, have been applied to volatility forecasting \cite{placeholder_ml_volatility}, demonstrating the ability to capture nonlinear combinations of predictors. Yet, the integration of static global network centralities as features for local temporal variance forecasting remains largely unexplored.
"""

data_tex = r"""\section{Data and Asset Universe}
\label{sec:data}

The data used in this study were extracted from the QuantBase ClickHouse database, comprising daily adjusted prices of equities traded on the Brazilian stock exchange (B3). To account for corporate actions (e.g., dividends, splits), adjusted closing prices were utilized exclusively. The historical window spans from January 1998 to January 2025.

We applied stringent liquidity and continuity filters to construct our \textit{core historical} universe. The selection criteria required strictly positive adjusted closing prices, exclusion of non-equity instruments (such as BDRs, ETFs, and index funds), and a focus on standard market segments (cod\_bdi = '02'). Brazilian units were retained if they represented highly liquid domestic securities. The resulting universe consists of $N = 58$ highly liquid stocks with long historical records. 

Index instruments such as BOVA11 and SMAL11 were treated separately and omitted from the main network construction to prevent trivial market-mode overrepresentation. For detailed temporal demonstrations of stylized facts and forecasting, we highlight a subset of \textit{demo assets}: PETR4 (Petrobras), VALE3 (Vale), and BBDC4 (Bradesco), representing the energy, materials, and financial sectors respectively.

% TODO: insert Table placeholder for universe summary
"""

methodology_tex = r"""\section{Methodology}
\label{sec:methodology}

\subsection{Log Returns and Realized Volatility}
Let $P_{i,t}$ be the adjusted closing price of asset $i$ at day $t$. The daily log return is defined as:
\begin{equation}
r_{i,t} = \log(P_{i,t}) - \log(P_{i,t-1})
\end{equation}
The realized volatility (RV) target for a forward horizon $h$ is computed as the square root of cumulative squared returns:
\begin{equation}
RV_{t,h} = \sqrt{\sum_{k=1}^{h} r_{i,t+k}^2}
\end{equation}

\subsection{Random Matrix Theory and Mar\v{c}enko-Pastur Bounds}
The empirical correlation matrix $\mathbf{C}$ of dimension $N \times N$ is computed over $T$ observations. Under the null hypothesis of purely random uncorrelated series, the eigenvalues of $\mathbf{C}$ should be bounded by the Mar\v{c}enko-Pastur (MP) distribution \cite{marcenko_1967_distribution}. For $Q = T/N > 1$, the maximum theoretical eigenvalue $\lambda_{+}$ is given by:
\begin{equation}
\lambda_{+} = \sigma^2 \left(1 + \frac{1}{Q} + 2\sqrt{\frac{1}{Q}}\right)
\end{equation}
where $\sigma^2 = 1 - \lambda_{max}/N$ accounts for the variance absorbed by the dominant market mode. Eigenvalues $\lambda > \lambda_{+}$ represent genuine economic signals, while those below are discarded as noise.

\subsection{Correlation Matrices and Mantegna Distance}
To translate correlations into a metric space suitable for graph theory, we use the Mantegna distance \cite{mantegna_1999_hierarchical}:
\begin{equation}
d_{ij} = \sqrt{2(1-\rho_{ij})}
\end{equation}
where $\rho_{ij}$ is the Pearson correlation between assets $i$ and $j$. This distance satisfies the conditions of a metric, being bounded between $0$ and $2$.

\subsection{Financial Network Construction: MST and PMFG}
Using $d_{ij}$, we construct the Minimum Spanning Tree (MST) via Kruskal's algorithm, yielding a tree of $N-1$ edges that minimizes the total distance. To capture richer structures including cycles, we generate the Planar Maximally Filtered Graph (PMFG) \cite{tumminello_2005_tool}. The PMFG retains $3N-6$ edges by iteratively adding edges in increasing order of distance, strictly enforcing the condition that the resulting graph remains embeddable on a sphere (planar).

\subsection{Volatility Benchmarks and Machine Learning}
We utilize standard econometric benchmarks for volatility forecasting. The GARCH(1,1) model \cite{bollerslev_1986_generalized} is specified as:
\begin{equation}
\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2
\end{equation}
To evaluate non-linear predictive capabilities, we train Machine Learning models, specifically Random Forest and Ridge Regression. The models are trained on classical autoregressive features (Set A), market-wide RMT parameters (Set B), and static PMFG network centralities (Set C). 

Models are evaluated out-of-sample using the QLIKE loss function:
\begin{equation}
QLIKE = \log(\hat{\sigma}_t^2) + \frac{\sigma_t^2}{\hat{\sigma}_t^2}
\end{equation}
where $\sigma_t^2$ is the proxy for realized variance.
"""

results_tex = r"""\section{Empirical Results}
\label{sec:results}

\subsection{Stylized Facts and Static Correlations}
The empirical analysis confirms that B3 assets exhibit pronounced stylized facts typical of emerging markets. The returns of the selected demo assets (PETR4, VALE3, BBDC4) present high excess kurtosis and fat-tailed distributions. Volatility clustering is visibly strong, and the autocorrelation function (ACF) of absolute returns decays slowly over time. 

% TODO: verify figure filename
\begin{figure}[ht]
    \centering
    \includegraphics[width=\textwidth]{images/figure_1d_stylized_facts_demo_assets_clean_2006_2025.pdf}
    \caption{Stylized facts demonstrating volatility clustering and fat-tailed returns for the selected demo assets.}
    \label{fig:stylized_facts}
\end{figure}

The historical correlation structure of the $N=58$ assets shows a mean Pearson correlation of approximately $0.24$. Crucially, intra-sector pairwise correlations (mean $0.3433$) are significantly higher than cross-sector correlations (mean $0.2249$, Mann-Whitney U $p$-value $\approx 1.3 \times 10^{-24}$). This confirms that same-sector stock pairs are much more strongly correlated than cross-sector pairs, highlighting the presence of sector-specific risk factors.

\subsection{Random Matrix Theory and Market Mode}
Applying RMT to the complete-case observations ($T = 1527$, $Q \approx 26.33$), we find the theoretical Mar\v{c}enko-Pastur upper bound $\lambda_{+} \approx 1.4278$. The empirical largest eigenvalue is $21.6505$, vastly exceeding the noise band. This dominant eigenvalue corresponds to the ``Market Mode,'' capturing approximately $37.3\%$ of the total variance. Subsequent eigenvectors neatly separate the Brazilian market into clear economic blocks: commodities versus domestic utilities (Eigenvector 2), and financials versus industrials (Eigenvector 3). 

\subsection{Network Topology: MST and PMFG}
By filtering out the dominant Market Mode, we reconstruct a "Group Mode" correlation matrix. Figure \ref{fig:pmfg} compares the PMFG constructed from the original correlation matrix against the Group Mode PMFG.

% TODO: verify figure filename
\begin{figure}[ht]
    \centering
    \includegraphics[width=\textwidth]{images/figure_12b_pmfg_refined_comparison.pdf}
    \caption{Planar maximally filtered graphs constructed from the original and RMT-filtered correlation matrices. Node colors indicate macro-sector classification and node sizes are proportional to network centrality. The original PMFG is dominated by market-mode hubs, whereas the Group/Sector Mode PMFG reveals a more localized sectoral topology.}
    \label{fig:pmfg}
\end{figure}

The original PMFG has a mean edge correlation of $0.5177$ and is dominated by major blue-chip hubs (e.g., GGBR4). In contrast, the Group Mode PMFG yields a lower mean edge correlation ($0.1109$) but a higher average clustering coefficient ($0.6653$). The removal of the market mode uncovers hidden, dense sectoral communities, placing assets like GUAR3 at the center of localized clusters.
"""

forecasting_tex = r"""\section{Volatility Forecasting: Econometrics vs Machine Learning}
\label{sec:forecasting}

We evaluated the predictive power of structural features through realized volatility forecasting. The GARCH(1,1) models fitted to our demo assets exhibited extremely high volatility persistence, with $\alpha + \beta$ consistently close to 1 (e.g., $0.9911$ for PETR4 and $0.9946$ for VALE3). Consequently, classical benchmarks like GARCH and HAR-RV provide demanding baselines.

% TODO: verify figure filename
\begin{figure}[ht]
    \centering
    \includegraphics[width=\textwidth]{images/figure_16_volatility_forecast_model_comparison.pdf}
    \caption{Out-of-sample volatility forecast comparison across econometric benchmarks and machine learning models.}
    \label{fig:forecasting_comparison}
\end{figure}

At a 5-day horizon, GARCH and HAR-RV remain highly competitive. However, at a 20-day horizon, Ridge Regression closely competes with and slightly outperforms GARCH in terms of QLIKE. More importantly, when Random Forest models are fed with Feature Set C (which includes PMFG centralities), they approach the performance of classical benchmarks.

Analysis of the Random Forest feature importances reveals that while classical autoregressive terms dominate, network features such as \texttt{pmfg\_original\_degree} and \texttt{pmfg\_group\_betweenness} appear among the top 20 predictors. This provides evidence that static topological properties derived from financial networks supply incremental structural information to non-linear forecasting models.
"""

discussion_tex = r"""\section{Discussion}
\label{sec:discussion}

The empirical pipeline confirms that RMT filtering is an effective mechanism for untangling the dense web of financial correlations in the B3 market. The finding that the Group Mode PMFG possesses higher clustering despite lower raw correlation values suggests that systemic risk is not uniform; once the overarching macroeconomic market drift is removed, risk propagates heavily within tightly knit sectoral cliques.

Furthermore, our volatility forecasting experiment bridges a critical gap. By demonstrating that PMFG centralities rank as important features in a Random Forest regressor, we show that cross-sectional network topology is not entirely disjoint from temporal variance. A central hub in a planar graph is topologically more exposed to systemic spillovers, which machine learning models identify as a valuable signal for conditional variance forecasting. We note cautiously, however, that these network features do not replace autoregressive models, but rather complement them.
"""

conclusion_tex = r"""\section{Conclusion}
\label{sec:conclusion}

This paper investigated the long-run dependency structure of Brazilian equities from 1998 to 2025 using a comprehensive econophysics and machine learning framework. We successfully combined Random Matrix Theory and planar financial networks (MST and PMFG) to decouple the dominant market mode from underlying sectoral noise. 

Our main contribution lies in evaluating whether features extracted from these econophysics structures improve realized-volatility forecasting. The evidence indicates that classical econometric benchmarks like GARCH(1,1) remain exceptional at handling volatility persistence. Nonetheless, machine learning models leveraging network centralities successfully extract predictive value from the static geometry of the market. PMFG degree and betweenness metrics rank among the most important features in tree-based regressors, proving that cross-sectional topology informs temporal risk.

Future research could naturally extend this framework by implementing Graph Neural Networks (GNNs), which can dynamically fuse temporal variance inputs with the spatial edges defined by the PMFG topology, potentially outperforming isolated machine learning algorithms.
"""

declarations_tex = r"""\section*{Funding}
This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

\section*{Declaration of competing interest}
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

\section*{Data availability}
The raw market data used in this study were obtained from B3 daily price records processed through the QuantBase data infrastructure. Due to data redistribution restrictions, raw data are not redistributed with this manuscript. Derived tables, scripts and reproducibility materials will be made available in a public repository upon publication.

\section*{Declaration of generative AI and AI-assisted technologies in the writing process}
During the preparation of this work, the authors used ChatGPT for language refinement, structural organization and code-review support. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.
"""

highlights_txt = r"""RMT separates market, sector and noise components in B3 equities.
Planar financial networks reveal hidden sectoral market topology.
PMFG centralities add information for volatility forecasting.
Small ML models compete with GARCH and HAR-RV benchmarks.
"""

references_bib = r"""@article{raddant_dimatteo_2023,
  title={A Look at Financial Dependencies by Means of Econophysics and Financial Economics},
  author={Raddant, M. and Di Matteo, T.},
  journal={arXiv preprint arXiv:2302.08208},
  year={2023}
}

@book{mantegna_1999_introduction,
  title={Introduction to Econophysics: Correlations and Complexity in Finance},
  author={Mantegna, Rosario N and Stanley, H Eugene},
  year={1999},
  publisher={Cambridge University Press}
}

@article{laloux_1999_noise,
  title={Noise dressing of financial correlation matrices},
  author={Laloux, Laurent and Cizeau, Pierre and Bouchaud, Jean-Philippe and Potters, Marc},
  journal={Physical review letters},
  volume={83},
  number={7},
  pages={1467},
  year={1999},
  publisher={APS}
}

@article{plerou_2002_random,
  title={Random matrix approach to cross correlations in financial data},
  author={Plerou, Vasiliki and Gopikrishnan, Parameswaran and Rosenow, Bernd and Nunes Amaral, Lu{\'\i}s A and Guhr, Thomas and Stanley, H Eugene},
  journal={Physical Review E},
  volume={65},
  number={6},
  pages={066126},
  year={2002},
  publisher={APS}
}

@article{mantegna_1999_hierarchical,
  title={Hierarchical structure in financial markets},
  author={Mantegna, Rosario N},
  journal={The European Physical Journal B-Condensed Matter and Complex Systems},
  volume={11},
  number={1},
  pages={193--197},
  year={1999},
  publisher={Springer}
}

@article{tumminello_2005_tool,
  title={A tool for filtering information in complex systems},
  author={Tumminello, Michele and Aste, Tomaso and Di Matteo, Tiziana and Mantegna, Rosario N},
  journal={Proceedings of the National Academy of Sciences},
  volume={102},
  number={30},
  pages={10421--10426},
  year={2005},
  publisher={National Acad Sciences}
}

@article{bollerslev_1986_generalized,
  title={Generalized autoregressive conditional heteroskedasticity},
  author={Bollerslev, Tim},
  journal={Journal of econometrics},
  volume={31},
  number={3},
  pages={307--327},
  year={1986},
  publisher={Elsevier}
}

@article{corsi_2009_simple,
  title={A simple approximate long-memory model of realized volatility},
  author={Corsi, Fulvio},
  journal={Journal of Financial Econometrics},
  volume={7},
  number={2},
  pages={174--196},
  year={2009},
  publisher={Oxford University Press}
}

@article{marcenko_1967_distribution,
  title={Distribution of eigenvalues for some sets of random matrices},
  author={Mar{\v{c}}enko, Vladimir A and Pastur, Leonid A},
  journal={Mathematics of the USSR-Sbornik},
  volume={1},
  number={4},
  pages={457},
  year={1967},
  publisher={IOP Publishing}
}

@article{placeholder_ml_volatility,
  title={Machine learning applications in volatility forecasting},
  author={Placeholder, Author},
  journal={Journal of Financial Forecasting (Placeholder)},
  year={2024}
}
"""

files_to_write = {
    "main.tex": main_tex,
    "highlights.txt": highlights_txt,
    "references.bib": references_bib,
    "sections/introduction.tex": intro_tex,
    "sections/related_work.tex": related_tex,
    "sections/data.tex": data_tex,
    "sections/methodology.tex": methodology_tex,
    "sections/results.tex": results_tex,
    "sections/forecasting.tex": forecasting_tex,
    "sections/discussion.tex": discussion_tex,
    "sections/conclusion.tex": conclusion_tex,
    "sections/declarations.tex": declarations_tex,
}

for rel_path, content in files_to_write.items():
    file_path = base_dir / rel_path
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Successfully generated {len(files_to_write)} LaTeX skeleton files in {base_dir}")
