import json
import os

def clean_notebook(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    changed = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_qs = "".join(cell['source'])
            if "LÓGICA DE IMPORTAÇÃO" in source_qs and "try:" in source_qs:
                print(f"Updating {filename}...")
                new_source = [
                    "# --- LÓGICA DE IMPORTAÇÃO ---\n",
                    "from loterias.megasena import MegaSena\n",
                ]
                # Add specific imports based on filename
                if "snapshot_factory" in filename:
                    new_source.append("from loterias.models import TransformerModel, CatBoostModel, LSTMModel\n")
                elif "model_cultivation" in filename:
                     new_source.append("from loterias.models import TransformerModel, AutoEncoderModel\n")
                elif "ensemble_dashboard" in filename:
                     new_source.append("from loterias.ensemble_backtester import EnsembleBacktester\n")
                
                new_source.append("print(\"✅ Módulos importados com sucesso.\")")
                
                cell['source'] = new_source
                cell['outputs'] = [] # Clear outputs to be safe
                cell['execution_count'] = None
                changed = True
    
    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')
        print(f"Saved {filename}")
    else:
        print(f"No changes needed for {filename}")

files = [
    '/workspaces/predicoes-loterias-caixa/snapshot_factory.ipynb',
    '/workspaces/predicoes-loterias-caixa/model_cultivation.ipynb',
    '/workspaces/predicoes-loterias-caixa/ensemble_dashboard.ipynb'
]

for f in files:
    try:
        clean_notebook(f)
    except Exception as e:
        print(f"Error processing {f}: {e}")
