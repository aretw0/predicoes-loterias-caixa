import pytest
import pandas as pd
import numpy as np
from models.deep.transformer import TransformerModel

@pytest.fixture
def mock_data():
    # 60 draws (needs > 50 for warm-up), numbers 1-10
    # Use explicit columns 'bola1', 'bola2' to match _prepare_sequences expectation
    data = []
    for i in range(60):
        # Draw 2 numbers
        drawn = sorted(list(np.random.choice(range(1, 11), 2, replace=False)))
        data.append({'concours': i, 'bola1': drawn[0], 'bola2': drawn[1]})
    return pd.DataFrame(data)

def test_transformer_initialization():
    model = TransformerModel(1, 10, 2)
    assert model.name == "Transformer Attention"
    assert not model.model

def test_transformer_train_predict(mock_data):
    # Use smaller model for test speed
    model = TransformerModel(1, 10, 2)
    model.head_size = 4
    model.num_heads = 2
    model.ff_dim = 4
    model.window_size = 5
    
    # Train
    model.train(mock_data, epochs=2, batch_size=8, window_size=5) 
    assert model.model is not None
    
    # Predict
    prediction = model.predict(count=2)
    assert len(prediction) == 2
    assert all(isinstance(x, (int, np.integer)) for x in prediction)
    assert all(1 <= x <= 10 for x in prediction)

def test_transformer_predict_untrained():
    model = TransformerModel(1, 10, 2)
    assert model.predict() == []
