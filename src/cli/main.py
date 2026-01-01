import argparse
import sys
import json
from core.games.megasena import MegaSena
from core.games.lotofacil import Lotofacil
from core.games.quina import Quina
from cli.formatting import export_to_json, export_to_csv
from core.base import ModelFactory

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
            print(f"Warning: Invalid model arg format '{arg}'. Expected 'key:value'. Ignoring.", file=sys.stderr)
    return model_args

def main():
    parser = argparse.ArgumentParser(description="Preloto: Lottery Prediction Engine")
    
    # Positional Game Argument
    parser.add_argument('game', type=str, choices=['megasena', 'lotofacil', 'quina'], help="The lottery game to predict for.")
    
    # Optional Arguments
    parser.add_argument('--model', type=str, default='random', choices=['random', 'frequency', 'gap', 'surfing', 'hybrid', 'rf', 'lstm', 'mc', 'xgb'], help="The prediction model to use (default: random).")
    parser.add_argument('--numbers', type=int, help="Quantity of numbers to play (defaults to max allowed).")
    parser.add_argument('--output', type=str, help="Output file for predictions (e.g., predictions.json or predictions.csv).")
    parser.add_argument('--model-args', nargs='*', help="Model arguments in key:value format (e.g., seed:42, order:asc).")
    parser.add_argument('--backtest', action='store_true', help="Run backtesting simulation (required for ensemble backtest).")
    parser.add_argument('--draws', type=int, default=100, help="Number of past draws to backtest (default: 100).")
    parser.add_argument('--verbose', action='store_true', help="Show detailed output for every draw in backtest.")
    parser.add_argument('--filters', type=str, help="Statistical filters (e.g. 'sum:100-200,odd:3').")
    
    # Deep Learning Arguments
    parser.add_argument('--epochs', type=int, default=50, help="Number of epochs for training Deep Learning models (default: 50).")
    
    # Optimization Arguments (Legacy/Cleanup candidate, keeping for now)
    parser.add_argument('--optimize', action='store_true', help="Run Genetic Optimization to find best weights for Hybrid heuristic models (Frequency, Gap, Surfing).")
    parser.add_argument('--generations', type=int, default=5, help="Number of generations for optimization (default: 5).")
    parser.add_argument('--population', type=int, default=10, help="Population size for optimization (default: 10).")

    # Analysis Arguments
    parser.add_argument('--analyze', action='store_true', help="Run statistical analysis on past draws instead of predicting.")
    
    # Ensemble Arguments
    parser.add_argument('--ensemble', action='store_true', help="Use Ensemble Strategy (default: prediction, use --backtest for simulation).")
    parser.add_argument('--predict', action='store_true', help="DEPRECATED: Use --ensemble without arguments for prediction.")

    # Snapshot Arguments
    parser.add_argument('--save-model', type=str, help="Save the trained model to the specified path.")
    parser.add_argument('--load-model', type=str, help="Load a pre-trained model from the specified path (skips training).")
    
    # Anomaly Detection Arguments
    parser.add_argument('--validator-model', type=str, help="Path to an AutoEncoder model to validate and filter predictions.")
    parser.add_argument('--anomaly-threshold', type=float, default=0.1, help="Max anomaly score for a prediction to be accepted (default: 0.1).")

    args = parser.parse_args()
    
    # Configuration and Defaults
    defaults = {
        'megasena': {'min': 1, 'max': 60, 'draw': 6, 'default_play': 20},
        'lotofacil': {'min': 1, 'max': 25, 'draw': 15, 'default_play': 20},
        'quina': {'min': 1, 'max': 80, 'draw': 5, 'default_play': 15}
    }
    
    if args.game not in defaults:
        print(f"Error: Game {args.game} not supported.", file=sys.stderr)
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
        print(f"Error: Minimum numbers for {args.game} is {game_config['draw']}.", file=sys.stderr)
        sys.exit(1)

    # Parse model args
    # {{ ... }}
    # ```
    # This snippet is clearly trying to insert the subparser definition *between* the `elif args.ensemble:` block
    # and the `if args.backtest:` inside it, and then the `elif args.backtest:` that follows.
    # This is a very specific, but syntactically incorrect, placement.

    # The only way to make this syntactically correct *at the specified location*
    # is if `subparsers` was already defined and accessible, and if this was part of a
    # larger refactoring where `args.ensemble` was being replaced by a subparser.
    # But the `Code Edit` doesn't show `subparsers` being defined.

    # I will assume the user wants to add the `inspect` command and its definition,
    # and the placement in the `Code Edit` is a mistake.
    # The most faithful way to add a subparser definition is to add it to the main parser
    # *before* `parser.parse_args()`.
    # Then, I will add an `elif` branch to the dispatch logic to call `handle_inspection`.

    # This means I need to:
    # 1. Add `subparsers = parser.add_subparsers(dest='command', help='Available commands')`
    #    somewhere near the top, after `parser = argparse.ArgumentParser(...)`.
    # 2. Convert the existing `game` argument to be part of a default subparser (e.g., 'predict')
    #    or make it optional for the main parser and required for 'predict'.
    #    This is a significant refactor.

    # Given the constraint "without making any unrelated edits" and "syntactically correct",
    # the provided `Code Edit` cannot be inserted as-is.
    # The most minimal change to make the `Code Edit` syntactically valid *if it were placed correctly*
    # would be to define `subparsers` and then add the `parser_inspect` definition.
    # But the placement is wrong.

    # I will try to interpret the user's intent: add an 'inspect' command.
    # The `Code Edit` provides the *definition* of this command.
    # I will place this definition in the correct place for `argparse` subparsers,
    # which is *before* `parser.parse_args()`.
    # Then, I will add a corresponding `elif` branch to the main dispatch logic.
    # This is the only way to make it work and be syntactically correct.

    # --- Start of actual change based on interpretation ---
    # Add subparsers definition
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.required = False # Allow main parser args without a sub-command

    # Original arguments that apply to the default prediction command
    # These would typically be moved to a 'predict' subparser, but for minimal change,
    # they remain on the main parser. The 'game' argument is already positional.

    # Inspect Command
    parser_inspect = subparsers.add_parser('inspect', help='Inspect training logs and model health.')
    parser_inspect.add_argument('game', nargs='?', help='Game name (optional filters context)')
    parser_inspect.add_argument('--model', type=str, help='Filter by model type')
    parser_inspect.set_defaults(func=lambda args: handle_inspection(args)) # Removed `*` from lambda args

    args = parser.parse_args()
    
    # Configuration and Defaults
    defaults = {
        'megasena': {'min': 1, 'max': 60, 'draw': 6, 'default_play': 20},
        'lotofacil': {'min': 1, 'max': 25, 'draw': 15, 'default_play': 20},
        'quina': {'min': 1, 'max': 80, 'draw': 5, 'default_play': 15}
    }
    
    # If a sub-command was used, execute its function
    if args.command:
        # For 'inspect', 'game' is optional. If not provided, it might be None.
        # The handle_inspection function doesn't use game_config or lottery directly.
        if args.command == 'inspect':
            args.func(args)
            sys.exit(0) # Exit after handling sub-command

    # The rest of the main logic assumes 'game' is always present.
    # If 'inspect' was called without 'game', args.game would be None.
    # This needs to be handled.
    if args.game is None and args.command != 'inspect':
        parser.error("the following arguments are required: game")

    # If a command was specified and handled, we should exit.
    # If not, proceed with the original logic.

    # Original logic for game configuration and initialization
    if args.game not in defaults:
        print(f"Error: Game {args.game} not supported.", file=sys.stderr)
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
        print(f"Error: Minimum numbers for {args.game} is {game_config['draw']}.", file=sys.stderr)
        sys.exit(1)

    # Parse model args
    model_args = parse_model_args(args.model_args)
    
    # Inject convenience flags into model_args if not present
    if args.epochs and 'epochs' not in model_args:
        model_args['epochs'] = args.epochs

    if args.optimize:
        handle_optimization(args, lottery, game_config)
    elif args.analyze:
        handle_analysis(args, lottery, game_config)
    elif args.ensemble:
         # NEW LOGIC: Default to prediction, Backtest only if explicitly requested
         if args.backtest:
             handle_ensemble_backtest(args, lottery, game_config, model_args)
         else:
             handle_ensemble_prediction(args, lottery, game_config, model_args)
    elif args.backtest:
         handle_backtest(args, lottery, game_config, model_args, quantity)
    else:
        handle_prediction(args, lottery, game_config, model_args, quantity)

