import pandas as pd
from src.loterias.lotofacil import Lotofacil

def analyze_lotofacil():
    print("Inicializando análise da Lotofácil...")
    lotofacil = Lotofacil()
    df_lotofacil = lotofacil.preprocess_data()

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

if __name__ == "__main__":
    analyze_lotofacil()