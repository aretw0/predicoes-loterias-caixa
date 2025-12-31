import pandas as pd
from loterias.quina import Quina

def analyze_quina():
    print("Inicializando análise da Quina...")
    quina = Quina()
    df_quina = quina.preprocess_data()

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

if __name__ == "__main__":
    analyze_quina()
