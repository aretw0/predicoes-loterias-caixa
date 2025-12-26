import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import argparse

# Add src to path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
src_path = project_root / 'src'
sys.path.append(str(src_path))

from loterias.megasena import MegaSena
from loterias.lotofacil import Lotofacil
from loterias.quina import Quina

GAME_CLASSES = {
    'megasena': MegaSena,
    'lotofacil': Lotofacil,
    'quina': Quina
}

def check_dependencies():
    missing = []
    try:
        import scipy.stats
    except ImportError:
        missing.append("scipy")
    try:
        import tabulate
    except ImportError:
        missing.append("tabulate")
    
    if missing:
        print(f"Missing dependencies for research: {', '.join(missing)}")
        print("Please run: pip install " + " ".join(missing))
        sys.exit(1)

def analyze_frequencies(df, game_name, outfile):
    outfile.write(f"\n## {game_name.upper()} - 1. Frequency Analysis (Uniformity)\n\n")
    
    # Flatten all numbers
    all_numbers = df['dezenas'].explode().astype(int)
    
    # Range detection
    min_val = all_numbers.min()
    max_val = all_numbers.max()
    total_range = max_val - min_val + 1
    
    observed_counts = all_numbers.value_counts().sort_index()
    
    # Fill missing numbers
    full_index = pd.Index(range(min_val, max_val + 1), name='dezenas')
    observed_counts = observed_counts.reindex(full_index, fill_value=0)
    
    outfile.write(f"Range: {min_val} to {max_val}\n")
    outfile.write(f"Total draws: {len(df)}\n")
    outfile.write(f"Total numbers drawn: {len(all_numbers)}\n")
    
    # Expected frequency (Uniform)
    expected_freq = len(all_numbers) / total_range
    outfile.write(f"Expected frequency per number: {expected_freq:.2f}\n")
    
    # Chi-square test
    from scipy.stats import chisquare
    chi2, p_value = chisquare(observed_counts, f_exp=expected_freq)
    
    outfile.write(f"Chi-square statistic: {chi2:.4f}\n")
    outfile.write(f"P-value: {p_value:.4e}\n")
    
    outfile.write("\n### Top 5 Frequent Numbers\n")
    outfile.write(observed_counts.sort_values(ascending=False).head(5).to_markdown() + "\n")
    
    outfile.write("\n### Top 5 Least Frequent Numbers\n")
    outfile.write(observed_counts.sort_values(ascending=True).head(5).to_markdown() + "\n")

def analyze_poisson(df, game_name, outfile):
    outfile.write(f"\n## {game_name.upper()} - 2. Parity Distribution (Even/Odd)\n\n")
    
    df['even_count'] = df['dezenas'].apply(lambda x: sum(1 for n in x if n % 2 == 0))
    
    outfile.write("### Even Numbers per Draw\n")
    even_counts = df['even_count'].value_counts().sort_index()
    outfile.write(even_counts.to_markdown() + "\n")
    
    # Hypergeometric comparison
    # Need total balls and draw size
    # Infer from data
    all_numbers = df['dezenas'].explode().astype(int)
    max_val = all_numbers.max() # Population size (approx)
    draw_size = len(df.iloc[0]['dezenas'])
    
    # Precise population size per game
    pop_map = {'megasena': 60, 'lotofacil': 25, 'quina': 80}
    M = pop_map.get(game_name, max_val)
    
    # Even numbers in population
    n_even = M // 2 
    
    outfile.write(f"\nTheoretical Probabilities (Hypergeometric M={M}, n={n_even}, N={draw_size}):\n")
    
    from scipy.stats import hypergeom
    rv = hypergeom(M=M, n=n_even, N=draw_size)
    x = np.arange(0, draw_size + 1)
    pmf = rv.pmf(x)
    
    comparison = pd.DataFrame({
        'Even Count': x,
        'Observed Freq': even_counts.reindex(x, fill_value=0) / len(df),
        'Theoretical PMF': pmf
    })
    outfile.write(comparison.to_markdown(index=False, floatfmt=".4f") + "\n")

def analyze_gaps(df, game_name, outfile):
    outfile.write(f"\n## {game_name.upper()} - 3. Gap Analysis\n\n")
    
    # Infer range
    all_numbers = df['dezenas'].explode().astype(int)
    min_val = all_numbers.min()
    max_val = all_numbers.max()
    
    all_gaps = []
    last_indices = {}
    
    for n in range(min_val, max_val + 1):
        is_in_draw = df['dezenas'].apply(lambda x: n in x)
        draw_indices = np.where(is_in_draw)[0]
        
        if len(draw_indices) > 0:
            diffs = np.diff(draw_indices) - 1
            all_gaps.extend(diffs)
            current_gap = len(df) - 1 - draw_indices[-1]
            last_indices[n] = current_gap
        else:
            last_indices[n] = len(df)

    gaps_series = pd.Series(all_gaps)
    
    outfile.write(f"Average Gap: {gaps_series.mean():.2f}\n")
    outfile.write(f"Median Gap: {gaps_series.median():.2f}\n")
    outfile.write(f"Max Gap Observed: {gaps_series.max()}\n")
    
    due_df = pd.DataFrame(list(last_indices.items()), columns=['Number', 'Current Gap'])
    outfile.write("\n### Top 10 Most Due Numbers\n")
    outfile.write(due_df.sort_values('Current Gap', ascending=False).head(10).to_markdown(index=False) + "\n")


def main():
    check_dependencies()
    
    parser = argparse.ArgumentParser(description="Run statistical research on lotteries.")
    parser.add_argument('--game', type=str, choices=['all'] + list(GAME_CLASSES.keys()), default='all')
    args = parser.parse_args()
    
    games_to_run = list(GAME_CLASSES.keys()) if args.game == 'all' else [args.game]
    
    output_path = project_root / 'research_results.md'
    
    with open(output_path, 'w') as f:
        f.write("# Lottery Statistical Research Results\n")
        f.write(f"Date: {pd.Timestamp.now()}\n")
        
        for game_name in games_to_run:
            print(f"\nAnalyzing {game_name}...")
            try:
                game_cls = GAME_CLASSES[game_name]
                instance = game_cls()
                print(f"Fetching data from {instance.data_url}...")
                df = instance.load_data()
                df = instance.preprocess_data()
                print(f"Data loaded: {len(df)} draws.")
                
                f.write(f"\n---\n# Analysis: {game_name.title()}\n")
                analyze_frequencies(df, game_name, f)
                analyze_poisson(df, game_name, f)
                analyze_gaps(df, game_name, f)
                
            except Exception as e:
                print(f"Error analyzing {game_name}: {e}")
                f.write(f"\nError analyzing {game_name}: {e}\n")

    print(f"\nAnalysis complete. Results written to {output_path}")

if __name__ == "__main__":
    main()
