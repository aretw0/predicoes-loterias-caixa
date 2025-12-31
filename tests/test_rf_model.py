import pytest
import pandas as pd
import numpy as np
from loterias.models.rf_model import RandomForestModel

@pytest.fixture
def mock_data():
    # 60 draws (needs > 50 for warm-up), numbers 1-10
    data = []
    for i in range(60):
        # Draw 2 numbers
        drawn = sorted(list(np.random.choice(range(1, 11), 2, replace=False)))
        data.append({'concours': i, 'dezenas': drawn})
    return pd.DataFrame(data)

def test_rf_initialization():
    model = RandomForestModel(1, 10, 2)
    assert model.name == "Random Forest Model"
    assert not model.trained

def test_rf_train_predict(mock_data):
    model = RandomForestModel(1, 10, 2)
    
    # Train
    model.train(mock_data)
    assert model.trained
    assert hasattr(model, 'final_gaps')
    
    # Predict
    prediction = model.predict(count=2)
    assert len(prediction) == 2
    assert all(isinstance(x, (int, np.integer)) for x in prediction)
    assert all(1 <= x <= 10 for x in prediction)

def test_rf_predict_untrained():
    model = RandomForestModel(1, 10, 2)
    with pytest.raises(ValueError):
        model.predict()
