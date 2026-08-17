# Roteiro de apresentacao: secao por secao, grafico por grafico

Base: artigo `Random Matrix Filtering and Planar Financial Networks for Volatility Forecasting in the Brazilian Stock Market`, versao `article/overleaf_viviane_revision`.

Objetivo deste documento: servir como apoio direto para apresentar o artigo aos professores. A ordem abaixo segue a estrutura do manuscrito: dados, metodologia, resultados de correlacao, RMT, clustering, redes, rede agregada por subsetor e previsao de volatilidade.

Use este roteiro como fala guiada. A cada figura ou tabela, tente sempre responder quatro coisas:

1. O que esta sendo mostrado?
2. Como foi construido?
3. Qual e a mensagem principal?
4. Qual e a cautela?

## 0. Abertura da apresentacao

Fala sugerida:

> "O artigo analisa a B3 como um sistema complexo. A ideia e partir de precos ajustados, calcular retornos logaritmicos, estimar uma matriz de correlacao para ativos brasileiros, separar sinal e ruido usando Random Matrix Theory, transformar essa estrutura em redes financeiras MST e PMFG, e por fim testar se essas informacoes ajudam na previsao de volatilidade."

Mensagem principal:

- O artigo nao e apenas sobre previsao.
- O fluxo e: dados -> retornos -> correlacao -> RMT -> redes -> features -> previsao.
- A contribuicao e integrar interpretacao estrutural de mercado com um teste preditivo.

Frase de seguranca:

> "A parte de previsao deve ser lida como evidencia incremental, nao como promessa de modelo perfeito."

## 1. Data and asset universe

### Tabela: Summary of the samples used in this study

No artigo: `Table - Summary of the samples used in this study`.

Mostra:

- amostra de 3 ativos representativos: PETR4, VALE3 e BBDC4;
- universo historico principal: 58 ativos;
- periodo amplo: 1998-2025;
- uso de cada amostra.

Fala sugerida:

> "Antes dos resultados, o artigo define duas escalas de analise. A primeira e uma amostra pequena, PETR4, VALE3 e BBDC4, usada para fatos estilizados e previsao. A segunda e o universo historico de 58 ativos, usado para correlacoes, RMT, clustering e redes."

Numeros para lembrar:

- Ativos representativos: `3`;
- Universo principal: `58` ativos;
- Painel sincronizado para RMT/redes: `N = 58`, `T = 1527`;
- Periodo dos ativos demonstrativos na tabela descritiva: 2006-2025, com `n = 4953`.

Se perguntarem por que sincronizar:

> "Porque RMT, autovalores, autovetores, distancias e redes precisam vir de uma unica matriz de correlacao consistente. Se cada par usa datas diferentes, a matriz mistura dependencia real com mudanca de amostra."

Se perguntarem por que PETR4, VALE3 e BBDC4:

> "Eles sao liquidos, economicamente relevantes e representam setores diferentes: petroleo, mineracao e financeiro."

## 2. Methodology

### Figura: Overview of the empirical workflow

No artigo: `fig:methodology_overview`.

Mostra:

- o pipeline completo do artigo;
- dados ajustados da B3;
- retornos sincronizados;
- fatos estilizados;
- matriz de correlacao;
- RMT;
- market mode, group mode e noise;
- clustering, MST/PMFG, rede de subsetores;
- previsao de volatilidade.

Fala sugerida:

> "Esta figura e o mapa do artigo. Primeiro eu construo retornos diarios a partir de precos ajustados. Depois estimo a matriz de correlacao. Em seguida uso RMT para separar o que parece modo de mercado, modo de grupo e ruido. A partir dessas matrizes, construo heatmaps, dendrogramas, MST, PMFG e agregacao por subsetor. No final, transformo parte dessa estrutura em features para previsao de volatilidade."

Mensagem principal:

- A metodologia e encadeada.
- RMT nao aparece isolada; ela alimenta clustering, redes e features.
- A previsao e a ultima etapa, nao o unico objetivo.

Se perguntarem o que e cada camada:

