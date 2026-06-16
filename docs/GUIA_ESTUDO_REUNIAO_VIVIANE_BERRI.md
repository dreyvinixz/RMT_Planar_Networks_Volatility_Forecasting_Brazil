# Guia de estudo para reuniao com Viviane e Berri

Base: artigo `Random Matrix Filtering and Planar Financial Networks for Volatility Forecasting in the Brazilian Stock Market`, versao `article/overleaf_viviane_revision`.

## 1. Resumo que voce deve saber falar em 1 minuto

O artigo analisa a estrutura de dependencia de acoes brasileiras da B3 usando uma abordagem de econofisica. A ideia central e que a matriz de correlacao dos retornos contem tres camadas: um modo de mercado dominante, modos setoriais ou de grupo e uma parte compativel com ruido amostral. Para separar essas camadas, o artigo usa Random Matrix Theory (RMT), depois transforma as matrizes original e filtradas em redes financeiras MST e PMFG. Por fim, testa se variaveis extraidas dessa estrutura ajudam a prever volatilidade realizada para PETR4, VALE3 e BBDC4.

Resultado principal: a estrutura de mercado da B3 tem um componente comum muito forte, mas tambem preserva padroes locais/setoriais. As redes filtradas por RMT ajudam a interpretar essa organizacao e as features de rede adicionam informacao modesta, mas nao dominante, para previsao de volatilidade.

## 2. Pergunta de pesquisa

A pergunta pode ser formulada assim:

> A estrutura de dependencia entre ativos da B3, depois de separar ruido, modo de mercado e componentes setoriais por RMT, contem informacao util para interpretar o mercado e melhorar previsoes de volatilidade?

Nao e um artigo apenas de previsao. O eixo e: dependencia -> filtragem espectral -> redes -> features -> previsao.

## 3. Dados e amostra

- Fonte: BovDB/BovDBv2, precos diarios ajustados da B3.
- Periodo amplo: 1998-2025 para o universo historico.
- Universo principal: 58 ativos.
- Painel sincronizado para RMT/redes: `N = 58` ativos e `T = 1527` observacoes comuns.
- Ativos demonstrativos e alvos de previsao: PETR4, VALE3 e BBDC4.
- Periodo desses ativos na tabela descritiva: 2006-2025, com `n = 4953` observacoes.

Justificativa da sincronizacao: para RMT, clustering, MST e PMFG, todos precisam vir de uma unica matriz de correlacao consistente. Se cada par usasse datas diferentes, os autovalores, autovetores e distancias poderiam refletir mudancas de amostra, nao estrutura real.

## 4. Matematica essencial

### Retornos logaritmicos

Formula:

```text
r_{i,t} = log(P_adj_{i,t}) - log(P_adj_{i,t-1})
```

Por que usar log-retornos:

- sao aproximadamente retornos percentuais para variacoes pequenas;
- sao aditivos no tempo;
- sao padrao em series financeiras;
- reduzem problemas de escala entre ativos.

### Padronizacao

Formula:

```text
tilde{r}_{i,t} = (r_{i,t} - mu_i) / sigma_i
```

Ideia: tirar media e dividir pelo desvio padrao de cada ativo. Assim a matriz de correlacao mede co-movimento, nao diferencas de volatilidade absoluta entre ativos.

### Matriz de correlacao

Formula:

```text
C = (1 / (T - 1)) * R_tilde' * R_tilde
```

Onde:

- `C` e `N x N`;
- diagonal igual a 1;
- `C_ij` e a correlacao de Pearson entre ativos `i` e `j`.

No artigo, a media das correlacoes fica perto de `0.24`, indicando co-movimento positivo moderado no mercado.

### RMT e Marcenko-Pastur

A RMT compara os autovalores da matriz empirica com o que seria esperado se as series fossem independentes e aleatorias.

Formula dos limites:

```text
lambda_+/- = 1 + 1/Q +/- 2 * sqrt(1/Q)
Q = T / N
```

No artigo:

- `N = 58`
- `T = 1527`
- `Q = 26.33`
- `lambda_- = 0.6482`
- `lambda_+ = 1.4278`

Interpretacao:

- autovalores dentro de `[lambda_-, lambda_+]`: compativeis com ruido amostral;
- autovalores acima de `lambda_+`: candidatos a modos coletivos reais;
- maior autovalor: modo de mercado.

Resultados:

- `lambda_1 = 21.6505`
- `lambda_2 = 3.0957`
- `lambda_3 = 1.7839`
- `lambda_4 = 1.6543`
- `lambda_5 = 1.4835`
- 5 autovalores acima de `lambda_+`
- o primeiro autovalor explica cerca de `37.3%` do traco da matriz.

