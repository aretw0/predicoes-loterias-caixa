# Cultivo de Modelos (Model Cultivation)

> "Não basta plantar a semente, é preciso regar e colher no momento certo."

O Preloto v0.6.0 introduz o conceito de **Cultivo de Modelos**. À medida que adotamos modelos mais complexos (Deep Learning, Gradient Boosting), o tempo de treinamento aumenta. Não faz sentido treinar uma Rede Neural por 30 minutos toda vez que você quer apenas gerar um palpite rápido.

Este guia define o fluxo de trabalho para:

1. **Cultivar (Treinar & Salvar)**: Investir tempo de computação uma vez.
2. **Colher (Carregar & Predizer)**: Reutilizar o "cérebro" treinado instantaneamente.
3. **Proteger (Validação)**: Usar AutoEncoders para filtrar palpites ruins.

---

## 1. O Ciclo de Vida via CLI

### Passo 1: O Plantio (Treinamento Pesado)

Escolha um modelo robusto (ex: CatBoost ou Transformer) e treine-o com parâmetros agressivos. Salve o resultado.

```bash
# Treinar CatBoost e salvar o snapshot
preloto megasena --model catboost --save-model meu_catboost_v1.cbm

# Treinar Transformer (Deep Learning) por 100 épocas e salvar
preloto megasena --model transformer --epochs 100 --save-model meu_transformer_v1.keras
```

**Saída:** Arquivos `.cbm` ou `.keras` serão criados. Estes são seus "modelos cultivados".

### Passo 2: A Colheita (Predição Rápida)

Agora você pode gerar palpites em segundos, pulando o treinamento.

```bash
# Carregar o modelo salvo e predizer
preloto megasena --load-model meu_catboost_v1.cbm --numbers 15
```

### Passo 3: A Proteção (Detecção de Anomalias)

Treine um **AutoEncoder** para aprender o padrão de jogos "normais" e rejeitar aberrações.

1. **Treinar o Validador:**

    ```bash
    preloto megasena --model autoencoder --epochs 50 --save-model fiscal_de_jogos.keras
    ```

2. **Usar na Predição (Filtro Inteligente):**

    ```bash
    # Gera palpites com Transformer, mas rejeita se o AutoEncoder achar estranho
    preloto megasena --load-model meu_transformer_v1.keras --validator-model fiscal_de_jogos.keras --anomaly-threshold 0.1
    ```

---

## 2. O Ciclo de Vida via Python Notebook

Para cientistas de dados que preferem Jupyter Notebooks, o processo é transparente usando as classes do `src`.

### Exemplo de Fluxo

```python
import pandas as pd
from loterias.megasena import MegaSena
from loterias.models import CatBoostModel, AutoEncoderModel

# 1. Carregar Dados
lottery = MegaSena()
df = lottery.preprocess_data()

# 2. Cultivar (Treinar)
print("Treinando modelo principal...")
model = CatBoostModel(range_min=1, range_max=60, draw_count=6)
model.train(df)

# 3. Salvar Snapshot
print("Salvando snapshot...")
model.save("meu_modelo_cultivado.cbm")

# --- (Em outro momento/célula) ---

# 4. Colher (Carregar)
print("Carregando modelo...")
loaded_model = CatBoostModel(1, 60, 6) # Instância vazia
loaded_model.load("meu_modelo_cultivado.cbm")

# 5. Predizer
palpite = loaded_model.predict(count=6)
print("Palpite Rápido:", palpite)
```

## 3. Melhores Práticas

1. **Versioning**: Use nomes descritivos para seus snapshots (ex: `transformer_fevereiro_epoch100.keras`).
2. **Re-treino Periódico**: Modelos "apodrecem" (Data Drift). Re-treine seus snapshots a cada 5-10 concursos novos.
3. **Backups**: Mantenha seus melhores modelos salvos. Se um novo treinamento piorar a performance, você pode voltar para o snapshot anterior.

---

## 4. Estratégia de Treinamento (Google Colab / GPU)

Se você tem acesso a hardware potente (como GPUs T4/A100 no Google Colab ou localmente), use parâmetros agressivos para criar modelos "SOTA" (State of the Art).

> **Dica**: Use o comando `mkdir snapshots` para criar uma pasta organizada.

### Parâmetros Agressivos (Copy-Paste)

> **Dica Colab**: Em vez de fazer upload dos arquivos Python manualmente, você pode instalar o projeto direto do GitHub na primeira célula do notebook:
> `!pip install git+https://github.com/aretw0/predicoes-loterias-caixa.git`

Estes comandos visam extrair o máximo de performance, mesmo que levem horas treinando.

