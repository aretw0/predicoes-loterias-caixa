import unittest
import os
import shutil
import pandas as pd
from unittest.mock import MagicMock
from src.loterias.snapshot_manager import SnapshotManager
from src.loterias.base import Lottery

class MockLottery(Lottery):
    def __init__(self):
        super().__init__("MockLottery", "mock_slug", "http://mock")
    
    def preprocess_data(self):
        # Return dataframe suitable for Transformer/LSTM
        data = []
        for i in range(20):
            row = {'concours': i}
            # Add ball columns expected by models
            for j in range(1, 7):
                row[f'bola{j}'] = j # simple
            data.append(row)
        return pd.DataFrame(data)

    def load_data(self):
        pass

class TestSnapshotManagerIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/data/snapshots_integration"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Override logger path strictly for test?
        # SnapshotManager uses global logger import which uses default path.
        # Ideally we'd patch TrainingLogger, but let's check the real file.
        # We'll rely on it writing to data/training_log.csv and cleanup not strictly necessary 
        # for personal dev env, but good practice.
        # Or better: patch TrainingLogger in SnapshotManager?
        
        # For simplicity in this environment, I'll let it write to real log and check it.
        # Actually, let's backup real log if exists.
        self.real_log = "data/training_log.csv"
        self.real_log_bak = "data/training_log.csv.bak"
        if os.path.exists(self.real_log):
            os.rename(self.real_log, self.real_log_bak)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
        # Restore log
        if os.path.exists(self.real_log_bak):
            if os.path.exists(self.real_log):
                os.remove(self.real_log)
            os.rename(self.real_log_bak, self.real_log)
        elif os.path.exists(self.real_log):
            # If we created it and no backup, maybe keep it? Or delete?
            # It's a test run, better delete to avoid pollution.
            os.remove(self.real_log)

    def test_cultivate_integration(self):
        lottery = MockLottery()
        manager = SnapshotManager(lottery, base_dir=self.test_dir)
        
        # Only train transformer for speed
        manager.cultivate_generalists(epochs=1, models=['transformer'], force_retrain=True)
        
        # Check if log file exists and has rows
        self.assertTrue(os.path.exists(self.real_log))
        df = pd.read_csv(self.real_log)
        self.assertGreater(len(df), 0)
        self.assertTrue((df['model_type'] == 'transformer').any())
        self.assertTrue((df['epoch'] == 1).any())
        
        # Check if snapshot saved
        # Manager saves to snapshots_integration/mocklottery/generalistas/transformer_...
        # Just check if directory structure exists
        expected_dir = os.path.join(self.test_dir, "mocklottery", "generalistas")
        self.assertTrue(os.path.exists(expected_dir), f"Directory {expected_dir} not found")
        files = os.listdir(expected_dir)
        self.assertTrue(any("transformer" in f for f in files))

if __name__ == '__main__':
    unittest.main()
