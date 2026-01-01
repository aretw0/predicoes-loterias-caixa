# Architecture Refactoring Proposal

Current status: `src/loterias` is a "God Package" containing domain logic, ML models, infrastructure, CLI, and orchestration.

## Proposed Structure (`v1.0` Goal)

We should aim to decouple technical infrastructure from lottery domain logic.

```
src/
├── core/                   # Pure Domain Entities
│   ├── base.py             # Abstract Base Classes (Lottery, Model)
│   ├── games/              # MegaSena, Lotofacil, Quina
│   └── interfaces.py       # Protocols for DataManager, etc.
│
├── data/                   # Data Access & Transformation
│   ├── manager.py          # DataManager (Downloads/Caching)
│   ├── features.py         # Feature Engineering (Math)
│   └── filters.py          # Pandas filters (e.g. Ironia, Primos)
│
├── models/                 # Predictive Models (The "Brains")
│   ├── base.py             # Model abstract base
│   ├── registry.py         # centralized model factory
│   ├── deep/               # LSTM, Transformer, AutoEncoder
│   ├── tree/               # RF, XGBoost, CatBoost
│   └── heuristic/          # Frequency, Gap, Surfing
│
├── ops/                    # MLOps & Infrastructure
│   ├── snapshot.py         # SnapshotManager (Training Orchestrator)
│   ├── versioning.py       # Model Versioning Logic (moved from judge?)
│   └── logger.py           # Training Logger (moved from judge?)
│
├── judge/                  # The Meta-Model System (v0.7+)
│   ├── ledger.py           # Prediction Ledger
│   └── meta_model.py       # Stacking Logic
│
└── cli/                    # Entry Points
    ├── main.py             # preloto command
    └── formatting.py       # JSON/Table output helpers
```

## Immediate Action Items (Phase 3.5)

To prepare for "The Judge" (which introduces more complexity), we should at least:

1. **Extract Models**: Move `src/loterias/models` -> `src/models`.
2. **Isolate Operations**: Move `SnapshotManager` and `backtester` logic out of `loterias` root.
3. **Update Imports**: This will require a `grep` across the codebase to fix imports.

## Benefits

1. **Testability**: Testing `src/core` won't require TensorFlow installed.
2. **Clarity**: New developers (or Agents) know exactly where to look for "Infrastructure" vs "Business Rules".
3. **Scale**: Adding a new game (e.g. "Milionaria") is just adding a file to `src/core/games`.
