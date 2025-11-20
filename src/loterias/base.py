from abc import ABC, abstractmethod
import pandas as pd

class Lottery(ABC):
    """Abstract base class for a Lottery game."""
    
    def __init__(self, name: str, data_url: str):
        self.name = name
        self.data_url = data_url
        self.data = None

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Loads the lottery data."""
        pass

    @abstractmethod
    def preprocess_data(self) -> pd.DataFrame:
        """Preprocesses the loaded data."""
        pass

class Model(ABC):
    """Abstract base class for a Prediction Model."""
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def train(self, data: pd.DataFrame):
        """Trains the model with the given data."""
        pass

    @abstractmethod
    def predict(self, **kwargs) -> list:
        """Generates a prediction."""
        pass
