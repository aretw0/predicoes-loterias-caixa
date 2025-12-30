import pandas as pd
import numpy as np
import catboost as cb
from sklearn.preprocessing import StandardScaler
from ..base import Model
from ..features import calculate_sum, count_odds, count_evens, calculate_spread
import sys

class CatBoostModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("CatBoost")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        
        # CatBoost Classifier
        self.model = cb.CatBoostClassifier(
            iterations=100,
            learning_rate=0.1,
            depth=5,
            random_seed=42,
            verbose=0,  # Silent mode
            loss_function='Logloss'
        )
        self.scaler = StandardScaler()
        self.trained = False

    def train(self, data: pd.DataFrame, **kwargs):
        # Allow configuring hyperparameters via model-args
        params = {}
        if 'iterations' in kwargs:
            try:
                params['iterations'] = int(kwargs['iterations'])
            except ValueError: pass
            
        if 'learning_rate' in kwargs:
             try:
                params['learning_rate'] = float(kwargs['learning_rate'])
             except ValueError: pass
            
        if 'depth' in kwargs:
             try:
                params['depth'] = int(kwargs['depth'])
             except ValueError: pass

        if params:
            self.model.set_params(**params)

        # Feature Engineering (Identical to Random Forest/XGBoost for consistency)
        X = []
        y = []
        
        # Stats trackers
        current_gaps = {n: 0 for n in range(self.range_min, self.range_max + 1)}
        freq_total = {n: 0 for n in range(self.range_min, self.range_max + 1)}
        freq_10 = {n: [] for n in range(self.range_min, self.range_max + 1)} 
        
        start_training_idx = 50
        last_draw_features = [0, 0, 0, 0] # Sum, Odd, Even, Spread
        
        # Determine number columns
        num_cols = [col for col in data.columns if 'bola' in col or 'dezenas' in col]

        for i, row in data.iterrows():
            drawn_numbers = []
            try:
                drawn_set = set(row['dezenas'])
            except:
                drawn_set = set()

            for col in data.columns:
                 if 'bola' in col or 'dezenas' in col:
                     try:
                         val = int(row[col])
                         drawn_numbers.append(val)
                     except: 
                         pass
            
            # Fallback: if dezenas column was not usable but we found numbers in columns
            if not drawn_set and drawn_numbers:
                drawn_set = set(drawn_numbers)
            
            if i >= start_training_idx:
                ctx_sum, ctx_odd, ctx_even, ctx_spread = last_draw_features
                
                for n in range(self.range_min, self.range_max + 1):
                    feat_gap = current_gaps[n]
                    feat_freq = freq_total[n]
                    feat_freq10 = sum(freq_10[n][-10:])
                    
                    X.append([feat_gap, feat_freq, feat_freq10, ctx_sum, ctx_odd, ctx_even, ctx_spread])
                    y.append(1 if n in drawn_set else 0)
            
            for n in range(self.range_min, self.range_max + 1):
                if n in drawn_set:
                    current_gaps[n] = 0
                    freq_total[n] += 1
                    freq_10[n].append(1)
                else:
                    current_gaps[n] += 1
                    freq_10[n].append(0)
            
            last_draw_features = [
                calculate_sum(drawn_numbers),
                count_odds(drawn_numbers),
                count_evens(drawn_numbers),
                calculate_spread(drawn_numbers)
            ]
        
        if not X:
            print("Warning: Not enough data to train CatBoost.", file=sys.stderr)
            return

        X_array = np.array(X)
        y_array = np.array(y)
        
        # CatBoost handles scaling well, but we stick to the pattern
        X_scaled = self.scaler.fit_transform(X_array)
        
        print(f"Training CatBoost with {len(X)} samples...", file=sys.stderr)
        self.model.fit(X_scaled, y_array)
        self.trained = True
        
        self.final_gaps = current_gaps
        self.final_freq = freq_total
        self.final_freq10 = freq_10
        self.last_draw_features = last_draw_features

    def predict(self, count: int = None, **kwargs) -> list:
        if not self.trained:
             return []
        
        final_count = count if count is not None else self.draw_count
        
        X_next = []
        numbers = []
        
        ctx_sum, ctx_odd, ctx_even, ctx_spread = self.last_draw_features
        
        for n in range(self.range_min, self.range_max + 1):
            feat_gap = self.final_gaps[n]
            feat_freq = self.final_freq[n]
            feat_freq10 = sum(self.final_freq10[n][-10:])
             
            X_next.append([feat_gap, feat_freq, feat_freq10, ctx_sum, ctx_odd, ctx_even, ctx_spread])
            numbers.append(n)
            
        X_next_array = np.array(X_next)
        X_next_scaled = self.scaler.transform(X_next_array)
        
        probs = self.model.predict_proba(X_next_scaled)[:, 1]
        
        df = pd.DataFrame({'dezenas': numbers, 'prob': probs})
        sorted_df = df.sort_values(by=['prob', 'dezenas'], ascending=[False, True])
        
        prediction = sorted_df.head(final_count)['dezenas'].tolist()
        return sorted(prediction)
