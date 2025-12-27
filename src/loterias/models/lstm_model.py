import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input
from ..base import Model

class LSTMModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("LSTM Deep Learning")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.tokenizer_num_words = range_max + 2  # +1 for 0-index (unused), +1 for padding if needed, safely cover max
        self.model = None
        self.window_size = 10 # Number of past draws to look at

    def _prepare_sequences(self, data: pd.DataFrame):
        # Extract all numbers as a single sequence of draws
        # Assuming data columns are like 'bola1', 'bola2', ...
        # reliable way: extract all numeric columns that look like balls
        ball_cols = [c for c in data.columns if 'bola' in c.lower() or 'dezenas' in c.lower()]
        # Sort values to ensure deterministic order within a draw if needed, 
        # but usually draws are given in ascending order.
        
        sequences = []
        targets = []
        
        # Convert dataframe to a list of lists (draws)
        draws = data[ball_cols].values.tolist()
        
        # We need to flatten? No, LSTM for this usually takes a sequence of sets (draws) 
        # or we treat it as a long sequence of numbers. 
        # Better approach for lottery: Sequence of sets is hard. 
        # Simplified approach: Treat each draw as a "word" is impossible because it is a set.
        # Alternative: Multi-hot encoding for each draw?
        # Let's try: Input = Sequence of last N draws (multi-hot encoded). Output = Next draw (multi-hot).
        
        X = []
        y = []
        
        rows = len(draws)
        if rows <= self.window_size:
            return np.array([]), np.array([])

        for i in range(rows - self.window_size):
            window = draws[i : i + self.window_size]
            target = draws[i + self.window_size]
            
            # Simple encoding: flattened or specialized? 
            # Let's use simple flattened sequence for now if we use Embedding, 
            # BUT Embedding expects single integers. 
            # If we want to predict a SET, we typically use Multi-Label classification.
            # Input: (Window Size, Draw Count) -> Flattened? 
            # Reference concept: "See story of numbers".
            
            # Let's treat it as a time series of features.
            # Feature vector for a draw: Multi-hot vector of size (range_max + 1)
            
            X.append(self._draws_to_multihot(window))
            y.append(self._draw_to_multihot(target))
            
        return np.array(X), np.array(y)

    def _draw_to_multihot(self, draw):
        vec = np.zeros(self.range_max + 1)
        for num in draw:
            try:
                n = int(num)
                if 0 <= n <= self.range_max:
                    vec[n] = 1.0
            except:
                pass
        return vec

    def _draws_to_multihot(self, draws):
        return np.array([self._draw_to_multihot(d) for d in draws])

    def _build_model(self):
        # Input shape: (Window Size, Max Number + 1)
        # Output shape: (Max Number + 1) -> Sigmoid for multi-label
        
        model = Sequential()
        model.add(Input(shape=(self.window_size, self.range_max + 1)))
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
