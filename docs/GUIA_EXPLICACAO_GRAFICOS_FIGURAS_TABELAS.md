# Guia para explicar graficos, figuras e tabelas na reuniao

Complemento do `docs/GUIA_ESTUDO_REUNIAO_VIVIANE_BERRI.md`.

Objetivo: ter um roteiro simples para comentar os visuais do artigo `Random Matrix Filtering and Planar Financial Networks for Volatility Forecasting in the Brazilian Stock Market` sem travar em detalhes. A ideia e explicar sempre: o que o visual mostra, como foi construido, qual e a leitura principal e qual cautela deve ser mencionada.

## 1. Metodo geral para explicar qualquer visual

Use esta ordem:

1. "Este grafico/tabela mostra..."
2. "Ele foi construido a partir de..."
3. "O padrao principal e..."
4. "Isso importa porque..."
5. "A cautela e..."

Exemplo generico:

> "Esta figura mostra a distribuicao das correlacoes entre os ativos. Ela foi construida a partir da matriz de correlacao dos retornos padronizados. O padrao principal e que a maior parte das correlacoes e positiva, com media em torno de 0.24. Isso importa porque mostra que existe um componente comum de mercado. A cautela e que correlacao nao implica causalidade e depende da janela amostral."

Se perguntarem algo que voce nao lembra, responda com estrutura:

> "O ponto central da figura nao e o valor isolado, mas a comparacao entre os grupos. Aqui a mensagem e que..."

## 2. Frases de seguranca

- "Esse visual e descritivo; ele ajuda a interpretar a estrutura, nao prova causalidade."
- "A escala importa: no group mode os valores medios caem porque o modo de mercado foi removido."
- "A comparacao correta e entre matrizes/filtros/modelos sob a mesma amostra."
- "O objetivo do grafico nao e mostrar previsao perfeita, mas evidenciar se ha informacao incremental."
- "O resultado deve ser lido junto com as limitacoes: janela sincronizada, tres ativos-alvo e redes parcialmente estaticas."

## 3. Figuras principais

### Figura 1 - Fatos estilizados de PETR4, VALE3 e BBDC4

Arquivo: `outputs/figures/vector/figure_1d_stylized_facts_demo_assets_clean_2006_2025.pdf`

Mostra:

- precos normalizados;
- retornos deslocados para visualizacao;
- caudas dos retornos;
- autocorrelacao dos retornos absolutos.

Como explicar:

> "A Figura 1 serve para mostrar que os tres ativos escolhidos apresentam fatos estilizados tipicos de series financeiras: retornos com media proxima de zero, caudas pesadas, eventos extremos e persistencia na magnitude dos retornos. A autocorrelacao dos retornos absolutos indica clustering de volatilidade."

Numeros uteis:

- PETR4 tem curtose excessiva `11.55` e pior retorno diario de aproximadamente `-35.2%`;
- VALE3 tem curtose excessiva `7.51`;
- BBDC4 tem curtose excessiva `7.96`;
- os tres tem ACF positiva dos retornos absolutos no lag 1.

Cautela:

> "A figura justifica estudar volatilidade, mas nao diz sozinha qual modelo vai prever melhor."

### Figura 2a - Histograma das correlacoes

Arquivo: `outputs/figures/vector/figure_2_correlation_histogram.pdf`

Mostra:

- distribuicao de todas as correlacoes de Pearson entre os 58 ativos;
- `1653` pares no total.

Como explicar:

> "Esta figura mostra a dependencia media do universo da B3. A maioria das correlacoes e positiva, com media perto de `0.24`, o que sugere um componente comum de mercado, mas ainda com heterogeneidade entre pares."

O que olhar:

- se a massa esta deslocada para valores positivos;
- se ha cauda para correlacoes altas;
- se existem poucas correlacoes negativas.

Cautela:

> "Uma correlacao positiva media nao significa que todos os ativos se movem juntos da mesma forma. A dispersao e importante porque preserva estrutura setorial e local."

### Figura 2b - Correlacao dentro e entre setores

Arquivo: `outputs/figures/vector/figure_3_sector_correlation_distribution.pdf`

Mostra:

- comparacao entre pares do mesmo setor e pares de setores diferentes.

Como explicar:

> "A figura mostra que pares do mesmo setor tendem a ter correlacoes maiores que pares entre setores. Isso e coerente economicamente: empresas expostas a fatores parecidos tendem a se mover mais juntas."

Numeros uteis:

