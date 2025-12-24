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

Use a specific model (e.g., Least Frequent numbers):

```bash
preloto lotofacil --model frequency --model-args order:asc
```

### Run Tests

```bash
pytest
```

## Documentation

* **[Product Vision](docs/PRODUCT.md)**: Features and goals.
* **[Technical Guide](docs/TECHNICAL.md)**: Architecture and development.
* **[Planning & Versioning](docs/PLANNING.md)**: Roadmap (Current: v0.1.0).
