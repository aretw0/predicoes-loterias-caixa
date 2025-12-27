from typing import List

def calculate_sum(numbers: List[int]) -> int:
    """Calculates the sum of the numbers."""
    return sum(numbers)

def count_odds(numbers: List[int]) -> int:
    """Counts the number of odd numbers."""
    return sum(1 for n in numbers if n % 2 != 0)

def count_evens(numbers: List[int]) -> int:
    """Counts the number of even numbers."""
    return sum(1 for n in numbers if n % 2 == 0)

def calculate_spread(numbers: List[int]) -> int:
    """Calculates the difference between max and min number."""
    if not numbers:
        return 0
    return max(numbers) - min(numbers)
