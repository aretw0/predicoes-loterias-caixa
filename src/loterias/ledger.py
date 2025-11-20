import csv
import os
import datetime
from typing import List, Dict, Any

class Ledger:
    def __init__(self, filename: str = "ledger.csv"):
        self.filename = filename
        self.headers = ["id", "date", "game", "contest", "numbers", "model", "cost", "status", "prize"]
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    def add_bet(self, game: str, model: str, numbers: List[int], contest: int, cost: float):
        """Records a new bet."""
        bet_id = self._generate_id()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        numbers_str = " ".join(map(str, numbers))
        
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([bet_id, date, game, contest, numbers_str, model, cost, "PENDING", 0.0])
        
        print(f"Bet recorded with ID: {bet_id}")

    def get_pending_bets(self, game: str = None) -> List[Dict[str, Any]]:
        """Returns bets that haven't been checked yet."""
        pending_bets = []
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['status'] == "PENDING":
                    if game and row['game'] != game:
                        continue
                    # Parse numbers back to list
                    row['numbers'] = [int(n) for n in row['numbers'].split()]
                    row['contest'] = int(row['contest']) if row['contest'] else 0
                    pending_bets.append(row)
        return pending_bets

    def update_bet(self, bet_id: str, status: str, prize: float):
        """Updates the status and prize of a bet."""
        rows = []
        updated = False
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        for row in rows:
            if row['id'] == bet_id:
                row['status'] = status
                row['prize'] = prize
                updated = True
        
        if updated:
            with open(self.filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(rows)

    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())[:8]
