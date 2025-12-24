import pytest
import pandas as pd
from src.loterias.models import RandomModel, FrequencyModel

@pytest.fixture
def mock_data():
    # Create a small dataset for testing
    # Numbers: 1 (appears 3x), 2 (appears 2x), 3 (appears 1x)
    data = {
        'dezenas': [
            [1, 2, 4],
            [1, 5, 2],
            [1, 6, 3]
        ]
    }
    return pd.DataFrame(data)

def test_random_model_determinism():
    """Test that RandomModel produces identical output with the same seed."""
    model = RandomModel(range_min=1, range_max=10, draw_count=5)
    
    # Run 1
    pred1 = model.predict(seed=42)
    
    # Run 2
    pred2 = model.predict(seed=42)
    
    assert pred1 == pred2, "Output should be identical for same seed"
    
def test_random_model_randomness():
    """Test that RandomModel produces different output without seed (likely)."""
    model = RandomModel(range_min=1, range_max=100, draw_count=5)
    pred1 = model.predict()
    pred2 = model.predict()
    # There is a tiny chance they are equal, but very unlikely with range 100
    assert pred1 != pred2

def test_frequency_model_least_frequent(mock_data):
    """Test 'surfing' strategy: picking numbers that appeared LESS."""
    # Data stats:
    # 1: 3 times
    # 2: 2 times
    # 3: 1 time
    # 4, 5, 6: 1 time
    # 7, 8, 9, 10: 0 times
    
    model = FrequencyModel(range_min=1, range_max=10, draw_count=3)
    model.train(mock_data)
    
    # Predict asking for least frequent (order='asc')
    # Should prefer numbers with count 0 (7,8,9,10), then count 1 (3,4,5,6)
    prediction = model.predict(count=3, order='asc')
    
    # Since 7,8,9,10 have 0 frequency, they should be top picks.
    # Deterministic tie-break (by value) means 7, 8, 9 should be picked if we sort by value secondary.
    assert prediction == [7, 8, 9]

def test_frequency_model_most_frequent(mock_data):
    """Test strategy: picking numbers that appeared MOST."""
    model = FrequencyModel(range_min=1, range_max=10, draw_count=3)
    model.train(mock_data)
    
    # Predict asking for most frequent (order='desc')
    # Should pick 1 (count 3), then 2 (count 2), then one of 3,4,5,6 (count 1)
    prediction = model.predict(count=2, order='desc')
    
    assert 1 in prediction
    assert 2 in prediction

def test_frequency_model_tie_breaking(mock_data):
    """Test that ties are broken deterministically (by value)."""
    # 4, 5, 6 appear once. 
    # If we ask for least frequent, after 7,8,9,10 (0 times), we have the 1-timers.
    # We need to ensure we get a consistent subset if we ask for more.
    
    model = FrequencyModel(range_min=1, range_max=10, draw_count=5)
    model.train(mock_data)
    
    # 0-freqs: 7, 8, 9, 10
    # 1-freqs: 3, 4, 5, 6
    # asking for 5 numbers.
    # Should get 7, 8, 9, 10 AND the lowest value from 1-freqs -> 3.
    # Prediction should be sorted: [3, 7, 8, 9, 10]
    
    prediction = model.predict(count=5, order='asc')
    assert prediction == [3, 7, 8, 9, 10]