- pares dentro do setor: `275`;
- pares entre setores: `1378`;
- media dentro do setor: `0.3433`;
- media entre setores: `0.2249`;
- Mann-Whitney unilateral: `p = 1.33389e-24`.

Cautela:

> "O p-valor deve ser lido com cautela porque os pares nao sao independentes: o mesmo ativo aparece em varios pares. Entao o teste reforca uma evidencia descritiva, nao uma inferencia perfeita."

### Figura 3 - Correlacao media rolling

Arquivo: `outputs/figures/vector/figure_4_rolling_average_correlation.pdf`

Mostra:

- evolucao temporal da correlacao media do mercado em janelas moveis.

Como explicar:

> "Esta figura mostra que a dependencia de mercado nao e constante. Em certos periodos, a correlacao media aumenta, sugerindo momentos de maior sincronizacao dos ativos, normalmente associados a estresse ou choques comuns."

O que olhar:

- picos de correlacao;
- mudancas de nivel ao longo do tempo;
- periodos em que o mercado parece mais ou menos sincronizado.

Cautela:

> "A figura mostra dinamica temporal, mas nao identifica sozinha a causa de cada pico."

### Figura 4 - Espectro de autovalores e Marcenko-Pastur

Arquivo: `outputs/figures/vector/figure_6_rmt_eigenvalue_spectrum.pdf`

Mostra:

- autovalores empiricos da matriz de correlacao;
- limites teoricos de Marcenko-Pastur.

Como explicar:

> "A Figura 4 e central para a parte de RMT. Ela compara os autovalores empiricos com o intervalo esperado se os retornos fossem essencialmente aleatorios e independentes. Autovalores dentro da banda sao compativeis com ruido amostral; autovalores acima da banda sugerem modos coletivos reais."

Numeros uteis:

- `N = 58`;
- `T = 1527`;
- `Q = 26.33`;
- `lambda_- = 0.6482`;
- `lambda_+ = 1.4278`;
- maior autovalor: `21.6505`;
- `5` autovalores acima de `lambda_+`.

Frase forte:

> "O primeiro autovalor e muito maior que o limite superior de Marcenko-Pastur, entao ele e interpretado como modo de mercado."

Cautela:

> "RMT indica que o autovalor esta fora do benchmark aleatorio; a interpretacao economica vem depois, olhando loadings, setores e coerencia com o mercado."

### Figura 5 - Matrizes market, group, noise e filtered

Arquivo: `outputs/figures/vector/figure_8_rmt_filtered_matrices.pdf`

Mostra:

- decomposicao da matriz de correlacao em componentes espectrais.

Como explicar:

> "Esta figura traduz a decomposicao RMT em imagens. O market mode captura o co-movimento amplo. O group mode preserva estruturas mais locais e setoriais. O noise mode representa componentes compativeis com ruido. A matriz filtered combina os modos acima do limite de Marcenko-Pastur."

O que olhar:

- market mode mais uniforme;
- group mode com blocos/localidades;
- noise mode menos interpretavel;
- filtered como reconstrucao mais limpa do sinal.

Cautela:

> "A matriz filtrada nao e uma verdade absoluta; ela e uma reconstrucao baseada no criterio espectral escolhido."

### Figura 6 - PMFG original versus group mode

Arquivo: `outputs/figures/vector/figure_12b_pmfg_refined_comparison.pdf`

Mostra:

- comparacao da rede PMFG usando matriz original e matriz group mode.

Como explicar:

> "A PMFG preserva mais conexoes que a MST e permite ver agrupamentos locais. Na matriz original, as conexoes ainda refletem bastante o modo de mercado. No group mode, o componente comum foi removido, entao as conexoes ficam mais fracas em media, mas podem revelar organizacao local mais clara."

Numeros uteis:

- PMFG tem `3N - 6 = 168` arestas;
- PMFG original: correlacao media `0.5177`, clustering `0.5273`;
- PMFG group mode: correlacao media `0.1109`, clustering `0.6653`.

Frase forte:

> "Menor correlacao media no group mode nao significa menos estrutura; significa menos componente comum de mercado. O aumento do clustering sugere organizacao local mais concentrada."

Cautela:

> "A posicao visual dos nos ajuda a interpretar, mas as conclusoes devem vir das metricas e das arestas, nao apenas do layout."

### Figura 7 - Rede agregada por subsetor

Arquivo: `outputs/figures/vector/figure_15_subsector_dependency_network.pdf`

Mostra:

- rede em nivel de subsetores, agregando dependencias entre grupos economicos.

Como explicar:

