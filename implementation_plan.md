# Plano de Revisão Estilística — Artigo B3 Econophysics

## Contexto

O artigo tem ~12.320 palavras nas seções `.tex`. A análise quantitativa de frequência revelou padrões repetitivos que, em conjunto, criam uma impressão de texto gerado por IA. Este plano detalha todas as mudanças necessárias, priorizadas por impacto.

---

## 1. Diagnóstico Quantitativo Global

### Termos com frequência excessiva (todo o artigo)

| Termo/Padrão | Ocorrências | Limite recomendado | Ação |
|---|---|---|---|
| `empirical` | **66** | ≤ 20 | Reduzir ~70% |
| `topology` / `topological` | **43** | ≤ 18 | Reduzir ~55% |
| `consistent with` | **19** | ≤ 6 | Reduzir ~68% |
| `provide` / `provides` | **29** | ≤ 10 | Trocar por verbos específicos |
| `interpreted as` | **18** | ≤ 8 | Variar construções |
| `should be interpreted` | **8** | ≤ 3 | Cortar interpretações defensivas |
| `rather than` | **17** | ≤ 7 | Reduzir ~60% |
| `incremental` | **13** | ≤ 5 | Alternativas: *modest*, *additional*, *marginal* |
| `therefore` | **12** | ≤ 6 | Variar: *hence*, *thus*, *accordingly*, ou reestruturar |
| `diagnostic` / `diagnostics` | **20** | ≤ 8 | Alternativas: *checks*, *tests*, *assessments* |
| `informative` | **12** | ≤ 5 | Alternativas: *meaningful*, *structured*, *significant* |
| `complementary` | **8** | ≤ 4 | Alternativas: *additional*, *supplementary* |
| `mesoscopic` | **9** | ≤ 4 | Usar só quando tecnicamente necessário |
| `pipeline` | **9** | ≤ 3 | Trocar por *workflow*, *framework*, *approach* |
| `This paper develops` | **2** | ≤ 1 | Manter só no abstract |
| `The analysis` (como sujeito) | **8** | ≤ 3 | Trocar por `We` ou sujeito concreto |
| `The purpose is` | **2** | → 0 | Converter em ação direta |
| `The appropriate conclusion` | **2** | → 0 | Reescrever |

### Padrão crítico: Quase ZERO uso de "We"

| Forma | Ocorrências |
|---|---|
| `We` (início de frase) | **1** |
| `we` (minúsculo, dentro da frase) | **0** |

> [!CAUTION]
> O artigo quase nunca usa "we" como sujeito. Isto é a **maior** fonte de texto robótico. Artigos da Elsevier aceitam e encorajam "we". O artigo de referência Raddant & Di Matteo usa "we" com frequência natural.

---

## 2. Comparação Estilística com os Artigos de Referência

### 2.1 Raddant & Di Matteo (2023) — Referência principal

Este artigo-review de econofísica em *Physics Reports* é a principal referência de escrita. Características que o nosso artigo deveria emular:

| Aspecto | Raddant & Di Matteo | Nosso artigo | Gap |
|---|---|---|---|
| **Uso de "we"** | Frequente e natural: *"we first touch upon", "we will focus", "we are guided by"* | Praticamente zero | ⚠️ **Crítico** |
| **Frases de abertura** | Variam: sujeito concreto, perguntas, dados | Quase todas: `The [noun]...` | ⚠️ **Alto** |
| **Hedging** | Moderado e natural: *"can", "often", "typically"* | Excessivo: *"should be interpreted as", "rather than", "consistent with"* | ⚠️ **Alto** |
| **Transições** | Naturais: *"Hence, while...", "Another aspect...", "It is well known that..."* | Mecânicas: *"The next step moves from...", "The analysis proceeds..."* | ⚠️ **Médio** |
| **Voz passiva** | Equilibrada com ativa | Predominantemente passiva/impessoal | ⚠️ **Alto** |
| **"empirical"** | Usado com parcimônia (~10x em 40+ páginas) | **66x** em ~12k palavras | ⚠️ **Crítico** |
| **"consistent with"** | Aparece ~3-4x em 40+ páginas | **19x** em 12k palavras | ⚠️ **Alto** |