Como explicar: "O primeiro modo e tao grande que nao pode ser explicado pelo benchmark aleatorio. Ele representa uma sincronizacao ampla do mercado. Os quatro seguintes sugerem estruturas de grupo, setor ou dependencia localizada."

### Decomposicao espectral

Formula:

```text
C = soma_k lambda_k u_k u_k'
```

Componentes:

```text
C_market = lambda_1 u_1 u_1'
C_group = soma_{k=2 ate K} lambda_k u_k u_k'
C_filtered = soma_{k=1 ate K} lambda_k u_k u_k'
C_noise = soma_{k=K+1 ate N} lambda_k u_k u_k'
```

Onde `K = 5`, pois ha 5 autovalores acima de `lambda_+`.

Ponto importante: uma reconstrucao parcial pode nao preservar diagonal exatamente igual a 1, entao a matriz filtrada e reescalada quando precisa ser usada como matriz de correlacao.

### Distancia de Mantegna

Formula:

```text
d_ij = sqrt(2 * (1 - C_ij))
```

Interpretacao:

- correlacao alta -> distancia pequena;
- correlacao baixa -> distancia maior;
- usada para clustering, MST e PMFG.

### MST

Minimum Spanning Tree:

- rede conectada mais esparsa;
- minimiza a soma das distancias;
- nao tem ciclos;
- com `N = 58`, tem `N - 1 = 57` arestas.

Boa frase: "A MST mostra o esqueleto minimo de dependencias fortes."

### PMFG

Planar Maximally Filtered Graph:

- rede planar mais rica;
- preserva mais conexoes que a MST;
- com `N = 58`, tem `3N - 6 = 168` arestas;
- permite triangulos e 4-cliques;
- contem a MST quando usa a mesma ordenacao de distancias.

Boa frase: "A PMFG e menos agressiva que a MST; ela preserva estrutura local, ciclos e agrupamentos."

### Volatilidade realizada

Formula:

```text
RV_{i,t,h} = sqrt( soma_{tau=1 ate h} r_{i,t+tau}^2 )
```

Horizontes:

- `h = 5` dias;
- `h = 20` dias.

Divisao temporal:

- treino: 2006-2017;
- validacao: 2018-2020;
- teste: 2021-2025.

Essa divisao reduz look-ahead bias porque o teste ocorre depois do treino e da validacao.

### QLIKE

Formula:

```text
QLIKE_t = log(sigma_hat_t^2) + sigma_t^2 / sigma_hat_t^2
```

Menor QLIKE e melhor. Ele e usado porque e comum em comparacao de previsao de volatilidade quando a volatilidade realizada e uma proxy imperfeita da variancia latente.

## 5. Estatistica essencial

### Fatos estilizados

PETR4, VALE3 e BBDC4 mostram:

- medias proximas de zero;
- caudas pesadas;
- curtose excessiva alta;
- eventos extremos;
- autocorrelacao positiva dos retornos absolutos.

Numeros principais:

- BBDC4: curtose excessiva `7.96`, ACF absoluta lag 1 `0.207`.
- PETR4: curtose excessiva `11.55`, pior retorno diario `-0.3524`, 41 dias com `|r| > 10%`.
- VALE3: curtose excessiva `7.51`, ACF absoluta lag 60 `0.119`.

Como explicar: "Retornos em si nao sao muito autocorrelacionados, mas a magnitude dos retornos e. Isso e clustering de volatilidade: choques grandes tendem a vir perto de outros choques grandes."

### Correlacao setorial

Total de pares no universo de 58 ativos:

```text
N(N - 1)/2 = 58 * 57 / 2 = 1653
```

Resultados:

- pares dentro do mesmo setor: 275;
- pares entre setores: 1378;
- media dentro do setor: `0.3433`;
- media entre setores: `0.2249`;
- teste Mann-Whitney unilateral: `p = 1.33389e-24`.

Como explicar com cautela: "O teste mostra uma diferenca muito forte, mas os pares nao sao perfeitamente independentes porque um mesmo ativo aparece em varios pares. Entao o p-valor deve ser lido como suporte descritivo, nao como inferencia perfeita."

### Clustering hierarquico

Cophenetic correlations:

- matriz original: `0.9500`;
- matriz filtrada: `0.9340`;
- group mode: `0.8705`.

Interpretacao: o group mode e menos "arvore-like" porque o modo de mercado foi removido. Isso nao significa ausencia de estrutura; significa que a estrutura fica mais local e menos dominada por um componente comum.