#### A. CatBoost (Gradient Boosting)

Ideal para padrões tabulares complexos.

```bash
preloto megasena --model catboost \
  --model-args iterations:10000 depth:8 learning_rate:0.01 early_stopping_rounds:500 \
  --save-model snapshots/catboost_heavy_v1.cbm
```

#### B. Transformer (Deep Learning / Attention)

Ideal para sequências e contexto histórico longo.

```bash
preloto megasena --model transformer \
  --epochs 200 --batch-size 64 --model-args head_size:256 num_heads:4 ff_dim:256 window_size:20 \
  --save-model snapshots/transformer_heavy_v1.keras
```

#### C. LSTM (Redes Neurais Recorrentes)

Clássico para séries temporais.

```bash
preloto megasena --model lstm \
  --epochs 300 --batch-size 32 --model-args units:256 window_size:30 \
  --save-model snapshots/lstm_heavy_v1.keras
```

#### D. AutoEncoder (O Juiz S severo)

Para criar um filtro extremamente rigoroso de anomalias.

```bash
preloto megasena --model autoencoder \
  --epochs 150 --batch-size 16 --model-args latent_dim:8 \
  --save-model snapshots/autoencoder_heavy_v1.keras
```

#### E. Modelos Especialistas (Ex: Mega da Virada)

Treine modelos que só viram sorteios "Especiais" (finais 0 ou 5).
Eles terão menos dados, mas serão especialistas no padrão específico desses sorteios.

```bash
# Exemplo teórico (filtragem deve ser feita no notebook por enquanto)
# Futuramente: preloto megasena --model catboost --filter "final_0_5" ...
```

Para criar especialistas hoje, use o **Python Notebook** para filtrar o DataFrame antes do treino.

---

## 5. Organização e Ciclo de Vida (MLOps)

Para evitar bagunça e perda de progresso, recomendamos a seguinte estrutura e processo.

### Estrutura de Pastas Avançada

Recomendamos organizar por **Jogo** e depois por **Especialidade**.

```text
/workspaces/predicoes-loterias-caixa/
├── snapshots/
│   ├── megasena/
│   │   ├── generalistas/          # Treinados com TODOS os dados
│   │   │   ├── best_catboost.cbm
│   │   │   └── best_transformer.keras
│   │   └── especialistas/         # Treinados com dados filtrados
│   │       ├── virada/            # Focados em finais 0 e 5
│   │       │   └── transformer_virada_v1.keras
│   │       └── acumulados/        # Focados em sorteios pós-acumulação
│   └── lotofacil/
│       └── ...
```

### O Ciclo "Campeão vs Desafiante" (Champion/Challenger)

Não apague seu modelo antigo assim que treinar um novo! Siga este fluxo para evitar **Data Drift** (quando o modelo novo "esquece" o que o antigo sabia) ou regressão de performance.

1. **Campeão Atual**: Você tem um modelo `best_model.cbm` que acerta bem.
2. **Desafiante**: Você treina um novo `challenger_v2.cbm` com mais dados ou parâmetros diferentes.
3. **O Duelo (Ensemble Backtest)**:
    Rode um backtest comparativo.
    *(Nota: Funcionalidade de backtest comparativo de snapshots será facilitada na v0.7.0, por enquanto faça manualmente via CLI comparando resultados).*
4. **Decisão**:
    * Se o `challenger` for melhor: Renomeie `best_model.cbm` -> `archive/v1.cbm` e promova o `challenger` para `best_model.cbm`.
    * Se for pior: Descarte ou investigue o `challenger`.

---

## 6. O Futuro: "The Judge" (O Juiz)

Por que estamos fazendo tudo isso?

Na versão **v0.7.0**, implementaremos o conceito de **Meta-Learning** ("O Juiz").
O Juiz não tenta prever os números. Ele tenta prever **qual modelo está certo**.

* **Hoje (v0.6.0)**: Você roda CatBoost, depois roda LSTM, e tenta adivinhar em quem confiar.
* **Amanhã (v0.7.0)**: Você alimenta o Juiz com seus snapshots (`snapshots/*.cbm`, `snapshots/*.keras`).
  * O Juiz olha o contexto do sorteio atual.
  * Ele diz: *"Neste tipo de cenário (acumulado, final 0), o CatBoost costuma errar, mas o Transformer vai bem. Vou dar peso 0.9 pro Transformer."*

Portanto, **quanto mais modelos variados e bem treinados (snapshots) você tiver guardado, mais inteligente será o seu "Juiz" no futuro.** Cultive seu jardim de modelos agora para colher uma Super-Inteligência depois.
