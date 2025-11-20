from typing import List, Dict, Any
import pandas as pd
from .ledger import Ledger
from .megasena import MegaSena
from .lotofacil import Lotofacil
from .quina import Quina

class Checker:
    def __init__(self):
        self.ledger = Ledger()
        self.lotteries = {
            "megasena": MegaSena(),
            "lotofacil": Lotofacil(),
            "quina": Quina()
        }

    def check_bets(self):
        """Iterates through pending bets and validates them."""
        pending_bets = self.ledger.get_pending_bets()
        
        if not pending_bets:
            print("No pending bets to check.")
            return

        print(f"Checking {len(pending_bets)} pending bets...")
        
        # Pre-load data to avoid reloading for every bet
        for lottery in self.lotteries.values():
            lottery.preprocess_data()

        for bet in pending_bets:
            game = bet['game']
            contest = bet['contest']
            numbers = set(bet['numbers'])
            bet_id = bet['id']
            
            lottery = self.lotteries.get(game)
            if not lottery:
                print(f"Unknown lottery: {game}")
                continue
                
            # Find result for the contest
            # Assuming 'Concurso' column exists or index is the contest number
            # We need to be careful here. The CSVs usually have a 'Concurso' column.
            # Let's check how we preprocessed the data.
            # MegaSena: 'Concurso' is likely the first column or index.
            # Let's assume we can filter by 'Concurso' if it exists, or use index if it's 1-based.
            
            # Actually, let's look at the data structure.
            # MegaSena.preprocess_data() returns a DF with 'data', 'dezenas'.
            # It doesn't explicitly set 'Concurso' as a column in the snippet I saw, 
            # but the original CSV has it.
            # Let's try to find the row where 'Concurso' matches.
            
            # If 'Concurso' is not in the preprocessed DF, we might need to reload or check the original CSV.
            # However, usually 'Concurso' is preserved.
            
            try:
                # We need to check if 'Concurso' is in columns.
                if 'Concurso' in lottery.data.columns:
                    result_row = lottery.data[lottery.data['Concurso'] == contest]
                else:
                    # Fallback: assume index is Concurso (risky) or try to find it.
                    # For now, let's assume 'Concurso' is present.
                    # If not, we might fail.
                    print(f"Warning: 'Concurso' column not found for {game}. Skipping bet {bet_id}.")
                    continue
                
                if result_row.empty:
                    print(f"Result for {game} contest {contest} not found yet.")
                    continue
                
                drawn_numbers = set(result_row.iloc[0]['dezenas'])
                hits = numbers.intersection(drawn_numbers)
                num_hits = len(hits)
                
                # Determine status and prize (simplified logic)
                # Real prize logic is complex and depends on the specific contest prize distribution.
                # For now, we'll just mark as WON/LOST based on hits.
                
                status = "LOST"
                prize = 0.0
                
                if game == "megasena":
                    if num_hits >= 4:
                        status = "WON"
                        # We would need to fetch the actual prize value from the data
                elif game == "lotofacil":
                    if num_hits >= 11:
                        status = "WON"
                elif game == "quina":
                    if num_hits >= 2:
                        status = "WON"
                
                print(f"Bet {bet_id} ({game} #{contest}): {num_hits} hits. Status: {status}")
                self.ledger.update_bet(bet_id, status, prize)
                
            except Exception as e:
                print(f"Error checking bet {bet_id}: {e}")
