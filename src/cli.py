import argparse
import sys
import json
from src.loterias.megasena import MegaSena
from src.loterias.lotofacil import Lotofacil
from src.loterias.quina import Quina
from src.loterias.models import RandomModel, FrequencyModel
from src.loterias.utils import export_to_json, export_to_csv
from src.loterias.ledger import Ledger
from src.loterias.checker import Checker

def parse_model_args(args_list):
    """Parses a list of strings in 'key:value' format into a dictionary."""
    if not args_list:
        return {}
    model_args = {}
    for arg in args_list:
        if ':' in arg:
            key, value = arg.split(':', 1)
            model_args[key] = value
        else:
            print(f"Warning: Invalid model arg format '{arg}'. Expected 'key:value'. Ignoring.")
    return model_args

def main():
    parser = argparse.ArgumentParser(description="Lottery Prediction Engine CLI")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Predict Command
    predict_parser = subparsers.add_parser('predict', help='Generate predictions')
    predict_parser.add_argument('--game', type=str, required=True, choices=['megasena', 'lotofacil', 'quina'], help="The lottery game to predict for.")
    predict_parser.add_argument('--model', type=str, required=True, choices=['random', 'frequency'], help="The prediction model to use.")
    predict_parser.add_argument('--numbers', type=int, help="Quantity of numbers to play (e.g., 6, 7, 15). Defaults to minimum for the game.")
    predict_parser.add_argument('--output', type=str, help="Output file for predictions (e.g., predictions.json or predictions.csv).")
    predict_parser.add_argument('--save', action='store_true', help="Save predictions to the Ledger.")
    predict_parser.add_argument('--contest', type=int, help="Target contest number (required if saving).")
    predict_parser.add_argument('--model-args', nargs='*', help="Model arguments in key:value format (e.g., order:asc).")

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
    # Defaults (Max numbers as requested)
    defaults = {
        'megasena': {'min': 1, 'max': 60, 'draw': 6, 'default_play': 20},
        'lotofacil': {'min': 1, 'max': 25, 'draw': 15, 'default_play': 20},
        'quina': {'min': 1, 'max': 80, 'draw': 5, 'default_play': 15}
    }

    if args.game not in defaults:
        print(f"Error: Game {args.game} not supported.")
        sys.exit(1)

    game_config = defaults[args.game]
    
    # Initialize Game
    if args.game == 'megasena':
        lottery = MegaSena()
    elif args.game == 'lotofacil':
        lottery = Lotofacil()
    elif args.game == 'quina':
        lottery = Quina()

    # Determine quantity of numbers
    quantity = args.numbers if args.numbers else game_config['default_play']
    
    # Validate quantity
    if quantity < game_config['draw']:
        print(f"Error: Minimum numbers for {args.game} is {game_config['draw']}.")
        sys.exit(1)

    # Parse model args
    model_args = parse_model_args(args.model_args)

    # Initialize Model
    if args.model == 'random':
        model = RandomModel(game_config['min'], game_config['max'], game_config['draw'])
    elif args.model == 'frequency':
        model = FrequencyModel(game_config['min'], game_config['max'], game_config['draw'])
        # Train model (suppress output or log to stderr if needed)
        # print(f"Loading data for {lottery.name}...", file=sys.stderr)
        df = lottery.preprocess_data()
        model.train(df)
    else:
        print(f"Error: Model {args.model} not supported.")
        sys.exit(1)

    # Calculate Costs
    price_per_bet = lottery.get_price(quantity)
    
    # Generate Prediction
    # Pass quantity and model_args to predict method
    # Convert 'seed' to int if present in model_args
    if 'seed' in model_args:
        try:
            model_args['seed'] = int(model_args['seed'])
        except ValueError:
            print(f"Error: seed must be an integer.", file=sys.stderr)
            sys.exit(1)

    prediction = model.predict(count=quantity, **model_args)
    
    result = {
        "game": args.game,
        "model": args.model,
        "numbers": prediction,
        "cost": price_per_bet,
        "parameters": model_args
    }
    
    # Main Output (JSON to stdout for easy parsing, or formatted text?)
    # User requested proper CLI tool. Defaults: human readable to stdout.
    # If --output is json, write to file.
    
    if args.save:
        if not args.contest:
             print("Error: --contest is required when saving to Ledger.", file=sys.stderr)
             sys.exit(1)
        ledger = Ledger()
        ledger.add_bet(args.game, args.model, prediction, args.contest, price_per_bet, parameters=model_args)

    # Export/Output
    if args.output:
        if args.output.endswith('.json'):
            export_to_json([result], args.output)
        elif args.output.endswith('.csv'):
             result_copy = result.copy()
             result_copy['numbers'] = " ".join(map(str, result['numbers']))
             export_to_csv([result_copy], args.output)
        else:
             print("Error: Unsupported output format. Use .json or .csv", file=sys.stderr)
    
    # Human readable output to stdout
    print(json.dumps(result, indent=2))

def run_check(args):
    checker = Checker()
    # Assuming checker prints to stdout
    checker.check_bets()

if __name__ == "__main__":
    main()
