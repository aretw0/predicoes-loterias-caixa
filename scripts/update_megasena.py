import requests
import pandas as pd

def update_megasena_results():
    """
    Fetches the latest Mega-Sena results and updates the CSV file.
    """
    url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data = response.json()
        file_path = "data/Mega-Sena.csv"
        new_df = pd.DataFrame([data])

        try:
            existing_df = pd.read_csv(file_path)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            updated_df.drop_duplicates(subset=['numero'], keep='last', inplace=True)
            updated_df.to_csv(file_path, index=False)
            print(f"Resultados da Mega-Sena atualizados com sucesso em {file_path}")
        except FileNotFoundError:
            new_df.to_csv(file_path, index=False)
            print(f"Arquivo {file_path} criado com os resultados da Mega-Sena.")
    else:
        print(f"Erro ao buscar os resultados da Mega-Sena. Status code: {response.status_code}")

if __name__ == "__main__":
    update_megasena_results()
