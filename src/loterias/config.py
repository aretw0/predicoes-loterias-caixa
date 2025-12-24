from pathlib import Path
import json

# Determine the absolute path to the project root
# This file is located at <project_root>/src/loterias/config.py
CURRENT_FILE = Path(__file__).resolve()
PACKAGE_ROOT = CURRENT_FILE.parent  # src/loterias
SRC_ROOT = PACKAGE_ROOT.parent      # src
PROJECT_ROOT = SRC_ROOT.parent      # <project_root>

CONFIG_DIR = SRC_ROOT / 'config'
PRICES_CONFIG_PATH = CONFIG_DIR / 'prices.json'

def get_prices_config() -> dict:
    """Loads the prices configuration from the JSON file."""
    if not PRICES_CONFIG_PATH.exists():
        print(f"Warning: Prices config file not found at {PRICES_CONFIG_PATH}")
        return {}
    
    try:
        with open(PRICES_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading prices config: {e}")
        return {}
