import pandas as pd

# URL for the Mega Sena data
MEGASENA_CSV_URL = "https://raw.githubusercontent.com/aretw0/loterias-caixa-db/refs/heads/main/data/megasena.csv"

# Load the Mega Sena data from the CSV file
try:
    df_megasena = pd.read_csv(MEGASENA_CSV_URL)
except Exception as e:
    print(f"Error loading Mega Sena data from URL: {e}")
    exit()

# Rename columns for consistency
column_mapping = {
    'Data do Sorteio': 'data',
}
df_megasena = df_megasena.rename(columns=column_mapping)

# Convert 'data' column to datetime objects
df_megasena['data'] = pd.to_datetime(df_megasena['data'], format='%d/%m/%Y')

# Combine the 'Bola' columns into a list of integers
bola_cols = [f'Bola{i}' for i in range(1, 7)]
df_megasena['dezenas'] = df_megasena[bola_cols].values.tolist()

# Explode the 'dezenas' column for frequency analysis
all_numbers = df_megasena['dezenas'].explode()

# Calculate the frequency of each number
number_frequency = all_numbers.value_counts().sort_index()

print("\nFrequência de cada número na Mega Sena (todos os sorteios):\n")
print(number_frequency)

# Calculate the sum of the numbers for each draw
df_megasena['sum_dezenas'] = df_megasena['dezenas'].apply(sum)

print("\nEstatísticas da soma das dezenas na Mega Sena:\n")
print(df_megasena['sum_dezenas'].describe())

# Analyze the frequency of odd and even numbers
def count_odd_even(numbers):
    odd_count = sum(1 for n in numbers if n % 2 != 0)
    even_count = sum(1 for n in numbers if n % 2 == 0)
    return odd_count, even_count

df_megasena[['odd_count', 'even_count']] = df_megasena['dezenas'].apply(count_odd_even).apply(pd.Series)

print("\nFrequência de números pares e ímpares na Mega Sena:\n")
print(df_megasena[['odd_count', 'even_count']].mean())

# Save basic statistics to a file
with open('megasena_statistics.txt', 'w') as f:
    f.write("Frequência de cada número na Mega Sena (todos os sorteios):\n")
    f.write(number_frequency.to_string())
    f.write("\n\nEstatísticas da soma das dezenas na Mega Sena:\n")
    f.write(df_megasena['sum_dezenas'].describe().to_string())
    f.write("\n\nFrequência de números pares e ímpares na Mega Sena:\n")
    f.write(df_megasena[['odd_count', 'even_count']].mean().to_string())

print("Análise estatística da Mega Sena salva em 'megasena_statistics.txt'")