import argparse
import sys
from src.loterias.megasena import MegaSena
from src.loterias.lotofacil import Lotofacil
from src.loterias.quina import Quina
from src.loterias.models import RandomModel, FrequencyModel
from src.loterias.utils import export_to_json, export_to_csv
from src.loterias.ledger import Ledger
from src.loterias.checker import Checker

def main():
    parser = argparse.ArgumentParser(description="Lottery Prediction Engine CLI")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Predict Command
    predict_parser = subparsers.add_parser('predict', help='Generate predictions')
    predict_parser.add_argument('--game', type=str, required=True, choices=['megasena', 'lotofacil', 'quina'], help="The lottery game to predict for.")
    predict_parser.add_argument('--model', type=str, required=True, choices=['random', 'frequency'], help="The prediction model to use.")
    predict_parser.add_argument('--count', type=int, default=1, help="Number of predictions to generate.")
    predict_parser.add_argument('--numbers', type=int, help="Quantity of numbers to play (e.g., 6, 7, 15). Defaults to minimum for the game.")
    predict_parser.add_argument('--output', type=str, help="Output file for predictions (e.g., predictions.json or predictions.csv).")
    predict_parser.add_argument('--save', action='store_true', help="Save predictions to the Ledger.")
    predict_parser.add_argument('--contest', type=int, help="Target contest number (required if saving).")
    predict_parser.add_argument('--split', type=int, default=1, help="Number of people to split the cost with.")

    # Check Command
    check_parser = subparsers.add_parser('check', help='Check pending bets in the Ledger')

    args = parser.parse_args()

    if args.command == 'predict':
        run_predict(args)
    elif args.command == 'check':
        run_check(args)
    else:
        parser.print_help()

def run_predict(args):
    # Initialize Game
    if args.game == 'megasena':
        lottery = MegaSena()
        range_min, range_max, default_draw_count = 1, 60, 6
    elif args.game == 'lotofacil':
        lottery = Lotofacil()
        range_min, range_max, default_draw_count = 1, 25, 15
    elif args.game == 'quina':
        lottery = Quina()
        range_min, range_max, default_draw_count = 1, 80, 5
    else:
        print(f"Game {args.game} not supported.")
        sys.exit(1)

    # Determine quantity of numbers
    quantity = args.numbers if args.numbers else default_draw_count
    
    # Validate quantity
    # Simple validation, could be more robust based on game rules
    if quantity < default_draw_count:
        print(f"Error: Minimum numbers for {args.game} is {default_draw_count}.")
        sys.exit(1)

    # Initialize Model
    if args.model == 'random':
        model = RandomModel(range_min, range_max, default_draw_count)
    elif args.model == 'frequency':
        model = FrequencyModel(range_min, range_max, default_draw_count)
        print(f"Loading data for {lottery.name}...")
        df = lottery.preprocess_data()
        print(f"Training {model.name}...")
        model.train(df)
    else:
        print(f"Model {args.model} not supported.")
        sys.exit(1)

    # Calculate Costs
    price_per_bet = lottery.get_price(quantity)
    if price_per_bet == 0.0:
        print(f"Warning: Could not find price for {quantity} numbers in {args.game}. Assuming 0.00.")
    
    total_cost = price_per_bet * args.count
    cost_per_person = total_cost / args.split

    print(f"\n--- Cost Analysis ---")
    print(f"Game: {lottery.name}")
    print(f"Numbers per bet: {quantity}")
    print(f"Price per bet: R$ {price_per_bet:.2f}")
    print(f"Total Cost ({args.count} bets): R$ {total_cost:.2f}")
    if args.split > 1:
        print(f"Split among {args.split} people: R$ {cost_per_person:.2f} per person")
    print(f"---------------------\n")

    # Generate Predictions
    predictions = []
    print(f"Generating {args.count} predictions using {model.name} for {lottery.name}...")
    
    ledger = Ledger() if args.save else None
    
    if args.save and not args.contest:
        print("Error: --contest is required when saving to Ledger.")
        sys.exit(1)

    for i in range(args.count):
        # Pass quantity to predict method
        prediction = model.predict(count=quantity)
        predictions.append({
            "game": args.game,
            "model": args.model,
            "prediction_id": i + 1,
            "numbers": prediction,
            "cost": price_per_bet
        })
        print(f"Prediction {i+1}: {prediction}")
        
        if ledger:
            ledger.add_bet(args.game, args.model, prediction, args.contest, price_per_bet)

    # Export
    if args.output:
        if args.output.endswith('.json'):
            export_to_json(predictions, args.output)
        elif args.output.endswith('.csv'):
            # Convert list of numbers to string for CSV
            csv_predictions = []
            for p in predictions:
                p_copy = p.copy()
                p_copy['numbers'] = " ".join(map(str, p['numbers']))
                csv_predictions.append(p_copy)
            export_to_csv(csv_predictions, args.output)
        else:
            print("Unsupported output format. Please use .json or .csv")

def run_check(args):
    checker = Checker()
    checker.check_bets()

if __name__ == "__main__":
    main()
