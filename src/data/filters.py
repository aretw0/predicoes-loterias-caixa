from typing import List, Tuple
from .features import calculate_sum, count_odds, count_evens

class PredictionFilter:
    def __init__(self, filters_str: str):
        """
        Initializes filters from a string format like "sum:100-200,odd:3-4".
        """
        self.filters = self._parse_filters(filters_str)

    def _parse_filters(self, filters_str: str) -> dict:
        parsed = {}
        if not filters_str:
            return parsed
        
        parts = filters_str.split(',')
        for part in parts:
            if ':' not in part:
                continue
            key, val = part.split(':', 1)
            key = key.strip().lower()
            val = val.strip()
            
            if key == 'sum':
                min_val, max_val = self._parse_range(val)
                parsed['sum'] = (min_val, max_val)
            elif key == 'odd':
                min_val, max_val = self._parse_range(val)
                parsed['odd'] = (min_val, max_val)
            elif key == 'even':
                min_val, max_val = self._parse_range(val)
                parsed['even'] = (min_val, max_val)
                
        return parsed

    def _parse_range(self, val: str) -> Tuple[int, int]:
        if '-' in val:
            min_s, max_s = val.split('-', 1)
            return int(min_s), int(max_s)
        else:
            v = int(val)
            return v, v

    def validate(self, numbers: List[int]) -> bool:
        """
        Checks if the provided numbers satisfy all active filters.
        """
        if not numbers:
            return False

        if 'sum' in self.filters:
            s = calculate_sum(numbers)
            min_v, max_v = self.filters['sum']
            if not (min_v <= s <= max_v):
                return False

        if 'odd' in self.filters:
            odd_count = count_odds(numbers)
            min_v, max_v = self.filters['odd']
            if not (min_v <= odd_count <= max_v):
                return False
                
        if 'even' in self.filters:
            even_count = count_evens(numbers)
            min_v, max_v = self.filters['even']
            if not (min_v <= even_count <= max_v):
                return False

        return True
