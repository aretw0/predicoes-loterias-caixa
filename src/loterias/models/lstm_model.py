import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input
from ..base import Model
from ..features import calculate_sum, count_odds, count_evens, calculate_spread

class LSTMModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("LSTM Deep Learning")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.tokenizer_num_words = range_max + 2 
        self.model = None
        self.window_size = 10 
        self.units = 128
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
        # Input shape: (Window Size, Input Size)
        model = Sequential()
        model.add(Input(shape=(self.window_size, self.input_size)))
        model.add(LSTM(self.units, return_sequences=False))
        model.add(Dense(self.range_max + 1, activation='sigmoid'))
        
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model = model

    def train(self, data: pd.DataFrame, epochs: int = 50, batch_size: int = 32, **kwargs):
        # Cast to int (CLI passes strings)
        epochs = int(epochs)
        batch_size = int(batch_size)
        
        # Hyperparameter Overrides
        if 'window_size' in kwargs:
            self.window_size = int(kwargs['window_size'])
        if 'units' in kwargs:
            self.units = int(kwargs['units'])
            
        # Re-build model if parameters changed (or first run)
        # Note: If model already exists, rebuilding it resets weights. 
        # For hyperparam tuning, this is desired.
        if self.units != 128 or self.model is None: # Simple check, or just always rebuild if not trained?
             # For safety, let's rebuild if not None but we want to be sure about units.
             # Actually _build_model uses self.units.
             self._build_model()

        print(f"Training LSTM: epochs={epochs}, batch={batch_size}, window={self.window_size}, units={self.units}")
        X, y = self._prepare_sequences(data)

        # Store last window for prediction
        ball_cols = [c for c in data.columns if 'bola' in c.lower() or 'dezenas' in c.lower()]
        draws = data[ball_cols].values.tolist()
        if len(draws) >= self.window_size:
            self.last_window = draws[-self.window_size:]
        else:
            self.last_window = None
        
        if len(X) == 0:
            print("Not enough data to train LSTM.")
            return

        if self.model is None:
            self._build_model()
            
        history = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)
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
            
            # Optimization: Use __call__ instead of predict() for faster single-batch inference 
            # and to avoid retracing warnings in loops.
            # Output of __call__ is a Tensor, convert to numpy.
            prediction_tensor = self.model(X_input, training=False)
            probs = prediction_tensor.numpy()[0]
            
            final_count = kwargs.get('count', self.draw_count)
            # Ensure final_count is int
            if final_count is None: final_count = self.draw_count
            final_count = int(final_count)

            top_indices = probs.argsort()[-final_count:][::-1]
            return sorted([int(x) for x in top_indices])
        
        return []

    def save(self, path: str):
        import pickle
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
        else:
             print(f"Warning: Keras model {keras_path} not found.")