- `market mode`: componente comum amplo do mercado;
- `group mode`: componentes localizados ou setoriais;
- `noise`: parte compativel com ruido amostral;
- `filtered`: reconstrucao usando os modos considerados informativos.

### Formulas essenciais da metodologia

Retorno logaritmico:

```text
r_{i,t} = log(P_adj_{i,t}) - log(P_adj_{i,t-1})
```

Padronizacao:

```text
tilde{r}_{i,t} = (r_{i,t} - mu_i) / sigma_i
```

Matriz de correlacao:

```text
C = (1 / (T - 1)) * R_tilde' * R_tilde
```

Distancia de Mantegna:

```text
d_ij = sqrt(2 * (1 - C_ij))
```

Fala curta:

> "A distancia de Mantegna transforma correlacao em distancia: correlacao alta vira distancia pequena. Isso permite usar a mesma geometria em clustering, MST e PMFG."

## 3. Stylized facts and correlation structure

### Figura 1: Stylized facts for PETR4, VALE3 and BBDC4

Arquivo: `images/figure_1d_stylized_facts_demo_assets_clean_2006_2025.pdf`.

Mostra:

- precos normalizados;
- retornos logaritmicos diarios;
- caudas da distribuicao de retornos absolutos;
- autocorrelacao dos retornos absolutos.

Fala sugerida:

> "A Figura 1 mostra por que faz sentido estudar volatilidade nesses ativos. Os retornos tem media pequena, mas apresentam caudas pesadas, eventos extremos e persistencia na magnitude dos retornos. A autocorrelacao dos retornos absolutos e evidencia de clustering de volatilidade."

Numeros para lembrar:

- PETR4: curtose excessiva `11.55`, pior retorno diario cerca de `-35.2%`;
- VALE3: curtose excessiva `7.51`;
- BBDC4: curtose excessiva `7.96`;
- PETR4 tem `41` dias com retorno absoluto maior que `10%`;
- VALE3 tem `26`;
- BBDC4 tem `16`.

Se perguntarem o que e clustering de volatilidade:

> "Retornos grandes tendem a aparecer perto de outros retornos grandes. O retorno em si pode nao ser muito autocorrelacionado, mas o tamanho do retorno e."

### Tabela: Descriptive statistics for the three demonstration assets

No artigo: `tab:descriptive_stats`.

Mostra:

- media;
- desvio padrao;
- assimetria;
- curtose;
- minimos e maximos;
- VaR empirico;
- autocorrelacao de retornos absolutos.

Fala sugerida:

> "Esta tabela coloca numeros nos fatos estilizados da figura anterior. Ela mostra que as medias sao proximas de zero, mas as curtoses sao altas e existem retornos extremos. Isso reforca a necessidade de modelos voltados para volatilidade e risco."

Cautela:

> "A tabela e descritiva. Ela justifica o problema, mas nao escolhe o modelo de previsao."

### Figura 2: Correlation structure in the core historical universe

Arquivos:

- `images/figure_2_correlation_histogram.pdf`;
- `images/figure_3_sector_correlation_distribution.pdf`.

Mostra:

- painel A: distribuicao de todas as correlacoes de Pearson entre pares de ativos;
- painel B: comparacao entre correlacoes dentro do mesmo setor e entre setores.

Fala sugerida:

> "Esta figura mostra a estrutura estatica de dependencia. No painel A, a distribuicao das correlacoes fica majoritariamente positiva, indicando um componente comum de mercado. No painel B, pares dentro do mesmo setor tendem a ter correlacoes maiores que pares de setores diferentes."

Numeros para lembrar:

- Total de pares: `58 * 57 / 2 = 1653`;
- media das correlacoes no universo: perto de `0.24`;
- pares dentro do setor: `275`;
- pares entre setores: `1378`;
- media within-sector: `0.3433`;
- media between-sector: `0.2249`.

Se perguntarem se isso prova causalidade setorial:

> "Nao prova causalidade. Mostra uma evidencia descritiva consistente com exposicoes setoriais comuns."

### Tabela: Within-sector and between-sector correlation summary

No artigo: `tab:sector_corr_summary`.

Mostra:

