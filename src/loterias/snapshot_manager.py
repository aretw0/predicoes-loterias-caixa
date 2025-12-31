import os
import tensorflow as tf
import pandas as pd
from typing import List, Optional, Callable, Dict, Any
from .base import Lottery
from .megasena import MegaSena
from .models import TransformerModel, LSTMModel, AutoEncoderModel
from .models.catboost_model import CatBoostModel

class SnapshotManager:
    """
    Orchestrator for cultivating (training) and saving model snapshots.
    Designed to be used in 'snapshot_factory.ipynb'.
    """
    def __init__(self, lottery: Lottery = None, base_dir: str = "snapshots"):
        self.lottery = lottery if lottery else MegaSena()
        self.base_dir = base_dir
        self.gpu_enabled = len(tf.config.list_physical_devices('GPU')) > 0
        
        print(f"SnapshotManager initialized for {self.lottery.name}")
        print(f"Base Directory: {self.base_dir}")
        print(f"GPU Acceleration: {'ENABLED' if self.gpu_enabled else 'DISABLED'}")

    def _ensure_dir(self, path: str):
        os.makedirs(path, exist_ok=True)

    def _get_model_path(self, model_name: str, context: str) -> str:
        """
        Generates standard path: snapshots/{game}/{context}/{model_name}_v1
        """
        # Clean paths (no version extension here, save() handles it)
        base = os.path.join(self.base_dir, self.lottery.name.lower(), context)
        self._ensure_dir(base)
        return os.path.join(base, model_name)

    def cultivate_generalists(self, 
                            epochs: int = 100, 
                            models: List[str] = ['transformer', 'lstm', 'catboost', 'autoencoder'],
                            force_retrain: bool = True):
        """
        Trains models on the FULL dataset.
        """
        print("\n=== Cultivating GENERALISTS (Full History) ===")
        df = self.lottery.preprocess_data()
        print(f"Dataset Size: {len(df)} draws")
        
        self._train_batch(df, "generalistas", models, epochs)

    def cultivate_specialists(self, 
                            filter_name: str,
                            filter_func: Callable[[pd.DataFrame], pd.DataFrame],
                            epochs: int = 150,
                            models: List[str] = ['transformer', 'lstm', 'catboost', 'autoencoder']):
        """
        Trains models on a FILTERED dataset (e.g. Acumulados).
        """
        print(f"\n=== Cultivating SPECIALISTS ({filter_name}) ===")
        df_full = self.lottery.preprocess_data()
        df_filtered = filter_func(df_full)
        
        print(f"Original Size: {len(df_full)} -> Filtered Size: {len(df_filtered)}")
        
        if len(df_filtered) < 50:
            print(f"Warning: Filtered dataset too small ({len(df_filtered)}). Results may be poor.")
            
        self._train_batch(df_filtered, f"especialistas/{filter_name}", models, epochs)

    def _train_batch(self, df: pd.DataFrame, context: str, models: List[str], epochs: int):
        
        # 1. Transformer
        if 'transformer' in models:
            print(f" >> Training Transformer [{context}]...")
            try:
                model = TransformerModel(1, 60, 6)
                model.train(df, epochs=epochs, batch_size=64, verbose=0)
                path = self._get_model_path("transformer_v1", context)
                model.save(path)
                print(f"    Saved: {path}")
            except Exception as e:
                print(f"    Error: {e}")

        # 2. LSTM
        if 'lstm' in models:
            print(f" >> Training LSTM [{context}]...")
            try:
                model = LSTMModel(1, 60, 6)
                model.train(df, epochs=epochs, batch_size=32, verbose=0)
                path = self._get_model_path("lstm_v1", context)
                model.save(path)
                print(f"    Saved: {path}")
            except Exception as e:
                print(f"    Error: {e}")

        # 3. AutoEncoder (Fiscal)
        if 'autoencoder' in models:
            print(f" >> Training AutoEncoder (Fiscal) [{context}]...")
            try:
                # Latent dim 16 is good default
                model = AutoEncoderModel(1, 60, 6, latent_dim=16) 
                # AE needs less epochs usually, but robust config is fine
                model.train(df, epochs=int(epochs/2)+10, batch_size=32, verbose=0)
                path = self._get_model_path("autoencoder_fiscal_v1", context)
                model.save(path)
                print(f"    Saved: {path}")
            except Exception as e:
                print(f"    Error: {e}")

        # 4. CatBoost
        if 'catboost' in models:
            print(f" >> Training CatBoost [{context}]...")
            try:
                model = CatBoostModel(1, 60, 6)
                # CatBoost handles its own verbose
                # If GPU is enabled, we should try to pass task_type='GPU' via kwargs if model supports
                # Taking advantage of dynamic kwargs in train()
                params = {'verbose': 0}
                if self.gpu_enabled:
                    params['task_type'] = 'GPU'
                    
                model.train(df, **params)
                path = self._get_model_path("catboost_v1", context)
                model.save(path)
                print(f"    Saved: {path}")
            except Exception as e:
                print(f"    Error: {e}")
