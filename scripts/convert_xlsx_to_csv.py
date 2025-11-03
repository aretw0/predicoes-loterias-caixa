import pandas as pd
import sys

def convert_xlsx_to_csv(xlsx_path, csv_path):
    """Converte um arquivo XLSX para CSV."""
    try:
        df = pd.read_excel(xlsx_path)
        df.to_csv(csv_path, index=False)
        print(f"Arquivo {xlsx_path} convertido com sucesso para {csv_path}")
    except FileNotFoundError:
        print(f"Erro: O arquivo {xlsx_path} não foi encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python convert_xlsx_to_csv.py <caminho_do_xlsx> <caminho_do_csv>")
        sys.exit(1)
    
    xlsx_file = sys.argv[1]
    csv_file = sys.argv[2]
    
    convert_xlsx_to_csv(xlsx_file, csv_file)
