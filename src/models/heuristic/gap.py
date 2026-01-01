import pandas as pd
import numpy as np
from core.base import Model

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
                
                # Finding the last occurrence in the provided dataframe
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