- media, mediana e dispersao das correlacoes por grupo;
- teste Mann-Whitney comparando within-sector e between-sector.

Fala sugerida:

> "A tabela confirma numericamente o que aparece no grafico. A media dentro do setor e maior que entre setores, e o teste Mann-Whitney indica uma diferenca muito forte."

Numero para lembrar:

- `p = 1.33389e-24`.

Cautela importante:

> "Os pares nao sao perfeitamente independentes, porque o mesmo ativo aparece em varios pares. Entao o p-valor deve ser lido como suporte descritivo forte, nao como inferencia perfeita."

### Figura 3: Rolling average market correlation

Arquivo: `images/figure_4_rolling_average_correlation.pdf`.

Mostra:

- correlacao media do mercado ao longo do tempo em janela movel.

Fala sugerida:

> "Esta figura mostra que a dependencia media do mercado varia no tempo. Em alguns periodos, os ativos ficam mais sincronizados, o que costuma acontecer em momentos de estresse ou choques comuns."

Mensagem principal:

- A correlacao nao e fixa.
- O mercado alterna periodos de maior e menor sincronizacao.

Cautela:

> "O grafico mostra picos de sincronizacao, mas nao identifica sozinho a causa de cada pico."

### Figura suplementar: Dynamic pairwise correlations

Arquivo: `images/figure_5_dynamic_pairwise_correlations.pdf`.

Mostra:

- correlacoes dinamicas para pares selecionados;
- estimativas de janela curta, janela longa e EWMA.

Fala sugerida:

> "Esta figura complementa a anterior mostrando que nao so a correlacao media do mercado varia; a dependencia entre pares especificos tambem muda bastante conforme a janela e o metodo de suavizacao."

Se perguntarem por que usar mais de uma janela:

> "Janelas curtas respondem mais rapido, mas sao mais ruidosas. Janelas longas sao mais estaveis, mas reagem mais devagar."

## 4. Random Matrix filtering

### Tabela: RMT summary for the core historical universe

No artigo: `tab:rmt_summary`.

Mostra:

- tamanho da amostra;
- razao `Q = T / N`;
- limites de Marcenko-Pastur;
- maior autovalor;
- numero de autovalores acima do limite superior.

Fala sugerida:

> "Esta tabela resume o benchmark de RMT. A pergunta e: se os retornos fossem essencialmente aleatorios e independentes, onde deveriam cair os autovalores da matriz de correlacao? Os autovalores fora da banda sao candidatos a sinal coletivo."

Numeros para lembrar:

- `N = 58`;
- `T = 1527`;
- `Q = 26.33`;
- `lambda_- = 0.6482`;
- `lambda_+ = 1.4278`;
- maior autovalor: `21.6505`;
- `5` autovalores acima de `lambda_+`.

### Figura 4: Empirical eigenvalue spectrum and Marcenko-Pastur bounds

Arquivo: `images/figure_6_rmt_eigenvalue_spectrum.pdf`.

Mostra:

- espectro empirico de autovalores;
- limites teoricos de Marcenko-Pastur;
- destaque do maior autovalor.

Fala sugerida:

> "Esta e uma das figuras centrais. A maior parte dos autovalores fica dentro ou perto da banda aleatoria, mas o primeiro autovalor esta muito acima do limite superior. Por isso ele e interpretado como modo de mercado. Alem dele, ha outros quatro autovalores acima da banda, interpretados como candidatos a modos de grupo ou setor."

Frase forte:

> "O primeiro autovalor e grande demais para ser explicado pelo benchmark aleatorio."

Se perguntarem se RMT prova estrutura economica:

> "RMT mostra que o autovalor esta fora do benchmark aleatorio. A interpretacao economica vem depois, olhando loadings, setores e redes."

### Tabela: RMT reconstruction diagnostics

No artigo: `tab:rmt_reconstruction`.

Mostra:

- diagnosticos da reconstrucao em componentes;
- separacao entre matriz original, market mode, group mode, noise e filtered.

Fala sugerida:

> "Esta tabela ajuda a verificar que a decomposicao espectral foi feita de forma consistente. O ponto nao e substituir a matriz original, mas separar camadas: mercado, grupos e ruido."

