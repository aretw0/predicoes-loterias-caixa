import pytest
import pandas as pd
import numpy as np
from loterias.models.lstm_model import LSTMModel

@pytest.fixture
def mock_data():
    # Create synthetic data resembling lottery draws
    # 20 draws, numbers 1-10
    columns = ['bola1', 'bola2', 'bola3', 'bola4', 'bola5', 'bola6']
    data = []
    for i in range(20):
        # Generate sorted random numbers
        draw = sorted(np.random.choice(range(1, 11), size=6, replace=False))
        data.append(draw)
    
    df = pd.DataFrame(data, columns=columns)
    df['data'] = pd.date_range(start='2023-01-01', periods=20)
    return df

def test_lstm_initialization():
    model = LSTMModel(range_min=1, range_max=10, draw_count=6)
    assert model.name == "LSTM Deep Learning"
    assert model.range_max == 10

def test_data_preparation(mock_data):
    model = LSTMModel(range_min=1, range_max=10, draw_count=6)
    model.window_size = 5
    X, y = model._prepare_sequences(mock_data)
    
    # 20 draws. Window=5. 
    # Total sequences = 20 - 5 = 15
    assert len(X) == 15
    assert len(y) == 15
    
    # X shape: (15, 5, 15) -> 11 one-hot + 4 features
    assert X.shape == (15, 5, 15)
    # y shape: (15, 11)
    assert y.shape == (15, 11)

def test_train_and_predict(mock_data):
    model = LSTMModel(range_min=1, range_max=10, draw_count=6)
    model.window_size = 3
    
    # Train for 1 epoch to speed up test
    history = model.train(mock_data, epochs=1, batch_size=2)
    assert history is not None
    assert model.model is not None
    
    # Predict
    # We pass data so it can pick the last window
    prediction = model.predict(data=mock_data, count=6)
    
    assert isinstance(prediction, list)
    assert len(prediction) == 6
    # Check values in range
    for num in prediction:
        assert 0 <= num <= 10
