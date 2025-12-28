# Processamento Isolado com Worker Container

Para evitar que tarefas pesadas ("Comando Supremo", Backtests longos) travem seu ambiente de desenvolvimento ou sua IDE, voc\u00ea pode rodar esses processos em um container separado e descart\u00e1vel.

## Como funciona

Usamos o arquivo `docker-compose.worker.yml` para subir um container id\u00eantico ao de desenvolvimento, mas totalmente isolado do seu terminal atual. Ele monta a pasta do projeto, ent\u00e3o qualquer c\u00f3digo que voc\u00ea editar salvar\u00e1 e refletir\u00e1 l\u00e1 imediatamente.

## Comandos

### 1. Rodar um comando avulso (Recomendado)

O comando abaixo sobe o container, roda o script e depois destr\u00f3i o container (`--rm`) para n\u00e3o deixar lixo.

```bash
# Exemplo: Rodando o Backtest Supremo
docker compose -f docker-compose.worker.yml run --rm worker python src/cli.py megasena --ensemble --draws 10 --model-args n_jobs:1
```

### 2. Deixar o worker rodando em background

Se voc\u00ea quiser rodar v\u00e1rios comandos em sequ\u00eancia sem esperar o container ligar a cada vez:

```bash
# 1. Sobe o worker em background
docker compose -f docker-compose.worker.yml up -d

# 2. Executa comandos dentro dele
docker compose -f docker-compose.worker.yml exec worker python src/cli.py megasena --analyze
docker compose -f docker-compose.worker.yml exec worker python src/cli.py lotofacil --prediction

# 3. Desliga quando acabar
docker compose -f docker-compose.worker.yml down
```

## Solu\u00e7\u00e3o de Problemas

* **Erro de GPU**: Se voc\u00ea n\u00e3o tiver NVIDIA/CUDA configurado na m\u00e1quina host (ou WSL2), remova a se\u00e7\u00e3o `deploy` do arquivo `docker-compose.worker.yml`.
* **Permiss\u00f5es de Arquivo**: Como o container roda como root (ou vscode user dependendo da config), arquivos criados por ele podem aparecer bloqueados no seu host Linux. N\u00e3o deve ser um problema no Windows/WSL2.
