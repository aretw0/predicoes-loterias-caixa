
import pandas as pd
import json

# Load the Mais Milionária data from the JSON file
with open("maismilionaria_all.json", "r") as f:
    maismilionaria_data = json.load(f)

# Convert the list of dictionaries to a pandas DataFrame
df_maismilionaria = pd.DataFrame(maismilionaria_data)

# Convert 'data' column to datetime objects
df_maismilionaria["data"] = pd.to_datetime(df_maismilionaria["data"], format="%d/%m/%Y")

# Extract the numbers and convert them to integers
df_maismilionaria["dezenas"] = df_maismilionaria["dezenas"].apply(lambda x: [int(n) for n in x])
df_maismilionaria["trevos"] = df_maismilionaria["trevos"].apply(lambda x: [int(n) for n in x])

# Explode the 'dezenas' column to have one number per row for frequency analysis
all_dezenas = df_maismilionaria["dezenas"].explode()
all_trevos = df_maismilionaria["trevos"].explode()

# Calculate the frequency of each dezena
dezena_frequency = all_dezenas.value_counts().sort_index()

print("\nFrequência de cada dezena na Mais Milionária (todos os sorteios):\n")
print(dezena_frequency)

# Calculate the frequency of each trevo
trevo_frequency = all_trevos.value_counts().sort_index()

print("\nFrequência de cada trevo na Mais Milionária (todos os sorteios):\n")
print(trevo_frequency)

# Calculate the sum of the dezenas for each draw
df_maismilionaria["sum_dezenas"] = df_maismilionaria["dezenas"].apply(sum)

print("\nEstatísticas da soma das dezenas na Mais Milionária:\n")
print(df_maismilionaria["sum_dezenas"].describe())

# Calculate the sum of the trevos for each draw
df_maismilionaria["sum_trevos"] = df_maismilionaria["trevos"].apply(sum)

print("\nEstatísticas da soma dos trevos na Mais Milionária:\n")
print(df_maismilionaria["sum_trevos"].describe())

# Analyze the frequency of odd and even dezenas
def count_odd_even(numbers):
    odd_count = sum(1 for n in numbers if n % 2 != 0)
    even_count = sum(1 for n in numbers if n % 2 == 0)
    return odd_count, even_count

df_maismilionaria[["odd_dezena_count", "even_dezena_count"]] = df_maismilionaria["dezenas"].apply(count_odd_even).apply(pd.Series)

print("\nFrequência de dezenas pares e ímpares na Mais Milionária:\n")
print(df_maismilionaria[["odd_dezena_count", "even_dezena_count"]].mean())

# Save basic statistics to a file
with open("maismilionaria_statistics.txt", "w") as f:
    f.write("Frequência de cada dezena na Mais Milionária (todos os sorteios):\n")
    f.write(dezena_frequency.to_string())
    f.write("\n\nFrequência de cada trevo na Mais Milionária (todos os sorteios):\n")
    f.write(trevo_frequency.to_string())
    f.write("\n\nEstatísticas da soma das dezenas na Mais Milionária:\n")
    f.write(df_maismilionaria["sum_dezenas"].describe().to_string())
    f.write("\n\nEstatísticas da soma dos trevos na Mais Milionária:\n")
    f.write(df_maismilionaria["sum_trevos"].describe().to_string())
    f.write("\n\nFrequência de dezenas pares e ímpares na Mais Milionária:\n")
    f.write(df_maismilionaria[["odd_dezena_count", "even_dezena_count"]].mean().to_string())

print("Análise estatística da Mais Milionária salva em \'maismilionaria_statistics.txt\'")


