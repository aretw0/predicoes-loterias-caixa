
import pandas as pd
import json

# URL for the Quina data
QUINA_CSV_URL = "https://raw.githubusercontent.com/aretw0/loterias-caixa-db/refs/heads/main/data/quina.csv"

# Load the Quina data from the CSV file
try:
    df_quina = pd.read_csv(QUINA_CSV_URL)
except Exception as e:
    print(f"Error loading Quina data from URL: {e}")
    exit()

# Assuming the CSV has columns like 'Data', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5'
# We need to adjust column names to match the original script's expectations or adapt the script.

# Rename columns for consistency with the original script's logic
# This is an assumption based on typical lottery data CSVs.
# If the actual column names are different, this part will need adjustment.
column_mapping = {
    'Data Sorteio': 'data',
    'Bola1': 'dezena1',
    'Bola2': 'dezena2',
    'Bola3': 'dezena3',
    'Bola4': 'dezena4',
    'Bola5': 'dezena5',
    # Add other mappings if necessary, e.g., 'Concurso', 'Ganhadores_5_Numeros', etc.
}
df_quina = df_quina.rename(columns=column_mapping)

# Convert 'data' column to datetime objects
df_quina['data'] = pd.to_datetime(df_quina['data'], format='%d/%m/%Y')

# Combine the 'dezena' columns into a list of integers
df_quina['dezenas'] = df_quina.apply(
    lambda row: [int(row[f'dezena{i}']) for i in range(1, 6)], axis=1
)

# Explode the 'dezenas' column to have one number per row for frequency analysis
all_numbers = df_quina['dezenas'].explode()

# Calculate the frequency of each number
number_frequency = all_numbers.value_counts().sort_index()

print("\nFrequência de cada número na Quina (todos os sorteios):\n")
print(number_frequency)

# Calculate the sum of the numbers for each draw
df_quina['sum_dezenas'] = df_quina['dezenas'].apply(sum)

print("\nEstatísticas da soma das dezenas na Quina:\n")
print(df_quina['sum_dezenas'].describe())

# Analyze the frequency of odd and even numbers
def count_odd_even(numbers):
    odd_count = sum(1 for n in numbers if n % 2 != 0)
    even_count = sum(1 for n in numbers if n % 2 == 0)
    return odd_count, even_count

df_quina[['odd_count', 'even_count']] = df_quina['dezenas'].apply(count_odd_even).apply(pd.Series)

print("\nFrequência de números pares e ímpares na Quina:\n")
print(df_quina[['odd_count', 'even_count']].mean())

# Save basic statistics to a file
with open('quina_statistics.txt', 'w') as f:
    f.write("Frequência de cada número na Quina (todos os sorteios):\n")
    f.write(number_frequency.to_string())
    f.write("\n\nEstatísticas da soma das dezenas na Quina:\n")
    f.write(df_quina['sum_dezenas'].describe().to_string())
    f.write("\n\nFrequência de números pares e ímpares na Quina:\n")
    f.write(df_quina[['odd_count', 'even_count']].mean().to_string())

print("Análise estatística da Quina salva em 'quina_statistics.txt'")
