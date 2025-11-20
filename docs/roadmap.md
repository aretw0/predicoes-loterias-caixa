# Roadmap do Projeto: Predições de Loterias da Caixa

Este documento define o roteiro de evolução do projeto, focando na transformação de scripts de análise isolados em um sistema robusto de predição, rastreamento e validação de hipóteses.

## Visão Geral

O objetivo é criar um ecossistema onde modelos preditivos (dos mais simples aos mais complexos) geram palpites que são sistematicamente registrados e conferidos contra os resultados reais. Isso criará um "laboratório" transparente para validar a eficácia (ou ineficácia) de diferentes estratégias, com um foco especial no monitoramento financeiro hipotético (Lucro/Prejuízo).

## Fases do Projeto

### Fase 1: Reestruturação e Fundação (Curto Prazo)
*Objetivo: Organizar o código para suportar múltiplos modelos e automação.*

- [ ] **Modularização do Código:** Refatorar os scripts atuais (`analyze_*.py`) em uma estrutura de pacote Python (ex: `src/loterias`), separando:
    - Coleta de dados (Data Ingestion).
    - Processamento e Análise (Core Logic).
    - Geração de Relatórios (Reporting).
- [ ] **Padronização de Interfaces:** Criar classes base para "Loterias" e "Modelos", permitindo que novos jogos ou estratégias sejam plugados facilmente.
- [ ] **Pipeline de Dados:** Garantir que a atualização dos dados do repositório externo (`loterias-caixa-db`) seja fluida e integrada.

### Fase 2: Motor de Predição e Serviço "Sob Demanda" (Médio Prazo)
*Objetivo: Gerar palpites configuráveis e exportáveis.*

- [ ] **Interface de Geração:** Criar um comando (CLI) que aceite parâmetros como:
    - Jogo (Mega, Quina, Lotofácil).
    - Modelo (Estatístico, Frequência, Aleatório, ML).
    - Quantidade de Jogos a gerar.
    - Filtros (ex: evitar sequências, equilibrar pares/ímpares).
- [ ] **Exportação de Dados:** Implementar a saída das predições em formatos estáticos padronizados (`.csv`, `.json`) para fácil consumo ou visualização.
    - Exemplo: `predicoes_quina_concurso_6000.csv`

### Fase 3: Sistema de Rastreamento Hipotético (O "Reality Check") (Médio/Longo Prazo)
*Objetivo: Automatizar a validação e o controle financeiro simulado.*

- [ ] **Registro de Apostas (Ledger):** Criar um sistema (banco de dados simples ou arquivos estruturados) para armazenar as predições geradas *antes* do sorteio ocorrer.
    - Campos: Data, Concurso Alvo, Modelo Usado, Jogos Gerados, Custo da Aposta.
- [ ] **Conferência Automática:** Script que roda após a atualização dos resultados oficiais, comparando as apostas registradas com os números sorteados.
- [ ] **Relatório de Performance (P&L):** Geração de relatórios que mostram:
    - Taxa de Acerto (Geral e por Faixa de Prêmio).
    - Custo Total Hipotético vs. Prêmios Hipotéticos.
    - ROI (Retorno sobre Investimento) de cada modelo.
    - *Meta:* Demonstrar visualmente a dificuldade de bater a aleatoriedade.

### Fase 4: Modelagem Avançada (Longo Prazo)
*Objetivo: Implementar e testar os modelos teóricos mapeados.*

- [ ] **Implementação de Modelos:**
    - Estatísticos (Médias Móveis, Desvio Padrão).
    - Machine Learning (Random Forest, LSTM) conforme `state_of_art_lottery_prediction.md`.
- [ ] **Backtesting:** Ferramenta para rodar modelos no passado e verificar como teriam performado (simulação histórica).

### Fase 5: Interface e Visualização (Static & Free)
*Objetivo: Facilitar a interação e análise dos resultados usando recursos estáticos do GitHub.*

- [ ] **Relatórios Estáticos Automatizados:** Gerar relatórios em Markdown atualizados automaticamente a cada sorteio (tabelas de performance, últimos palpites).
- [ ] **Dados Abertos:** Manter arquivos CSV/JSON atualizados para consumo direto.
- [ ] **GitHub Pages:** Investigar e implementar uma visualização web estática (HTML/JS/Jekyll) que consuma os JSONs/CSVs gerados para exibir gráficos e dashboards sem necessidade de backend ativo.

## Fluxo de Trabalho Proposto (Ciclo de Vida de um Concurso)

1.  **Atualização:** O sistema detecta que o último concurso foi realizado e atualiza a base local.
2.  **Conferência:** O sistema verifica as predições feitas para o concurso que acabou de sair e atualiza o "Saldo Hipotético".
3.  **Predição:** O sistema roda os modelos configurados para o *próximo* concurso.
4.  **Registro:** As novas predições são salvas (CSV/DB) e registradas no Ledger de apostas pendentes.
5.  **Publicação:** Relatórios estáticos são atualizados com as novas predições e o desempenho recente.
