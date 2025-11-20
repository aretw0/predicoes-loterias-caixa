import pandas as pd
import os

class DataManager:
    """Handles data fetching and optional caching."""
    
    @staticmethod
    def load_csv(url: str) -> pd.DataFrame:
        """Loads a CSV from a URL."""
        try:
            return pd.read_csv(url)
        except Exception as e:
            print(f"Error loading data from {url}: {e}")
            raise e
