import unittest
import os
import shutil
import pandas as pd
import numpy as np
from loterias.models.frequency_model import FrequencyModel
from loterias.models.transformer_model import TransformerModel

class TestSnapshots(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_snapshots_tmp"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Mock Data
        data = []
        for i in range(20):
             data.append({'concours': i, 'dezenas': [1, 2, 3, 4, 5, 6]})
        self.df = pd.DataFrame(data)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_frequency_model_save_load(self):
        # 1. Train
        model = FrequencyModel(range_min=1, range_max=10, draw_count=6)
        model.train(self.df)
        self.assertIsNotNone(model.weights)
        
        # 2. Save
        save_path = os.path.join(self.test_dir, "freq_model.pkl")
        model.save(save_path)
        
        # 3. Load into new instance
        new_model = FrequencyModel(range_min=1, range_max=10, draw_count=6)
        self.assertIsNone(new_model.weights)
        
        new_model.load(save_path)
        
        # 4. Verify
        self.assertIsNotNone(new_model.weights)
        pd.testing.assert_series_equal(model.weights, new_model.weights)

    def test_transformer_model_save_load(self):
        # 1. Train (requires different data format usually, but let's try minimal)
        # Adapt data for Transformer
        data = []
        for i in range(60): # Needs > window size
             data.append({'concours': i, 'bola1': 1, 'bola2': 2, 'bola3': 3, 'bola4': 4, 'bola5': 5, 'bola6': 6})
        df_trans = pd.DataFrame(data)
        
        model = TransformerModel(range_min=1, range_max=10, draw_count=6)
        # Set small params for speed
        model.window_size = 5
        model.epochs = 1
        model.batch_size = 2
        model.head_size = 2
        model.num_heads = 1
        model.ff_dim = 2
        
        model.train(df_trans, epochs=1, batch_size=2)
        self.assertIsNotNone(model.model)
        
        # 2. Save
        save_path = os.path.join(self.test_dir, "trans_model.pkl")
        model.save(save_path)
        
        # Verify both files exist (pkl + keras)
        self.assertTrue(os.path.exists(save_path))
        self.assertTrue(os.path.exists(save_path + ".keras"))
        
        # 3. Load
        new_model = TransformerModel(range_min=1, range_max=10, draw_count=6)
        self.assertIsNone(new_model.model)
        
        new_model.load(save_path)
        
        # 4. Verify
        self.assertIsNotNone(new_model.model)
        # Check if can predict
        pred = new_model.predict(count=6, data=df_trans)
        self.assertEqual(len(pred), 6)

if __name__ == '__main__':
    unittest.main()
