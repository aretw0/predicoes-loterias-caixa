import pytest
import pandas as pd
import numpy as np
from src.loterias.models.catboost_model import CatBoostModel

@pytest.fixture
def mock_data():
    # 60 draws (needs > 50 for warm-up), numbers 1-10
    data = []
    for i in range(60):
        # Draw 2 numbers
        drawn = sorted(list(np.random.choice(range(1, 11), 2, replace=False)))
        data.append({'concours': i, 'dezenas': drawn})
    return pd.DataFrame(data)

def test_catboost_initialization():
    model = CatBoostModel(1, 10, 2)
    assert model.name == "CatBoost"
    assert not model.trained

def test_catboost_train_predict(mock_data):
    model = CatBoostModel(1, 10, 2)
    
    # Train
    model.train(mock_data, iterations=10) # Reduce iterations for speed in test
    assert model.trained
    assert hasattr(model, 'final_gaps')
    
    # Predict
    prediction = model.predict(count=2)
    assert len(prediction) == 2
    assert all(isinstance(x, (int, np.integer)) for x in prediction)
    assert all(1 <= x <= 10 for x in prediction)

def test_catboost_predict_untrained():
    model = CatBoostModel(1, 10, 2)
    # CatBoostModel returns empty list if untrained, unlike RF which raises ValueError
    assert model.predict() == []
