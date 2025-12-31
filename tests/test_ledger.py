import pytest
import pandas as pd
import os
import shutil
from src.judge.ledger import PredictionLedger

TEST_LEDGER_FILE = "tests/data/test_ledger.csv"

@pytest.fixture
def ledger():
    # Setup
    if os.path.exists(TEST_LEDGER_FILE):
        os.remove(TEST_LEDGER_FILE)
    
    l = PredictionLedger(filepath=TEST_LEDGER_FILE)
    yield l
    
    # Teardown
    if os.path.exists("tests/data"):
        shutil.rmtree("tests/data")

def test_ledger_creation(ledger):
    assert os.path.exists(TEST_LEDGER_FILE)
    df = pd.read_csv(TEST_LEDGER_FILE)
    expected_cols = ["timestamp", "game", "draw_number", "model_name", "predicted_numbers", "outcome", "metadata"]
    assert list(df.columns) == expected_cols

def test_log_prediction(ledger):
    ledger.log_prediction(
        model_name="test_model",
        game="megasena",
        draw_number=2000,
        predicted_numbers=[1, 2, 3, 4, 5, 6],
        metadata={"version": "v1"}
    )
    
    df = pd.read_csv(TEST_LEDGER_FILE)
    assert len(df) == 1
    assert df.iloc[0]['model_name'] == "test_model"
    assert df.iloc[0]['game'] == "megasena"
    assert "[1, 2, 3, 4, 5, 6]" in df.iloc[0]['predicted_numbers']
    assert '{"version": "v1"}' in df.iloc[0]['metadata']

def test_fetch_history_filtering(ledger):
    ledger.log_prediction("model_A", "megasena", 100, [1,2])
    ledger.log_prediction("model_B", "megasena", 100, [3,4])
    ledger.log_prediction("model_A", "lotofacil", 50, [1,2])
    
    df_a = ledger.fetch_history(model_name="model_A")
    assert len(df_a) == 2
    
    df_mega = ledger.fetch_history(game="megasena")
    assert len(df_mega) == 2
    
    df_combo = ledger.fetch_history(model_name="model_A", game="lotofacil")
    assert len(df_combo) == 1

def test_get_last_draw(ledger):
    ledger.log_prediction("m", "g", 10, [1])
    ledger.log_prediction("m", "g", 25, [1])
    ledger.log_prediction("m", "g", 5, [1])
    
    assert ledger.get_last_draw_number("g") == 25
    assert ledger.get_last_draw_number("other") == 0
