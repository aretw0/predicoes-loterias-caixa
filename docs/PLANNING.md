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

### v0.2.0 - Model Research & Expansion (Next)

* [x] **Research**: Study statistical distributions (e.g., Law of Large Numbers, Poisson) to identify potential "surfing" strategies.
* [x] **New Models**: Implement models based on research (GapModel, SurfingModel).
  * `GapModel`: Exploits mean reversion (gambler's fallacy).
  * `SurfingModel`: Exploits clustering (hot hands).
* [ ] **Academic Integrity**: Write disclaimer about the stochastic nature (probabilistic vs deterministic guarantees).
* [ ] Advanced statistical filters.
* [ ] Machine Learning implementations (if proven viable in analysis).

### v0.2.1 - CLI Refactor (Current)

* [ ] **Refactor**: Split `src/cli.py` monolith into `handle_prediction` and `handle_backtest`.

### v0.3.0 - Future & Integration

* [ ] "Hypothetical P&L": Tracking theoretical performance over time.
* [ ] External Tools: Integration with analysis pipelines.

## Future Ideas

* **Web Interface**: A static site generating daily predictions.
* **Backtesting Engine**: Simulate strategies over past years.
