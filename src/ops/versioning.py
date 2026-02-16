import os
import glob
import datetime
import hashlib
import json
from typing import Optional, Dict, Any

class SnapshotVersioning:
    """
    Manages model snapshot versioning to prevent overwrites and track experiments.
    Naming convention: {model_type}_{timestamp}_{params_hash}.{ext}
    Example: lstm_20251231-2359_a1b2c3.keras
    """
    
    @staticmethod
    def generate_versioned_filename(model_type: str, extension: str, params: Dict[str, Any] = None) -> str:
        """
        Generates a unique filename based on time and parameters.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        
        # specific short hash for params to identify config changes
        if params:
            # Sort keys to ensure deterministic hash for same params
            param_str = json.dumps(params, sort_keys=True)
            param_hash = hashlib.md5(param_str.encode()).hexdigest()[:6]
        else:
            param_hash = "manual"
            
        # Extension handling (remove dot if present)
        ext = extension.lstrip('.')
        
        return f"{model_type}_{timestamp}_{param_hash}.{ext}"

    @staticmethod
    def find_latest_snapshot(directory: str, model_type: str, extension: str) -> Optional[str]:
        """
        Finds the most recent snapshot for a model type in the directory.
        Assumes standard naming convention where timestamp allows sorting.
        """
        if not os.path.exists(directory):
            return None
            
        # Pattern: model_type_*.extension
        pattern = os.path.join(directory, f"{model_type}_*.{extension}")
        files = glob.glob(pattern)
        
        if not files:
             # Fallback to legacy naming (e.g. catboost_v1.cbm)
            legacy_pattern = os.path.join(directory, f"{model_type}_v*.{extension}")
            legacy_files = glob.glob(legacy_pattern)
            if legacy_files:
                # Sort legacy logic if needed, usually just one
                return sorted(legacy_files)[-1]
            return None
            
        # Sort by filename (timestamp makes this work for finding latest)
        # Reverse to get latest first
        files.sort(reverse=True)
        return files[0]

    @staticmethod
    def create_metadata(model_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a metadata dictionary for logging."""
        return {
            "model_type": model_type,
            "timestamp": datetime.datetime.now().isoformat(),
            "params": params,
            "version_schema": "v2_governance"
        }
