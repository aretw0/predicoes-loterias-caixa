import pandas as pd

# URL for the Lotofácil data
LOTOFACIL_CSV_URL = "https://raw.githubusercontent.com/aretw0/loterias-caixa-db/refs/heads/main/data/lotofacil.csv"

# Load the Lotofácil data from the CSV file
try:
    df_lotofacil = pd.read_csv(LOTOFACIL_CSV_URL)
except Exception as e:
    print(f"Error loading Lotofácil data from URL: {e}")
    exit()

# Rename columns for consistency
column_mapping = {
    'Data Sorteio': 'data',
}
df_lotofacil = df_lotofacil.rename(columns=column_mapping)

# Convert 'data' column to datetime objects
df_lotofacil['data'] = pd.to_datetime(df_lotofacil['data'], format='%d/%m/%Y')

# Combine the 'Bola' columns into a list of integers
bola_cols = [f'Bola{i}' for i in range(1, 16)]
df_lotofacil['dezenas'] = df_lotofacil[bola_cols].values.tolist()

# Explode the 'dezenas' column for frequency analysis
all_numbers = df_lotofacil['dezenas'].explode()

# Calculate the frequency of each number
number_frequency = all_numbers.value_counts().sort_index()

print("\nFrequência de cada número na Lotofácil (todos os sorteios):\n")
print(number_frequency)

# Calculate the sum of the numbers for each draw
df_lotofacil['sum_dezenas'] = df_lotofacil['dezenas'].apply(sum)

print("\nEstatísticas da soma das dezenas na Lotofácil:\n")
print(df_lotofacil['sum_dezenas'].describe())

# Analyze the frequency of odd and even numbers
def count_odd_even(numbers):
    odd_count = sum(1 for n in numbers if n % 2 != 0)
    even_count = sum(1 for n in numbers if n % 2 == 0)
    return odd_count, even_count

df_lotofacil[['odd_count', 'even_count']] = df_lotofacil['dezenas'].apply(count_odd_even).apply(pd.Series)

print("\nFrequência de números pares e ímpares na Lotofácil:\n")
print(df_lotofacil[['odd_count', 'even_count']].mean())

# Save basic statistics to a file
with open('lotofacil_statistics.txt', 'w') as f:
    f.write("Frequência de cada número na Lotofácil (todos os sorteios):\n")
    f.write(number_frequency.to_string())
    f.write("\n\nEstatísticas da soma das dezenas na Lotofácil:\n")
    f.write(df_lotofacil['sum_dezenas'].describe().to_string())
    f.write("\n\nFrequência de números pares e ímpares na Lotofácil:\n")
    f.write(df_lotofacil[['odd_count', 'even_count']].mean().to_string())

print("Análise estatística da Lotofácil salva em 'lotofacil_statistics.txt'")