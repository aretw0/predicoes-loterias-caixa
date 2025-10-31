
import pandas as pd
import json

# Load the Mega Sena data from the JSON file
with open('megasena_all.json', 'r') as f:
    megasena_data = json.load(f)

# Convert the list of dictionaries to a pandas DataFrame
df_megasena = pd.DataFrame(megasena_data)

# Convert 'data' column to datetime objects
df_megasena['data'] = pd.to_datetime(df_megasena['data'], format='%d/%m/%Y')

# Extract the numbers and convert them to integers
df_megasena['dezenas'] = df_megasena['dezenas'].apply(lambda x: [int(n) for n in x])

# Explode the 'dezenas' column to have one number per row for frequency analysis
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

# Analyze the frequency of numbers by position (if dezenasOrdemSorteio is available)
if 'dezenasOrdemSorteio' in df_megasena.columns:
    df_megasena['dezenasOrdemSorteio'] = df_megasena['dezenasOrdemSorteio'].apply(lambda x: [int(n) for n in x])
    
    print("\nFrequência de números por posição de sorteio na Mega Sena:\n")
    for i in range(6):
        position_numbers = df_megasena['dezenasOrdemSorteio'].apply(lambda x: x[i])
        print(f"Posição {i+1}:\n{position_numbers.value_counts().sort_index().head(10)}\n")

# Save basic statistics to a file
with open('megasena_statistics.txt', 'w') as f:
    f.write("Frequência de cada número na Mega Sena (todos os sorteios):\n")
    f.write(number_frequency.to_string())
    f.write("\n\nEstatísticas da soma das dezenas na Mega Sena:\n")
    f.write(df_megasena['sum_dezenas'].describe().to_string())
    f.write("\n\nFrequência de números pares e ímpares na Mega Sena:\n")
    f.write(df_megasena[['odd_count', 'even_count']].mean().to_string())
    if 'dezenasOrdemSorteio' in df_megasena.columns:
        f.write("\n\nFrequência de números por posição de sorteio na Mega Sena:\n")
        for i in range(6):
            position_numbers = df_megasena['dezenasOrdemSorteio'].apply(lambda x: x[i])
            f.write(f"Posição {i+1}:\n{position_numbers.value_counts().sort_index().head(10).to_string()}\n\n")

print("Análise estatística da Mega Sena salva em 'megasena_statistics.txt'")


