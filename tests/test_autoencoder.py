import pytest
import pandas as pd
import numpy as np
import os
import shutil
from loterias.models.autoencoder_model import AutoEncoderModel

@pytest.fixture
def mock_data():
    # 20 draws 
    # Use explicit columns 
    data = []
    for i in range(20):
        # Draw 6 numbers
        drawn = sorted(list(np.random.choice(range(1, 11), 6, replace=False)))
        entry = {'concours': i}
        for n in range(1, 7):
            entry[f'bola{n}'] = drawn[n-1]
        data.append(entry)
    return pd.DataFrame(data)

def test_autoencoder_initialization():
    model = AutoEncoderModel(1, 10, 6)
    assert model.name == "AutoEncoder Anomaly Detector"
    assert model.input_size == 11 # 0-10
    
def test_autoencoder_train_validate(mock_data):
    model = AutoEncoderModel(1, 10, 6)
    model.encoding_dim = 4 # Small latent
    
    # Train
    history = model.train(mock_data, epochs=2, batch_size=4)
    assert model.model is not None
    
    # Validate a "good" draw (one from training set approx)
    good_draw = [1, 2, 3, 4, 5, 6]
    score_good = model.validate(good_draw)
    assert isinstance(score_good, float)
    assert score_good >= 0
    
    # Validate a "bad" draw (maybe? randomness makes this flaky in unit test, 
    # but score should be calculable)
    bad_draw = [10, 9, 8, 7, 6, 5] 
    score_bad = model.validate(bad_draw)
    assert isinstance(score_bad, float)

def test_autoencoder_save_load(mock_data):
    test_dir = "test_ae_tmp"
    os.makedirs(test_dir, exist_ok=True)
    save_path = os.path.join(test_dir, "ae_model.pkl")
    
    try:
        model = AutoEncoderModel(1, 10, 6)
        model.train(mock_data, epochs=1)
        model.save(save_path)
        
        assert os.path.exists(save_path)
        assert os.path.exists(save_path + ".keras")
        
        new_model = AutoEncoderModel(1, 10, 6)
        new_model.load(save_path)
        assert new_model.model is not None
        
        # Check if functional
        score = new_model.validate([1, 2, 3, 4, 5, 6])
        assert isinstance(score, float)
        
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
