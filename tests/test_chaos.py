
import pytest
from judge.ensemble import EnsemblePredictor
from core.games.megasena import MegaSena

def test_ensemble_chaos_prediction():
    """
    Verifies that EnsemblePredictor respects the 'count' argument
    returning more than the standard amount of numbers (Chaos Engineering).
    """
    lottery = MegaSena()
    
    # Use small range for speed in test
    # Mocking lottery range temporarily or just running with real data (slow but accurate)
    # We'll run with real data but limit models params for speed
    
    model_args = {
        'n_estimators': 2, # Super fast RF/XGB
        'epochs': 1        # Super fast LSTM
    }
    
    predictor = EnsemblePredictor(lottery, 1, 60, 6, model_args=model_args)
    
    # Request 15 numbers (Chaos Bet)
    result = predictor.predict_next(count=15)
    
    assert 'suggestion' in result
    assert len(result['suggestion']) == 15
    assert result['suggestion'] == sorted(result['suggestion'])
    
    # Request 20 numbers
    result_20 = predictor.predict_next(count=20)
    assert len(result_20['suggestion']) == 20