> "Esta figura reduz a complexidade da rede de ativos para uma rede de subsetores. Ela ajuda a ver quais areas do mercado funcionam como hubs ou pontes de dependencia."

Numeros uteis:

- `22` subsetores;
- `66` arestas;
- densidade `0.2857`;
- dependencia media `0.0566`;
- maior degree: Retail;
- maior betweenness: Electric Utility;
- maior weighted degree: Apparel and Footwear.

Cautela:

> "A classificacao setorial e uma aproximacao macro. Entao a leitura deve ser economica e descritiva, nao uma taxonomia oficial definitiva."

### Figura 8 - Comparacao de modelos de previsao de volatilidade

Arquivo: `outputs/figures/vector/figure_16_volatility_forecast_model_comparison.pdf`

Mostra:

- desempenho de modelos e feature sets em previsao de volatilidade.

Como explicar:

> "Esta figura testa se a estrutura RMT/rede tambem tem utilidade preditiva. A comparacao e feita entre features classicas, features com RMT/mercado e features com redes. O ponto principal e que as features de rede ajudam de forma incremental, mas nao substituem as variaveis tradicionais de volatilidade."

Numeros uteis:

- horizonte de 5 dias: melhor QLIKE no teste foi Random Forest + Set C, `QLIKE = -5.2508`;
- horizonte de 20 dias: melhor QLIKE no teste foi Ridge + Set C, `QLIKE = -3.8812`.

Cautela:

> "O ganho depende de horizonte, modelo e metrica. Nao da para dizer que redes sempre vencem; da para dizer que adicionam informacao complementar."

### Figura 9 - Feature importance do Random Forest

Arquivo: `outputs/figures/vector/figure_18_ml_feature_importance.pdf`

Mostra:

- importancia relativa das features no Random Forest.

Como explicar:

> "Esta figura ajuda a entender o mecanismo da previsao. As features classicas de volatilidade continuam dominando, mas algumas variaveis de rede aparecem com importancia nao nula. Isso apoia a leitura de contribuicao incremental."

O que olhar:

- quais features classicas aparecem no topo;
- se features PMFG/MST/RMT aparecem em posicoes relevantes;
- diferencas entre horizontes.

Cautela:

> "Feature importance de Random Forest mede importancia dentro daquele modelo. Nao e causalidade e pode ser afetada por correlacao entre features."

## 4. Figuras de apendice

### Appendix A1 - Correlacoes dinamicas por pares

Arquivo: `outputs/figures/vector/figure_5_dynamic_pairwise_correlations.pdf`

Como explicar:

> "Mostra que correlacoes entre pares especificos variam no tempo. Isso reforca que a dependencia de mercado e dinamica, nao fixa."

### Appendix A2/A3 - Loadings dos autovetores

Arquivos:

- `outputs/figures/vector/figure_7b_rmt_top_eigenvectors_top_loadings.pdf`
- `outputs/figures/vector/figure_7a_rmt_top_eigenvectors_all_assets.pdf`

Como explicar:

> "Essas figuras ajudam a interpretar os autovalores fora da banda. O primeiro autovetor tende a representar o modo de mercado; os seguintes podem capturar grupos, setores ou contrastes entre ativos."

Cautela:

> "O sinal do autovetor pode inverter sem mudar o conteudo economico. O importante e o padrao relativo dos loadings."

### Appendix A4/A5 - Dendrogramas e heatmaps ordenados

Arquivos:

- `outputs/figures/vector/figure_9_dendrograms_comparison.pdf`
- `outputs/figures/vector/figure_10_ordered_heatmaps.pdf`

Como explicar:

> "Essas figuras mostram a organizacao hierarquica das dependencias. O dendrograma resume a arvore de similaridade; o heatmap ordenado mostra se aparecem blocos de correlacao."

Numeros uteis:

- cophenetic original: `0.9500`;
- cophenetic filtered: `0.9340`;
- cophenetic group mode: `0.8705`.

Cautela:

> "Cophenetic menor no group mode nao quer dizer pior resultado. Quer dizer que, ao remover o modo de mercado, a estrutura fica menos dominada por uma arvore global e mais local."

### Appendix A6 - MST original versus group mode

Arquivo: `outputs/figures/vector/figure_11b_mst_refined_comparison.pdf`

Como explicar:

> "A MST e o esqueleto minimo de dependencias fortes. Com `N = 58`, ela tem `57` arestas. Comparar original e group mode ajuda a ver quais conexoes sobrevivem quando o modo de mercado e removido."

