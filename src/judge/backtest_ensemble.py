import pandas as pd
import sys
from core.base import ModelFactory, Lottery
from typing import List, Dict, Any
from models.tree.rf import RandomForestModel
from models.deep.lstm import LSTMModel
from models.heuristic.monte_carlo import MonteCarloModel
from models.tree.xgboost import XGBoostModel
from data.features import calculate_sum, count_odds, count_evens, calculate_spread
import tensorflow as tf
import gc


class EnsembleBacktester:
    def __init__(self, lottery: Lottery, range_min: int, range_max: int, draw_count: int, model_args: Dict[str, Any] = None, snapshot_paths: Dict[str, str] = None):
        self.lottery = lottery
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model_args = model_args or {}
        self.snapshot_paths = snapshot_paths or {}
        
    def run(self, draws_to_test: int = 10, verbose: bool = True) -> Dict[str, Any]:
        """
        Runs the ensemble backtest.
        Evaluates: MC, RF, LSTM, XGB, CatBoost vs Consensus.
        """
        # Ensure data is loaded
        df = self.lottery.preprocess_data()
        total_draws = len(df)
        
        if draws_to_test > total_draws:
            draws_to_test = total_draws
        
        start_index = total_draws - draws_to_test
        results = []
        
        # Parse common model args or defaults
        rf_estimators = int(self.model_args.get('rf_n_estimators', self.model_args.get('n_estimators', 100)))
        xgb_estimators = int(self.model_args.get('xgb_n_estimators', self.model_args.get('n_estimators', 100)))

        lstm_epochs = int(self.model_args.get('epochs', 10))
        lstm_units = int(self.model_args.get('units', 128))
        
        if verbose:
            print(f"Starting Ensemble Backtest on {self.lottery.name} for last {draws_to_test} draws...")
            print("Models: MC, RF, LSTM, XGB, CatBoost.")
            print(f"Configuration: RF={rf_estimators} trees, XGB={xgb_estimators} trees, LSTM={lstm_epochs} epochs.")
            if self.snapshot_paths:
                print(f"Snapshots loaded: {list(self.snapshot_paths.keys())} (Warm Start / Validation)")

        # Initialize models ONCE (optimization)
        try:
            mc = MonteCarloModel(self.range_min, self.range_max, self.draw_count)
            rf = RandomForestModel(self.range_min, self.range_max, self.draw_count)
            
            # Loading RF Snapshot if exists
            if 'rf' in self.snapshot_paths:
                 rf.load(self.snapshot_paths['rf'])
            
            # XGB Setup
            xgb_model = XGBoostModel(self.range_min, self.range_max, self.draw_count)
            xgb_args = self.model_args.copy()
            xgb_args['n_estimators'] = xgb_estimators
            if 'rf_n_estimators' in xgb_args: del xgb_args['rf_n_estimators']
            
            if 'xgb' in self.snapshot_paths:
                 xgb_model.load(self.snapshot_paths['xgb'])
            
            # LSTM Setup
            lstm = LSTMModel(self.range_min, self.range_max, self.draw_count)
            lstm_args = self.model_args.copy()
            if 'epochs' in lstm_args: del lstm_args['epochs']
            if 'units' in lstm_args: del lstm_args['units']
            
            if 'lstm' in self.snapshot_paths:
                 lstm.load(self.snapshot_paths['lstm'])
                 
            # CatBoost Setup
            from models.tree.catboost import CatBoostModel
            cat = CatBoostModel(self.range_min, self.range_max, self.draw_count)
            if 'catboost' in self.snapshot_paths:
                cat.load(self.snapshot_paths['catboost'])
            
        except Exception as e:
            print(f"Critical Error initializing models: {e}", file=sys.stderr)
            return {}

        for i in range(start_index, total_draws):
            train_data = df.iloc[:i].copy()
            target_draw = df.iloc[i]
            target_numbers = set(target_draw['dezenas'])
            
            # Predict with all models
            preds = {}
            
            # 1. Monte Carlo
            try:
                mc.train(train_data) 
                preds['mc'] = set(mc.predict())
            except Exception as e:
                print(f"Error in MC: {e}", file=sys.stderr)
                preds['mc'] = set()

            # 2. Random Forest
            try:
                # If snapshot was loaded, 'train' might retrain or refine. 
                # Scikit-learn Random Forest doesn't support incremental learning (partial_fit) easily.
                # So calling train() will RETRAIN from scratch on train_data.
                # IF the user wants to use the snapshot as is (Validation), we should SKIP train?
                # But backtester usually implies re-training on available history.
                # COMPROMISE: If snapshot exists, SKIP train (assume Fixed Model Validation).
                # ELSE train normally.
                if 'rf' not in self.snapshot_paths:
                    rf.train(train_data, n_estimators=rf_estimators, **self.model_args)
                preds['rf'] = set(rf.predict())
            except Exception as e:
                print(f"Error in RF: {e}", file=sys.stderr)
                preds['rf'] = set()

            # 3. XGBoost
            try:
                if 'xgb' not in self.snapshot_paths:
                    xgb_model.train(train_data, **xgb_args) 
                preds['xgb'] = set(xgb_model.predict())
            except Exception as e:
                print(f"Error in XGB: {e}", file=sys.stderr)
                preds['xgb'] = set()

            # 4. LSTM (Deep Learning)
            try:
                # LSTM supports incremental provided weights are preserved.
                # But our LSTM.train() calls _build_model if self.model is None.
                # If loaded, self.model is NOT None.
                # However, calling fit() on existing model continues training (Fine Tuning).
                # This seems desirable for LSTM (Online Learning). 
                # But to keep consistent with "Frozen Snapshot Validation", let's skip if snapshot present.
                if 'lstm' not in self.snapshot_paths:
                    lstm.train(train_data, epochs=lstm_epochs, batch_size=32, verbose=0, units=lstm_units, **lstm_args) 
                preds['lstm'] = set(lstm.predict())
            except Exception as e:
                print(f"Error in LSTM: {e}", file=sys.stderr)
                preds['lstm'] = set()
                
            # 5. CatBoost
            try:
                if 'catboost' not in self.snapshot_paths:
                    cat.train(train_data, verbose=0)
                preds['catboost'] = set(cat.predict())
            except Exception as e:
                 print(f"Error in CatBoost: {e}", file=sys.stderr)
                 preds['catboost'] = set()

            # Calculate Consensus
            all_votes = []
            for p in preds.values():
                all_votes.extend(list(p))
            
            # Count frequency of each number
            from collections import Counter
            vote_counts = Counter(all_votes)
            
            # Consensus Sets
            con_5 = {n for n, c in vote_counts.items() if c >= 5}
            con_4 = {n for n, c in vote_counts.items() if c >= 4}
            con_3 = {n for n, c in vote_counts.items() if c >= 3}
            
            # Evaluation
            row_result = {
                'draw_index': i,
                'target': list(target_numbers),
                'models': {k: list(v) for k, v in preds.items()},
                'consensus': {
                    '5_of_5': list(con_5), # Since we have 5 models now
                    '4_of_5': list(con_4),
                    '3_of_5': list(con_3)
                },
                'hits': {
                    'mc': len(preds['mc'].intersection(target_numbers)),
                    'rf': len(preds['rf'].intersection(target_numbers)),
                    'xgb': len(preds['xgb'].intersection(target_numbers)),
                    'lstm': len(preds['lstm'].intersection(target_numbers)),
                    'catboost': len(preds['catboost'].intersection(target_numbers)),
                    'con_4': len(con_4.intersection(target_numbers)),
                    'con_3': len(con_3.intersection(target_numbers)),
                }
            }
            results.append(row_result)
            
            if verbose:
                # Simplified output for brevity
                print(f"Draw {i} | Consensus(3+): {len(con_3)} hits: {len(con_3.intersection(target_numbers))}")

        # Cleanup at the END of backtest, not every loop
        del lstm, rf, xgb_model, mc
        tf.keras.backend.clear_session()
        gc.collect()

        return {'draws': len(results), 'details': results}
