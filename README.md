# Repositório de Knowledge Base: Aplicabilidade das Predições Matemáticas em Loterias

Este repositório contém uma análise aprofundada sobre a aplicabilidade de predições matemáticas e modelos de aprendizado de máquina em jogos de loteria da Caixa Econômica Federal. O objetivo é explorar o estado da arte, documentar as particularidades de cada modalidade de loteria, implementar análises estatísticas e modelos preditivos, e estabelecer um sistema de monitoramento contínuo.

## Conteúdo do Repositório

### 1. Estado da Arte da Predição em Loterias

* **`state_of_art_lottery_prediction.md`**: Documento detalhando os fundamentos teóricos da aleatoriedade em loterias, as técnicas de predição matemática e aprendizado de máquina aplicáveis (ARIMA, LSTM, Random Forest, XGBoost, Monte Carlo, CPR, VWAP), suas limitações e o potencial para o treinamento de modelos. Este documento serve como a base teórica para todo o projeto.

### 2. Documentação das Modalidades de Loteria

* **`lottery_modalities_documentation.md`**: Documento técnico que descreve as características principais e a estrutura de jogo das loterias analisadas (Mega-Sena, Lotofácil, Quina). Inclui detalhes sobre o universo de números, quantidade de dezenas sorteadas e outras particularidades relevantes para a modelagem preditiva.

### 3. Análises Estatísticas

Os dados históricos das loterias são obtidos do repositório público [loterias-caixa-db](https://github.com/aretw0/loterias-caixa-db). Scripts Python foram desenvolvidos para realizar análises estatísticas básicas sobre esses dados.

* **`analyze_megasena.py`**: Script Python para análise estatística da Mega-Sena.
* **`megasena_statistics.txt`**: Resultados da análise estatística da Mega-Sena.

* **`analyze_lotofacil.py`**: Script Python para análise estatística da Lotofácil.
* **`lotofacil_statistics.txt`**: Resultados da análise estatística da Lotofácil.

* **`analyze_quina.py`**: Script Python para análise estatística da Quina.
* **`quina_statistics.txt`**: Resultados da análise estatística da Quina.

## Como Utilizar

### Configuração do Ambiente

Este projeto foi desenhado para ser executado em **DevContainers** (recomendado) ou em um ambiente Python local.

#### Opção A: DevContainers (Recomendado)

1. Abra este repositório no VS Code.
2. Quando solicitado, clique em "Reopen in Container".
3. O ambiente será configurado automaticamente com todas as dependências.

#### Opção B: Python Local

1. Certifique-se de ter Python 3.10+ instalado.
2. Crie um ambiente virtual: `python -m venv .venv`
3. Ative o ambiente:
    * Linux/Mac: `source .venv/bin/activate`
    * Windows: `.venv\Scripts\activate`
4. Instale as dependências: `pip install -r requirements.txt`

### Executando Predições (CLI)

O projeto possui uma CLI unificada para gerar predições e registrar no Ledger.

**Sintaxe Básica:**

```bash
python main.py predict --game [megasena|lotofacil|quina] --model [frequency|random] --numbers [QTD] [OPCOES]
```

**Exemplos:**

1. **Predição Padrão (Números mais frequentes):**
    Gera uma aposta com 6 números para a Mega-Sena baseada na frequência histórica.

    ```bash
    python main.py predict --game megasena --model frequency --numbers 6
    ```

2. **Estratégia Inversa (Números menos frequentes):**
    Usa o argumento `--model-args` para inverter a lógica do modelo de frequência.

    ```bash
    python main.py predict --game megasena --model frequency --numbers 6 --model-args order:asc
    ```

3. **Salvar no Ledger:**
    Adicione `--save` e o número do concurso `--contest` para registrar a aposta.

    ```bash
    python main.py predict --game lotofacil --model frequency --numbers 15 --save --contest 3000
    ```

### Executando Análises Estatísticas

Os scripts de análise estatística continuam disponíveis:

```bash
python scripts/analyze_megasena.py
```

## Próximos Passos

* **Implementação de Modelos Preditivos:** Adicionar implementações dos modelos ARIMA, LSTM, Random Forest, XGBoost, etc., para cada modalidade de loteria, com foco em gerar sequências que atinjam múltiplas faixas de premiação.
* **Avaliação de Desempenho:** Desenvolver métricas e metodologias para avaliar o "desempenho" dos modelos, mesmo reconhecendo a aleatoriedade inerente.
* **Visualização de Dados:** Criar gráficos e dashboards para visualizar as frequências, padrões e o desempenho dos modelos ao longo do tempo.
* **Interface de Usuário:** Desenvolver uma interface simples para interagir com o sistema, permitindo a consulta de resultados, a execução de análises e a visualização de predições (com as devidas ressalvas sobre a aleatoriedade).

Este repositório serve como um ponto de partida para a exploração da ciência de dados no contexto das loterias, enfatizando a análise de dados e a compreensão dos limites da predição em sistemas complexos e aleatórios.
