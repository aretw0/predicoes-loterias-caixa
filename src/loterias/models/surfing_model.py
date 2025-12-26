import pandas as pd
from ..base import Model

class SurfingModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Surfing Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.frequencies = None
        self.window_size = 30 # Default window size

    def train(self, data: pd.DataFrame):
        self.data = data
        # Pre-calculate default frequencies
        self._calculate_frequencies(self.window_size)

    def _calculate_frequencies(self, window: int):
        subset = self.data.tail(window)
        
        all_numbers = subset['dezenas'].explode()
        if all_numbers.empty:
            self.frequencies = pd.Series(0, index=pd.Index(range(self.range_min, self.range_max + 1), name='dezenas'))
            return

        counts = all_numbers.value_counts().sort_index()
        
        full_index = pd.Index(range(self.range_min, self.range_max + 1), name='dezenas')
        counts = counts.reindex(full_index, fill_value=0)
        
        self.frequencies = counts

    def predict(self, count: int = None, **kwargs) -> list:
        if self.data is None:
             raise ValueError("Model has not been trained yet.")
        
        final_count = count if count is not None else self.draw_count
        
        # Check for window arg
        if 'window' in kwargs:
            try:
                window = int(kwargs['window'])
                self._calculate_frequencies(window)
            except ValueError:
                pass # Ignore invalid window
        elif self.frequencies is None:
             self._calculate_frequencies(self.window_size)
            
        # Sort by frequency (descending) -> "Hot" numbers
        df = self.frequencies.reset_index(name='count')
        
        sorted_df = df.sort_values(by=['count', 'dezenas'], ascending=[False, True])
        
        prediction = sorted_df.head(final_count)['dezenas'].tolist()
        return sorted(prediction)
