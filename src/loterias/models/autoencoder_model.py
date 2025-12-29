from .base import Model
import pandas as pd

class AutoEncoderModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("AutoEncoder (Anomaly)")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model = None

    def train(self, data: pd.DataFrame, **kwargs):
        """
        Trains an AutoEncoder to learn the representation of 'valid' lottery draws.
        """
        raise NotImplementedError("AutoEncoder implementation pending for v0.6.0")

    def predict(self, **kwargs) -> list:
        """
        Scoring method: Returns reconstruction error or filters input.
        """
        raise NotImplementedError("AutoEncoder implementation pending for v0.6.0")
