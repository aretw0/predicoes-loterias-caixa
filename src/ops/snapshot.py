import os
import tensorflow as tf
import pandas as pd
from typing import List, Optional, Callable, Dict, Any
from core.base import Lottery
from core.games.megasena import MegaSena
from models.deep.transformer import TransformerModel
from models.deep.lstm import LSTMModel
from models.deep.autoencoder import AutoEncoderModel
from models.tree.catboost import CatBoostModel

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

    def _get_model_path(self, model_name: str, context: str, extension: str, params: Dict[str, Any] = None) -> str:
        """
        Generates a VERSIONED path: snapshots/{game}/{context}/{generated_name}
        """
        base = os.path.join(self.base_dir, self.lottery.name.lower(), context)
        self._ensure_dir(base)
        
        # Use SnapshotVersioning to generate name
        from ops.versioning import SnapshotVersioning
        filename = SnapshotVersioning.generate_versioned_filename(model_name, extension, params)
        
        return os.path.join(base, filename)

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
        from ops.logger import TrainingLogger
        from ops.callbacks import TrainingLoggerCallback
        
        logger = TrainingLogger()
        
        # 1. Transformer
        if 'transformer' in models:
            print(f" >> Training Transformer [{context}]...")
            try:
                model = TransformerModel(1, 60, 6)
                
                # Callback setup
                cb = TrainingLoggerCallback(
                    logger=logger, 
                    model_type="transformer", 
                    params_hash="snapshot_run", 
                    metadata={'context': context}
                )
                
                model.train(df, epochs=epochs, batch_size=64, verbose=0, callbacks=[cb])
                
                params = {'epochs': epochs, 'batch_size': 64}
                path_with_ext = self._get_model_path("transformer", context, "keras", params)
                path_base = path_with_ext.replace(".keras", "") 
                
                model.save(path_base)
                print(f"    Saved: {path_with_ext}")
            except Exception as e:
                print(f"    Error: {e}")

        # 2. LSTM
        if 'lstm' in models:
            print(f" >> Training LSTM [{context}]...")
            try:
                model = LSTMModel(1, 60, 6)
                
                cb = TrainingLoggerCallback(
                    logger=logger, 
                    model_type="lstm", 
                    params_hash="snapshot_run",
                    metadata={'context': context}
                )
                
                model.train(df, epochs=epochs, batch_size=32, verbose=0, callbacks=[cb])
                
                params = {'epochs': epochs, 'batch_size': 32}
                path_with_ext = self._get_model_path("lstm", context, "keras", params)
                path_base = path_with_ext.replace(".keras", "")
                
                model.save(path_base)
                print(f"    Saved: {path_with_ext}")
            except Exception as e:
                print(f"    Error: {e}")

        # 3. AutoEncoder (Fiscal)
        if 'autoencoder' in models:
            print(f" >> Training AutoEncoder (Fiscal) [{context}]...")
            try:
                model = AutoEncoderModel(1, 60, 6, latent_dim=16) 
                # Note: AutoEncoderModel.train might also need update to accept callbacks
                # Attempting to pass it anyway via kwargs if supported
                model.train(df, epochs=int(epochs/2)+10, batch_size=32, verbose=0)
                
                params = {'epochs': int(epochs/2)+10, 'latent_dim': 16}
                path_with_ext = self._get_model_path("autoencoder_fiscal", context, "keras", params)
                path_base = path_with_ext.replace(".keras", "")
                
                model.save(path_base)
                print(f"    Saved: {path_with_ext}")
            except Exception as e:
                print(f"    Error: {e}")

        # 4. CatBoost
        if 'catboost' in models:
            print(f" >> Training CatBoost [{context}]...")
            try:
                model = CatBoostModel(1, 60, 6)
                params = {'verbose': 0}
                if self.gpu_enabled:
                    params['task_type'] = 'GPU'
                    
                # CatBoost doesn't support Keras callbacks directly, skipping logs for now
                # or we could log final metric manually
                model.train(df, **params)
                
                path_with_ext = self._get_model_path("catboost", context, "cbm", params)
                path_base = path_with_ext.replace(".cbm", "")
                
                model.save(path_base)
                print(f"    Saved: {path_with_ext}")
            except Exception as e:
                print(f"    Error: {e}")
