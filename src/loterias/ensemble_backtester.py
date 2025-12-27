import pandas as pd
from .base import ModelFactory, Lottery
from typing import List, Dict, Any
from .models import RandomForestModel, LSTMModel, MonteCarloModel, XGBoostModel
from .features import calculate_sum, count_odds, count_evens, calculate_spread

class EnsembleBacktester:
    def __init__(self, lottery: Lottery, range_min: int, range_max: int, draw_count: int, model_args: Dict[str, Any] = None):
        self.lottery = lottery
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        self.model_args = model_args or {}
        
    def run(self, draws_to_test: int = 10, verbose: bool = True) -> Dict[str, Any]:
        """
        Runs the ensemble backtest.
        Evaluates: MC, RF, LSTM, XGB vs Consensus (3/4 and 4/4).
        """
        # Ensure data is loaded
        df = self.lottery.preprocess_data()
        total_draws = len(df)
        
        if draws_to_test > total_draws:
            draws_to_test = total_draws
        
        start_index = total_draws - draws_to_test
        results = []
        
        # Parse common model args or defaults
        # Priority: Specific (rf_n_estimators) > Generic (n_estimators) > Default (100)
        rf_estimators = int(self.model_args.get('rf_n_estimators', self.model_args.get('n_estimators', 100)))
        xgb_estimators = int(self.model_args.get('xgb_n_estimators', self.model_args.get('n_estimators', 100)))

        lstm_epochs = int(self.model_args.get('epochs', 10))
        lstm_units = int(self.model_args.get('units', 128))
        
        if verbose:
            print(f"Starting Ensemble Backtest on {self.lottery.name} for last {draws_to_test} draws...")
            print("Models: MC, RF, LSTM, XGB.")
            print(f"Configuration: RF={rf_estimators} trees, XGB={xgb_estimators} trees, LSTM={lstm_epochs} epochs.")
            print("Warning: This will perform full training for each step.")

        for i in range(start_index, total_draws):
            train_data = df.iloc[:i].copy()
            target_draw = df.iloc[i]
            target_numbers = set(target_draw['dezenas'])
            
            # Predict with all models
            preds = {}
            
            # 1. Monte Carlo
            try:
                mc = MonteCarloModel(self.range_min, self.range_max, self.draw_count)
                mc.train(train_data) 
                preds['mc'] = set(mc.predict())
            except: preds['mc'] = set()

            # 2. Random Forest
            try:
                rf = RandomForestModel(self.range_min, self.range_max, self.draw_count)
                rf.train(train_data, n_estimators=rf_estimators)
                preds['rf'] = set(rf.predict())
            except: preds['rf'] = set()

            # 3. XGBoost
            try:
                xgb_model = XGBoostModel(self.range_min, self.range_max, self.draw_count)
                
                # Prepare XGB-specific args to avoid pollution
                xgb_args = self.model_args.copy()
                xgb_args['n_estimators'] = xgb_estimators
                
                # Filter out RF specific args if they exist to be clean
                if 'rf_n_estimators' in xgb_args: del xgb_args['rf_n_estimators']
                
                xgb_model.train(train_data, **xgb_args) 
                preds['xgb'] = set(xgb_model.predict())
            except: preds['xgb'] = set()

            # 4. LSTM
            try:
                lstm = LSTMModel(self.range_min, self.range_max, self.draw_count)
                lstm.train(train_data, epochs=lstm_epochs, batch_size=32, verbose=0, units=lstm_units, **self.model_args) 
                preds['lstm'] = set(lstm.predict())
            except: preds['lstm'] = set()

            # Calculate Consensus
            all_votes = []
            for p in preds.values():
                all_votes.extend(list(p))
            
            # Count frequency of each number
            from collections import Counter
            vote_counts = Counter(all_votes)
            
            # Consensus Sets
            con_4 = {n for n, c in vote_counts.items() if c >= 4}
            con_3 = {n for n, c in vote_counts.items() if c >= 3}
            con_2 = {n for n, c in vote_counts.items() if c >= 2}
            
            # Evaluation
            row_result = {
                'draw_index': i,
                'target': list(target_numbers),
                'models': {k: list(v) for k, v in preds.items()},
                'consensus': {
                    '4_of_4': list(con_4),
                    '3_of_4': list(con_3),
                    '2_of_4': list(con_2)
                },
                'hits': {
                    'mc': len(preds['mc'].intersection(target_numbers)),
                    'rf': len(preds['rf'].intersection(target_numbers)),
                    'xgb': len(preds['xgb'].intersection(target_numbers)),
                    'lstm': len(preds['lstm'].intersection(target_numbers)),
                    'con_4': len(con_4.intersection(target_numbers)),
                    'con_3': len(con_3.intersection(target_numbers)),
                    'con_2': len(con_2.intersection(target_numbers)),
                }
            }
            results.append(row_result)
            
            if verbose:
                print(f"Draw {i}: Target={list(target_numbers)}")
                print(f"  > Hit Rates: MC={row_result['hits']['mc']}, RF={row_result['hits']['rf']}, XGB={row_result['hits']['xgb']}, LSTM={row_result['hits']['lstm']}")
                print(f"  > Consensus: 4/4 hits {row_result['hits']['con_4']} (size {len(con_4)}), 3/4 hits {row_result['hits']['con_3']}")

        return {'draws': len(results), 'details': results}