### Figura 5: Empirical and RMT-filtered matrix components

Arquivo: `images/figure_8_rmt_filtered_matrices.pdf`.

Mostra:

- matriz original;
- market mode;
- group/sector mode;
- noise;
- matriz filtered.

Fala sugerida:

> "Esta figura transforma a decomposicao espectral em algo visual. A matriz original mistura tudo. O market mode captura o co-movimento amplo. O group mode mostra estruturas mais locais. O noise mode e menos interpretavel. A matriz filtered tenta preservar os modos informativos."

Mensagem principal:

- O mercado tem uma camada comum forte.
- Ainda existe estrutura local depois de remover o modo de mercado.
- Essa estrutura local motiva clustering e redes.

Cautela:

> "A matriz filtrada depende do criterio escolhido, aqui o limite de Marcenko-Pastur."

### Figura 6: Top eigenvector loadings for leading RMT modes

Arquivo: `images/figure_7b_rmt_top_eigenvectors_top_loadings.pdf`.

Mostra:

- ativos com maiores loadings nos principais autovetores;
- interpretacao do primeiro modo e dos modos seguintes.

Fala sugerida:

> "Os autovalores dizem quais modos sao estatisticamente grandes. Os autovetores ajudam a interpretar quem participa de cada modo. O primeiro autovetor tende a ter loadings amplamente positivos, caracteristica de modo de mercado. Os modos seguintes podem destacar grupos de ativos ou setores."

Cautela:

> "O sinal do autovetor pode inverter sem mudar a interpretacao. O importante e o padrao relativo dos loadings."

## 5. Hierarchical clustering and ordered heatmaps

### Figura 7: Ordered heatmaps for original and RMT-filtered matrices

Arquivo: `images/figure_10_ordered_heatmaps.pdf`.

Mostra:

- heatmaps ordenados por clustering;
- comparacao entre matriz original e componentes filtrados.

Fala sugerida:

> "Os heatmaps ordenados ajudam a ver blocos de dependencia que podem ficar escondidos numa matriz sem ordenacao. Quando ativos similares ficam proximos, blocos de cor aparecem com mais clareza."

Mensagem principal:

- A estrutura nao e aleatoria;
- A ordenacao hierarquica revela blocos;
- A filtragem RMT ajuda a separar estrutura global e local.

### Tabela: Cophenetic correlations for hierarchical clustering

No artigo: `tab:cophenetic_summary`.

Mostra:

- quao bem o dendrograma preserva as distancias originais.

Numeros para lembrar:

- original: `0.9500`;
- filtered: `0.9340`;
- group mode: `0.8705`.

Fala sugerida:

> "A correlacao cofenetica mede o quanto a arvore representa bem as distancias originais. A matriz original e a filtrada sao mais tree-like. O group mode cai um pouco porque, ao remover o modo de mercado, a estrutura fica menos global e mais local."

Cautela:

> "Cophenetic menor no group mode nao significa ausencia de estrutura; significa que a estrutura ficou menos dominada por uma arvore global."

### Figura 8: Dendrogram comparison

Arquivo: `images/figure_9_dendrograms_comparison.pdf`.

Mostra:

- dendrogramas para matriz original, filtered e group mode;
- agrupamentos hierarquicos construidos com distancia de Mantegna.

Fala sugerida:

> "O dendrograma e a versao em arvore das dependencias. Ele mostra como ativos vao se agrupando a partir das distancias. A comparacao entre original, filtered e group mode mostra como a estrutura muda quando removemos o componente comum de mercado."

Se perguntarem por que usar dendrograma e redes:

> "O dendrograma mostra hierarquia. As redes mostram topologia: hubs, ciclos, clustering e conexoes locais."

## 6. Financial network topology

### Figura 9: Refined MST comparison

Arquivo: `images/figure_11b_mst_refined_comparison.pdf`.

Mostra:

- MST da matriz original;
- MST da matriz group mode;
- cores por setor;
- tamanho dos nos por centralidade.

Fala sugerida:

