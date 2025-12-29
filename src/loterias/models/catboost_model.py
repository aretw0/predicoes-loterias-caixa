from .base import Model
import pandas as pd

class CatBoostModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("CatBoost")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        # TODO: Initialize CatBoostClassifier here
        self.model = None

    def train(self, data: pd.DataFrame, **kwargs):
        raise NotImplementedError("CatBoost implementation pending for v0.6.0")

    def predict(self, **kwargs) -> list:
        raise NotImplementedError("CatBoost implementation pending for v0.6.0")
