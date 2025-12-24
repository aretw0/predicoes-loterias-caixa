# Product Documentation

## Vision

**Preloto** is a laboratory for validating lottery prediction hypotheses. Unlike "lucky number" generators, it aims to be a scientific tool to test whether statistical or mathematical models can perform differently from pure chance over time.

## Key Features

### 1. Deterministic Generation

* **Reproducibility**: Experiments can be repeated exactly using seeds (`--model-args seed:42`).
* **Consistency**: Tie-breaking in frequency models is deterministic.

### 2. Multi-Game Support

Supports the major Brazilian lotteries:

* Mega-Sena
* Lotofácil
* Quina

### 3. Extensible Models

* **Random**: Pure chaos (baseline).
* **Frequency**: Hot (most frequent) or Cold (least frequent) number strategies.

### 4. Machine-Readable Output

Outputs clean JSON/CSV, making it easy to integrate into larger pipelines or analysis tools.