Numeros uteis:

- MST original: correlacao media `0.5796`, same-sector ratio `0.7193`;
- MST group mode: correlacao media `0.1388`, same-sector ratio `0.6316`.

### Appendix A7 - Comparacao topologica MST/PMFG

Arquivo: `outputs/figures/vector/figure_13_network_topology_comparison.pdf`

Como explicar:

> "Esta figura compara metricas de rede entre MST e PMFG. A MST e mais esparsa e nao tem ciclos; a PMFG e mais rica, preserva triangulos e permite analisar clustering."

### Appendix A8 - Ranking de hubs

Arquivo: `outputs/figures/vector/figure_14_network_hub_rank_comparison.pdf`

Como explicar:

> "Mostra que a nocao de hub depende da matriz usada e da metrica escolhida. Um ativo pode ser central por degree, outro por betweenness, e isso muda entre original, filtered e group mode."

Cautela:

> "Hub nao significa necessariamente ativo mais importante economicamente. Significa mais central dentro da rede estimada."

### Appendix A9 - Volatilidade realizada versus prevista

Arquivo: `outputs/figures/vector/figure_17_realized_vs_predicted_volatility.pdf`

Como explicar:

> "Esta figura mostra visualmente se as previsoes acompanham a volatilidade realizada. O esperado e capturar o nivel e parte dos picos, mas nao prever todos os choques extremos."

Cautela:

> "Modelos de volatilidade geralmente suavizam picos. Errar choques extremos nao invalida o modelo, mas afeta metricas como RMSE e QLIKE."

## 5. Tabelas principais

### Tabela 1 - Estatisticas descritivas

Arquivo: `outputs/tables/table_1_descriptive_stats_2006_2025.csv`

Mostra:

- media, desvio padrao, assimetria, curtose, minimos, maximos, VaR empirico e autocorrelacoes absolutas.

Como explicar:

> "A Tabela 1 quantifica os fatos estilizados vistos na Figura 1. As medias sao pequenas, as curtoses sao altas e ha eventos extremos. Isso justifica o foco em volatilidade."

Numeros para lembrar:

- `n = 4953` para cada ativo;
- PETR4 tem maior desvio padrao entre os tres: `0.0276`;
- PETR4 tem maior curtose excessiva: `11.55`;
- PETR4 tem `41` dias com retorno absoluto acima de `10%`;
- BBDC4 tem `16`;
- VALE3 tem `26`.

### Tabela 2 - Correlacao dentro e entre setores

Arquivo: `outputs/tables/core_historical_sector_correlation_summary_1998_2025.csv`

Como explicar:

> "Esta tabela e a versao numerica da Figura 2b. Ela mostra que a media de correlacao dentro do setor e maior que entre setores, reforcando a existencia de estrutura setorial."

Numeros:

- within-sector: media `0.3433`;
- between-sector: media `0.2249`;
- `p = 1.33389e-24`.

### Tabela 3 - Resumo RMT

Arquivo: `outputs/tables/rmt_summary_core_historical_1998_2025.csv`

Como explicar:

> "Esta tabela resume os parametros da comparacao com Marcenko-Pastur. O ponto mais importante e que ha cinco autovalores acima do limite superior, e o maior deles e muito grande."

Numeros:

- `N = 58`;
- `T = 1527`;
- `lambda_+ = 1.4278`;
- maior autovalor `21.6505`;
- `5` autovalores acima do limite.

### Tabela 4 - Comparacao topologica das redes

Arquivo: `outputs/tables/network_topology_comparison_core_historical_1998_2025.csv`

Como explicar:

> "Esta tabela transforma as redes em metricas comparaveis. Ela mostra como MST e PMFG mudam quando usamos matriz original, filtered ou group mode."

Numeros:

- MST sempre tem `57` arestas;
- PMFG sempre tem `168` arestas;
- PMFG original: clustering `0.5273`;
- PMFG group mode: clustering `0.6653`;
- MST original: same-sector ratio `0.7193`;
- MST group mode: same-sector ratio `0.6316`.

Cautela:

> "Nao compare apenas a correlacao media. No group mode ela cai por construcao, porque o modo comum foi removido."

### Tabela 5 - Parametros GARCH

Arquivo: `outputs/tables/garch_parameters_2006_2025.csv`

Como explicar:

> "Esta tabela apresenta os parametros do benchmark econometrico GARCH(1,1). Ela serve como base tradicional de comparacao com os modelos de machine learning e features de rede."

O que comentar:

