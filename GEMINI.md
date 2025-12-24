# GEMINI.md - Project Context & Agent Guide

## Project Overview

**Predições de Loterias da Caixa** is a laboratory for experimenting with mathematical and statistical models for predicting lottery results.
**Goal:** Validate hypotheses by tracking predictions against real results, focusing on hypothetical financial performance.

## Architecture

- **`src.loterias`**: Core package.
  - `base.py`: Base classes `Lottery` (Data) and `Model` (Logic).
  - `data_manager.py`: Handles data fetching/caching from `loterias-caixa-db`.
  - `models.py`: Implementations (`RandomModel`, `FrequencyModel`).
- **`src.cli`**: Main entry point (`loto-cli`).
- **`tests/`**: Unit tests via `pytest`.

## Instructions

### 1. Installation

This project supports editable installation for ease of development:

```bash
pip install -e .
```

### 2. Execution

Use the CLI tool to generate predictions:

```bash
preloto megasena
```

Or for reproducibility:

```bash
preloto megasena --model random --model-args seed:42
```

### 3. Testing

Run the test suite:

```bash
pytest
```

## Documentation

- **Architecture**: See `src/loterias/`.
