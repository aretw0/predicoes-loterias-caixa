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
preloto megasena --ensemble --draws 10
```

### Como ler o resultado

* **Consenso 4/4 ("Unanimidade")**: Ouro. Modelos matemáticos (MC) e preditivos (LSTM/XGB) concordaram. Jogue.
* **Consenso 3/4 ("Maioria")**: Prata. Muito forte. Use para completar o volante.
* **Consenso 2/4 ("Dúvida")**: Bronze. Use sua intuição ou análise do passo 1 para desempatar.

## 3. Calibragem Fina ("Rodar pra Valer")

Para a aposta final, quando você não se importa com o tempo de processamento, use o **Ensemble High Compute**.

Como XGBoost e Random Forest usam parâmetros com nomes iguais (ex: `n_estimators`), criamos prefixos especiais para o modo Ensemble:

* **`rf_n_estimators`**: Árvores apenas para o Random Forest.
* **`xgb_n_estimators`**: Árvores apenas para o XGBoost.

### O Comando Supremo (High Compute)

```bash
preloto megasena --ensemble --draws 10 --model-args rf_n_estimators:2000 xgb_n_estimators:1000 xgb_learning_rate:0.01 epochs:500 units:256 window_size:15
```

**O que isso faz:**

* **RF**: Usa 2000 árvores (Extrema estabilidade).
* **XGB**: Usa 1000 árvores com taxa de aprendizado lenta (0.01) para precisão cirúrgica.
* **LSTM**: Treina por 500 épocas (Convergência total).
* **MC**: Roda a simulação padrão.

Este processo pode levar vários minutos, mas é a análise mais profunda que a ferramenta pode oferecer.

## Resumo do Fluxo

1. **Analise** (`--analyze`) para ver se o terreno é seguro.
2. **Simule** (Ensemble) para ter a lista rápida de cortes.
3. **Refine** (Comandos High Compute) se quiser a "baleia branca" dos números.