### Redes

MST:

- original: 57 arestas, correlacao media `0.5796`, same-sector ratio `0.7193`;
- group mode: 57 arestas, correlacao media `0.1388`, same-sector ratio `0.6316`.

PMFG:

- original: 168 arestas, correlacao media `0.5177`, clustering `0.5273`;
- group mode: 168 arestas, correlacao media `0.1109`, clustering `0.6653`.

Frase-chave: "Ao remover o modo de mercado, as correlacoes medias caem, mas a PMFG fica mais localmente agrupada. Menor peso medio nao quer dizer menos estrutura; quer dizer menos componente comum."

### Subsetores

Rede agregada:

- 22 subsetores;
- 66 arestas;
- densidade `0.2857`;
- dependencia media `0.0566`;
- top degree: Retail;
- top betweenness: Electric Utility;
- top weighted degree: Apparel and Footwear.

## 6. Previsao de volatilidade

Feature sets:

- Set A: features classicas de retorno e volatilidade.
- Set B: Set A + mercado/RMT.
- Set C: Set B + MST/PMFG/network.

Resultados no teste 2021-2025:

5 dias:

- melhor QLIKE: Random Forest + Set C, `QLIKE = -5.2508`;
- Ridge + Set C teve melhor RMSE que Random Forest, mas QLIKE um pouco pior;
- MLP e CNN tiveram bons MAE/RMSE, mas nao dominaram em QLIKE.

20 dias:

- melhor QLIKE: Ridge + Set C, `QLIKE = -3.8812`;
- CNN-1D foi competitivo em MAE, RMSE e `R^2_oos`;
- MLP ficou bom em MAE/RMSE, mas fraco em QLIKE.

Interpretacao correta:

> As features de rede ajudam de forma incremental. Elas nao substituem volatilidade defasada, EWMA, rolling volatility e realized volatility lagged. A contribuicao e complementar e depende do horizonte, modelo e metrica.

## 7. Perguntas provaveis e respostas

### 1. Qual e a contribuicao principal do artigo?

Contribuicao: integrar RMT, redes financeiras filtradas e previsao de volatilidade para a B3 em um workflow reprodutivel. O artigo nao apenas estima correlacoes; ele separa componentes de mercado, grupo e ruido, constroi MST/PMFG e testa se essa estrutura tem valor preditivo.

### 2. Por que usar RMT?

Porque a matriz de correlacao empirica mistura sinal e ruido. A RMT fornece um benchmark teorico: se os ativos fossem independentes, os autovalores deveriam cair dentro da banda de Marcenko-Pastur. Autovalores acima da banda indicam modos coletivos candidatos a estrutura real.

### 3. O que significa o maior autovalor?

O maior autovalor representa o modo de mercado. No artigo, `lambda_1 = 21.6505`, explicando cerca de `37.3%` do traco. Como o autovetor correspondente tem loadings amplamente positivos, ele indica co-movimento generalizado do mercado.

### 4. Por que remover o modo de mercado?

Porque ele domina a matriz original. Se a rede for construida diretamente da matriz original, muitas arestas podem refletir apenas co-movimento comum. Remover o modo de mercado permite observar dependencias mais locais, setoriais ou de grupo.

### 5. Se a correlacao media do group mode cai, por que ele ainda e util?

Porque menor correlacao media nao significa ausencia de estrutura. O group mode remove o componente comum amplo; as dependencias restantes sao mais fracas em magnitude, mas podem ser mais informativas sobre organizacao local. Isso aparece no PMFG: clustering sobe de `0.5273` para `0.6653`.

### 6. Por que MST e PMFG? Nao bastava uma matriz de correlacao?

A matriz mostra todos os pares, mas e dificil interpretar. A MST extrai o backbone minimo de conexoes fortes. A PMFG preserva mais estrutura, incluindo ciclos, triangulos e 4-cliques, permitindo estudar hubs, clustering e organizacao local.

### 7. Qual e a diferenca entre MST e PMFG?

MST tem `N - 1` arestas e e uma arvore, portanto nao tem ciclos. PMFG tem `3N - 6` arestas e preserva planariadade, entao e mais rica. Para `N = 58`, MST tem 57 arestas e PMFG tem 168.

### 8. Por que usar correlacao de Pearson? E Spearman?

Pearson e padrao para RMT, PCA, matriz de correlacao e distancia de Mantegna. Spearman pode ser uma extensao robusta para relacoes monotonicamente nao lineares, mas o framework espectral tradicional usa Pearson sobre retornos padronizados. No roadmap, Spearman aparece como extensao pendente.