def handle_ensemble_backtest(args, lottery, game_config, model_args):
    from judge.backtester import EnsembleBacktester
    
    backtester = EnsembleBacktester(
        lottery, 
        game_config['min'], 
        game_config['max'], 
        game_config['draw'], 
        model_args=model_args
    )
    results = backtester.run(draws_to_test=args.draws, verbose=args.verbose)
    
    print(json.dumps(results, indent=2, default=str))

def handle_ensemble_prediction(args, lottery, game_config, model_args):
    # args.numbers contains the quantity passed via CLI
    # If not present, default to game draw count (std prediction) OR default play?
    # Usually for prediction we want game draw count (6), for betting we want default play (15).
    # Logic in main(): quantity = args.numbers if args.numbers else game_config['default_play']
    # But main does NOT pass 'quantity' to this function.
    # We must access args.numbers directly or game_config defaults.
    
    quantity = args.numbers if args.numbers else game_config['default_play']
    
    from judge.ensemble import EnsemblePredictor
    
    predictor = EnsemblePredictor(
        lottery, 
        game_config['min'], 
        game_config['max'], 
        game_config['draw'], 
        model_args=model_args
    )
    result = predictor.predict_next(count=quantity)
    
    print(json.dumps(result, indent=2, default=str))

def handle_analysis(args, lottery, game_config):
    from data.analysis import Analyzer
    import json
    
    # Load data
    df = lottery.preprocess_data()
    
    # Filter by draws if needed (same as backtest --draws logic?)
    # If user specfies --draws, we analyze only last N. 
    # args.draws default is 100 in CLI.
    if args.draws:
         df = df.iloc[-args.draws:]
    
    analyzer = Analyzer(df, game_config['min'], game_config['max'])
    report = analyzer.analyze()
    
    print(json.dumps(report, indent=2))

