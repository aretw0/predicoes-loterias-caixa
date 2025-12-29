
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
    def __init__(self, lottery: Lottery, range_min: int, range_max: int, draw_count: int, model_args: Dict[str, Any] = None):
        self.lottery = lottery
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model_args = model_args or {}
        
    def predict_next(self) -> Dict[str, Any]:
        """
        Trains with ALL available data and predicts the next unknown draw.
        """
        print(f"--- Starting FUTURE PREDICTION for {self.lottery.name} ---", file=sys.stderr)
        
        # Ensure data is loaded
        df = self.lottery.preprocess_data()
        
        # Parameters
        rf_estimators = int(self.model_args.get('rf_n_estimators', self.model_args.get('n_estimators', 100)))
        xgb_estimators = int(self.model_args.get('xgb_n_estimators', self.model_args.get('n_estimators', 100)))
        lstm_epochs = int(self.model_args.get('epochs', 10))
        lstm_units = int(self.model_args.get('units', 128))
        
        print(f"Using database with {len(df)} draws.", file=sys.stderr)
        print(f"Training robust models (RF={rf_estimators}, XGB={xgb_estimators}, LSTM={lstm_epochs})...", file=sys.stderr)
        
        preds = {}
        
        # 1. Monte Carlo
        print(" > 1/4: Monte Carlo...", file=sys.stderr)
        try:
            mc = MonteCarloModel(self.range_min, self.range_max, self.draw_count)
            mc.train(df)
            preds['mc'] = set(mc.predict())
        except Exception as e:
            print(f"Error in MC: {e}", file=sys.stderr)
            preds['mc'] = set()

        # 2. Random Forest
        print(" > 2/4: Random Forest...", file=sys.stderr)
        try:
            rf = RandomForestModel(self.range_min, self.range_max, self.draw_count)
            # Pass model_args so n_jobs and other params are respected
            rf.train(df, n_estimators=rf_estimators, **self.model_args)
            preds['rf'] = set(rf.predict())
        except Exception as e:
            print(f"Error in RF: {e}", file=sys.stderr)
            preds['rf'] = set()

        # 3. XGBoost
        print(" > 3/4: XGBoost...", file=sys.stderr)
        try:
            xgb_model = XGBoostModel(self.range_min, self.range_max, self.draw_count)
            xgb_args = self.model_args.copy()
            xgb_args['n_estimators'] = xgb_estimators
            if 'rf_n_estimators' in xgb_args: del xgb_args['rf_n_estimators']
            xgb_model.train(df, **xgb_args)
            preds['xgb'] = set(xgb_model.predict())
        except Exception as e:
            print(f"Error in XGB: {e}", file=sys.stderr)
            preds['xgb'] = set()

        # 4. LSTM
        print(" > 4/4: LSTM (Deep Learning)...", file=sys.stderr)
        try:
            lstm = LSTMModel(self.range_min, self.range_max, self.draw_count)
            lstm_args = self.model_args.copy()
            if 'epochs' in lstm_args: del lstm_args['epochs']
            if 'units' in lstm_args: del lstm_args['units']
            lstm.train(df, epochs=lstm_epochs, batch_size=32, verbose=0, units=lstm_units, **lstm_args)
            preds['lstm'] = set(lstm.predict())
        except Exception as e:
            print(f"Error in LSTM: {e}", file=sys.stderr)
            preds['lstm'] = set()

        # Consensus
        all_votes = []
        for p in preds.values():
            all_votes.extend(list(p))
        
        vote_counts = Counter(all_votes)
        
        # Create Result Object
        result = {
            'models': {k: sorted(list(v)) for k, v in preds.items()},
            'consensus_ranking': []
        }
        
        common = vote_counts.most_common()
        for num, votes in common:
            result['consensus_ranking'].append({'number': num, 'votes': votes})

        # Suggestion: Top N
        suggestion = [num for num, _ in common[:self.draw_count]]
        result['suggestion'] = sorted(suggestion)

        # Cleanup
        del lstm, rf, xgb_model, mc
        tf.keras.backend.clear_session()
        gc.collect()
        
        return result
