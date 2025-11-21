# Hypothetical Tracking System Walkthrough

This walkthrough documents the implementation and verification of the Hypothetical Tracking System (Phase 3), including the refined pricing logic.

## Features Implemented

### Ledger

- `src/loterias/ledger.py`: Manages a CSV-based ledger (`ledger.csv`) to store bets.
- Records: ID, Date, Game, Contest, Numbers, Model, Cost, Status, Prize.

### Checker

- `src/loterias/checker.py`: Validates pending bets against historical data.
- Updates bet status (WON/LOST) and prize.

### Pricing & Cost Analysis

- `src/config/prices.json`: Stores current bet prices, including tables for betting with more numbers.
- CLI updated to accept `--numbers` and calculate cost based on the quantity of numbers played.
- **Note**: Prices in `prices.json` reflect the current configuration (e.g., Mega Sena base R$ 6.00).

## Verification Results

### Cost Analysis (Mega Sena)

Command: `python -m src.cli predict --game megasena --numbers 7 --count 1`
Result:

```txt
--- Cost Analysis ---
Game: Mega Sena
Numbers per bet: 7
Price per bet: R$ 42.00
Total Cost (1 bets): R$ 42.00
---------------------
```

(Calculated as 7 combinations * R$ 6.00)

### Cost Analysis (Lotofácil)

Command: `python -m src.cli predict --game lotofacil --numbers 16 --count 1`
Result:

```txt
--- Cost Analysis ---
Game: Lotofacil
Numbers per bet: 16
Price per bet: R$ 56.00
Total Cost (1 bets): R$ 56.00
---------------------
```

(Calculated as 16 combinations * R$ 3.50)

### Group Bet Logic (Count = Split)

Command: `python -m src.cli predict --game megasena --numbers 7 --split 3`
Result:

```txt
--- Cost Analysis ---
Game: Mega Sena
Numbers per bet: 7
Price per bet: R$ 42.00
Total Cost (3 bets): R$ 126.00
Split among 3 people: R$ 42.00 per person
---------------------
```

(Automatically generated 3 bets for 3 people)

### Ledger Recording

Command: `python -m src.cli predict --game megasena --model random --count 1 --save --contest 2500`
Result: Bet recorded in `ledger.csv` with status `PENDING`.

### Checker Validation

Command: `python -m src.cli check`
Result:

```txt
Checking 1 pending bets...
Bet 5b12db18 (megasena #2500): 0 hits. Status: LOST
```

Ledger updated with status `LOST`.
