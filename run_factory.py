#!/usr/bin/env python3
import argparse
import sys
import os

# Add src to path if running from root without package install
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from loterias.megasena import MegaSena
from loterias.snapshot_manager import SnapshotManager

def main():
    parser = argparse.ArgumentParser(description="🏭 Preloto Snapshot Factory (Local Edition)")
    parser.add_argument('--game', default='megasena', help='Lottery game (currently only megasena supported)')
    parser.add_argument('--epochs', type=int, default=100, help='Number of training epochs (default: 100)')
    parser.add_argument('--mode', choices=['all', 'generalist', 'specialist'], default='all', help='Cultivation mode')
    
    args = parser.parse_args()

    print(f"🏭 Starting Local Factory")
    print(f"   Game: {args.game}")
    print(f"   Epochs: {args.epochs}")
    print(f"   Mode: {args.mode}")
    print("-" * 30)

    # Instantiate Manager
    if args.game == 'megasena':
        lottery = MegaSena()
    else:
        print(f"Error: Game {args.game} not yet supported in this script.")
        return

    manager = SnapshotManager(lottery)

    # 1. Generalists
    if args.mode in ['all', 'generalist']:
        print("\n🌱 Cultivating Generalists...")
        manager.cultivate_generalists(epochs=args.epochs)

    # 2. Specialists
    if args.mode in ['all', 'specialist']:
        print("\n🌱 Cultivating Specialists (Virada/Acumulados)...")
        
        # Filtro Acumulados (Final 0 ou 5)
        # Note: This reproduces logic from snapshot_factory.ipynb
        def filtro_acumulados(df):
            if 'Concurso' in df.columns:
                return df[df['Concurso'] % 5 == 0].copy()
            return df[df.index % 5 == 0].copy()

        manager.cultivate_specialists(
            filter_name="virada", # Saving as 'virada' to match notebook folder structure
            filter_func=filtro_acumulados,
            epochs=args.epochs
        )

    print("\n✅ Factory Work Complete! Snapshots saved in 'snapshots/' folder.")

if __name__ == "__main__":
    main()
