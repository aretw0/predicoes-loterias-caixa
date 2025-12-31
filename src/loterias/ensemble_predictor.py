
import pandas as pd
import sys
import gc
from typing import List, Dict, Any
from collections import Counter
import tensorflow as tf
from .base import Lottery
from .models import RandomForestModel, LSTMModel, MonteCarloModel, XGBoostModel
from .features import calculate_sum, count_odds, count_evens, calculate_spread

class EnsemblePredictor:
    def __init__(self, lottery: Lottery, range_min: int, range_max: int, draw_count: int, model_args: Dict[str, Any] = None, snapshot_paths: Dict[str, str] = None):
        self.lottery = lottery
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model_args = model_args or {}
        self.snapshot_paths = snapshot_paths or {}
        
    def predict_next(self, count: int = None) -> Dict[str, Any]:
        """
        Trains with ALL available data (or loads snapshots) and predicts the next unknown draw.
        """
        final_count = count if count is not None else self.draw_count
        print(f"--- Starting FUTURE PREDICTION for {self.lottery.name} (Top {final_count} numbers) ---", file=sys.stderr)
        
        # Ensure data is loaded
        df = self.lottery.preprocess_data()
        
        # Parameters
        rf_estimators = int(self.model_args.get('rf_n_estimators', self.model_args.get('n_estimators', 100)))
        xgb_estimators = int(self.model_args.get('xgb_n_estimators', self.model_args.get('n_estimators', 100)))
        lstm_epochs = int(self.model_args.get('epochs', 10))
        lstm_units = int(self.model_args.get('units', 128))
        
        print(f"Using database with {len(df)} draws.", file=sys.stderr)
        
        preds = {}
        
        # 1. Monte Carlo (Fast, no snapshot needed usually)
        print(" > 1/5: Monte Carlo...", file=sys.stderr)
        try:
            mc = MonteCarloModel(self.range_min, self.range_max, self.draw_count)
            mc.train(df)
            preds['mc'] = set(mc.predict(count=final_count))
        except Exception as e:
            print(f"Error in MC: {e}", file=sys.stderr)
            preds['mc'] = set()

        # 2. Random Forest
        print(" > 2/5: Random Forest...", file=sys.stderr)
        try:
            rf = RandomForestModel(self.range_min, self.range_max, self.draw_count)
            # Check Snapshot
            if 'rf' in self.snapshot_paths:
                print(f"   [Snapshot] Loading RF from {self.snapshot_paths['rf']}...", file=sys.stderr)
                rf.load(self.snapshot_paths['rf'])
            else:
                rf.train(df, n_estimators=rf_estimators, **self.model_args)
                
            preds['rf'] = set(rf.predict(count=final_count))
        except Exception as e:
            print(f"Error in RF: {e}", file=sys.stderr)
            preds['rf'] = set()

        # 3. XGBoost
        print(" > 3/5: XGBoost...", file=sys.stderr)
        try:
            xgb_model = XGBoostModel(self.range_min, self.range_max, self.draw_count)
            if 'xgb' in self.snapshot_paths:
                print(f"   [Snapshot] Loading XGB from {self.snapshot_paths['xgb']}...", file=sys.stderr)
                xgb_model.load(self.snapshot_paths['xgb'])
            else:
                xgb_args = self.model_args.copy()
                xgb_args['n_estimators'] = xgb_estimators
                if 'rf_n_estimators' in xgb_args: del xgb_args['rf_n_estimators']
                xgb_model.train(df, **xgb_args)
                
            preds['xgb'] = set(xgb_model.predict(count=final_count))
        except Exception as e:
            print(f"Error in XGB: {e}", file=sys.stderr)
            preds['xgb'] = set()

        # 4. LSTM
        print(" > 4/5: LSTM (Deep Learning)...", file=sys.stderr)
        try:
            lstm = LSTMModel(self.range_min, self.range_max, self.draw_count)
            if 'lstm' in self.snapshot_paths:
                print(f"   [Snapshot] Loading LSTM from {self.snapshot_paths['lstm']}...", file=sys.stderr)
                lstm.load(self.snapshot_paths['lstm'])
            else:
                lstm_args = self.model_args.copy()
                if 'epochs' in lstm_args: del lstm_args['epochs']
                if 'units' in lstm_args: del lstm_args['units']
                lstm.train(df, epochs=lstm_epochs, batch_size=32, verbose=0, units=lstm_units, **lstm_args)
            
            preds['lstm'] = set(lstm.predict(count=final_count))
        except Exception as e:
            print(f"Error in LSTM: {e}", file=sys.stderr)
            preds['lstm'] = set()

        # 5. CatBoost (New)
        print(" > 5/5: CatBoost...", file=sys.stderr)
        try:
            from .models.catboost_model import CatBoostModel
            cat = CatBoostModel(self.range_min, self.range_max, self.draw_count)
            if 'catboost' in self.snapshot_paths:
                print(f"   [Snapshot] Loading CatBoost from {self.snapshot_paths['catboost']}...", file=sys.stderr)
                cat.load(self.snapshot_paths['catboost'])
            else:
                # Default training if no snapshot
                cat.train(df, verbose=0)
            
            preds['catboost'] = set(cat.predict(count=final_count))
        except Exception as e:
            print(f"Error in CatBoost: {e}", file=sys.stderr)
            preds['catboost'] = set()

        # 6. Canary Models (Fast Heuristics) - For Ledger Only
        print(" > 6/6: Running Canaries (Analysis)...", file=sys.stderr)
        canary_preds = {}
        try:
            from .models.frequency_model import FrequencyModel
            from .models.gap_model import GapModel
            from .models.surfing_model import SurfingModel

            # Frequency
            freq = FrequencyModel(self.range_min, self.range_max, self.draw_count)
            freq.train(df)
            canary_preds['frequency'] = set(freq.predict(count=final_count))

            # Gap
            gap = GapModel(self.range_min, self.range_max, self.draw_count)
            gap.train(df)
            canary_preds['gap'] = set(gap.predict(count=final_count))

            # Surfing
            surf = SurfingModel(self.range_min, self.range_max, self.draw_count)
            surf.train(df)
            canary_preds['surfing'] = set(surf.predict(count=final_count))
            
        except Exception as e:
            print(f"Error in Canaries: {e}", file=sys.stderr)

        # Logging to Ledger
        try:
            from judge.ledger import PredictionLedger
            ledger = PredictionLedger() # Default path
            
            # Log Heavy Models
            draw_col = 'Concurso' if 'Concurso' in df.columns else 'concurso'
            last_draw = int(df[draw_col].max())
            
            for model_name, p_set in preds.items():
                ledger.log_prediction(
                    model_name=model_name, 
                    game=self.lottery.slug, 
                    draw_number=last_draw + 1, 
                    predicted_numbers=sorted(list(p_set))
                )
            
            # Log Canaries
            for model_name, p_set in canary_preds.items():
                ledger.log_prediction(
                    model_name=f"{model_name}_canary", 
                    game=self.lottery.slug, 
                    draw_number=last_draw + 1, 
                    predicted_numbers=sorted(list(p_set))
                )
                
            print("   [Ledger] Predictions logged successfully.", file=sys.stderr)
        except Exception as e:
            print(f"   [Ledger] Failed to log: {e}", file=sys.stderr)

        # Consensus
        all_votes = []
        for p in preds.values():
            all_votes.extend(list(p))
        
        vote_counts = Counter(all_votes)
        
        # Create Result Object
        result = {
            'models': {k: sorted(list(v)) for k, v in preds.items()},
            'canaries': {k: sorted(list(v)) for k, v in canary_preds.items()}, 
            'consensus_ranking': []
        }
        
        common = vote_counts.most_common()
        for num, votes in common:
            result['consensus_ranking'].append({'number': num, 'votes': votes})

        # Suggestion: Top N based on requested count
        suggestion = [num for num, _ in common[:final_count]]
        result['suggestion'] = sorted(suggestion)

        # Cleanup
        del lstm, rf, xgb_model, mc
        try: del cat
        except: pass
        
        tf.keras.backend.clear_session()
        gc.collect()
        
        return result