> "A MST e o esqueleto minimo de dependencias fortes. Com 58 ativos, ela tem 57 arestas. A comparacao entre original e group mode mostra como o backbone muda quando o modo de mercado e removido."

Numeros para lembrar:

- MST tem `N - 1 = 57` arestas;
- MST original: correlacao media `0.5796`, same-sector ratio `0.7193`;
- MST group mode: correlacao media `0.1388`, same-sector ratio `0.6316`.

Cautela:

> "A MST e muito esparsa. Ela e boa para ver backbone, mas descarta muitos ciclos e conexoes locais."

### Figura 10: Refined PMFG comparison

Arquivo: `images/figure_12b_pmfg_refined_comparison.pdf`.

Mostra:

- PMFG da matriz original;
- PMFG da matriz group mode;
- conexoes mais ricas que na MST;
- comunidades e hubs locais.

Fala sugerida:

> "A PMFG e a rede principal do artigo porque preserva mais estrutura que a MST. Com 58 ativos, ela tem 168 arestas. No painel original, ainda vemos forte influencia do modo de mercado. No group mode, as correlacoes medias caem, mas aparecem estruturas mais locais."

Numeros para lembrar:

- PMFG tem `3N - 6 = 168` arestas;
- PMFG original: correlacao media `0.5177`, clustering `0.5273`;
- PMFG group mode: correlacao media `0.1109`, clustering `0.6653`.

Frase forte:

> "Menor correlacao media no group mode nao significa menos estrutura; significa menos componente comum. O aumento do clustering sugere organizacao local mais forte."

Se perguntarem por que essa figura e bonita/importante:

> "Porque ela mostra visualmente a passagem de uma rede dominada pelo mercado para uma rede com canais locais de dependencia."

### Tabela: Selected MST and PMFG topology statistics

No artigo: `tab:network_summary`.

Mostra:

- numero de arestas;
- correlacao media;
- proporcao same-sector;
- clustering;
- principais hubs.

Fala sugerida:

> "Esta tabela da base quantitativa para a leitura das redes. Ela confirma que a remocao do market mode reduz a forca media das arestas, mas preserva organizacao setorial e aumenta clustering na PMFG group mode."

Cautela:

> "Nao devemos comparar so a correlacao media. Em redes filtradas, tambem importam clustering, hubs, proporcao setorial e cliques."

### Tabela: PMFG clique and planarity diagnostics

No artigo: `tab:pmfg_cliques`.

Mostra:

- diagnosticos de construcao da PMFG;
- triangulos e 4-cliques;
- validacao de que a rede tem a topologia esperada.

Fala sugerida:

> "Esta tabela e um check tecnico importante. A PMFG deve ter 3N-6 arestas e preserva triangulos e 4-cliques. Esses ciclos sao justamente o que permite estudar estrutura local melhor que a MST."

Numeros para lembrar:

- com `N = 58`, PMFG tem `168` arestas;
- PMFG tem `166` triangulos;
- PMFG tem `55` 4-cliques.

### Figura 11: Network structure comparison

Arquivo: `images/figure_13_network_topology_comparison.pdf`.

Mostra:

- comparacao de metricas entre MST e PMFG;
- matrizes original, filtered e group mode.

Fala sugerida:

> "Esta figura resume metricas topologicas. Ela mostra que MST e PMFG respondem de formas diferentes a filtragem. A MST e sempre uma arvore, entao nao tem clustering. A PMFG preserva ciclos e por isso permite analisar clustering e comunidades locais."

Mensagem principal:

- PMFG e mais informativa para estrutura local;
- MST e mais simples e interpretavel como backbone;
- group mode tem menor peso medio, mas nao perde organizacao.

### Figura 12: Hub-rank comparison

Arquivo: `images/figure_14_network_hub_rank_comparison.pdf`.

Mostra:

- mudanca de ranking de hubs entre original e group mode;
- comparacao de centralidades.

Fala sugerida:

> "Esta figura mostra que os ativos centrais dependem do filtro usado. Quando removemos o modo de mercado, alguns hubs deixam de ser dominantes e outros ativos aparecem como pontes ou centros locais."

Exemplos para lembrar:

