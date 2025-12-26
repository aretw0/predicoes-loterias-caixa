import pandas as pd
import numpy as np
from ..base import Model
from .frequency_model import FrequencyModel
from .gap_model import GapModel
from .surfing_model import SurfingModel

class HybridModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Hybrid Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        
        # Sub-models
        self.gap_model = GapModel(range_min, range_max, draw_count)
        self.freq_model = FrequencyModel(range_min, range_max, draw_count)
        self.surf_model = SurfingModel(range_min, range_max, draw_count)
        
        self.trained = False

    def train(self, data: pd.DataFrame):
        self.gap_model.train(data)
        self.freq_model.train(data)
        self.surf_model.train(data)
        self.trained = True

    def predict(self, count: int = None, **kwargs) -> list:
        if not self.trained:
             raise ValueError("Model has not been trained yet.")
        
        final_count = count if count is not None else self.draw_count
        
        # Parse weights from kwargs
        # Default weights: 1.0 (balanced)
        w_gap = float(kwargs.get('w_gap', 1.0))
        w_freq = float(kwargs.get('w_freq', 1.0))
        w_surf = float(kwargs.get('w_surf', 1.0))
        
        # --- 1. Gap Scores ---
        # Gaps are in self.gap_model.gaps (Series: index=number, value=gap)
        gap_series = self.gap_model.gaps.copy()
        # Normalize: Score = gap / max_gap
        max_gap = gap_series.max()
        if max_gap > 0:
            gap_scores = gap_series / max_gap
        else:
            gap_scores = gap_series * 0 # All zero if max is 0
            
        # --- 2. Frequency Scores ---
        # Weights are in self.freq_model.weights (Series: index=number, value=probability)
        freq_series = self.freq_model.weights.copy()
        # Normalize: Score = prob / max_prob
        max_prob = freq_series.max()
        if max_prob > 0:
            freq_scores = freq_series / max_prob
        else:
            freq_scores = freq_series * 0
            
        # --- 3. Surfing Scores ---
        # Counts are in self.surf_model.frequencies (Series: index=number, value=count)
        # Handle surfing window override
        surf_window = kwargs.get('window') 
        if surf_window:
             self.surf_model._calculate_frequencies(int(surf_window))
             
        surf_series = self.surf_model.frequencies.copy()
        # Normalize: Score = count / max_count
        max_count = surf_series.max()
        if max_count > 0:
            surf_scores = surf_series / max_count
        else:
            surf_scores = surf_series * 0
            
        # --- Combine Scores ---
        # Ensure all series are aligned by index (they should be, as models reindex to range)
        
        # Weighted Combination
        total_score = (w_gap * gap_scores) + (w_freq * freq_scores) + (w_surf * surf_scores)
        
        # --- Select Winners ---
        # Sort by total_score (descending), then number (ascending) for determinism
        df = total_score.reset_index(name='score')
        sorted_df = df.sort_values(by=['score', 'dezenas'], ascending=[False, True])
        
        prediction = sorted_df.head(final_count)['dezenas'].tolist()
        return sorted(prediction)