**Exemplos concretos de estilo Raddant & Di Matteo:**
- *"For most of the following analyses we use daily data covering the time period from..."* (direto, concreto)
- *"Hence, one aspect of the returns is that their distributions are non-Gaussian..."* (transição natural)
- *"These findings are important for two reasons."* (sem "The empirical findings provide...")
- *"It is well known that..."* (construção coloquial acadêmica, mas natural)
- *"We start by sorting all pairs of stocks..."* (ação direta)

### 2.2 Zaccone & Trachenko (2026) — Chaos, Solitons & Fractals

Artigo de física teórica com estilo limpo e assertivo:

| Aspecto | Zaccone & Trachenko | Nosso artigo |
|---|---|---|
| **Claims** | Diretas: *"we show that", "we obtain", "we consider"* | Defensivas: *"The results support the view that..."* |
| **Matemática** | Introduzida com frases curtas: *"We consider a nonlinear model in which..."* | Precedida de justificativas longas |
| **Hedging** | Preciso: *"we do not claim that..."* (1x, quando necessário) | Excessivo em todo o texto |

### 2.3 Artigos ICCSA/ICEIS (Andrey et al.)

Artigos de conferência mais curtos, mas com estilo direto:

| Aspecto | Artigos Andrey | Nosso artigo |
|---|---|---|
| **"The objective"** | *"The main objective of this article is to investigate..."* (1x, na intro) | Variantes de "The purpose is..." aparecem 3x |
| **Related Work** | Cada parágrafo: *"[Author] showed/found/reported..."* → *"In the present work..."* | Vários parágrafos sem sujeito claro |
| **Transições** | *"Taken together, these studies address..."* | *"The analysis proceeds through..."* |

---

## 3. Catálogo Expandido de Padrões IA (Além dos Já Identificados)

> [!IMPORTANT]
> Estes padrões **não estavam na lista original do usuário** mas foram encontrados na análise do texto completo.

### 3.1 Padrão: "This [noun] is [adjective] because..."

Aparece muitas vezes como justificativa automática:

| Frase atual | Sugestão |
|---|---|
| *"This universe is intentionally historical rather than purely current."* | *"The universe is historical rather than purely current, covering..."* |
| *"This distinction is relevant because..."* | *"The distinction matters because..."* |
| *"This is especially relevant in..."* | Cortar ou integrar na frase anterior |
| *"This choice provides a consistent synchronized panel..."* | *"The synchronized panel ensures that..."* |
| *"This complete-panel restriction ensures that..."* | *"Complete-panel estimation ensures that..."* |

### 3.2 Padrão: "interpreted as" / "should be interpreted"

**26 ocorrências** totais. Texto parece que está constantemente se defendendo:

| Frase atual | Sugestão |
|---|---|
| *"is interpreted as a market mode"* | *"captures broad co-movement (market mode)"* |
| *"should be interpreted as model diagnostics rather than causal measures"* | *"are model diagnostics, not causal measures"* |
| *"should not be interpreted simply as a weaker version"* | *"is not simply a weaker version"* |
| *"should be interpreted descriptively"* | *"is descriptive"* ou cortar |

### 3.3 Padrão: Excesso de advérbios qualificadores

| Advérbio | Ocorrências | Recomendação |
|---|---|---|
| `especially` | 7 | Reduzir para ≤ 3 |
| `particularly` | 5 | Reduzir para ≤ 2 |
| `intentionally` | 2 | Cortar ambos |
| `deliberately` | 2 | Manter ≤ 1 |

### 3.4 Padrão: Redundância explicativa

Frases que explicam o que já é óbvio pelo contexto:

