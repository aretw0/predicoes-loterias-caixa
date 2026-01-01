import unittest
import subprocess
import sys
import json

class TestCLIFlow(unittest.TestCase):
    
    def test_preloto_simple(self):
        # Run preloto megasena
        cmd = [sys.executable, "-m", "cli.main", "megasena"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"CLI failed: {result.stderr}")
        
        # Check Output
        data = json.loads(result.stdout)
        self.assertEqual(data['game'], "megasena")
        self.assertEqual(data['model'], "random")
        self.assertEqual(len(data['numbers']), 20) # Default max

    def test_preloto_with_model_args(self):
        # Run preloto megasena --model frequency --model-args order:asc
        cmd = [
            sys.executable, "-m", "cli.main", 
            "megasena",
            "--model", "frequency",
            "--model-args", "order:asc"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"CLI failed: {result.stderr}")
        
        # Check Output
        data = json.loads(result.stdout)
        self.assertEqual(data['game'], "megasena")
        self.assertEqual(data['model'], "frequency")
        # CLI injects 'epochs' by default (from args.epochs=50)
        self.assertEqual(data['parameters'], {"order": "asc", "epochs": 50})

if __name__ == '__main__':
    unittest.main()
