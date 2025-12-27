import argparse
import sys
import json
from src.loterias.megasena import MegaSena
from src.loterias.lotofacil import Lotofacil
from src.loterias.quina import Quina
from src.loterias.utils import export_to_json, export_to_csv
from src.loterias.base import ModelFactory

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
    parser.add_argument('--model', type=str, default='random', choices=['random', 'frequency', 'gap', 'surfing', 'hybrid', 'rf', 'lstm', 'mc'], help="The prediction model to use (default: random).")
    parser.add_argument('--numbers', type=int, help="Quantity of numbers to play (defaults to max allowed).")
    parser.add_argument('--output', type=str, help="Output file for predictions (e.g., predictions.json or predictions.csv).")
    parser.add_argument('--model-args', nargs='*', help="Model arguments in key:value format (e.g., seed:42, order:asc).")
    parser.add_argument('--backtest', action='store_true', help="Run backtesting simulation.")
    parser.add_argument('--draws', type=int, default=100, help="Number of past draws to backtest (default: 100).")
    parser.add_argument('--verbose', action='store_true', help="Show detailed output for every draw in backtest.")
    parser.add_argument('--filters', type=str, help="Statistical filters (e.g. 'sum:100-200,odd:3').")
    
    # Deep Learning Arguments
    parser.add_argument('--epochs', type=int, default=50, help="Number of epochs for training Deep Learning models (default: 50).")
    
    # Optimization Arguments
    parser.add_argument('--optimize', action='store_true', help="Run Genetic Optimization to find best model weights.")
    parser.add_argument('--generations', type=int, default=5, help="Number of generations for optimization (default: 5).")
    parser.add_argument('--population', type=int, default=10, help="Population size for optimization (default: 10).")

    # Analysis Arguments
    parser.add_argument('--analyze', action='store_true', help="Run statistical analysis on past draws instead of predicting.")

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
    model_args = parse_model_args(args.model_args)

    if args.optimize:
        handle_optimization(args, lottery, game_config)
    elif args.analyze:
        handle_analysis(args, lottery, game_config)
    elif args.backtest:
        handle_backtest(args, lottery, game_config, model_args, quantity)
    else:
        handle_prediction(args, lottery, game_config, model_args, quantity)

def handle_analysis(args, lottery, game_config):
    from src.loterias.analysis import Analyzer
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
    from src.loterias.optimizer import GeneticOptimizer
    
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

def handle_backtest(args, lottery, game_config, model_args, quantity):
    from src.loterias.backtester import Backtester
    
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
        
        # Train model if needed (Frequency, Gap, Surfing all need data)
        # Train model if needed (Frequency, Gap, Surfing, LSTM, MC all need data)
        if args.model != 'random':
             df = lottery.preprocess_data()
             
             # Prepare training arguments
             train_args = model_args.copy()
             if args.model == 'lstm' and args.epochs:
                 train_args['epochs'] = args.epochs
                 
             model.train(df, **train_args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize Filters
    from src.loterias.filters import PredictionFilter
    prediction_filter = PredictionFilter(args.filters) if args.filters else None

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
    
    for _ in range(max_retries):
        temp_prediction = model.predict(count=quantity, **model_args)
        
        if prediction_filter:
            if prediction_filter.validate(temp_prediction):
                prediction = temp_prediction
                break
            # If not valid, loop continues (reject)
        else:
            prediction = temp_prediction
            break
    else:
        # Loop finished without break -> Retries exhausted
        print(f"Error: Could not generate a prediction satisfying filters '{args.filters}' after {max_retries} retries.", file=sys.stderr)
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
