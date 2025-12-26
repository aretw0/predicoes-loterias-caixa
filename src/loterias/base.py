from abc import ABC, abstractmethod
import pandas as pd
import json
import os

class Lottery(ABC):
    """Abstract base class for a Lottery game."""
    
    def __init__(self, name: str, data_url: str, slug: str):
        self.name = name
        self.data_url = data_url
        self.slug = slug
        self.data = None

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Loads the lottery data."""
        pass

    @abstractmethod
    def preprocess_data(self) -> pd.DataFrame:
        """Preprocesses the loaded data."""
        pass

    def get_price(self, quantity: int = None) -> float:
        """Gets the current price of a bet for this lottery based on quantity of numbers."""
        try:
            from .config import get_prices_config
            
            prices_data = get_prices_config()
            game_data = prices_data.get(self.slug, {})
            
            if not game_data:
                return 0.0
            
            # If quantity is not provided, use the minimum quantity (first key in prices)
            if quantity is None:
                # Find min quantity
                quantities = [int(k) for k in game_data.get('prices', {}).keys()]
                if not quantities:
                    return 0.0
                quantity = min(quantities)
            
            return game_data.get('prices', {}).get(str(quantity), 0.0)
        except Exception as e:
            print(f"Error loading price for {self.name}: {e}")
            return 0.0

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

class ModelFactory:
    """Factory for creating prediction models."""
    
    @staticmethod
    def create_model(model_type: str, range_min: int, range_max: int, draw_count: int) -> Model:
        from .models import RandomModel, FrequencyModel, GapModel, SurfingModel
        
        if model_type == 'random':
            return RandomModel(range_min, range_max, draw_count)
        elif model_type == 'frequency':
            return FrequencyModel(range_min, range_max, draw_count)
        elif model_type == 'gap':
            return GapModel(range_min, range_max, draw_count)
        elif model_type == 'surfing':
            return SurfingModel(range_min, range_max, draw_count)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
