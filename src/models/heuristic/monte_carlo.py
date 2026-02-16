import pandas as pd
import random
import statistics
from core.base import Model
from data.features import calculate_sum, count_odds, calculate_spread

class MonteCarloModel(Model):
    def __init__(self, range_min: int, range_max: int, draw_count: int):
        super().__init__("Monte Carlo Simulation")
        self.range_min = range_min
        self.range_max = range_max
        self.draw_count = draw_count
        
        # Learned Stats
        self.sum_stats = {}
        self.odd_probs = {}
        self.spread_stats = {}
        self.trained = False

    def train(self, data: pd.DataFrame):
        sums = []
        odds = []
        spreads = []
        
        # Prefer 'dezenas' column (list of ints) if available
        if 'dezenas' in data.columns:
             for _, row in data.iterrows():
                try:
                    draw = row['dezenas']
                    if not isinstance(draw, list):
                        continue
                    # Ensure ints
                    draw = [int(x) for x in draw]
                    
                    sums.append(calculate_sum(draw))
                    odds.append(count_odds(draw))
                    spreads.append(calculate_spread(draw))
                except Exception:
                    continue
        else:
            # Fallback to column scraping
            ball_cols = [c for c in data.columns if 'bola' in c.lower()]
            for _, row in data.iterrows():
                draw = []
                try:
                    for c in ball_cols:
                        draw.append(int(row[c]))
                except Exception:
                    continue
                if not draw:
                    continue
                sums.append(calculate_sum(draw))
                odds.append(count_odds(draw))
                spreads.append(calculate_spread(draw))
            
        if not sums:
            print("Warning: No data for Monte Carlo training.")
            return

        # Learn Sum Distribution (Normal Approximation)
        self.sum_stats = {
            "mean": statistics.mean(sums),
            "stdev": statistics.stdev(sums) if len(sums) > 1 else 0
        }
        
        # Learn Odd Distribution (Probability Map)
        total = len(odds)
        self.odd_probs = {}
        for o in set(odds):
            self.odd_probs[o] = odds.count(o) / total
            
        # Learn Spread
        self.spread_stats = {
            "mean": statistics.mean(spreads),
            "stdev": statistics.stdev(spreads) if len(spreads) > 1 else 0
        }
        
        self.trained = True

    def predict(self, count: int = None, **kwargs) -> list:
        if not self.trained:
             return []
        
        final_count = count if count is not None else self.draw_count
        
        # Simulation Parameters
        # We simulate N random games.
        # We keep only those that are statistically "normal" (within bounds).
        # We count number frequency in the valid pool.
        
        simulations = 10000 
        valid_draws = []
        
        # Validation Bounds (e.g., Mean +/- 1.5 StdDev covering ~87% of cases)
        min_sum = self.sum_stats['mean'] - 1.5 * self.sum_stats['stdev']
        max_sum = self.sum_stats['mean'] + 1.5 * self.sum_stats['stdev']
        
        min_spread = self.spread_stats['mean'] - 1.5 * self.spread_stats['stdev']
        max_spread = self.spread_stats['mean'] + 1.5 * self.spread_stats['stdev']
        
        # Probability Threshold for discrete features (Odd/Even)
        # We accept if the pattern appeared at least 5% of time in history
        min_prob = 0.05
        
        rng = list(range(self.range_min, self.range_max + 1))
        
        for _ in range(simulations):
            # Generate Random Draw
            draw = random.sample(rng, self.draw_count)
            
            # Check Features
            s = calculate_sum(draw)
            if not (min_sum <= s <= max_sum):
                continue
                
            sp = calculate_spread(draw)
            if not (min_spread <= sp <= max_spread):
                continue
                
            o = count_odds(draw)
            if self.odd_probs.get(o, 0) < min_prob:
                continue
                
            valid_draws.append(draw)
            
        if not valid_draws:
            print("Warning: Monte Carlo simulation too strict, no valid draws found.")
            # Fallback: Validation failed, return random
            return sorted(random.sample(rng, final_count))
            
        # Select most frequent numbers from Valid Pool
        freqs = {n: 0 for n in rng}
        for draw in valid_draws:
            for n in draw:
                freqs[n] += 1
                
        # Sort by likelihood
        sorted_nums = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
        top_numbers = [n for n, c in sorted_nums[:final_count]]
        
        return sorted(top_numbers)
