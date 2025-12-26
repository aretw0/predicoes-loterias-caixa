# Research & Roadmap: v0.4.0 and Beyond

This document outlines potential future directions for `preloto`, focusing on advanced AI and usability.

## 1. Deep Learning (LSTM / Transformers) - *Heavy Computation*

* **Concept**: Use Recurrent Neural Networks (LSTMs) or Transformers, which are designed for sequence prediction. Unlike Random Forest (which just sees "state"), LSTMs see the "story" of the numbers over time.
* **Why**: It might catch temporal patterns that existing models miss (e.g., "Number 5 appears often after a sequence of low numbers").
* **Implementation**:
  * **Library**: `tensorflow` or `pytorch`.
  * **Architecture**: Embedding Layer -> LSTM Layers -> Dense Output (60 classes, softmax).
  * **Cost**: extremely slow to train on CPU.
* **How you can do it**:
    1. I can create the `LSTMPredictor` class structure.
    2. You would run: `preloto megasena --train-lstm --epochs 1000`.
    3. Leave your computer running overnight.

## 2. Advanced Visualization (Dashboard)

* **Concept**: A CLI is great for power users, but seeing impacts is better.
* **Features**:
  * Plot the "Heatmap" of number frequencies over time.
  * Graph the "Bankroll" curve from backtesting (Profit vs. Loss).
  * Visual comparison of Hybrid vs. RF models.
* **Tooling**: `matplotlib` or `plotly` (exporting HTML files to view in browser).

## 3. Real-Time Data & API

* **Concept**: Currently, we rely on cached CSVs or a single URL.
* **Usage**: Create a FastAPI/Flask server that serves predictions as JSON.
* **Integration**: Allow a Telegram Bot or Discord Bot to query `preloto`.

## 4. "Grid Search" Optimization - *Heavy Computation*

* **Concept**: Genetic Algorithms are random. "Grid Search" tries *every possible combination* of weights.
* **Why**: Mathematical certainty of the absolute best weights for past data.
* **Cost**: If we check weights 0..10 with step 0.1 for 3 parameters -> 1,000,000 combinations.
* **How you can do it**:
  * I write `grid_search.py`.
  * You run it on a server with many cores (`joblib` parallelization).

## Recommendation

If you have compute power availability: **Option 1 (LSTM)** is the most exciting "Next Gen" leap.
If you want usability/polish: **Option 2 (Visualization)** makes the tool more "professional".
