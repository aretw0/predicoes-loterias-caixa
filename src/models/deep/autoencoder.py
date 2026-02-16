import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input, Dropout
from core.base import Model
import pickle
import os

class AutoEncoderModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int, latent_dim: int = 16):
        super().__init__("AutoEncoder Anomaly Detector")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model = None
        # Input size is simply the range of numbers (one-hot encoded draw)
        self.input_size = self.range_max + 1
        self.encoding_dim = latent_dim # Bottleneck size configurable

    def _draw_to_onehot(self, draw):
        vec = np.zeros(self.input_size)
        for num in draw:
            try:
                n = int(num)
                if 0 <= n <= self.range_max:
                    vec[n] = 1.0
            except Exception:
                pass
        return vec

    def _prepare_data(self, data: pd.DataFrame):
        ball_cols = [c for c in data.columns if 'bola' in c.lower() or 'dezenas' in c.lower()]
        draws = data[ball_cols].values.tolist()
        
        X = []
        for d in draws:
            X.append(self._draw_to_onehot(d))
            
        return np.array(X)

    def _build_model(self):
        # Dense AutoEncoder
        # Input -> Encoder -> Bottleneck -> Decoder -> Output
        model = Sequential()
        model.add(Input(shape=(self.input_size,)))
        # Encoder
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.1))
        # Bottleneck
        model.add(Dense(self.encoding_dim, activation='relu'))
        # Decoder
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.1))
        # Output (Reconstruction) - Sigmoid for multi-label probabilities
        model.add(Dense(self.input_size, activation='sigmoid'))
        
        model.compile(optimizer='adam', loss='binary_crossentropy')
        self.model = model

    def train(self, data: pd.DataFrame, epochs: int = 50, batch_size: int = 32, **kwargs):
        epochs = int(epochs)
        batch_size = int(batch_size)
        
        X = self._prepare_data(data)
        
        if self.model is None:
            self._build_model()
            
        # AutoEncoder trains to reconstruct input (X -> X)
        print(f"Training AutoEncoder: epochs={epochs}, batch={batch_size}, latent={self.encoding_dim}")
        callbacks = kwargs.get('callbacks', [])
        history = self.model.fit(X, X, epochs=epochs, batch_size=batch_size, verbose=1, shuffle=True, callbacks=callbacks)
        return history

    def predict(self, **kwargs) -> list:
        # For an AutoEncoder, "predict" usually means "reconstruct" or "score".
        # But our interface expects a list of numbers.
        # Maybe return the most probable reconstruction of the last draw?
        # Or if used as a generator, return a random valid-looking draw?
        
        # NOTE: This model is primarily a VALIDATOR. 
        # But to satisfy the abstract base class, let's implement a 'reconstruction' prediction
        # based on the last draw, or just random generation refined by the AE?
        
        # Let's implemented a simple "denoising" or "refinement" of the last draw if provided,
        # otherwise it's hard to use as a primary predictor.
        
        # For now, return empty list or throw warning, as it's meant for validation.
        print("Warning: AutoEncoder is designed for validation (--validator-model), not primary prediction.")
        return []

    def validate(self, numbers: list) -> float:
        """
        Calculates anomaly score for a given set of numbers.
        Lower score = More "normal" (better reconstruction).
        Higher score = Anomaly.
        """
        if self.model is None:
            raise ValueError("Model not trained.")
            
        vec = self._draw_to_onehot(numbers)
        reconstruction = self.model.predict(np.array([vec]), verbose=0)[0]
        
        # Calculate reconstruction error (MSE)
        mse = np.mean(np.power(vec - reconstruction, 2))
        return float(mse)

    def save(self, path: str):
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
        
        keras_path = path + ".keras"
        # Backward compatibility check (if user points to .keras directly)
        if path.endswith(".keras"):
            keras_path = path
            path.replace(".keras", "") 
            # This might fail if pickle doesn't exist, we need the wrapper.
            # Assume standar usage via CLI: path without extension or path to save file.
        
        if not os.path.exists(path) and os.path.exists(path + ".keras"):
             # User probably passed the keras file path, but we need the wrapper pickle
             # This is tricky. Let's assume standard usage: load(wrapper_path)
             pass

        try:
            with open(path, 'rb') as f:
                loaded = pickle.load(f)
                self.__dict__.update(loaded.__dict__)
        except Exception as e:
            print(f"Error loading wrapper {path}: {e}")
            # If wrapper fails, we can't really restore state easily without re-init.
            return

        if os.path.exists(keras_path):
            self.model = load_model(keras_path)
        else:
             print(f"Warning: Keras model {keras_path} not found.")
