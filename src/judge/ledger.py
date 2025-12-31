import os
import pandas as pd
from datetime import datetime
import json
from typing import List, Dict, Any, Union

class PredictionLedger:
    def __init__(self, filepath: str = "data/ledger.csv"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the CSV file exists with the correct headers."""
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            df = pd.DataFrame(columns=[
                "timestamp", "game", "draw_number", "model_name", 
                "predicted_numbers", "outcome"
            ])
            df.to_csv(self.filepath, index=False)

    def log_prediction(self, 
                       model_name: str, 
                       game: str, 
                       draw_number: int, 
                       predicted_numbers: List[int],
                       outcome: str = None):
        """
        Logs a single prediction to the ledger.
        """
        # Format predicted_numbers as simplified string/json for storage
        # Using simple JSON string for robust parsing later
        pred_str = json.dumps(sorted(list(predicted_numbers)))
        
        new_row = {
            "timestamp": datetime.now().isoformat(),
            "game": game,
            "draw_number": draw_number,
            "model_name": model_name,
            "predicted_numbers": pred_str,
            "outcome": outcome
        }
        
        # Append to CSV
        # We use mode='a' and header=False to append efficiently
        df = pd.DataFrame([new_row])
        df.to_csv(self.filepath, mode='a', header=not os.path.exists(self.filepath), index=False)

    def fetch_history(self, model_name: str = None, game: str = None) -> pd.DataFrame:
        """
        Retrieves prediction history, optionally filtering by model or game.
        """
        if not os.path.exists(self.filepath):
            return pd.DataFrame()
            
        try:
            df = pd.read_csv(self.filepath)
        except pd.errors.EmptyDataError:
             return pd.DataFrame()

        if model_name:
            df = df[df['model_name'] == model_name]
        
        if game:
            df = df[df['game'] == game]
            
        return df

    def get_last_draw_number(self, game: str) -> int:
        """Returns the last draw number logged for a specific game."""
        df = self.fetch_history(game=game)
        if df.empty:
            return 0
        return int(df['draw_number'].max())
