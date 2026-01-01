import json
import csv
from typing import List, Dict, Any

def export_to_json(predictions: List[Dict[str, Any]], filename: str):
    """Exports predictions to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(predictions, f, indent=4)
    print(f"Predictions exported to {filename}")

def export_to_csv(predictions: List[Dict[str, Any]], filename: str):
    """Exports predictions to a CSV file."""
    if not predictions:
        print("No predictions to export.")
        return

    fieldnames = predictions[0].keys()
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(predictions)
    print(f"Predictions exported to {filename}")
