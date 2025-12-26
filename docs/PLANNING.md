# Planning & Roadmap

## Versioning Strategy

We use Semantic Versioning (SemVer).

* **Current Version**: `0.1.0`

## Roadmap

### v0.1.0 - Foundation (Current)

* [x] Robust CLI (`preloto`)
* [x] Deterministic Models (`seed`, sorting)
* [x] Automated Testing Infrastructure
* [x] Documentation Restructure
* [x] Editable Install Support

### v0.2.0 - Model Research & Expansion (Current)

* [x] **Research**: Study statistical distributions (e.g., Law of Large Numbers, Poisson) to identify potential "surfing" strategies.
* [x] **New Models**: Implement models based on research (GapModel, SurfingModel).
  * `GapModel`: Exploits mean reversion (gambler's fallacy).
  * `SurfingModel`: Exploits clustering (hot hands).
* [x] **Refactor**: Split `src/cli.py` monolith into `handle_prediction` and `handle_backtest`.
* [x] **Academic Integrity**: Write disclaimer about the stochastic nature (probabilistic vs deterministic guarantees).
* [x] **Advanced statistical filters**: Rejection sampling for sum, odd/even constraints.
* [x] **Machine Learning**: Evaluation - Deferred in favor of heuristic models and statistical filters.

### v0.3.0 - Ensemble & Optimization (Next)

* [ ] **Hybrid Model**: Combine `Gap`, `Frequency`, and `Surfing` into a weighted consensus model.
* [ ] **Genetic Optimizer**: Use Genetic Algorithms (GA) to "evolve" the optimal weights for the Hybrid Model using the Backtester.
* [ ] **ML Exploration**: Implement a `RandomForestModel` using `scikit-learn` to benchmark against heuristics.

## Future Ideas

* **Web Interface**: A static site generating daily predictions.
