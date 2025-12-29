# Planning & Roadmap

## Versioning Strategy

We use Semantic Versioning (SemVer).

* **Current Version**: `0.5.0`

## Roadmap

### v0.1.0 - Foundation (Completed)

* [x] Robust CLI (`preloto`)
* [x] Deterministic Models (`seed`, sorting)
* [x] Automated Testing Infrastructure
* [x] Documentation Restructure
* [x] Editable Install Support

### v0.2.0 - Model Research & Expansion (Completed)

* [x] **Research**: Study statistical distributions (e.g., Law of Large Numbers, Poisson).
* [x] **New Models**: Implement models based on research (GapModel, SurfingModel).
* [x] **Refactor**: Split `src/cli.py` monolith.
* [x] **Filters**: Rejection sampling strategy.

### v0.3.0 - Ensemble, Optimization & ML (Completed)

* [x] **Hybrid Model**: Weighted consensus model.
* [x] **Genetic Optimizer**: GA for weight optimization.
* [x] **ML Exploration**: `RandomForestModel` implementation.
* [x] **Deep Learning**: `LSTMModel` implementation.

### v0.4.0 - Visibility & Simulation (Completed)

**Goal**: "Pé no Chão" (Grounded). Focus on understanding data before predicting.

* [x] **Analysis Module**: `preloto analyze` (See the chaos).
* [x] **Feature Engineering**: Enrich models with structural features.
* [x] **Simulation**: Implement **Monte Carlo** simulation.

### v0.5.0 - Consensus & High Performance (Completed)

**Goal**: Validate the "Tira-Teima" and optimize for deeper insights.

* [x] **Ensemble Backtesting**: Validate intersection strategies (Implemented via `EnsembleBacktester`).
* [x] **XGBoost**: Gradient Boosting for high-performance decision trees.
* [x] **Ensemble Prediction**: `EnsemblePredictor` for future draws (CLI `--predict`).
* [x] **Weight Optimization**: Genetic Algorithm for Hybrid Model weights (Partial "Hyperparameter Tuning").

### v0.6.0 - State of the Art & Chaos Engineering (Current)

**Goal**: Push the limits of prediction with Transformers, Chaos Theory, and Grokking.

* [ ] **Advanced Models**:
  * **CatBoost**: Better handling of categorical data / decision trees.
  * **Transformer (Attention)**: Move beyond LSTM sequences to attention mechanisms.
  * **AutoEncoders**: Anomaly detection to filter "statistically trash" games.
* [ ] **Strategy & Monitoring**:
  * **Model Snapshots**: Ability to save/load trained states (`.pkl` / `.h5`).
  * **Grokking Detection**: Monitoring loss curves for "sudden generalization".
* [ ] **Chaos Engineering**:
  * **Max Numbers**: Support for high-cost system bets (e.g., 20 numbers) by respecting the `--numbers` CLI argument in Ensemble mode.
  * **Feature Engineering V2**: Escaping the "statistical trash".

## Future Ideas

* **Web Interface**: A static site generating daily predictions.
