import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from ..base import Model
from ..features import calculate_sum, count_odds, count_evens, calculate_spread

class RandomForestModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Random Forest Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=1)
        self.scaler = StandardScaler()
        self.trained = False

    def train(self, data: pd.DataFrame, **kwargs):
        # Allow configuring n_estimators and n_jobs via model-args
        n_jobs = int(kwargs.get('n_jobs', 1))
        
        if 'n_estimators' in kwargs:
            try:
                n = int(kwargs['n_estimators'])
                self.model = RandomForestClassifier(n_estimators=n, random_state=42, n_jobs=n_jobs)
                import sys
                print(f"Re-initialized Random Forest with {n} estimators and n_jobs={n_jobs}.", file=sys.stderr)
            except ValueError:
                pass
        else:
            # Update n_jobs if it wasn't re-initialized
            self.model.n_jobs = n_jobs


        # We need to transform the time-series data into a supervised learning problem.
        # X: Features of previous draw state
        # y: Whether number N appeared in current draw
        
        # Features per number:
        # 1. Gap (current gap)
        # 2. Frequency (total frequency)
        # 3. Frequency (last 10 draws)
        
        X = []
        y = []
        
        # Pre-calculation structures
        total_draws = len(data)
        
        # Efficiently iterating is hard. Let's do a simplified approach.
        # We process draw by draw.
        
        # Stats trackers
        current_gaps = {n: 0 for n in range(self.range_min, self.range_max + 1)}
        freq_total = {n: 0 for n in range(self.range_min, self.range_max + 1)}
        freq_10 = {n: [] for n in range(self.range_min, self.range_max + 1)} # Queue of last 10 appearances (1 or 0)
        
        # We skip the first 50 draws to build up history stats
        start_training_idx = 50
        
        # Context of *previous* draw (features)
        # We need to store features of row i-1 to use for predicting row i
        last_draw_features = [0, 0, 0, 0] # Sum, Odd, Even, Spread
        
        for i, row in data.iterrows():
            # Get current draw numbers
            drawn_numbers = []
            drawn_set = set(row['dezenas'])
            for col in data.columns:
                 if 'bola' in col or 'dezenas' in col:
                     try:
                         drawn_numbers.append(int(row[col]))
                     except:
                         pass
            
            # If we are past warm-up, we record this state as a training example
            if i >= start_training_idx:
                # Features from global context (previous draw state)
                ctx_sum, ctx_odd, ctx_even, ctx_spread = last_draw_features
                
                for n in range(self.range_min, self.range_max + 1):
                    # Features
                    feat_gap = current_gaps[n]
                    feat_freq = freq_total[n]
                    feat_freq10 = sum(freq_10[n][-10:])
                    
                    # Augmented Features: "What was the context when this number appeared/didn't appear?"
                    # We are asking: Does High Sum yesterday affect Number 5 today?
                    
                    X.append([feat_gap, feat_freq, feat_freq10, ctx_sum, ctx_odd, ctx_even, ctx_spread])
                    y.append(1 if n in drawn_set else 0)
            
            # Update stats AFTER the draw
            for n in range(self.range_min, self.range_max + 1):
                if n in drawn_set:
                    current_gaps[n] = 0
                    freq_total[n] += 1
                    freq_10[n].append(1)
                else:
                    current_gaps[n] += 1
                    freq_10[n].append(0)
            
            # Update last draw features for NEXT iteration
            last_draw_features = [
                calculate_sum(drawn_numbers),
                count_odds(drawn_numbers),
                count_evens(drawn_numbers),
                calculate_spread(drawn_numbers)
            ]
        
        if not X:
            print("Warning: Not enough data to train Random Forest.")
            return

        X_array = np.array(X)
        y_array = np.array(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_array)
        
        # Train
        self.model.fit(X_scaled, y_array)
        self.trained = True
        
        # Store final state for prediction
        self.final_gaps = current_gaps
        self.final_freq = freq_total
        self.final_freq10 = freq_10
        self.last_draw_features = last_draw_features

    def predict(self, count: int = None, **kwargs) -> list:
        if not self.trained:
             raise ValueError("Model has not been trained yet.")
        
        final_count = count if count is not None else self.draw_count
        
        # Build features for "next" draw
        X_next = []
        numbers = []
        
        # Context is the features of the VERY LAST draw seen
        ctx_sum, ctx_odd, ctx_even, ctx_spread = self.last_draw_features
        
        for n in range(self.range_min, self.range_max + 1):
            feat_gap = self.final_gaps[n]
            feat_freq = self.final_freq[n]
            feat_freq10 = sum(self.final_freq10[n][-10:])
             
            X_next.append([feat_gap, feat_freq, feat_freq10, ctx_sum, ctx_odd, ctx_even, ctx_spread])
            numbers.append(n)
            
        X_next_array = np.array(X_next)
        X_next_scaled = self.scaler.transform(X_next_array)
        
        # Predict Proba (Class 1)
        probs = self.model.predict_proba(X_next_scaled)[:, 1]
        
        # Create DF to sort
        df = pd.DataFrame({'dezenas': numbers, 'prob': probs})
        
        sorted_df = df.sort_values(by=['prob', 'dezenas'], ascending=[False, True])
        
        prediction = sorted_df.head(final_count)['dezenas'].tolist()
        return sorted(prediction)