- GARCH captura persistencia de volatilidade;
- e um benchmark conhecido;
- nao usa diretamente a estrutura cross-sectional das redes.

Cautela:

> "GARCH e importante como baseline, mas o artigo nao depende apenas dele; a pergunta e se informacao estrutural da rede acrescenta algo."

### Tabela 6 - Comparacao de modelos de volatilidade

Arquivo: `outputs/tables/volatility_model_comparison_2006_2025.csv`

Como explicar:

> "Esta tabela e a evidencia quantitativa da parte de previsao. Ela compara modelos, horizontes e conjuntos de features usando MAE, RMSE, QLIKE e `R2_oos`."

Numeros para lembrar:

- 5 dias: Random Forest + Set C teve melhor QLIKE no teste, `-5.2508`;
- 20 dias: Ridge + Set C teve melhor QLIKE no teste, `-3.8812`;
- Set C inclui features classicas, RMT/mercado e rede.

Cautela:

> "A conclusao nao e que o modelo mais complexo sempre vence. A conclusao e que features de rede podem melhorar de forma incremental em alguns casos."

## 6. Como responder perguntas dificeis sobre visuais

### "Esse grafico prova que os setores causam correlacao?"

Resposta:

> "Nao prova causalidade. Ele mostra que, descritivamente, pares dentro do mesmo setor tem correlacao maior. Isso e coerente com exposicoes economicas comuns, mas causalidade exigiria outro desenho."

### "Por que a correlacao do group mode e tao baixa?"

Resposta:

> "Porque o group mode remove o componente de mercado dominante. Depois de tirar o fator comum, o que sobra sao dependencias mais locais, naturalmente menores em magnitude."

### "Se o group mode tem correlacao menor, por que olhar para ele?"

Resposta:

> "Porque ele ajuda a enxergar estrutura que fica escondida pelo modo de mercado. O interesse nao e ter maior correlacao media, mas separar dependencia comum de dependencia local."

### "A rede depende do layout?"

Resposta:

> "A visualizacao depende do layout, mas as metricas nao. Por isso a leitura deve combinar figura e tabela: arestas, clustering, centralidade e proporcao same-sector."

### "Por que QLIKE e nao so RMSE?"

Resposta:

> "RMSE mede erro na escala da volatilidade. QLIKE avalia previsao de variancia e e comum quando a volatilidade realizada e uma proxy imperfeita da variancia latente. Por isso os rankings podem mudar."

### "Por que usar apenas PETR4, VALE3 e BBDC4 na previsao?"

Resposta:

> "Eles sao ativos liquidos, relevantes e de setores diferentes, entao funcionam como casos demonstrativos. A extensao natural e ampliar a previsao para mais ativos."

### "As features de rede sao estaticas?"

Resposta:

> "Em parte, sim. Essa e uma limitacao honesta. Um desenho totalmente real-time exigiria recalcular RMT e redes em janelas rolling ou recursivas usando apenas informacao disponivel ate cada data."

## 7. Roteiro curto para apresentar todos os visuais

Use esta fala se precisar passar rapidamente pelas figuras:

> "As primeiras figuras estabelecem os fatos estilizados e a estrutura de correlacao: os ativos tem caudas pesadas, volatilidade persistente e correlacoes predominantemente positivas, especialmente dentro de setores. Depois, a parte de RMT mostra que a matriz de correlacao tem cinco autovalores acima do benchmark de Marcenko-Pastur, com um modo de mercado muito dominante. As matrizes filtradas e as redes mostram o que acontece quando separamos modo de mercado, grupo e ruido. A PMFG e a rede por subsetor ajudam a interpretar a organizacao local do mercado. Por fim, as figuras e tabelas de previsao mostram que as features de rede nao substituem as features classicas de volatilidade, mas adicionam informacao complementar em alguns modelos e horizontes."

## 8. Checklist antes da reuniao

Voce deve conseguir explicar:

- o que cada eixo representa nas figuras de correlacao e volatilidade;
- por que a Figura 4 e central para justificar RMT;
- por que `lambda_1` e chamado de modo de mercado;
- diferenca visual entre market mode, group mode, noise e filtered;
- por que PMFG tem mais informacao que MST;
- por que menor correlacao no group mode nao invalida a rede;
- o que uma tabela acrescenta em relacao a figura;
- por que QLIKE pode dar ranking diferente de RMSE;
- quais conclusoes sao fortes e quais sao apenas descritivas;
- quais limitacoes voce deve mencionar espontaneamente.