### 9. O teste Mann-Whitney e valido se os pares nao sao independentes?

Com cautela. Os pares se sobrepoem porque cada ativo participa de varios pares, entao a independencia estrita e violada. Por isso o artigo interpreta o teste como evidência descritiva forte de deslocamento entre distribuicoes, nao como inferencia causal perfeita.

### 10. Ha look-ahead bias na previsao?

A divisao treino-validacao-teste e temporal, o que reduz look-ahead bias. Porem, o proprio artigo reconhece uma limitacao: algumas features RMT/rede sao estaticas ou lentamente variantes. Para um desenho totalmente real-time, seria necessario recalcular RMT e redes de forma rolling/recursiva usando apenas informacao disponivel em cada origem de previsao.

### 11. Por que PETR4, VALE3 e BBDC4?

Porque sao ativos liquidos, economicamente importantes e de setores distintos: petroleo/energia, mineracao/materiais basicos e financeiro. Eles sao bons alvos iniciais e exemplos interpretaveis, mas nao representam todo o mercado.

### 12. O que as redes acrescentam para previsao?

Elas acrescentam informacao estrutural da geometria cross-sectional do mercado. Na feature importance, variaveis classicas de volatilidade dominam, mas algumas features PMFG entram com importancia nao nula. O ganho e incremental, nao revolucionario.

### 13. Por que usar QLIKE?

Porque volatilidade realizada e uma proxy imperfeita da variancia latente. QLIKE e uma metrica comum em previsao de volatilidade e e sensivel a erros na variancia prevista. No artigo, menor QLIKE e melhor.

### 14. Por que os modelos com menor MAE/RMSE nem sempre vencem em QLIKE?

MAE/RMSE medem erro na escala da volatilidade. QLIKE avalia erro em termos de variancia e penaliza previsoes ruins de forma diferente, especialmente sub/superestimacao de variancia. Por isso rankings podem divergir.

### 15. Qual e o ponto fraco mais importante do artigo?

O ponto mais forte para reconhecer honestamente e que a previsao ainda e inicial: poucos ativos-alvo, features de rede em parte estaticas e arquiteturas neurais simples. A extensao natural e usar RMT/redes rolling, ampliar os ativos e testar modelos temporais ou GNNs.

## 8. Frases prontas para responder com clareza

- "O artigo trata a matriz de correlacao como um objeto com camadas: mercado, grupos/setores e ruido."
- "A RMT nao prova causalidade economica; ela separa modos estatisticamente fora do benchmark aleatorio."
- "O primeiro autovalor e interpretado como modo de mercado porque e muito maior que o limite de Marcenko-Pastur e tem loadings amplamente positivos."
- "A PMFG e preferida para analisar estrutura local porque preserva ciclos e cliques, enquanto a MST e apenas o esqueleto minimo."
- "As features de rede nao substituem features tradicionais de volatilidade; elas adicionam informacao estrutural complementar."
- "A previsao e conservadora: treino, validacao e teste seguem ordem temporal."
- "A principal limitacao e que um desenho totalmente em tempo real exigiria recalcular RMT e redes em janelas rolling."

## 9. Checklist de dominio antes da reuniao

Voce deve conseguir explicar sem olhar:

- o que e retorno logaritmico;
- por que usar preco ajustado;
- por que sincronizar o painel;
- como a matriz de correlacao e calculada;
- o que e Marcenko-Pastur;
- por que `lambda_1` e modo de mercado;
- diferenca entre market mode, group mode, filtered e noise;
- o que a distancia de Mantegna faz;
- diferenca entre MST e PMFG;
- por que a PMFG tem 168 arestas com 58 ativos;
- o que significa clustering maior no group-mode PMFG;
- como a volatilidade realizada e definida;
- por que QLIKE e usado;
- quais sao as limitacoes honestas.

## 10. Mini-roteiro para sua fala inicial

"A ideia do artigo e analisar a B3 como um sistema complexo. Comecamos com precos ajustados, calculamos retornos logaritmicos e construimos uma matriz de correlacao para 58 ativos em um painel sincronizado. A RMT mostra que cinco autovalores ficam acima do limite de Marcenko-Pastur, com um modo de mercado muito forte explicando cerca de 37% do traco. Ao remover esse modo, conseguimos observar estruturas mais locais por meio de clustering, MST e principalmente PMFG. Depois usamos essas medidas como features em previsao de volatilidade para PETR4, VALE3 e BBDC4. O resultado e que as variaveis tradicionais de volatilidade continuam dominando, mas features de rede adicionam sinal incremental, especialmente em alguns modelos e horizontes."
