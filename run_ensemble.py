#!/usr/bin/env python3
import argparse
import sys
import os
import glob
import glob

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from loterias.megasena import MegaSena
from loterias.ensemble_predictor import EnsemblePredictor

def find_snapshots(game_name, mode='auto'):
    """
    Automatically finds the best snapshot for each model type.
    Mode 'auto': Priority Especialista > Generalista
    Mode 'generalist': Only Generalista
    Mode 'specialist': Only Especialista
    """
    base_dir = f"snapshots/{game_name}"
    snapshots = {}
    
    # Paths to search based on mode
    paths_to_check = []
    
    if mode in ['auto', 'specialist']:
        paths_to_check.append(f"{base_dir}/especialistas/virada/")
        # paths_to_check.append(f"{base_dir}/especialistas/acumulados/") # Future support
        
    if mode in ['auto', 'generalist']:
        paths_to_check.append(f"{base_dir}/generalistas/")
        
    def find_first(pattern):
        for path in paths_to_check:
            files = glob.glob(f"{path}/{pattern}")
            if files:
                return files[0]
        return None

    # 1. CatBoost
    cb_path = find_first("catboost_*.cbm")
    if cb_path: 
        # Strip extension because model.load() expects base path (it adds .cbm itself)
        snapshots['catboost'] = cb_path.replace(".cbm", "")

    # 2. LSTM
    lstm_path = find_first("lstm_*.keras")
    if lstm_path: 
        # Strip extension because model.load() expects base path (it adds .keras itself)
        snapshots['lstm'] = lstm_path.replace(".keras", "")

    # 3. Transformer (Optional)
    trans_path = find_first("transformer_*.keras")
    # if trans_path: ... (EnsemblePredictor needs support first)
    
    return snapshots

def main():
    parser = argparse.ArgumentParser(description="🔮 Preloto Ensemble Runner (Local Inference)")
    parser.add_argument('--game', default='megasena', help='Lottery game')
    parser.add_argument('--mode', choices=['auto', 'generalist', 'specialist'], default='auto', help='Snapshot selection strategy (default: auto)')
    args = parser.parse_args()

    print(f"🔮 Starting Local Ensemble Prediction")
    print(f"   Game: {args.game}")
    print(f"   Mode: {args.mode}")
    print("-" * 30)

    if args.game == 'megasena':
        lottery = MegaSena()
    elif args.game == 'lotofacil':
        from loterias.lotofacil import Lotofacil
        lottery = Lotofacil()
    elif args.game == 'quina':
        from loterias.quina import Quina
        lottery = Quina()
    else:
        print(f"Error: Game {args.game} not supported.")
        return

    # Auto-detect snapshots
    print("🔎 Searching for cultivated snapshots...")
    # Handle folder name nuances (Mega Sena vs megasena)
    # Factory uses 'Mega Sena' (from .name) or 'megasena' (from slug)? 
    # SnapshotManager uses self.lottery.name.lower(). For MegaSena it is "mega sena".
    search_name = lottery.name.lower()
    
    snapshot_paths = find_snapshots(search_name, mode=args.mode)
    if not snapshot_paths and ' ' in search_name:
         # Try slug fallback if name with space fails
         snapshot_paths = find_snapshots(lottery.slug, mode=args.mode)
    
    if snapshot_paths:
        for model, path in snapshot_paths.items():
            print(f"   found {model}: {path}")
    else:
        print("   ⚠️ No snapshots found! Ensemble will train from scratch (slow).")

    # Instantiate Ensemble
    print("\n🧠 Initializing Ensemble...")
    # Instantiate Ensemble
    print("\n🧠 Initializing Ensemble...")
    predictor = EnsemblePredictor(
        lottery, 
        range_min=getattr(lottery, 'range_min', 1), 
        range_max=getattr(lottery, 'range_max', 60), 
        draw_count=getattr(lottery, 'draw_count', 6), 
        snapshot_paths=snapshot_paths
    )

    # Predict
    print("\n🎲 Generating Predictions...")
    prediction = predictor.predict_next()

    print("\n" + "="*30)
    print(f"✨ PALPITE FINAL ({args.game}):")
    print(f"   {prediction}")
    print("="*30)

if __name__ == "__main__":
    main()
