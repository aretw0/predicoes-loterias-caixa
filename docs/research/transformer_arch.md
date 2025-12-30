# Research: Transformer Architecture for Lottery Prediction

## Objective

Limit the "State of the Art" scope of v0.6.0 to exploring attention mechanisms for sequence prediction in lottery games.
We want to move beyond LSTM (Recurrent) to Transformers (Attention-based), which effectively handle long-range dependencies and can parallelize training.

## The Problem

Lottery draws are a sequence of sets.
$D_1 = \{n_1, n_2, ...\}, D_2 = \{...\}, ..., D_t$
We want to predict $D_{t+1}$.

## Proposed Architectures

### Option A: Simple "Sequence to Embedding" (Encoder Only)

Treat the last $K$ draws as a sequence of tokens.
Each draw is embedded (e.g., Multi-Hot encoding projected to dense vector).
Feed into a standard Transformer Encoder.
Output: Probability distribution over all possible numbers (Classification problem).

* **Input**: Sequence of $K$ tensors (each size $N=25$ or similar).
* **Model**:
  * Linear Projection -> $d_{model}$
  * Positional Encoding (Time-based)
  * Transformer Encoder Block x $L$
  * Dense Head -> Sigmoid/Softmax over Numbers coverage.
* **Pros**: Simple, fast, focuses on pattern recognition in history.
* **Cons**: Ignores the "internal structure" of a draw (though Multi-Hot handles it implicitly).

### Option B: "Next Token Prediction" (Masked Language Model style)

Treat every number in the history as a token.
Separators between draws (SPECIAL_TOKEN_DRAW_SEP).
Predict the next numbers token by token?

* **Pros**: extremely powerful for finding relationships between specific numbers across draws.
* **Cons**: Order within a draw doesn't matter (sets), so imposing an order (sorted) might introduce bias.

### Recommendation (Start Simple)

We should proceed with **Option A**.
It aligns with our current "Time Series of Features" mindset but upgrades the mechanism to Attention.

## Implementation Steps

1. **Data Prep**: Create a sliding window dataset $X \in (Batch, SeqLen, FeatDim)$.
   * FeatDim could be just the Multi-Hot vector of numbers (Length 25 for Lotofacil).
2. **Model**:
   * Use `keras.layers.MultiHeadAttention` or PyTorch `nn.TransformerEncoder`.
   * Since we use Tensorflow in `requirements.txt`, we stick to Keras/TF.

## Technical Implications: TensorFlow vs PyTorch

### Sticking with TensorFlow (Keras) - **Recommended**

* **Implications**:
  * **Consistency**: We already use Keras for `LSTMModel`. The codebase remains unified.
  * **Performance**: `tensorflow[and-cuda]` is already installed and optimized. No new download.
  * **Capability**: Keras has robust `MultiHeadAttention` layers standard since TF 2.5+. It handles this architecture easily.
  * **Downside**: Slightly less "trendy" in academic research papers than PyTorch, but fully capable for production engineering.

### Introducing PyTorch

* **Implications**:
  * **Bloat**: Adds a massive dependency (~1-2GB). The Docker image size will balloon.
  * **Complexity**: We would have two distinct deep learning backends. Debugging CUDA issues becomes harder (TF and Torch competing for GPU memory).
  * **Benefit**: Easier to use "Cutting Edge" research code if we heavily pivot to custom dynamic graphs later.

### Decision Record

* **Architecture**: Option A (Draw-level embeddings) - **APPROVED**
* **Framework**: Recommendation is **TensorFlow/Keras** to keep the project "Low Chaos" in terms of dependencies.
