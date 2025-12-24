# [DEPRECATED] Plano do Projeto: Predições de Loterias da Caixa

> [!CAUTION]
> **Arquivo Arquivado**: Este documento é mantido apenas para fins históricos. A fonte da verdade para o roteiro do projeto é o [roadmap.md](../roadmap.md).

## Visão

Estudar e experimentar modelos matemáticos e estatísticos para análise e predição de resultados de loterias da Caixa, com foco no aprendizado e na exploração de técnicas de análise de dados.

## Metas

1. **Estruturação do Projeto:** Organizar o código e a documentação de forma clara e escalável.
2. **Coleta e Tratamento de Dados:** Automatizar a coleta de resultados históricos das loterias e prepará-los para análise.
3. **Análise Exploratória:** Desenvolver scripts para realizar análises estatísticas descritivas dos dados.
4. **Modelagem Preditiva:** Experimentar diferentes modelos (estatísticos, de machine learning, etc.) para identificar padrões e tendências.
5. **Visualização de Dados:** Criar visualizações que facilitem a compreensão dos dados e dos resultados dos modelos.

## Filosofia e Estratégia de Predição

O projeto reconhece a natureza aleatória dos sorteios de loteria. A nossa abordagem não se baseia na premissa de que é possível prever os resultados com certeza. Em vez disso, o objetivo é "surfar na distribuição natural" dos números sorteados. A estratégia consiste em focar nos números que têm aparecido com menos frequência, partindo do princípio de que, ao longo do tempo, a distribuição dos números tende a se equilibrar.

A estratégia de predição do projeto não se limita a acertar o resultado principal (e.g., 6 dezenas na Mega-Sena). O objetivo é desenvolver modelos que possam gerar sequências de números com alta probabilidade de atingir qualquer uma das faixas de premiação.

As métricas de sucesso para os modelos de predição serão baseadas na capacidade de gerar sequências que resultem em prêmios, mesmo que menores. O "tuning" dos modelos será focado em maximizar a frequência de acertos em qualquer faixa de premiação.

A fase de "produção" de um modelo consistirá em utilizar o seu estado treinado para gerar uma ou mais sequências de números a serem "apostadas" no próximo sorteio. O sucesso será verificado comparando as sequências geradas com os resultados reais, contabilizando os acertos em todas as faixas de premiação.

## Plano

- [x] Inicializar o repositório Git.
- [x] Configurar o ambiente de desenvolvimento python com containers.
- [x] Refatorar o projeto para consumir dados de um repositório externo (`loterias-caixa-db`).
- [x] Realizar uma análise estatística básica dos resultados da Quina, Lotofácil e Mega-Sena.
- [x] Definir Roadmap de Evolução (ver [docs/roadmap.md](roadmap.md)).
- [x] Implementar um modelo de predição inicial para a Quina.
- [x] Expandir a modelagem para Lotofácil e Mega-Sena.
- [x] Implementar CLI para geração de predições e registro em Ledger.
- [x] Adicionar testes automatizados para validação do fluxo.
- [ ] Desenvolver um sistema de backtesting para avaliar a performance do modelo.
- [ ] Criar visualizações para os resultados da análise e dos modelos.
- [ ] Documentar as descobertas e os resultados dos modelos.