| Frase redundante | Ação |
|---|---|
| *"The term $\mathbf{u}_k\mathbf{u}_k^{\top}$ is the outer product that reconstructs the matrix contribution of mode $k$."* | Cortar — óbvio para leitores-alvo |
| *"Rows correspond to synchronized trading days and columns correspond to assets."* | Cortar — segue da notação |
| *"Because the associated eigenvector has positive loadings for nearly all assets and the eigenvalue lies far above..."* | Simplificar: *"The eigenvector has broadly positive loadings, confirming its interpretation as a market mode."* |

### 3.5 Padrão: "This is an important result" / construções avaliativas

| Frase | Sugestão |
|---|---|
| *"This is an important result:"* (results_networks.tex, L26) | Cortar a frase avaliativa; deixar o resultado falar por si |
| *"This is a central finding:"* (discussion.tex, L10) | Substituir por transição mais natural |

---

## 4. Plano Seção-a-Seção (Com Frases Exatas)

### 4.1 Abstract ([main.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/main.tex#L91-L101))

| # | Frase atual (trecho) | Frase sugerida | Motivo |
|---|---|---|---|
| A1 | *"This paper develops an econophysics pipeline for Brazilian equities"* | *"We develop an econophysics workflow for Brazilian equities"* | "This paper develops" + "pipeline" |
| A2 | *"evaluates whether the resulting dependency structure contains information"* | *"test whether the resulting dependency structure contributes to"* | Mais direto |
| A3 | *"the empirical spectrum is decomposed"* | *"the spectrum is decomposed"* | "empirical" desnecessário aqui |
| A4 | *"consistent with localized sectoral organization"* | *"aligned with localized sectoral organization"* | Variar "consistent with" |
| A5 | *"provide competitive and incremental evidence rather than uniformly dominating"* | *"offer competitive accuracy but do not consistently outperform"* | Menos defensivo |
| A6 | *"The results support the view that RMT-filtered topology is useful for interpreting market structure and may complement"* | *"Overall, RMT-filtered topology helps interpret market structure and can serve as a complementary input for"* | Mais assertivo |

### 4.2 Highlights ([main.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/main.tex#L95-L101))

| # | Frase atual | Frase sugerida |
|---|---|---|
| H1 | *"RMT provides a spectral decomposition of..."* | *"RMT decomposes the correlation matrix into..."* |
| H2 | *"consistent with sectoral organization"* | *"aligned with sectoral organization"* |
| H3 | *"Network features provide limited but nonzero incremental evidence"* | *"Network features add modest but nonzero predictive value"* |

### 4.3 Introduction ([introduction.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/introduction.tex))

| # | Linha | Frase atual (trecho) | Frase sugerida |
|---|---|---|---|
| I1 | 4 | *"A central task of empirical econophysics is therefore to distinguish"* | *"A central task is therefore to separate"* |
| I2 | 8 | *"These characteristics suggest that the empirical dependency matrix may combine"* | *"The dependency matrix therefore combines"* |
| I3 | 8 | *"the Brazilian equity market remains relatively underexplored in the complex-systems literature"* | *"the Brazilian equity market has received limited attention in the complex-systems literature"* |
| I4 | 8 | *"but a broad B3 equity pipeline combining..."* | *"but a comprehensive B3 equity study combining..."* |
| I5 | 10 | *"The empirical difficulty is that correlation matrices are noisy"* | *"Correlation matrices are noisy"* |
| I6 | 14 | *"This paper develops an integrated econophysics pipeline"* | *"We develop an integrated econophysics workflow"* |
| I7 | 14 | *"The analysis proceeds through three stages."* | *"The workflow has three stages."* |
| I8 | 14 | *"whether the extracted features provide incremental predictive information"* | *"whether the extracted features improve forecasts"* |
| I9 | 17 | *"The contribution of this paper is fourfold:"* | *"The paper makes four contributions:"* |
| I10 | 19 | *"It builds a reproducible econophysics pipeline"* | *"It constructs a reproducible econophysics workflow"* |
| I11 | 20 | *"providing a spectral interpretation"* | *"yielding a spectral interpretation"* |
| I12 | 25 | *"the empirical methodology"* | *"the methodology"* |
| I13 | 25 | *"report the empirical results"* | *"report the results"* |