- PMFG original: BBDC4 aparece como top degree, GGBR4 como top betweenness;
- PMFG group mode: GUAR3 aparece como hub importante.

Cautela:

> "Hub na rede nao significa necessariamente empresa mais importante economicamente. Significa centralidade dentro da rede estimada."

## 7. Aggregated subsector dependency network

### Tabela: Aggregated subsector network summary

No artigo: `tab:subsector_summary`.

Mostra:

- numero de subsetores;
- numero de arestas;
- densidade;
- dependencia media;
- subsetores mais centrais.

Fala sugerida:

> "Depois das redes em nivel de ativo, esta secao agrega a informacao por subsetor. A ideia e traduzir a topologia para uma linguagem economica mais direta: quais subsetores se conectam mais e quais funcionam como pontes."

Numeros para lembrar:

- `22` subsetores;
- `66` arestas;
- densidade `0.2857`;
- dependencia media `0.0566`;
- top degree: Retail;
- top betweenness: Electric Utility;
- top weighted degree: Apparel and Footwear.

### Figura 13: Aggregated subsector dependency network

Arquivo oficial: `images/figure_15_subsector_dependency_network.pdf`.

Mostra:

- nos como subsetores;
- cor do no por macro-setor;
- tamanho por numero de ativos no subsetor;
- arestas por dependencia media retida.

Fala sugerida:

> "Esta figura e uma leitura agregada. Em vez de olhar cada ativo, olhamos subsetores. Isso ajuda a interpretar a rede em linguagem economica: por exemplo, varejo, utilities, materiais basicos e financeiro aparecem conectados de formas diferentes."

Mensagem principal:

- A rede agregada facilita interpretacao economica;
- Ela e mais resumida que a PMFG;
- Ela nao substitui a rede de ativos, mas ajuda a contar a historia.

Cautela:

> "Como a agregacao reduz a granularidade, ela melhora interpretabilidade, mas perde detalhes de ativo individual."

### Figura alternativa recomendada: PMFG cluster-sector decomposition

Arquivo novo:

- `outputs/figures/vector/figure_15b_pmfg_cluster_sector_decomposition.pdf`;
- `outputs/figures/preview/figure_15b_pmfg_cluster_sector_decomposition.png`.

Quando usar:

- se voce quiser uma figura visualmente mais forte para apresentacao;
- se quiser mostrar clusters numerados e composicao setorial de cada cluster;
- se os professores perguntarem sobre comunidades/setores dentro da PMFG.

Fala sugerida:

> "Esta figura alternativa mostra a PMFG group-mode de forma clusterizada. A parte superior mostra comunidades de ativos na rede; a parte inferior mostra a composicao setorial de cada cluster. Assim, consigo conectar a topologia da rede com a interpretacao economica por setor."

Mensagem principal:

- Clusters de rede nao sao necessariamente setores puros;
- Alguns clusters sao setorialmente concentrados;
- Outros misturam setores, sugerindo dependencia transversal.

Cautela:

> "Esta figura e uma visualizacao complementar. Ela depende do algoritmo de comunidade e do layout, entao deve ser usada como apoio interpretativo, nao como prova isolada."

## 8. Volatility forecasting

### Figura 14: Volatility forecasting comparison

Arquivo: `images/figure_16_volatility_forecast_model_comparison.pdf`.

Mostra:

- comparacao de modelos;
- horizontes de 5 e 20 dias;
- metrica QLIKE;
- feature set selecionado por validacao.

Fala sugerida:

> "Esta figura testa se a estrutura RMT/rede tem conteudo preditivo. Os modelos usam tres conjuntos de features: Set A com variaveis classicas, Set B adicionando mercado/RMT e Set C adicionando MST/PMFG. A metrica principal aqui e QLIKE, em que menor e melhor."

Numeros para lembrar:

- 5 dias: Random Forest + Set C tem melhor QLIKE, `-5.2508`;
- 20 dias: Ridge + Set C tem melhor QLIKE, `-3.8812`;
- CNN-1D e competitivo em 20 dias por MAE/RMSE e `R2_oos`.

Mensagem principal:

