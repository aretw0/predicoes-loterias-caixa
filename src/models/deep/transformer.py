import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model as KerasModel
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input, MultiHeadAttention, LayerNormalization, Dropout, GlobalAveragePooling1D
from core.base import Model
from data.features import calculate_sum, count_odds, count_evens, calculate_spread

class TransformerModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Transformer Attention")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model = None
        self.window_size = 10 
        
        # Hyperparameters
        self.head_size = 256
        self.num_heads = 4
        self.ff_dim = 256
        self.dropout = 0.1
        
        # Feature vector size: (range_max + 1) + 4 extra features (Sum, Odd, Even, Spread)
        self.input_size = (self.range_max + 1) + 4

    def _prepare_sequences(self, data: pd.DataFrame):
        ball_cols = [c for c in data.columns if 'bola' in c.lower() or 'dezenas' in c.lower()]
        
        sequences = []
        targets = []
        
        draws = data[ball_cols].values.tolist()
        
        X = []
        y = []
        
        rows = len(draws)
        if rows <= self.window_size:
            return np.array([]), np.array([])

        for i in range(rows - self.window_size):
            window = draws[i : i + self.window_size]
            target = draws[i + self.window_size]
            
            X.append(self._draws_to_multihot(window))
            y.append(self._draw_to_multihot(target, include_features=False)) # Target is just the numbers
            
        return np.array(X), np.array(y)

    def _draw_to_multihot(self, draw, include_features=True):
        # Base vector: One-hot for numbers
        vec = np.zeros(self.range_max + 1)
        valid_numbers = []
        for num in draw:
            try:
                n = int(num)
                if 0 <= n <= self.range_max:
                    vec[n] = 1.0
                    valid_numbers.append(n)
            except:
                pass
        
        if not include_features:
            return vec

        # Enrich with statistical features
        # Normalize to 0-1 range roughly to help Neural Net
        
        # 1. Sum Normalize: Max possible sum approx RangeMax * DrawCount
        max_sum_theoretical = self.range_max * self.draw_count
        s = calculate_sum(valid_numbers) / max_sum_theoretical
        
        # 2. Odd Normalize: Max is DrawCount
        o = count_odds(valid_numbers) / self.draw_count
        
        # 3. Even Normalize: Max is DrawCount
        e = count_evens(valid_numbers) / self.draw_count
        
        # 4. Spread Normalize: Max is RangeMax
        sp = calculate_spread(valid_numbers) / self.range_max
        
        # Append features
        features = np.array([s, o, e, sp])
        return np.concatenate([vec, features])

    def _draws_to_multihot(self, draws):
        return np.array([self._draw_to_multihot(d, include_features=True) for d in draws])

    def _build_model(self):
        # Define Input
        inputs = Input(shape=(self.window_size, self.input_size))
        
        # Transformer Block
        # 1. Multi-Head Self Attention
        attention_output = MultiHeadAttention(
            key_dim=self.head_size, num_heads=self.num_heads, dropout=self.dropout
        )(inputs, inputs)
        
        # 2. Add & Norm
        x = LayerNormalization(epsilon=1e-6)(attention_output + inputs)
        
        # 3. Feed Forward Part
        x_ff = Dense(self.ff_dim, activation="relu")(x)
        x_ff = Dropout(self.dropout)(x_ff)
        x_ff = Dense(self.input_size)(x_ff)
        
        # 4. Add & Norm
        x = LayerNormalization(epsilon=1e-6)(x_ff + x)
        
        # Output Head
        # Global Average Pooling to flatten the time dimension
        x = GlobalAveragePooling1D()(x)
        x = Dropout(self.dropout)(x)
        
        outputs = Dense(self.range_max + 1, activation='sigmoid')(x)
        
        model = KerasModel(inputs=inputs, outputs=outputs)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        self.model = model

    def train(self, data: pd.DataFrame, epochs: int = 50, batch_size: int = 32, **kwargs):
        # Cast to int
        epochs = int(epochs)
        batch_size = int(batch_size)
        
        # Hyperparameter Overrides
        if 'window_size' in kwargs:
            self.window_size = int(kwargs['window_size'])
        if 'head_size' in kwargs:
            self.head_size = int(kwargs['head_size'])
            
        if self.model is None: 
             self._build_model()

        print(f"Training Transformer: epochs={epochs}, batch={batch_size}, window={self.window_size}")
        X, y = self._prepare_sequences(data)

        # Store last window for prediction
        ball_cols = [c for c in data.columns if 'bola' in c.lower() or 'dezenas' in c.lower()]
        draws = data[ball_cols].values.tolist()
        if len(draws) >= self.window_size:
            self.last_window = draws[-self.window_size:]
        else:
            self.last_window = None
        
        if len(X) == 0:
            print("Not enough data to train Transformer.")
            return

        callbacks = kwargs.get('callbacks', [])
        history = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1, callbacks=callbacks)
        return history

    def predict(self, **kwargs) -> list:
        # Check if data is provided in kwargs, otherwise use stored last_window
        data = kwargs.get('data')
        current_window = None

        if data is not None and not data.empty:
            ball_cols = [c for c in data.columns if 'bola' in c.lower() or 'dezenas' in c.lower()]
            draws = data[ball_cols].values.tolist()
            if len(draws) >= self.window_size:
                current_window = draws[-self.window_size:]
        elif hasattr(self, 'last_window') and self.last_window is not None:
             current_window = self.last_window

        if current_window:
            X_input = np.array([self._draws_to_multihot(current_window)])
            
            if self.model is None:
                return []
            
            # Optimization: Use __call__ for faster inference
            prediction_tensor = self.model(X_input, training=False)
            probs = prediction_tensor.numpy()[0]
            
            # Mask out numbers below range_min (e.g. 0)
            if self.range_min > 0:
                probs[:self.range_min] = -1.0
            
            
            final_count = kwargs.get('count', self.draw_count)
            # Ensure final_count is int
            if final_count is None: final_count = self.draw_count
            final_count = int(final_count)

            top_indices = probs.argsort()[-final_count:][::-1]
            return sorted([int(x) for x in top_indices])
        
        return []

    def save(self, path: str):
        import pickle
        # Keras models can be saved to H5 or Keras format
        keras_path = path + ".keras"
        
        if self.model:
            self.model.save(keras_path)
            
        temp_model = self.model
        self.model = None
        
        try:
             with open(path, 'wb') as f:
                pickle.dump(self, f)
        finally:
            self.model = temp_model

    def load(self, path: str):
        import pickle
        from tensorflow.keras.models import load_model
        import os
        
        keras_path = path + ".keras"
        
        with open(path, 'rb') as f:
            loaded = pickle.load(f)
            self.__dict__.update(loaded.__dict__)
            
        if os.path.exists(keras_path):
            self.model = load_model(keras_path)
            # Compile logic is usually embedded in save/load for keras
        else:
             print(f"Warning: Keras model {keras_path} not found.")