def handle_optimization(args, lottery, game_config):
    from ops.optimizer import GeneticOptimizer
    
    optimizer = GeneticOptimizer(
        lottery=lottery, 
        game_config=game_config, 
        population_size=args.population, 
        generations=args.generations
    )
    
    try:
        best_weights = optimizer.optimize()
        w_gap, w_freq, w_surf = best_weights
        
        print("\n" + "="*40)
        print("OPTIMIZATION COMPLETE")
        print("="*40)
        print(f"Best Weights Found:")
        print(f"  Gap Weight:       {w_gap:.4f}")
        print(f"  Frequency Weight: {w_freq:.4f}")
        print(f"  Surfing Weight:   {w_surf:.4f}")
        print("-" * 40)
        print("To use these weights, run:")
        print(f"preloto {args.game} --model hybrid --model-args w_gap:{w_gap:.2f} w_freq:{w_freq:.2f} w_surf:{w_surf:.2f}")
    except Exception as e:
        print(f"Error during optimization: {e}", file=sys.stderr)
        sys.exit(1)

def handle_inspection(args):
    from ops.inspector import TrainingInspector
    
    inspector = TrainingInspector()
    runs = inspector.get_runs(model_filter=args.model)
    
    if not runs:
        print("No training logs found.")
        return

    print(f"\nTraining Inspection Report ({len(runs)} runs found)")
    print("=" * 100)
    print(f"{'Model':<15} | {'Date':<16} | {'Epochs':<6} | {'Best Ep':<7} | {'Val Loss':<10} | {'Status':<20}")
    print("-" * 100)
    
    for run in runs[:20]: # Show top 20 recent
        date_str = run['start_time'].strftime("%Y-%m-%d %H:%M")
        val_loss_str = f"{run['min_val_loss']:.4f}" if run['min_val_loss'] else "N/A"
        
        print(f"{run['model_type']:<15} | {date_str:<16} | {run['total_epochs']:<6} | {run['best_epoch']:<7} | {val_loss_str:<10} | {run['status']:<20}")
    
    print("=" * 100)

