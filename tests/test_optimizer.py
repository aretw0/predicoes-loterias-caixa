import pytest
from unittest.mock import MagicMock, patch
from loterias.optimizer import GeneticOptimizer
from loterias.base import Lottery

@pytest.fixture
def mock_lottery():
    lottery = MagicMock(spec=Lottery)
    lottery.slug = 'megasena'
    lottery.name = 'Mega Sena'
    return lottery

@pytest.fixture
def game_config():
    return {'min': 1, 'max': 60, 'draw': 6, 'default_play': 6}

def test_optimizer_init(mock_lottery, game_config):
    opt = GeneticOptimizer(mock_lottery, game_config)
    assert opt.population_size == 20
    assert opt.prize_tiers == [4, 5, 6]

def test_create_individual(mock_lottery, game_config):
    opt = GeneticOptimizer(mock_lottery, game_config)
    ind = opt._create_individual()
    assert len(ind) == 3
    assert all(0.0 <= x <= 10.0 for x in ind)

@patch('loterias.optimizer.Backtester')
def test_calculate_fitness(mock_backtester_cls, mock_lottery, game_config):
    # Setup mock
    mock_instance = mock_backtester_cls.return_value
    mock_instance.run.return_value = {
        'hits_distribution': {4: 1, 0: 49} # 1 Quadra, 49 misses
    }
    
    opt = GeneticOptimizer(mock_lottery, game_config)
    ind = [1.0, 1.0, 1.0]
    
    score = opt._calculate_fitness(ind)
    
    # Check if backtester was called with silent=True (from our previous fix)
    mock_instance.run.assert_called_with(draws_to_test=50, prediction_size=6, silent=True)
    
    # Score should be > 0 (Quadra bonus)
    assert score > 0

@patch('loterias.optimizer.Backtester')
def test_optimize_flow(mock_backtester_cls, mock_lottery, game_config):
    # Mock return
    mock_instance = mock_backtester_cls.return_value
    mock_instance.run.return_value = {'hits_distribution': {0: 50}} # Zero hits
    
    # Run small optimization
    opt = GeneticOptimizer(mock_lottery, game_config, population_size=4, generations=2)
    best_weights = opt.optimize()
    
    assert len(best_weights) == 3
