# Technical Documentation

## Architecture

The project has been refactored (v0.7.0) into a modular hex-like architecture:

* **`src/core`**: Domain Entities.
  * `base.py`: Abstract Base Classes (`Lottery`, `Model`).
  * `games/`: specific implementations (`MegaSena`, `Lotofacil`).
* **`src/data`**: Data Layer.
  * `data_manager.py`: Downloads/Caches Caixa data.
  * `features.py`: Feature Engineering (Sum, Spread, Odd/Even).
  * `filters.py`: Statistical Filters.
* **`src/models`**: Predictive Models.
  * `deep/`: LSTM, Transformer, AutoEncoder.
  * `tree/`: RandomForest, XGBoost, CatBoost.
  * `heuristic/`: Frequency, Gap, Surfing.
* **`src/ops`**: Operations & MLOps.
  * `snapshot.py`: `SnapshotManager` for model cultivation.
  * `optimizer.py`: Genetic Optimizer for hybrid weights.
  * `inspector.py`: `TrainingInspector` for log analysis.
  * `logger.py`: Training metrics logger.
* **`src/judge`**: Meta-Learning System.
  * `ledger.py`: `PredictionLedger` (CSV-based brain).
  * `ensemble.py`: `EnsemblePredictor`.
* **`src/cli`**: Command Line Interface entry points.

## Model Cultivation (MLOps)

We use a "Factory" pattern to train and version models.

### Scripts

* **`run_factory.py`**: Local training script.
  * Usage: `python run_factory.py --epochs 100 --mode all`
  * Cultivates both Generalist (Full history) and Specialist (Filtered) models.
* **`run_ensemble.py`**: Local inference script using the best snapshots.
  * Usage: `python run_ensemble.py`

### Auto-Versioning

Models are saved in `snapshots/{game}/{context}/` with versioned names (Timestamp + Hash), e.g., `lstm_20251231-2359_a1b2c3.keras`.

## CLI Implementation

The CLI primarily resides in `src/cli/main.py`.

* **`preloto predict`**: Standard prediction.
* **`preloto inspect`**: Check training health.
* **`preloto optimize`**: Find best heuristic weights.
* **`preloto backtest`**: Validate strategies.

## Development Setup

### Installation

```bash
pip install -e .
```

### Testing

```bash
pytest
```

Tests are located in `tests/` and cover all distinct modules (`core`, `models`, `ops`, `judge`).
