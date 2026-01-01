import pytest
import os
import shutil
import pandas as pd
from src.judge.logger import TrainingLogger

TEST_LOG_FILE = "tests/data/test_training_log.csv"

@pytest.fixture
def logger():
    if os.path.exists(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)
    l = TrainingLogger(filepath=TEST_LOG_FILE)
    yield l
    if os.path.exists("tests/data"):
        shutil.rmtree("tests/data")

def test_logger_creation(logger):
    assert os.path.exists(TEST_LOG_FILE)
    df = pd.read_csv(TEST_LOG_FILE)
    assert "val_loss" in df.columns

def test_log_epoch(logger):
    metrics = {"loss": 0.5, "accuracy": 0.8, "val_loss": 0.6, "val_accuracy": 0.7}
    logger.log_epoch("lstm", 1, metrics, params_hash="abc", metadata={"lr": 0.001})
    
    df = pd.read_csv(TEST_LOG_FILE)
    assert len(df) == 1
    assert df.iloc[0]['model_type'] == "lstm"
    assert df.iloc[0]['epoch'] == 1
    assert df.iloc[0]['loss'] == 0.5
    assert '{"lr": 0.001}' in df.iloc[0]['metadata']

def test_get_history(logger):
    logger.log_epoch("lstm", 1, {"loss": 0.5}, params_hash="abc")
    logger.log_epoch("lstm", 2, {"loss": 0.4}, params_hash="abc")
    logger.log_epoch("rf", 1, {"loss": 0.1}, params_hash="xyz")
    
    df = logger.get_history(model_type="lstm")
    assert len(df) == 2
    
    df_hash = logger.get_history(params_hash="xyz")
    assert len(df_hash) == 1
