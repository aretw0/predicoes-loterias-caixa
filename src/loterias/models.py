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

    def predict(self, count: int = None, **kwargs) -> list:
        final_count = count if count is not None else self.draw_count
        seed = kwargs.get('seed')
        
        rng = random.Random(seed) if seed is not None else random
        return sorted(rng.sample(range(self.range_min, self.range_max + 1), final_count))

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

    def predict(self, count: int = None, **kwargs) -> list:
        if self.weights is None:
            raise ValueError("Model has not been trained yet.")
            
        final_count = count if count is not None else self.draw_count
        order = kwargs.get('order', 'asc')
        
        # Convert Series to DataFrame for multi-column sorting
        df = self.weights.reset_index(name='weight')
        
        if order == 'asc':
            # Least frequent numbers
            # Sort by weight (asc), then by dezenas (asc) for determinism
            sorted_df = df.sort_values(by=['weight', 'dezenas'], ascending=[True, True])
        else:
            # Most frequent numbers
            # Sort by weight (desc), then by dezenas (asc) for determinism
            sorted_df = df.sort_values(by=['weight', 'dezenas'], ascending=[False, True])
            
        prediction = sorted_df.head(final_count)['dezenas'].tolist()
            
        return sorted(prediction)
