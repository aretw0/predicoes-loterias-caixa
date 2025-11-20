import argparse
import sys
from src.loterias.megasena import MegaSena
from src.loterias.lotofacil import Lotofacil
from src.loterias.quina import Quina
from src.loterias.models import RandomModel, FrequencyModel
from src.loterias.utils import export_to_json, export_to_csv

def main():
    parser = argparse.ArgumentParser(description="Lottery Prediction Engine CLI")
    
    parser.add_argument('--game', type=str, required=True, choices=['megasena', 'lotofacil', 'quina'], help="The lottery game to predict for.")
    parser.add_argument('--model', type=str, required=True, choices=['random', 'frequency'], help="The prediction model to use.")
    parser.add_argument('--count', type=int, default=1, help="Number of predictions to generate.")
    parser.add_argument('--output', type=str, help="Output file for predictions (e.g., predictions.json or predictions.csv).")

    args = parser.parse_args()

    # Initialize Game
    if args.game == 'megasena':
        lottery = MegaSena()
        range_min, range_max, draw_count = 1, 60, 6
    elif args.game == 'lotofacil':
        lottery = Lotofacil()
        range_min, range_max, draw_count = 1, 25, 15
    elif args.game == 'quina':
        lottery = Quina()
        range_min, range_max, draw_count = 1, 80, 5
    else:
        print(f"Game {args.game} not supported.")
        sys.exit(1)

    # Initialize Model
    if args.model == 'random':
        model = RandomModel(range_min, range_max, draw_count)
    elif args.model == 'frequency':
        model = FrequencyModel(range_min, range_max, draw_count)
        print(f"Loading data for {lottery.name}...")
        df = lottery.preprocess_data()
        print(f"Training {model.name}...")
        model.train(df)
    else:
        print(f"Model {args.model} not supported.")
        sys.exit(1)

    # Generate Predictions
    predictions = []
    print(f"Generating {args.count} predictions using {model.name} for {lottery.name}...")
    
    for i in range(args.count):
        prediction = model.predict()
        predictions.append({
            "game": args.game,
            "model": args.model,
            "prediction_id": i + 1,
            "numbers": prediction
        })
        print(f"Prediction {i+1}: {prediction}")

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

if __name__ == "__main__":
    main()
