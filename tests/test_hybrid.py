import pytest
import pandas as pd
from loterias.models import HybridModel

@pytest.fixture
def mock_data():
    # 1 appears 3x
    # 2 appears 2x
    # 3 appears 1x
    # 4 appears 0x (Gap is large)
    data = {
        'dezenas': [
            [1, 2, 3], # Draw 0
            [1, 2, 5],
            [1, 6, 7]  # Draw 2 (Last)
        ]
    }
    return pd.DataFrame(data)

def test_hybrid_gap_dominance(mock_data):
    # Set only gap weight to 1, others 0
    model = HybridModel(range_min=1, range_max=10, draw_count=1)
    model.train(mock_data)
    
    # 4 has never appeared, so gap is 3 (max).
    # 1 appeared last draw, gap 0.
    
    prediction = model.predict(count=1, w_gap=1.0, w_freq=0.0, w_surf=0.0)
    # The gap model favors 4 (never appeared / longest since).
    assert 4 in prediction

def test_hybrid_freq_dominance(mock_data):
    # Set only freq weight to 1
    model = HybridModel(range_min=1, range_max=10, draw_count=1)
    model.train(mock_data)
    
    # 1 is most frequent (3x).
    prediction = model.predict(count=1, w_gap=0.0, w_freq=1.0, w_surf=0.0)
    assert prediction == [1]

def test_hybrid_mixed(mock_data):
    # 1 is high freq (Score ~1.0) but low gap (Score ~0.0)
    # 4 is low freq (Score ~0.0) but high gap (Score ~1.0)
    
    model = HybridModel(range_min=1, range_max=10, draw_count=1)
    model.train(mock_data)
    
    # If we weight gap same as freq...
    # 1: F=1.0, G=0.0 -> T=0.5
    # 4: F=0.0, G=1.0 -> T=0.5
    # Tie break (by number value): 1 wins (1 < 4).
    
    prediction = model.predict(count=1, w_gap=1.0, w_freq=1.0, w_surf=0.0)
    assert prediction == [1] 
    
    # If we weight gap higher
    prediction = model.predict(count=1, w_gap=2.0, w_freq=1.0, w_surf=0.0)
    # 1: 1.0 + 0 = 1.0
    # 4: 0 + 2.0 = 2.0
    # 4 wins.
    assert prediction == [4]
