import random
import pandas as pd
from .base import Model

class RandomModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Random Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count

    def train(self, data: pd.DataFrame):
        # Random model doesn't need training
        pass

    def predict(self, **kwargs) -> list:
        return sorted(random.sample(range(self.range_min, self.range_max + 1), self.draw_count))

class FrequencyModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Frequency Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.weights = None

    def train(self, data: pd.DataFrame):
        # Calculate frequency of each number
        all_numbers = data['dezenas'].explode()
        frequency = all_numbers.value_counts().sort_index()
        
        # Ensure all numbers in range are present
        full_index = pd.Index(range(self.range_min, self.range_max + 1), name='dezenas')
        frequency = frequency.reindex(full_index, fill_value=0)
        
        # Normalize to get probabilities (weights)
        self.weights = frequency / frequency.sum()

    def predict(self, **kwargs) -> list:
        if self.weights is None:
            raise ValueError("Model has not been trained yet.")
            
        # Select numbers based on frequency weights
        # We use random.choices which allows replacement, but lottery numbers must be unique.
        # So we might need to sample more and take unique ones, or use numpy.random.choice with replace=False
        # Since we want to avoid numpy dependency if possible for simple logic, let's use a weighted sample approach.
        
        # A simple approach using pandas sample
        prediction = self.weights.sample(n=self.draw_count, weights=self.weights, replace=False).index.tolist()
        return sorted(prediction)
