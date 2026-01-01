import unittest
import pandas as pd
import os
from datetime import datetime, timedelta
from ops.inspector import TrainingInspector

class TestTrainingInspector(unittest.TestCase):
    def setUp(self):
        self.test_log = "tests/test_training_log.csv"
        # Create dummy log
        data = []
        base_time = datetime.now() - timedelta(hours=1)
        
        # Run 1: LSTM (Improving)
        for i in range(1, 6):
            data.append({
                'timestamp': (base_time + timedelta(minutes=i)).isoformat(),
                'model_type': 'lstm',
                'epoch': i,
                'loss': 0.5 - (i * 0.01),
                'accuracy': 0.5 + (i * 0.01),
                'val_loss': 0.5 - (i * 0.01), # Improving
                'val_accuracy': 0.5 + (i * 0.01),
                'params_hash': 'hash1',
                'metadata': '{}'
            })
            
        # Run 2: Transformer (Overfitting)
        base_time_2 = datetime.now()
        for i in range(1, 10):
            val_loss = 0.4 if i == 4 else 0.45 + abs(i-4)*0.01  # Epoch 4 is 0.4, others higher
            data.append({
                'timestamp': (base_time_2 + timedelta(minutes=i)).isoformat(),
                'model_type': 'transformer',
                'epoch': i,
                'loss': 0.3 - (i * 0.01), 
                'accuracy': 0.8,
                'val_loss': val_loss, 
                'val_accuracy': 0.7,
                'params_hash': 'hash2',
                'metadata': '{}'
            })
            
        df = pd.DataFrame(data)
        df.to_csv(self.test_log, index=False)
        
    def tearDown(self):
        if os.path.exists(self.test_log):
            os.remove(self.test_log)
            
    def test_run_grouping(self):
        inspector = TrainingInspector(self.test_log)
        runs = inspector.get_runs()
        
        self.assertEqual(len(runs), 2)
        # Sorts by recency, so Transformer (Run 2) should be first
        self.assertEqual(runs[0]['model_type'], 'transformer')
        self.assertEqual(runs[0]['total_epochs'], 9)
        
        self.assertEqual(runs[1]['model_type'], 'lstm')
        self.assertEqual(runs[1]['total_epochs'], 5)

    def test_metrics_lstm(self):
        inspector = TrainingInspector(self.test_log)
        runs = inspector.get_runs(model_filter='lstm')
        run = runs[0]
        
        self.assertEqual(run['status'], "Learning (Improving)")
        self.assertEqual(run['best_epoch'], 5) # Continually improved
        
    def test_metrics_transformer(self):
        inspector = TrainingInspector(self.test_log)
        runs = inspector.get_runs(model_filter='transformer')
        run = runs[0]
        
        self.assertIn("OVERFITTING", run['status'])
        self.assertEqual(run['best_epoch'], 4) # Epoch 4 had 0.4, Epoch 5 had 0.4 + 0 = 0.4. Wait. 
        # range(1, 10): 1,2,3,4. 
        # i=1 (idx 0): 0.4
        # i=4 (idx 3): 0.4
        # i=5 (idx 4): 0.4 + 0 = 0.4.
        # i=6: 0.45.
        # So min loss is 0.4. Best epoch could be 1, 2, 3, 4, 5. Min usually takes first occurrence? 
        # Our code: `val_losses.index(min_val_loss)`. So first index.
        # So it should be Epoch 1. 
        # Let's adjust expectation or data to be stricter.
        
if __name__ == '__main__':
    unittest.main()