### 4.4 Data ([data.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/data.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| D1 | 6 | *"The empirical analysis uses Brazilian equity data derived from BovDB"* | *"The dataset consists of Brazilian equity prices from BovDB"* |
| D2 | 8 | *"The main empirical objects are adjusted closing prices"* | *"The main objects of interest are adjusted closing prices"* |
| D3 | 12 | *"The empirical analysis uses adjusted closing prices because"* | *"Adjusted closing prices are used because"* |
| D4 | 16 | *"The purpose of this step is to keep the dependency matrix focused on"* | *"This filter keeps the dependency matrix focused on"* |
| D5 | 22 | *"This universe is intentionally historical rather than purely current."* | *"The universe is historical rather than purely current."* |
| D6 | 58 | *"The main empirical claims of the paper are based on"* | *"The main results are based on"* |

### 4.5 Methodology ([methodology.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/methodology.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| M1 | 4 | *"The empirical design follows an integrated methodology that transforms"* | *"The methodology transforms"* |
| M2 | 4 | *"The purpose is not only to estimate dependencies, but to distinguish"* | *"The workflow estimates dependencies and separates"* |
| M3 | 83 | *"The analysis then proceeds through..."* | *"The workflow proceeds through..."* |
| M4 | 100 | *"commonly used in empirical studies of financial fluctuations"* | *"standard in studies of financial returns"* |
| M5 | 118 | *"The empirical correlation matrix is denoted by $\mathbf{C}$"* | *"Let $\mathbf{C}$ denote the Pearson correlation matrix"* |
| M6 | 154 | *"the analysis computes"* | *"we compute"* |
| M7 | 162 | *"These diagnostics assess whether the selected Brazilian return series display empirical regularities"* | *"These checks assess whether B3 returns display the regularities"* |
| M8 | 167 | *"The empirical Pearson correlation matrix is estimated"* | *"The Pearson correlation matrix is estimated"* |
| M9 | 197 | *"the empirical dependency matrix"* | *"the dependency matrix"* |
| M10 | 224 | *"$k=1$ denotes the largest empirical mode"* | *"$k=1$ denotes the largest mode"* |
| M11 | 276 | *"This decomposition allows the analysis to compare networks"* | *"This decomposition separates networks"* |
| M12 | 318 | *"the analysis reports"* | *"we report"* |
| M13 | 337 | *"This aggregation converts ticker-level dependencies into a mesoscopic map"* | *"The aggregation converts ticker-level dependencies into a subsector-level map"* |

### 4.6 Results — Stylized Facts ([results_stylized_correlation.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/results_stylized_correlation.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| S1 | 14 | *"a pattern consistent with volatility clustering"* | *"a pattern indicating volatility clustering"* |
| S2 | 14 | *"which is consistent with heavy-tailed return behaviour"* | *"pointing to heavy-tailed returns"* |
| S3 | 14 | *"consistent with persistent volatility dynamics"* | *"indicating persistent volatility"* |
| S4 | 20 | *"These properties are consistent with the well-documented stylized facts"* | *"These properties match the well-documented stylized facts"* |
| S5 | 48 | *"The next step moves from univariate behaviour to cross-sectional dependence."* | *"We now turn from individual return behaviour to cross-sectional dependence."* |
| S6 | 102 | *"This behaviour is consistent with the emergence of a dominant leading eigenvalue"* | *"which helps explain the dominant leading eigenvalue"* |

### 4.7 Results — RMT ([results_rmt.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/results_rmt.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| R1 | 6 | *"This separation measures the deviation of the empirical correlation matrix from the random-matrix benchmark."* | Cortar — redundante com a frase anterior |
| R2 | 21 | *"Table~\ref{tab:rmt_summary} provides the numerical basis for the RMT filtering step."* | *"Table~\ref{tab:rmt_summary} reports the numerical inputs for RMT filtering."* |
| R3 | 23 | *"consistent with a dominant market mode and a small number of group or sector modes"* | *"indicating a dominant market mode and a small number of group or sector modes"* |
| R4 | 36 | *"The key methodological point is that the market mode is informative but also visually dominant."* | *"The market mode is informative but visually dominant."* |
| R5 | 62 | *"The relevant empirical point is that the eigenvectors beyond the leading component display loading patterns that are consistent with localized or sector-related dependencies."* | *"Empirically, the eigenvectors beyond the leading component show loading patterns suggesting localized or sector-related dependencies."* |

