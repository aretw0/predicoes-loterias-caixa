import requests
import pandas as pd

# URL da API da Caixa para a Mega-Sena
url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena"

# Faz a requisição para a API
response = requests.get(url, verify=False)

if response.status_code == 200:
    # Carrega o JSON da resposta
    data = response.json()

    # Cria um DataFrame com os dados
    df = pd.DataFrame([data])

    # Salva o DataFrame em um arquivo Excel
    df.to_excel("data/Mega-Sena.xlsx", index=False)

    print("Resultados da Mega-Sena salvos com sucesso em data/Mega-Sena.xlsx")
else:
    print(f"Erro ao buscar os resultados da Mega-Sena. Status code: {response.status_code}")
