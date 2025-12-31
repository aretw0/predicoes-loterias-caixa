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

### v0.6.0 - Models & Persistence (Completed)

**Goal**: Establish state-of-the-art models and the ability to save work (Snapshots).

* [x] **Optimization**:
  * [x] Fix TensorFlow function retracing (Performance).
  * [x] Support `--numbers` CLI argument for System Bets (max numbers).
* [x] **New Models**:
  * [x] **CatBoost**: Best-in-class for tabular data (Implemented).
  * [x] **Transformer (Attention)**: Context-aware sequence prediction (Implemented).
* [x] **Persistence**:
  * [x] **Model Snapshots**: Save/Load trained models (`.pkl` / `.h5`) to avoid retraining.
* [x] **Anomaly Detection**:
  * [x] **AutoEncoders**: Filter out statistically unlikely games (Moved from v0.8.0).
* [x] **Documentation**:
  * [x] **Model Cultivation**: Guide for cultivation workflow.

### v0.7.0 - The Judge (Meta-Learning) (In Progress)

**Goal**: Build the "Trust System" to weigh model opinions dynamically.

* [ ] **Prediction Ledger**: Persistent database tracking every guess.
* [ ] **Heuristic Canaries**: Integrate stateless models (Gap, Freq, Surf) into the Ledger to serve as baseline benchmarks.
* [ ] **Kinetic Analytics**: Data Observability dashboard tracking feature *movement* (Gap Derivatives, Heat Flow) rather than just static stats.
* [ ] **Meta-Learning (Stacking)**: The "Judge" model that learns from the Ledger.
* [ ] **Grokking Detection**: Monitoring loss curves for "sudden generalization".

### v0.8.0 - Simulation & Chaos

**Goal**: Financial simulation and filtering statistical "trash".

* [ ] **Portfolio Simulator**: Track "Virtual P&L" (Profit & Loss) for different strategies (e.g., 6 vs 20 numbers).
* [ ] **Feature Engineering V2**: Deeper chaos features.

## Future Ideas

* **Web Interface**: A static site generating daily predictions.
