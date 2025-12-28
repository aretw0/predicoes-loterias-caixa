# Processamento Isolado com Worker Container

Para evitar que tarefas pesadas ("Comando Supremo", Backtests longos) travem seu ambiente de desenvolvimento ou sua IDE, você pode rodar esses processos em um container separado e descartável.

## Como funciona

Usamos o arquivo `docker-compose.worker.yml` para subir um container idêntico ao de desenvolvimento, mas totalmente isolado do seu terminal atual. Ele monta a pasta do projeto, então qualquer código que você editar salvará e refletirá lá imediatamente.

## Comandos

### 1. Rodar um comando avulso (Recomendado)

O comando abaixo sobe o container, roda o script e depois destrói o container (`--rm`) para não deixar lixo.

```bash
# Exemplo: Rodando o Backtest Supremo
docker compose -f docker-compose.worker.yml run --rm worker python src/cli.py megasena --ensemble --draws 10 --model-args n_jobs:1
```

### 2. Deixar o worker rodando em background

Se você quiser rodar vários comandos em sequência sem esperar o container ligar a cada vez:

```bash
# 1. Sobe o worker em background
docker compose -f docker-compose.worker.yml up -d

# 2. Executa comandos dentro dele
docker compose -f docker-compose.worker.yml exec worker python src/cli.py megasena --analyze
docker compose -f docker-compose.worker.yml exec worker python src/cli.py lotofacil --prediction

# 3. Desliga quando acabar
docker compose -f docker-compose.worker.yml down
```

## Solução de Problemas

* **Erro de GPU**: Se você não tiver NVIDIA/CUDA configurado na máquina host (ou WSL2), remova a seção `deploy` do arquivo `docker-compose.worker.yml`.
* **Permissões de Arquivo**: Como o container roda como root (ou vscode user dependendo da config), arquivos criados por ele podem aparecer bloqueados no seu host Linux. Não deve ser um problema no Windows/WSL2.
