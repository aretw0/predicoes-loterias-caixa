from .base import Model
import pandas as pd

class TransformerModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Transformer (Attention)")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model = None

    def train(self, data: pd.DataFrame, **kwargs):
        raise NotImplementedError("Transformer implementation pending for v0.6.0")

    def predict(self, **kwargs) -> list:
        raise NotImplementedError("Transformer implementation pending for v0.6.0")
