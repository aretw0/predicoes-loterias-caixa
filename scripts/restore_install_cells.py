import json
import os

def add_install_cell(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Check if install cell already exists
    has_install = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_str = "".join(cell['source'])
            if "pip install" in source_str:
                has_install = True
                break
    
    if has_install:
        print(f"Install cell already present in {filename}")
        return

    print(f"Adding install cell to {filename}...")
    
    # Define the new cell
    install_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# --- INSTALAÇÃO ---\n",
            "# Descomente a linha abaixo para instalar no Colab/Kaggle\n",
            "# !pip install --force-reinstall git+https://github.com/aretw0/predicoes-loterias-caixa.git\n"
        ]
    }

    # Insert after the first cell (usually title markdown)
    # If the first cell is not markdown, insert at 0
    insert_idx = 1 if nb['cells'] and nb['cells'][0]['cell_type'] == 'markdown' else 0
    nb['cells'].insert(insert_idx, install_cell)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write('\n')
    print(f"Saved {filename}")

files = [
    '/workspaces/predicoes-loterias-caixa/snapshot_factory.ipynb',
    '/workspaces/predicoes-loterias-caixa/model_cultivation.ipynb',
    '/workspaces/predicoes-loterias-caixa/ensemble_dashboard.ipynb'
]

for f in files:
    try:
        add_install_cell(f)
    except Exception as e:
        print(f"Error processing {f}: {e}")