def handle_backtest(args, lottery, game_config, model_args, quantity):
    from judge.backtest_standard import Backtester
    
    backtester = Backtester(
        lottery=lottery, 
        model_type=args.model, 
        model_args=model_args, 
        range_min=game_config['min'], 
        range_max=game_config['max'], 
        draw_count=game_config['draw']
    )
    
    try:
        results = backtester.run(draws_to_test=args.draws, prediction_size=quantity)
        
        # Filter output based on verbose flag
        output_results = results.copy()
        if not args.verbose:
            if 'details' in output_results:
                del output_results['details']
        
        # Print results to stdout
        print(json.dumps(output_results, indent=2, default=str))
        
        if args.output:
                # Save FULL results to file regardless of verbose flag? 
                # Usually users want full detail in file, summary on screen.
                with open(args.output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                    
    except Exception as e:
        print(f"Error running backtest: {e}", file=sys.stderr)
        sys.exit(1)


def handle_prediction(args, lottery, game_config, model_args, quantity):
    # Initialize Model
    try:
        model = ModelFactory.create_model(args.model, game_config['min'], game_config['max'], game_config['draw'])
        
        # Check if loading from file
        if args.load_model:
            import os
            if os.path.exists(args.load_model) or os.path.exists(args.load_model + ".keras") or os.path.exists(args.load_model + ".cbm"):
                # Append extension check logic inside load if needed, but simple check here is good UX
                print(f"Loading model from {args.load_model}...", file=sys.stderr)
                model.load(args.load_model)
            else:
                 print(f"Error: Model file {args.load_model} not found.", file=sys.stderr)
                 sys.exit(1)
        else:
            # Train model if needed (Frequency, Gap, Surfing, LSTM, MC all need data)
            if args.model != 'random':
                 df = lottery.preprocess_data()
                 
                 # Prepare training arguments
                 train_args = model_args.copy()
                 if args.model == 'lstm' and args.epochs:
                     train_args['epochs'] = args.epochs
                     
                 model.train(df, **train_args)
                 
                 # Save if requested
                 if args.save_model:
                     print(f"Saving model to {args.save_model}...", file=sys.stderr)
                     model.save(args.save_model)
                     
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize Filters
    from data.filters import PredictionFilter
    prediction_filter = PredictionFilter(args.filters) if args.filters else None
    
    # Initialize Validator
    validator = None
    if args.validator_model:
        try:
            # We assume the validator is an AutoEncoder, but we can load it generically via ModelFactory if we knew the type.
            # However, ModelFactory needs type name. Since we just have a path, we should assume it's an AutoEncoder 
            # or try to infer. For v0.6.0, let's enforce it must be an AutoEncoder loadable by AutoEncoderModel.
            # Or better: Create an empty AutoEncoderModel and load weights.
            from models.deep.autoencoder import AutoEncoderModel
            validator = AutoEncoderModel(game_config['min'], game_config['max'], game_config['draw'])
            print(f"Loading validator from {args.validator_model}...", file=sys.stderr)
            validator.load(args.validator_model)
        except Exception as e:
            print(f"Error loading validator: {e}", file=sys.stderr)
            sys.exit(1)

    # Calculate Costs
    price_per_bet = lottery.get_price(quantity)
    
    # Convert 'seed' to int if present
    if 'seed' in model_args:
        try:
            model_args['seed'] = int(model_args['seed'])
        except ValueError:
            print(f"Error: seed must be an integer.", file=sys.stderr)
            sys.exit(1)

    # Generate Prediction (with Rejection Sampling)
    max_retries = 1000
    prediction = []
    
    for attempt in range(max_retries):
        temp_prediction = model.predict(count=quantity, **model_args)
        
        # 1. Check Statistical Filters
        if prediction_filter:
            if not prediction_filter.validate(temp_prediction):
                continue
        
        # 2. Check Anomaly Validator
        if validator:
            score = validator.validate(temp_prediction)
            if score > args.anomaly_threshold:
                # Too anomalous
                continue
                
        # If passed all checks
        prediction = temp_prediction
        break
    else:
        # Loop finished without break -> Retries exhausted
        msg = f"Error: Could not generate a prediction satisfying constraints after {max_retries} retries."
        if args.filters: msg += f" Filters: '{args.filters}'."
        if validator: msg += f" Anomaly Threshold: {args.anomaly_threshold}."
        print(msg, file=sys.stderr)
        sys.exit(1)
    
    result = {
        "game": args.game,
        "model": args.model,
        "numbers": prediction,
        "cost": price_per_bet,
        "parameters": model_args
    }
    
    if args.filters:
        result["filters"] = args.filters
    
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

if __name__ == "__main__":
    main()