### 4.8 Results — Clustering ([results_clustering.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/results_clustering.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| C1 | 6 | *"The purpose is exploratory and diagnostic: the heatmaps assess whether"* | *"The heatmaps serve as diagnostic tools, assessing whether"* |
| C2 | 8 | *"consistent with the large leading eigenvalue"* | *"reflecting the large leading eigenvalue"* |

### 4.9 Results — Networks ([results_networks.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/results_networks.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| N1 | 26 | *"This is an important result: removing the market mode"* | *"Removing the market mode"* (cortar avaliação) |
| N2 | 41 | *"retain patterns consistent with sectoral and subsectoral organization"* | *"retain patterns aligned with sectoral and subsectoral groupings"* |
| N3 | 63 | *"This pattern is consistent with localized dependency structure"* | *"This pattern suggests localized dependency structure"* |

### 4.10 Results — Forecasting ([results_forecasting.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/results_forecasting.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| F1 | 83 | *"This behaviour is consistent with the aggregate results"* | *"This matches the aggregate results"* |
| F2 | 99 | *"The appropriate conclusion is therefore incremental: topology does not replace..."* | *"In summary, topology does not replace classical volatility features, but may add structural information..."* |

### 4.11 Discussion ([discussion.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/discussion.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| Ds1 | 4 | *"the empirical results support a layered interpretation of Brazilian equity dependencies, consistent with"* | *"the results point to a layered interpretation of Brazilian equity dependencies, in line with"* |
| Ds2 | 10 | *"This combination is a central finding"* | *"Notably" ou cortar |
| Ds3 | 14 | *"They do not show that machine learning uniformly dominates classical volatility models."* | *"Machine learning does not uniformly outperform classical volatility models."* |

### 4.12 Conclusion ([conclusion.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/conclusion.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| Co1 | 4 | *"This paper develops an econophysics pipeline"* | *"This study examined the dependency structure of Brazilian equities"* |
| Co2 | 6 | *"provides descriptive evidence that Brazilian equities display empirical signatures commonly associated with"* | *"shows that Brazilian equities display signatures commonly associated with"* |
| Co3 | 6 | *"supporting the interpretation that sectoral organization is reflected in the empirical dependency matrix"* | *"confirming that sectoral organization is reflected in the dependency matrix"* |
| Co4 | 8 | *"Random Matrix Theory provides a spectral decomposition"* | *"Random Matrix Theory decomposes"* |
| Co5 | 8 | *"are consistent with commodity, financial and utility-related group structures"* | *"suggest commodity, financial and utility-related group structures"* |
| Co6 | 14 | *"The appropriate conclusion is incremental"* | *"The net contribution of network features is incremental"* |

### 4.13 Related Work ([related_work.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/related_work.tex))

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| RW1 | 8 | *"the empirical goal is not merely to estimate"* | *"the goal is not merely to estimate"* |
| RW2 | 22 | *"This terminology is a filtering convention, not a claim that every eigenvector has a unique economic label."* | *"These labels should be read as filtering categories; they do not imply that each eigenvector has a unique economic interpretation."* |
| RW3 | 42 | *"This integration matters because the interpretation of a financial network depends on the matrix from which it is built."* | *"This integration matters because a network's interpretation depends on the matrix used to build it."* |

### 4.14 Limitations ([limitations.tex](file:///C:/mysystems/projects/b3-econophysics-ai/article/overleaf_viviane_revision/sections/limitations.tex))

Esta seção está relativamente limpa. Mudanças menores:

