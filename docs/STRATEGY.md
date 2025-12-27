# Estratégia de Uso: O Ritual do Tira-Teima (v0.5.0)

> "A estatística não garante a vitória, mas protege contra o absurdo."

Com a chegada da **Fase de Consenso (v0.5.0)**, o fluxo de uso do Preloto evoluiu. Deixamos de caçar números manualmente para focar na **supervisão de inteligências artificiais**.

## 1. O Diagnóstico Rápido

Antes de qualquer coisa, entenda o "humor" do jogo.

```bash
preloto megasena --analyze --draws 20
```

Se a aleatoriedade estiver se comportando normalmente (Soma média ~180, Equilíbrio Par/Ímpar), seus modelos funcionarão bem. Se houver anomalias recentes, espere um retorno à média.

## 2. A Máquina de Consenso (O Caminho Padrão)

Não tente adivinhar qual modelo (MC, RF ou LSTM) está certo hoje. Deixe que eles briguem entre si.

O **Ensemble Strategy** roda todos os modelos simultaneamente e busca a intersecção.

```bash
# Roda MC, RF, LSTM e XGBoost. Retorna o consenso.
preloto megasena --backtest --ensemble --draws 10
```

### Como ler o resultado:
*   **Consenso 4/4 ("Unanimidade")**: Ouro. Modelos matemáticos (MC) e preditivos (LSTM/XGB) concordaram. Jogue.
*   **Consenso 3/4 ("Maioria")**: Prata. Muito forte. Use para completar o volante.
*   **Consenso 2/4 ("Dúvida")**: Bronze. Use sua intuição ou análise do passo 1 para desempatar.

## 3. Calibragem Fina ("Rodar pra Valer")

Se você tem tempo de processamento e quer a máxima precisão possível, não use os padrões. Force os modelos ao limite.

### Parâmetros Ideais (High Compute)

Para rodar "pra valer", você deve aumentar a profundidade de busca das árvores e a memória da rede neural.

**Comando Sugerido (Manual)**:

Como o `--ensemble` usa padrões equilibrados para velocidade, para a aposta final sugiro rodar os modelos individualmente com força total e cruzar os resultados você mesmo (ou editar o código do ensemble).

#### XGBoost (A Besta de Performance)

```bash
preloto megasena --model xgb --model-args n_estimators:1000 learning_rate:0.01 max_depth:7
```
*   *Por que?* `learning_rate` baixo com muitas árvores (`1000`) evita overfit e encontra padrões sutis.

#### Random Forest (O Consultor Conservador)

```bash
preloto megasena --model rf --model-args n_estimators:2000
```
*   *Por que?* 2000 árvores garantem uma estabilidade estatística quase perfeita.

#### LSTM (O Vidente de Sequências)

```bash
# Pergunte à Rede Neural (foco em sequências recentes)
# Dica: 'epochs' define o tempo de treino. 'units' define a inteligência (padrão 128). 'window_size' o contexto (padrão 10).
# Você pode usar a flag --epochs direto ou colocar via --model-args
preloto megasena --model lstm --epochs 100 --model-args units:256 window_size:20
```
*   *Por que?* 100 épocas são um bom ponto de partida para a convergência. `window_size:20` captura ciclos de médio prazo.

#### Monte Carlo (A Peneira)
```bash
preloto megasena --model mc
```
*   *Por que?* O padrão já simula 10.000 jogos. É suficiente.

## Resumo do Fluxo

1.  **Analise** (`--analyze`) para ver se o terreno é seguro.
2.  **Simule** (Ensemble) para ter a lista rápida de cortes.
3.  **Refine** (Comandos High Compute) se quiser a "baleia branca" dos números.
