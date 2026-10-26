# Pacote de revisao do manuscrito

Este pacote organiza as revisoes de tres professores para a versao submetida do artigo sobre redes filtradas por RMT e avaliacao retrospectiva de volatilidade.

## Versao de referencia

- Arquivo: `reference/_Andrey___Preprint_submitted_to_Elsevier___RMT_filtered_networks__retrospective_volatility_assessment.zip`
- SHA-256: `fe40fa80c4ca4bc1d94a0d686971e81ff14a1d52992d9fbb88182b423a6f6f08`
- Integridade do ZIP verificada em 2026-10-26; 65 arquivos, incluindo `main.tex` e figuras.
- O ZIP de referencia nao contem PDF compilado do manuscrito.

O arquivo de referencia e uma copia byte a byte do ZIP indicado. Nao edite essa copia; use-a para localizar a versao exata comentada. As respostas e alteracoes devem ser feitas no workspace do artigo, mantendo o historico de cada decisao.

## Revisores

- `reviewer_1/`
- `reviewer_2/`
- `reviewer_3/`

Para cada professor, guarde a revisao recebida em `REVIEW_RECEIVED.md` ou em seu formato original dentro da pasta correspondente. Depois registre os pontos no `RESPONSE_LOG.md`, um item por comentario. Nao descarte comentarios repetidos: relacione-os entre revisores.

## Fluxo de analise

1. Trabalhar com um revisor por vez, preservando o texto recebido.
2. Separar cada observacao em: comentario, interpretacao, acao proposta, decisao, mudanca realizada e evidencia.
3. Classificar a decisao como `aceitar`, `aceitar parcialmente`, `nao aceitar (justificar)` ou `esclarecer com o revisor`.
4. Registrar secao/figura/tabela e localizacao na versao revisada; atualizar `MASTER_TRACKER.csv`.
5. Manter respostas factuais e respeitosas. Nao afirmar que uma analise, citacao ou verificacao foi feita ate que exista evidencia.
6. Ao concluir cada rodada, revisar consistencia entre manuscrito, respostas e tracker antes de iniciar o proximo revisor.

## Arquivos

- `MASTER_TRACKER.csv`: acompanhamento consolidado dos comentarios dos tres revisores.
- Cada pasta de revisor contem um registro de respostas e um modelo para preservar a revisao recebida.

## Estado da nova comparacao — 2026-10-26

As tres revisoes foram relidas e comparadas com o ZIP canonico revisado. O detalhamento item a item esta em `MASTER_TRACKER.csv` e nos `RESPONSE_LOG.md` por professor. O usuario autorizou os ajustes pendentes/parciais, com excecao de Related Work, que deve permanecer como esta.

Foram atualizados: a regra de purga dos alvos e seus totais no texto, a integracao das limitacoes na Discussao, os grants conforme instrucao do usuario, a citacao do software sem inventar DOI, a terminologia de group mode e os registros de resposta. A recomendacao de reduzir a segmentacao de Related Work foi deliberadamente mantida em aberto por instrucao expressa do usuario. A redistribuicao do extrato local 1998-2025 e de matrizes derivadas continua excluida porque os termos especificos de redistribuicao nao foram verificados; essa limitacao esta declarada no manuscrito.