> "As features de rede ajudam de forma incremental, mas nao dominam universalmente."

Se perguntarem por que QLIKE:

> "Porque volatilidade realizada e uma proxy imperfeita da variancia latente. QLIKE e uma metrica comum para previsao de volatilidade e penaliza erros na variancia prevista."

### Tabela: Aggregated test-set forecasting comparison

No artigo: `tab:forecast_comparison`.

Mostra:

- MAE;
- RMSE;
- QLIKE;
- `R2_oos`;
- resultados agregados de PETR4, VALE3 e BBDC4.

Fala sugerida:

> "A tabela complementa a figura porque mostra varias metricas. O ranking por QLIKE nao e sempre igual ao ranking por MAE ou RMSE. Isso acontece porque cada metrica penaliza erros de forma diferente."

Numeros para lembrar:

- 5 dias, Random Forest Set C: MAE `0.0161`, RMSE `0.0227`, QLIKE `-5.2508`;
- 5 dias, Ridge Set C: RMSE melhor que RF, `0.0214`, mas QLIKE um pouco pior;
- 20 dias, Ridge Set C: QLIKE `-3.8812`;
- 20 dias, CNN-1D: RMSE `0.0306`, competitivo com Ridge.

Cautela:

> "A conclusao nao e que machine learning sempre vence. A conclusao e que redes e RMT podem adicionar informacao complementar em alguns modelos e horizontes."

### Figura 15: Realized versus predicted volatility

Arquivo: `images/figure_17_realized_vs_predicted_volatility.pdf`.

Mostra:

- volatilidade realizada;
- volatilidade prevista;
- separacao visual entre treino/validacao/teste;
- periodo de teste a partir de 2021.

Fala sugerida:

> "Esta figura verifica se as previsoes acompanham visualmente os regimes de volatilidade. Os modelos conseguem seguir parte das mudancas de nivel, mas choques extremos continuam dificeis de prever."

Mensagem principal:

- Modelos capturam regimes;
- Picos extremos sao dificeis;
- Isso e esperado em previsao de volatilidade.

Cautela:

> "Errar picos extremos nao invalida o modelo, mas afeta metricas como RMSE e QLIKE."

### Figura 16: Feature importance for Random Forest

Arquivo: `images/figure_18_ml_feature_importance.pdf`.

Mostra:

- importancia das features no Random Forest;
- comparacao entre horizontes;
- papel das variaveis classicas e de rede.

Fala sugerida:

> "Esta figura ajuda a interpretar o mecanismo dos modelos. As features tradicionais de volatilidade dominam, como rolling absolute return, realized volatility defasada, rolling volatility e EWMA. Mas algumas features de rede aparecem com importancia nao nula, o que sustenta a ideia de contribuicao incremental."

Mensagem principal:

- Variaveis classicas continuam dominando;
- PMFG/MST entram como sinal complementar;
- Importancia nao e causalidade.

Cautela:

> "Feature importance de Random Forest pode ser afetada por correlacao entre variaveis. Ela e uma verificacao do modelo, nao uma prova causal."

## 9. Discussion

Fala sugerida:

> "A discussao junta as tres partes do artigo. Primeiro, a B3 tem um modo de mercado dominante. Segundo, depois da filtragem, ainda existem estruturas locais e setoriais. Terceiro, essas estruturas podem ser transformadas em features que adicionam algum sinal para previsao de volatilidade."

Mensagem principal:

- RMT ajuda a separar camadas da matriz;
- PMFG ajuda a interpretar topologia local;
- Previsao mostra valor incremental, nao dominancia absoluta.

Frase pronta:

> "O resultado mais importante nao e que redes vencem sempre, mas que a geometria cross-sectional do mercado contem informacao que nao e totalmente redundante com as features classicas de volatilidade."

## 10. Limitations

Fala sugerida:

> "As limitacoes principais sao importantes para nao vender o resultado alem do que ele mostra. A previsao ainda usa tres ativos-alvo, algumas features de rede sao estaticas ou lentamente variantes, e um desenho totalmente real-time exigiria recalcular RMT e redes em janelas rolling."

