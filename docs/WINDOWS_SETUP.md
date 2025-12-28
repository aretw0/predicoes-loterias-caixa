# Rodando Preloto no Windows (PowerShell)

Se você preferir rodar o projeto nativamente no Windows sem usar o Dev Container, é perfeitamente possível, mas você perderá a aceleração de GPU para o TensorFlow/Keras, a menos que configure o WSL2.

## Pré-requisitos

1. **Python 3.11+**: Baixe e instale do [site oficial](https://www.python.org/downloads/windows/).
    * **Importante**: Marque a opção "Add Python to PATH" durante a instalação.
2. **Git**: Para clonar o repositório (se já não tiver).

## Instalação

Abra o seu PowerShell e navegue até a pasta do projeto:

```powershell
# Crie um ambiente virtual (recomendado)
python -m venv .venv

# Ative o ambiente
.\.venv\Scripts\Activate.ps1

# Instale as depend\u00eancias
pip install -r requirements.txt
```

## Rodando os Comandos

A sintaxe é idêntica, você só precisa chamar o script Python diretamente se o alias `preloto` não estiver configurado.

```powershell
# Diagnóstico
python src/cli.py megasena --analyze --draws 20

# Ensemble Backtest (O Comando que estava travando)
python src/cli.py megasena --backtest --ensemble --draws 10
```

## Sobre GPU e Desempenho (CUDA)

O TensorFlow **removeu o suporte nativo a GPU no Windows** a partir da versão 2.10. Isso significa que, rodando no PowerShell nativo, seus modelos TensorFlow (LSTM) rodarão **apenas na CPU**.

### Alternativas para GPU no Windows

1. **WSL2 (Recomendado)**: É basicamente o que o Dev Container faz. Você instala o "Subsistema Windows para Linux", instala os drivers da NVIDIA no Windows, e o Linux dentro do WSL2 enxerga a placa de vídeo.
2. **DirectML**: Existe um fork chamado `tensorflow-directml` que roda em qualquer placa (AMD/Intel/NVIDIA) no Windows nativo, mas ele é instável e geralmente desatualizado. Não recomendamos para este projeto.

## Solução de Travamentos (Importante)

Se você estiver rodando nativamente ou no container, o "High Compute" pode travar sua máquina se usar todos os núcleos da CPU.

Já atualizamos o código para usar `n_jobs=1` (um núcleo por modelo) por padrão. Isso evita que o computador congele.
