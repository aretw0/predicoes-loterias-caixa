import pandas as pd
import statistics
from typing import Dict, Any
from .features import calculate_sum, count_odds, calculate_spread

class Analyzer:
    def __init__(self, data: pd.DataFrame, range_min: int, range_max: int):
        self.data = data
        self.range_min = range_min
        self.range_max = range_max
        
        # Extract numerical columns (balls)
        self.ball_cols = [c for c in data.columns if 'bola' in c.lower() or 'dezenas' in c.lower()]

    def analyze(self) -> Dict[str, Any]:
        """Generates a comprehensive analysis report."""
        if self.data.empty:
            return {"error": "No data available"}

        report = {
            "total_draws": len(self.data),
            "frequency_map": self._analyze_frequencies(),
            "features_stats": self._analyze_features(),
            # "gap_map": self._analyze_gaps() # TODO: Implement later if needed clearly
        }
        return report

    def _analyze_frequencies(self) -> Dict[str, int]:
        """Calculates frequency of each number."""
        counts = {str(n): 0 for n in range(self.range_min, self.range_max + 1)}
        
        for _, row in self.data.iterrows():
            for col in self.ball_cols:
                try:
                    val = int(row[col])
                    if str(val) in counts:
                        counts[str(val)] += 1
                except Exception:
                    pass
        
        # Sort by frequency desc
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    def _analyze_features(self) -> Dict[str, Any]:
        """Analyzes structural features like Sum, Odds, etc."""
        sums = []
        odds = []
        spreads = []
        
        for _, row in self.data.iterrows():
            draw_numbers = []
            for col in self.ball_cols:
                try:
                    draw_numbers.append(int(row[col]))
                except Exception:
                    pass
            
            if not draw_numbers:
                continue
                
            sums.append(calculate_sum(draw_numbers))
            odds.append(count_odds(draw_numbers))
            spreads.append(calculate_spread(draw_numbers))
            
        stats = {
            "sum": {
                "mean": statistics.mean(sums) if sums else 0,
                "stdev": statistics.stdev(sums) if len(sums) > 1 else 0,
                "min": min(sums) if sums else 0,
                "max": max(sums) if sums else 0
            },
            "odd_even_balance": {
                "avg_odds": statistics.mean(odds) if odds else 0,
                # Simple distribution count
                "distribution": {str(k): odds.count(k) for k in set(odds)}
            },
             "spread": {
                "mean": statistics.mean(spreads) if spreads else 0,
                "min": min(spreads) if spreads else 0,
                "max": max(spreads) if spreads else 0
            }
        }
        return stats
