import tensorflow as tf
from typing import Dict, Any

class TrainingLoggerCallback(tf.keras.callbacks.Callback):
    def __init__(self, logger, model_type: str, params_hash: str = None, metadata: Dict[str, Any] = None):
        super().__init__()
        self.logger = logger
        self.model_type = model_type
        self.params_hash = params_hash
        self.metadata = metadata

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        # Keras epochs are 0-indexed, we log as 1-indexed
        self.logger.log_epoch(
            self.model_type, 
            epoch + 1, 
            metrics={
                "loss": logs.get("loss"), 
                "accuracy": logs.get("accuracy"), 
                "val_loss": logs.get("val_loss"), 
                "val_accuracy": logs.get("val_accuracy")
            },
            params_hash=self.params_hash,
            metadata=self.metadata
        )
