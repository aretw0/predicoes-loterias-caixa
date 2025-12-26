import random
import pandas as pd
import numpy as np
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

class GapModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Gap Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.gaps = None

    def train(self, data: pd.DataFrame):
        # Calculate gaps (draws since last appearance) for each number
        # data['dezenas'] is a Series of lists
        
        last_indices = {}
        total_draws = len(data)
        
        # Iterate over all possible numbers
        for n in range(self.range_min, self.range_max + 1):
            # Find all draws where n appeared
            # This is a bit slow but robust
            is_in_draw = data['dezenas'].apply(lambda x: n in x)
            # Get indices where true
            indices = is_in_draw.index[is_in_draw].tolist()
            
            if indices:
                # Use implicit index (assuming data is sorted by date/draw, or at least sequential index)
                # But safer to use position
                last_idx = total_draws - 1 # Current (imaginary) draw index
                
                # If we assume data index is 0..N-1
                # But let's check if index is integer or something else
                # Actually, data is dataframe.
                # Let's use iloc logic manually
                
                # Finding the last occurrence in the provided dataframe
                # We can just use the last true value
                # indices are labels.
                
                # Let's rely on position:
                # Convert to boolean numpy array
                mask = is_in_draw.to_numpy() # Boolean array
                true_indices = np.where(mask)[0]
                
                if len(true_indices) > 0:
                    last_pos = true_indices[-1]
                    current_gap = total_draws - 1 - last_pos
                else:
                    current_gap = total_draws # Never appeared
                    
                last_indices[n] = current_gap
            else:
                last_indices[n] = total_draws
        
        self.gaps = pd.Series(last_indices, name='gap')
        self.gaps.index.name = 'dezenas'

    def predict(self, count: int = None, **kwargs) -> list:
        if self.gaps is None:
            raise ValueError("Model has not been trained yet.")
        
        final_count = count if count is not None else self.draw_count
        
        # Sort by gap (descending) -> Most due
        # Deterministic tie-breaking: by number (asc)
        df = self.gaps.reset_index(name='gap')
        
        # We want largest gap first. If gaps are equal, smaller number first.
        sorted_df = df.sort_values(by=['gap', 'dezenas'], ascending=[False, True])
        
        prediction = sorted_df.head(final_count)['dezenas'].tolist()
        return sorted(prediction)

class SurfingModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Surfing Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.frequencies = None
        self.window_size = 30 # Default window size

    def train(self, data: pd.DataFrame):
        # Only look at the last N draws
        subset = data.tail(self.window_size)
        
        all_numbers = subset['dezenas'].explode()
        if all_numbers.empty:
            # Fallback to zeros if window is empty
            self.frequencies = pd.Series(0, index=pd.Index(range(self.range_min, self.range_max + 1), name='dezenas'))
            return

        counts = all_numbers.value_counts().sort_index()
        
        # Ensure all numbers are present
        full_index = pd.Index(range(self.range_min, self.range_max + 1), name='dezenas')
        counts = counts.reindex(full_index, fill_value=0)
        
        self.frequencies = counts

    def predict(self, count: int = None, **kwargs) -> list:
        if self.frequencies is None:
            raise ValueError("Model has not been trained yet.")
            
        final_count = count if count is not None else self.draw_count
        
        # Sort by frequency (descending) -> "Hot" numbers
        # Deterministic tie-breaking: by number (asc)
        df = self.frequencies.reset_index(name='count')
        
        sorted_df = df.sort_values(by=['count', 'dezenas'], ascending=[False, True])
        
        prediction = sorted_df.head(final_count)['dezenas'].tolist()
        return sorted(prediction)
