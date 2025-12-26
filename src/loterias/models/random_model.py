import random
import pandas as pd
from ..base import Model

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
