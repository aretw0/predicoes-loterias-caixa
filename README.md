# Preloto: Lottery Prediction Lab

**Preloto** is a CLI tool for experimenting with mathematical and statistical models for predicting lottery results (Mega-Sena, Lotofácil, Quina). It serves as a laboratory to validate hypotheses by tracking predictions against real results.

## Quick Start

### Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/your-repo/predicoes-loterias-caixa.git
cd predicoes-loterias-caixa
pip install -e .
```

### Usage

Generate a prediction (Defaults: Random model, Max numbers):

```bash
preloto megasena
```

Generate a reproducible prediction:

```bash
preloto megasena --model random --model-args seed:42
```

Use the **Gap Model** (picks "due" numbers):

```bash
preloto megasena --model gap
```

Use the **Surfing Model** (picks "hot" numbers):

```bash
preloto lotofacil --model surfing
```

### Advanced Usage

**Hybrid Model (Ensemble)**:
Combine strategies with custom weights.

```bash
preloto megasena --model hybrid --model-args w_gap:1 w_freq:0.5
```

**Genetic Optimization**:
Automatically find the best weights for the Hybrid model.

```bash
preloto megasena --optimize
```

**Advanced Filters**:
Apply statistical constraints (e.g., Sum of numbers between 100-200, exactly 3 odd numbers).

```bash
preloto megasena --filters "sum:100-200,odd:3"
```

**Backtesting**:
Test how a model would have performed in the past.

```bash
preloto megasena --model surfing --backtest --draws 50
```

**Machine Learning (Experimental)**:
Use Random Forest to predict probabilities.

```bash
preloto megasena --model rf
```

**Deep Learning (LSTM)**:
Train a neural network to find temporal patterns. Requires TensorFlow.

```bash
preloto megasena --model lstm --epochs 100
```

**Monte Carlo Simulation**:
Simulate thousands of games and pick those that fit the statistical profile (Sum, Spread, Odds).

```bash
preloto megasena --model mc
```

**Analysis (Visibility)**:
View the "shape" of the chaos directly.

```bash
preloto megasena --analyze
```

**XGBoost (High Performance)**:
Gradient Boosting for decision trees. Requires `xgboost`.

```bash
preloto megasena --model xgb
```

**Ensemble Strategy (Tira-Teima)**:
Run ALL models (MC, RF, LSTM, XGB) and find the consensus.

```bash
preloto megasena --backtest --ensemble --draws 10
```

### Run Tests

```bash
pytest
```

## Model Cultivation (MLOps)

**Factory (Training)**:
Train models locally (Transformers, LSTM, etc.).

```bash
python run_factory.py --epochs 100 --mode all
```

**Inspection (Health Check)**:
Check if models are overfitting.

```bash
preloto inspect
```

**Ensemble Inference**:
Use trained snapshots to predict.

```bash
python run_ensemble.py
```

## Documentation

* **[Product Vision](docs/PRODUCT.md)**: Features and goals.
* **[Technical Guide](docs/TECHNICAL.md)**: Architecture and development.
* **[Architecture](docs/ARCHITECTURE.md)**: Deep dive into System Design (v0.7.0).
* **[Planning & Versioning](docs/PLANNING.md)**: Roadmap (Current: v0.7.0).
* **[Strategy Guide](docs/STRATEGY.md)**: How to win (statistically).
* **[Disclaimer](docs/DISCLAIMER.md)**: Mathematical validity and academic integrity.
