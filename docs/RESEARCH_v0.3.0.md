# Research Report: State of the Art & Future Directions (v0.3.0)

## Overview

In response to the request for "next steps" and "combining models," we conducted a review of current state-of-the-art (SOTA) techniques in lottery prediction.

## Key Findings

### 1. Ensemble Learning (SOTA)

The most robust "scientific" approach found is **Ensemble Learning**. Instead of relying on a single heuristic (like "hot numbers"), ensemble methods combine multiple weak predictors to create a strong one.

* **Random Forest / XGBoost**: These algorithms are excellent at finding non-linear patterns (e.g., "If number 5 and 10 appeared last week, number 20 is less likely").
* **Stacking**: Using a meta-model to weight the outputs of our existing `Gap`, `Frequency`, and `Surfing` models.

### 2. Hybrid Models (User Suggestion)

Combining existing models is a proven strategy.

* **Weighted Scoring**: Assign a score to each number based on multiple factors.
  * *Score = (w1 * GapScore) + (w2 * FrequencyScore) + (w3 * SurfingScore)*
* This creates a "Consensus Model" that balances long-term stats (Frequency) with short-term trends (Surfing).

### 3. Genetic Algorithms (Optimization)

Genetic Algorithms (GA) are not typically effective for direct prediction but are excellent for **optimizing parameters**.

* We can use GA to "evolve" the best weights (`w1, w2, w3`) for the Hybrid Model by running thousands of backtests.

## Recommendations for v0.3.0

1. **Implement `HybridModel`**: A simple weighted ensemble of our current models.
2. **Implement `GeneticOptimizer`**: A script that runs the `Backtester` repeatedly to find the optimal weights for the `HybridModel`.
3. **Explore SciKit-Learn**: Introduce a basic Random Forest implementation as a `MLModel` to compare against heuristics.

## References

* *Compound-Dirichlet-Multinomial (CDM)* for statistical distribution modeling.
* *Lottery Ticket Hypothesis* (Neural Networks) - Tangentially related but inspires efficient parameter search.
