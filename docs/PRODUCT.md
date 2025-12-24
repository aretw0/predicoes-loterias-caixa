# Product Documentation

## Vision

**Preloto** is a laboratory for experimenting with probability.

**Philosophy**: We approach lottery games with scientific humility. We understand that these are games of independent random events. Our goal is not to "break" the system or find nonexistent patterns, but to **surf the natural distribution** of probabilities. We provide a tool to generate bets that respect statistical likelihoods, avoiding statistically anomalous sequences (unless desired) and allowing users to play in harmony with the math.

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
