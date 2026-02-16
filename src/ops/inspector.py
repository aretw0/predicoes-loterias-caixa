import pandas as pd
from typing import List, Dict, Any
import os

class TrainingInspector:
    def __init__(self, log_path: str = "data/training_log.csv"):
        self.log_path = log_path
        
    def get_runs(self, model_filter: str = None) -> List[Dict[str, Any]]:
        """
        Parses the training log and groups records into 'Runs'.
        Returns a list of run summaries, sorted by recency (newest first).
        """
        if not os.path.exists(self.log_path):
            return []
            
        try:
            df = pd.read_csv(self.log_path)
        except pd.errors.EmptyDataError:
            return []
            
        if df.empty:
            return []
            
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        runs = []
        current_run = None
        
        for _, row in df.iterrows():
            # Check if this row belongs to current run
            is_continuation = False
            if current_run:
                # Continuation criteria:
                # Same Model Type
                # Epoch is Next (or close enough, but for now simple +1 check)
                if (row['model_type'] == current_run['model_type'] and 
                    row['epoch'] > current_run['metrics'][-1]['epoch']): 
                       # Relaxed check: epoch just needs to be greater, usually +1
                       is_continuation = True
            
            if is_continuation:
                current_run['metrics'].append({
                    'epoch': row['epoch'],
                    'loss': row['loss'],
                    'val_loss': row['val_loss'],
                    'accuracy': row['accuracy'],
                    'val_accuracy': row['val_accuracy'],
                    'timestamp': row['timestamp']
                })
                # Update End Time
                current_run['end_time'] = row['timestamp']
            else:
                # Close previous run if exists
                if current_run:
                    runs.append(self._summarize_run(current_run))
                    
                # Start new run
                current_run = {
                    'model_type': row['model_type'],
                    'params_hash': row['params_hash'],
                    'start_time': row['timestamp'],
                    'end_time': row['timestamp'],
                    'metadata': row['metadata'],
                    'metrics': [{
                        'epoch': row['epoch'],
                        'loss': row['loss'],
                        'val_loss': row['val_loss'],
                        'accuracy': row['accuracy'],
                        'val_accuracy': row['val_accuracy'],
                        'timestamp': row['timestamp']
                    }]
                }
                
        # Append last
        if current_run:
            runs.append(self._summarize_run(current_run))
            
        # Filter
        if model_filter:
            runs = [r for r in runs if r['model_type'] == model_filter]
            
        # Sort by Recency (Newest first)
        runs.sort(key=lambda x: x['start_time'], reverse=True)
            
        return runs

    def _summarize_run(self, run_raw: Dict) -> Dict:
        """Calculates aggregate stats for a run."""
        metrics = run_raw['metrics']
        
        # Valid Loss (might be NaN if not validation)
        val_losses = [m['val_loss'] for m in metrics if pd.notnull(m['val_loss'])]
        val_accs = [m['val_accuracy'] for m in metrics if pd.notnull(m['val_accuracy'])]
        losses = [m['loss'] for m in metrics if pd.notnull(m['loss'])]
        
        if not val_losses:
             best_epoch = -1
             min_val_loss = None
             status = "Unknown (No Val Data)"
        else:
             min_val_loss = min(val_losses)
             # Find epoch of min val loss
             val_losses.index(min_val_loss)
             # Map back to real epoch number (since we filtered Nones, careful)
             # Actually let's assume all have it for now or iterate
             # Safer:
             best_metric = min(metrics, key=lambda x: x['val_loss'] if pd.notnull(x['val_loss']) else float('inf'))
             best_epoch = best_metric['epoch']
             min_val_loss = best_metric['val_loss']
             
             # Status Detection
             # Look at last 5 epochs
             recent = metrics[-5:]
             if len(recent) < 3:
                 status = "Insufficient Data"
             else:
                 # Trend of val_loss
                 recent_vals = [m['val_loss'] for m in recent if pd.notnull(m['val_loss'])]
                 if len(recent_vals) < 2:
                     status = "Insufficient Val Data"
                 else:
                     # Simple logic: Is average of last 2 > average of previous 2?
                     if recent_vals[-1] > min_val_loss * 1.01: # 1% tolerance
                        # If current loss is significantly worse than best -> Overfitting
                        status = "OVERFITTING (Probable)"
                     elif recent_vals[-1] < recent_vals[0]:
                        status = "Learning (Improving)"
                     else:
                        status = "Plateau (Stable)"

        return {
            'model_type': run_raw['model_type'],
            'start_time': run_raw['start_time'],
            'duration': run_raw['end_time'] - run_raw['start_time'],
            'total_epochs': len(metrics),
            'best_epoch': best_epoch,
            'min_val_loss': min_val_loss,
            'best_val_acc': max(val_accs) if val_accs else 0.0,
            'final_loss': losses[-1] if losses else 0.0,
            'status': status
        }