Limitacoes para mencionar espontaneamente:

- apenas PETR4, VALE3 e BBDC4 como alvos iniciais;
- classificacao setorial e uma aproximacao;
- features de rede parcialmente estaticas;
- possivel extensao para janelas rolling;
- extensao futura para DCC-GARCH, GNNs e mais ativos.

Se perguntarem se ha look-ahead bias:

> "A divisao treino-validacao-teste e temporal, o que reduz look-ahead. Mas para uma previsao totalmente real-time seria melhor recalcular RMT e redes de forma rolling ou recursiva."

## 11. Conclusion

Fala sugerida:

> "A conclusao e que a matriz de correlacao da B3 tem camadas: um modo de mercado muito forte, modos de grupo e uma parte compativel com ruido. A filtragem por RMT e as redes PMFG/MST ajudam a interpretar essa estrutura. Na previsao, as features de rede nao substituem as variaveis classicas de volatilidade, mas aparecem como informacao complementar."

Fechamento de 30 segundos:

> "Em resumo, o artigo mostra que a B3 pode ser analisada como uma rede financeira filtrada por RMT. O maior autovalor revela um modo de mercado dominante, mas ao remover esse componente ainda aparecem estruturas locais. A PMFG e especialmente util porque preserva ciclos e comunidades. Quando essas informacoes viram features, elas geram ganhos modestos e dependentes do modelo, mas indicam que a topologia do mercado contem sinal adicional para risco e volatilidade."

## 12. Sequencia recomendada de slides

Se voce for montar slides, uma sequencia eficiente seria:

1. Problema e pergunta de pesquisa.
2. Dados e amostras.
3. Pipeline metodologico.
4. Fatos estilizados dos 3 ativos.
5. Correlacoes: histograma e setores.
6. RMT: espectro de autovalores.
7. RMT: matrizes decompostas.
8. Clustering: heatmaps/dendrogramas.
9. MST e PMFG.
10. PMFG refinada original vs group mode.
11. Rede agregada por subsetor ou `figure_15b` alternativa.
12. Previsao: comparacao de modelos.
13. Realizado vs previsto.
14. Feature importance.
15. Limitacoes e conclusao.

## 13. Perguntas provaveis dos professores

### "Qual e a contribuicao principal?"

> "Integrar RMT, redes financeiras filtradas e previsao de volatilidade para a B3 em um workflow reprodutivel."

### "Por que RMT?"

> "Porque a matriz empirica mistura sinal e ruido. A RMT oferece um benchmark para separar autovalores compativeis com ruido daqueles que sugerem modos coletivos."

### "Por que PMFG e nao apenas MST?"

> "A MST mostra o backbone minimo, mas nao tem ciclos. A PMFG preserva mais estrutura, incluindo triangulos e cliques, entao e melhor para estudar comunidades locais e hubs."

### "Por que a correlacao cai no group mode?"

> "Porque o modo de mercado foi removido. A queda da correlacao media e esperada; o interesse e observar se sobra estrutura local."

### "As redes melhoram a previsao?"

> "Elas ajudam de forma incremental em alguns modelos e horizontes. Nao substituem features classicas de volatilidade."

### "Qual e o ponto mais fraco?"

> "A previsao ainda e inicial: poucos ativos-alvo e features de rede parcialmente estaticas. A extensao natural e usar redes rolling e ampliar os ativos."

## 14. Mini-roteiro final para falar sem olhar

> "O artigo comeca documentando fatos estilizados e correlacoes da B3. Depois, usa RMT para separar a matriz de correlacao em modo de mercado, modos de grupo e ruido. O maior autovalor e muito acima do limite de Marcenko-Pastur, indicando um modo de mercado dominante. Ao remover esse modo, as redes MST e principalmente PMFG mostram estruturas mais locais e setoriais. A rede agregada por subsetor traduz essa topologia em linguagem economica. Por fim, o artigo testa se essas informacoes ajudam a prever volatilidade para PETR4, VALE3 e BBDC4. O resultado e complementar: features classicas continuam dominando, mas variaveis de rede adicionam sinal modesto em alguns modelos e horizontes."

