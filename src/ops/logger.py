import os
import pandas as pd
from datetime import datetime
import json
from typing import Dict, Any

class TrainingLogger:
    def __init__(self, filepath: str = "data/training_log.csv"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the CSV file exists with the correct headers."""
        columns = [
            "timestamp", "model_type", "epoch", 
            "loss", "accuracy", "val_loss", "val_accuracy", 
            "params_hash", "metadata"
        ]
        
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.filepath, index=False)

    def log_epoch(self, 
                  model_type: str, 
                  epoch: int, 
                  metrics: Dict[str, float],
                  params_hash: str = None,
                  metadata: Dict[str, Any] = None):
        """
        Logs a single epoch's metrics.
        """
        row = {
            "timestamp": datetime.now().isoformat(),
            "model_type": model_type,
            "epoch": epoch,
            "loss": metrics.get('loss'),
            "accuracy": metrics.get('accuracy'),
            "val_loss": metrics.get('val_loss'),
            "val_accuracy": metrics.get('val_accuracy'),
            "params_hash": params_hash,
            "metadata": json.dumps(metadata) if metadata else None
        }
        
        df = pd.DataFrame([row])
        # robust append
        if os.path.exists(self.filepath):
             df.to_csv(self.filepath, mode='a', header=False, index=False)
        else:
             df.to_csv(self.filepath, mode='w', header=True, index=False)
             
    def get_history(self, model_type: str = None, params_hash: str = None) -> pd.DataFrame:
        if not os.path.exists(self.filepath):
            return pd.DataFrame()
        try:
            df = pd.read_csv(self.filepath)
        except Exception:
            return pd.DataFrame()
            
        if model_type:
            df = df[df['model_type'] == model_type]
        if params_hash:
            df = df[df['params_hash'] == params_hash]
            
        return df
