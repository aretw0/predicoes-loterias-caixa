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
        model.add(LSTM(128, return_sequences=False))
        model.add(Dense(self.range_max + 1, activation='sigmoid'))
        
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model = model

    def train(self, data: pd.DataFrame, epochs: int = 50, batch_size: int = 32):
        print(f"Training LSTM for {epochs} epochs...")
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
                
            prediction = self.model.predict(X_input)
            probs = prediction[0]
            
            top_indices = probs.argsort()[-self.draw_count:][::-1]
            return sorted([int(x) for x in top_indices])
        
        return []
