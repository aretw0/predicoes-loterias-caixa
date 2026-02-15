import pandas as pd
import os

class DataManager:
    """Handles data fetching, caching, and export in multiple formats."""
    
    @staticmethod
    def load_csv(url: str) -> pd.DataFrame:
        """Loads a CSV from a URL."""
        try:
            return pd.read_csv(url)
        except Exception as e:
            print(f"Error loading data from {url}: {e}")
            raise e

    @staticmethod
    def export_parquet(df: pd.DataFrame, path: str) -> str:
        """Exports a DataFrame to Parquet format for interoperability.
        
        Args:
            df: The DataFrame to export.
            path: Destination file path (should end in .parquet).
            
        Returns:
            The absolute path to the written file.
        """
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        df.to_parquet(path, engine="pyarrow", index=False)
        return os.path.abspath(path)

    @staticmethod
    def load_parquet(path: str) -> pd.DataFrame:
        """Loads a DataFrame from a Parquet file.
        
        Args:
            path: Path to the Parquet file.
            
        Returns:
            The loaded DataFrame.
        """
        return pd.read_parquet(path, engine="pyarrow")
