import pandas as pd
from .base import ModelFactory, Lottery
from typing import List, Dict, Any

class Backtester:
    def __init__(self, lottery: Lottery, model_type: str, model_args: Dict[str, Any], range_min: int, range_max: int, draw_count: int):
        self.lottery = lottery
        self.model_type = model_type
        self.model_args = model_args
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        
    def run(self, draws_to_test: int = 100, prediction_size: int = None, silent: bool = False) -> Dict[str, Any]:
        """
        Runs the backtest.
        :param draws_to_test: Number of most recent draws to test.
        :param prediction_size: Number of balls to predict per draw (bet size).
        :param silent: If True, suppresses print output.
        """
        if prediction_size is None:
            prediction_size = self.draw_count # Default to drawing game size
            
        # Ensure data is loaded and preprocessed
        df = self.lottery.preprocess_data()
        
        total_draws = len(df)
        if draws_to_test > total_draws:
            draws_to_test = total_draws
            
        start_index = total_draws - draws_to_test
        
        results = []
        total_cost = 0.0
        total_prize = 0.0
        hits_distribution = {}
        
        if not silent:
            print(f"Starting backtest for {self.model_type} on {self.lottery.name}...")
            print(f"Testing last {draws_to_test} draws. Prediction size: {prediction_size}.")
        
        # Iterating through history
        min_history = 100 # Safe margin
        if start_index < min_history:
             if not silent:
                print(f"Warning: Start index {start_index} is low. Early predictions might be poor.")
             
        for i in range(start_index, total_draws):
            # Split data
            # Train on history up to i (exclusive)
            train_data = df.iloc[:i].copy()
            # Target draw is at i
            target_draw = df.iloc[i]
            target_numbers = set(target_draw['dezenas'])
            
            # Instantiate and train model
            # We recreate model each time to prevent state leakage (unless model natively supports incremental, but clean slate is safer)
            model = ModelFactory.create_model(self.model_type, self.range_min, self.range_max, self.draw_count)
            try:
                model.train(train_data)
                prediction = model.predict(count=prediction_size, **self.model_args)
            except Exception as e:
                # If model fails (e.g. not enough data), skip
                # print(f"Draw {i}: Model error {e}")
                continue
                
            prediction_set = set(prediction)
            
            # Check hits
            hits = len(prediction_set.intersection(target_numbers))
            
            # Calculate cost and prize
            # We need a Prize Calculator?
            # For now, let's just track hits. Prize logic is complex (split pots etc).
            # We can use fixed prize table approximation if available, or just Cost.
            
            cost = self.lottery.get_price(prediction_size)
            
            # Approximate Prize (Very rough, just to show mechanics)
            # MegaSena: 4 (Quadra), 5 (Quina), 6 (Sena)
            prize = 0.0
            # TODO: Implement realistic prize lookup if possible, otherwise just track hits.
            
            results.append({
                'draw_index': i,
                'draw_date': target_draw['data'],
                'prediction': prediction,
                'actual': list(target_numbers),
                'hits': hits,
                'cost': cost
            })
            
            total_cost += cost
            hits_distribution[hits] = hits_distribution.get(hits, 0) + 1
            
        return {
            'total_bets': len(results),
            'total_cost': total_cost,
            'hits_distribution': hits_distribution,
            'details': results
        }
