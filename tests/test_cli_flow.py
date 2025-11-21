import unittest
import os
import csv
import json
import subprocess
import sys

class TestCLIFlow(unittest.TestCase):
    TEST_LEDGER = "test_ledger.csv"

    def setUp(self):
        # Clean up test ledger if exists
        if os.path.exists(self.TEST_LEDGER):
            os.remove(self.TEST_LEDGER)
        
        # We need to mock the Ledger class to use a different filename, 
        # but since we are running via subprocess, we can't easily inject it.
        # Instead, we will rename the real ledger.csv temporarily if it exists,
        # or just accept that we are writing to the real ledger?
        # NO, that's dangerous.
        # Let's modify the CLI to accept a --ledger argument? 
        # Or just rename the real ledger temporarily.
        self.real_ledger = "ledger.csv"
        self.backup_ledger = "ledger.csv.bak"
        if os.path.exists(self.real_ledger):
            os.rename(self.real_ledger, self.backup_ledger)

    def tearDown(self):
        # Restore real ledger
        if os.path.exists(self.TEST_LEDGER):
            os.remove(self.TEST_LEDGER) # Actually, the CLI writes to 'ledger.csv'
        
        if os.path.exists("ledger.csv"):
            os.remove("ledger.csv")

        if os.path.exists(self.backup_ledger):
            os.rename(self.backup_ledger, self.real_ledger)

    def test_predict_with_model_args(self):
        # Run the CLI command
        cmd = [
            sys.executable, "src/cli.py", "predict",
            "--game", "megasena",
            "--model", "frequency",
            "--numbers", "6",
            "--model-args", "order:asc",
            "--save",
            "--contest", "9999"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check if command ran successfully
        self.assertEqual(result.returncode, 0, f"CLI failed: {result.stderr}")
        
        # Check if ledger.csv was created
        self.assertTrue(os.path.exists("ledger.csv"), "ledger.csv was not created")
        
        # Check content of ledger.csv
        with open("ledger.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1, "Should have exactly 1 bet")
            row = rows[0]
            self.assertEqual(row['game'], "megasena")
            self.assertEqual(row['model'], "frequency")
            self.assertEqual(row['contest'], "9999")
            
            # Check parameters
            params = json.loads(row['parameters'])
            self.assertEqual(params, {"order": "asc"})

if __name__ == '__main__':
    unittest.main()
