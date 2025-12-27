# Planning & Roadmap

## Versioning Strategy

We use Semantic Versioning (SemVer).

* **Current Version**: `0.4.0`

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
* [x] **Deep Learning**: `LSTMModel` implementation (v0.3.5).

### v0.4.0 - Consolidation & Visibility (Current Focus)

**Goal**: "Pé no Chão" (Grounded). Focus on understanding data before predicting.

* [ ] **Analysis Module (`preloto analyze`)**:
    *   Generate machine-readable JSON reports (statistics, distributions).
    *   Generate human-readable insights.
* [ ] **Feature Engineering**:
    *   Enrich models (`RF`, `LSTM`) with structural features (Sum, Odd/Even, Quadrants) instead of raw numbers.
* [ ] **Simulation**:
    *   Implement **Monte Carlo** simulation based on enriched distributions.
* [ ] **Cleanup**: remove noise and consolidate experimental code.

## Future Ideas

* **Web Interface**: A static site generating daily predictions.
