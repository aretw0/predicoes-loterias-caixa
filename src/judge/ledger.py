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
        columns = [
            "timestamp", "game", "draw_number", "model_name", 
            "predicted_numbers", "outcome", "metadata"
        ]
        
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.filepath, index=False)
        else:
            # Migration check: Append metadata column if missing
            try:
                df = pd.read_csv(self.filepath)
                if 'metadata' not in df.columns:
                    df['metadata'] = None
                    df.to_csv(self.filepath, index=False)
            except Exception as e:
                print(f"Warning: Could not check schema migration: {e}")

    def log_prediction(self, 
                       model_name: str, 
                       game: str, 
                       draw_number: int, 
                       predicted_numbers: List[int],
                       outcome: str = None,
                       metadata: Dict[str, Any] = None):
        """
        Logs a single prediction to the ledger.
        """
        # Format predicted_numbers as simplified string/json for storage
        pred_str = json.dumps(sorted(list(predicted_numbers)))
        meta_str = json.dumps(metadata) if metadata else None
        
        new_row = {
            "timestamp": datetime.now().isoformat(),
            "game": game,
            "draw_number": draw_number,
            "model_name": model_name,
            "predicted_numbers": pred_str,
            "outcome": outcome,
            "metadata": meta_str
        }
        
        # Append to CSV
        df = pd.DataFrame([new_row])
        # Force column order if possible, but append mode handles it usually or we use full write if header mismatch
        # Simpler to just append to existing file
        if os.path.exists(self.filepath):
             df.to_csv(self.filepath, mode='a', header=False, index=False)
        else:
             df.to_csv(self.filepath, mode='w', header=True, index=False)

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