| # | Linha | Frase atual | Frase sugerida |
|---|---|---|---|
| L1 | 12 | *"The nonzero importance of PMFG features suggests incremental signal"* | *"PMFG features show nonzero but modest importance"* |

---

## 5. Regras Globais para Aplicação

### Regra 1: Introduzir "we" sistematicamente
- **Abstract**: Manter *"This paper"* 1x na abertura → trocar para *"We develop..."*
- **Introduction**: Usar *"we"* para descrever ações do estudo
- **Methodology**: Usar *"we compute"*, *"we estimate"*, *"we apply"*
- **Results**: Usar *"we observe"*, *"we report"*, *"we find"*
- **Discussion/Conclusion**: Usar *"we"* para interpretações

### Regra 2: Substituição de "empirical"
Manter **apenas** em:
- *empirical correlation matrix* (quando em contraste com modelo teórico)
- *empirical spectrum/eigenspectrum*
- *empirical results* (1-2x máx)
- *empirical regularities* (1x na intro)

**Remover** em todos os outros usos: *empirical analysis, empirical design, empirical claims, empirical difficulty, empirical object, empirical setting, empirical dependency matrix, empirical features, empirical signatures*.

### Regra 3: Verbos específicos em vez de "provides"
| Em vez de | Usar |
|---|---|
| *provides a decomposition* | *decomposes* |
| *provides evidence* | *indicates*, *shows*, *suggests* |
| *provides the numerical basis* | *reports the numerical inputs* |
| *provides a compact entry point* | *offers a compact entry point* |

### Regra 4: Reduzir hedging defensivo
Manter hedging **apenas** quando genuinamente necessário (limitações, caveats reais). Cortar em frases que descrevem resultados próprios.

### Regra 5: Diversificar inícios de parágrafos
Evitar sequências de `The [noun] [verb]...`. Alternar com:
- Sujeito concreto: *"Correlations are..."*, *"PETR4, VALE3..."*
- Ação: *"We compute...", "Removing the market mode..."*
- Resultado: *"Five eigenvalues exceed..."*

---

## 6. Prioridade de Execução

| Prioridade | Grupo | Impacto |
|---|---|---|
| 🔴 P1 | Introduzir "we" em todo o artigo | Maior impacto na naturalidade |
| 🔴 P1 | Reduzir "empirical" de 66→~20 | Remove a marca IA mais visível |
| 🔴 P1 | Reduzir "consistent with" de 19→~6 | Remove cautela excessiva |
| 🟠 P2 | Trocar "provides/provide" por verbos específicos | Diversifica vocabulário |
| 🟠 P2 | Reduzir "interpreted as" / "should be interpreted" | Remove tom defensivo |
| 🟠 P2 | Eliminar "The purpose is", "The analysis proceeds" | Remove frases mecânicas |
| 🟡 P3 | Reduzir "rather than" de 17→~7 | Naturaliza argumentação |
| 🟡 P3 | Reduzir "incremental" de 13→~5 | Diversifica vocabulário |
| 🟡 P3 | Reduzir "diagnostic(s)" de 20→~8 | Evita repetição técnica |
| 🟢 P4 | Diversificar "topology/topological" de 43→~18 | Polimento fino |
| 🟢 P4 | Reduzir advérbios qualificadores | Polimento fino |
| 🟢 P4 | Cortar redundâncias explicativas | Concisão |

---

## 7. Verificação

### Após as edições
1. Recompilar o `.tex` e verificar que não há erros de LaTeX
2. Contar novamente a frequência dos termos-chave
3. Verificar que cada seção usa "we" pelo menos 2-3x
4. Verificar que "empirical" aparece ≤ 20x no total
5. Verificar que "consistent with" aparece ≤ 6x
6. Leitura em voz alta de abstract, introdução e conclusão para verificar naturalidade

> [!IMPORTANT]
> **Quer que eu prossiga com a execução das edições nos arquivos `.tex`?** Posso fazer seção por seção, começando pelo abstract e introdução (P1), ou todas de uma vez. As mudanças são todas textuais no LaTeX e não afetam figuras, tabelas ou referências.
