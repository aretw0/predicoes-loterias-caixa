import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from ..base import Model

class RandomForestModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Random Forest Model")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.scaler = StandardScaler()
        self.trained = False

    def train(self, data: pd.DataFrame):
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
        
        processed_data = [] # List of draws
        
        for i, row in data.iterrows():
            drawn_numbers = set(row['dezenas'])
            
            # If we are past warm-up, we record this state as a training example
            if i >= start_training_idx:
                # Capture state BEFORE knowing the result of this draw
                # For efficiency, we might random sample negative examples?
                # Or just put all ~60 examples per draw? (60 * 2000 = 120k rows, feasible)
                
                for n in range(self.range_min, self.range_max + 1):
                    # Features
                    feat_gap = current_gaps[n]
                    feat_freq = freq_total[n]
                    feat_freq10 = sum(freq_10[n][-10:])
                    
                    X.append([feat_gap, feat_freq, feat_freq10])
                    y.append(1 if n in drawn_numbers else 0)
            
            # Update stats AFTER the draw
            for n in range(self.range_min, self.range_max + 1):
                if n in drawn_numbers:
                    current_gaps[n] = 0
                    freq_total[n] += 1
                    freq_10[n].append(1)
                else:
                    current_gaps[n] += 1
                    freq_10[n].append(0)
        
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

    def predict(self, count: int = None, **kwargs) -> list:
        if not self.trained:
             raise ValueError("Model has not been trained yet.")
        
        final_count = count if count is not None else self.draw_count
        
        # Build features for "next" draw
        X_next = []
        numbers = []
        
        for n in range(self.range_min, self.range_max + 1):
            feat_gap = self.final_gaps[n]
            feat_freq = self.final_freq[n]
            feat_freq10 = sum(self.final_freq10[n][-10:])
             
            X_next.append([feat_gap, feat_freq, feat_freq10])
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
