# Technical Documentation

## Architecture

The project follows a modular architecture within `src/loterias`:

* **`base.py`**: Abstract Base Classes (`Lottery`, `Model`) defining the contract for new games and models.
* **`data_manager.py`**: Handles downloading, caching, and loading data from the external [loterias-caixa-db](https://github.com/aretw0/loterias-caixa-db) repository.
* **`models.py`**: Concrete implementations of prediction logic (`RandomModel`, `FrequencyModel`).
* **Game Implementations**: `megasena.py`, `lotofacil.py`, `quina.py` inherit from `Lottery` to handle game-specific rules and data parsing.
* **`utils.py`**: Helper functions for exporting data (JSON/CSV).

## Development Setup

### Requirementss

* Python 3.8+
* `pip`

### Installation

The project is configured for editable installation:

```bash
pip install -e .
```

This installs dependencies (`pandas`, `requests`, `openpyxl`, `pytest`) and registers the `preloto` CLI command.

### Testing

We use `pytest` for unit testing.

```bash
pytest
```

Tests are located in `tests/` and cover:

* CLI flow (`tests/test_cli_flow.py`)
* Model logic and determinism (`tests/test_models.py`)

## CLI Implementation

The CLI (`src/cli.py`) uses `argparse` to provide a single entry point `preloto`.

* **Defaults**: It attempts to use smart defaults (e.g., `model=random`, `numbers=max_allowed`) to minimize user typing.
* **Output**: Primarily JSON to `stdout` to allow piping to other tools. Errors go to `stderr`.
