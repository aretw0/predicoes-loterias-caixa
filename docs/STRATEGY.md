# Estratégia de Uso: O Ritual do Tira-Teima

> "Garantias não existem em jogos de azar. O que existe é a eliminação do improvável."

Este guia define o fluxo de trabalho ideal para utilizar as ferramentas do **Preloto v0.4.0** com o objetivo de maximizar suas chances estatísticas.

## 1. O Diagnóstico (Visibilidade)

Antes de jogar, entenda o comportamento atual do jogo.

```bash
preloto megasena --analyze --draws 20
```

**O que buscar:**
*   **Distribuição Ímpar/Par**: Se nos últimos 5 jogos saíram muitos Pares, a estatística tende a "corrigir" para Ímpares ou equilibrar.
*   **Soma**: A média é ~180. Se os últimos jogos tiveram soma 250 (muito alta), espere um jogo de soma baixa.
*   **Cold Numbers**: Números que não saem há muito tempo mas têm alta frequência histórica.

## 2. A "Peneira" (Simulação)

Use o Método de Monte Carlo para gerar jogos que respeitam a matemática, eliminando o "lixo aleatório".

```bash
# Gere uma lista de candidatos sólidos
preloto megasena --model mc
```

*   O computador vai simular 10.000 jogos e te dar os 6-10 números que mais apareceram nos jogos "válidos".
*   *Anote esses números.* Eles são sua base estatística segura.

## 3. A Consulta ao Oráculo (Inteligência)

Agora pergunte aos modelos que tentam encontrar padrões sequenciais (o que o Monte Carlo ignora).

```bash
# Pergunte à Rede Neural (foco em sequências recentes)
# Dica: 'epochs' define o tempo de treino. 'units' define a inteligência (padrão 128). 'window_size' o contexto (padrão 10).
preloto megasena --model lstm --epochs 100 --model-args units:256 window_size:20
```

*   **Nota sobre Calibragem LSTM**:
    *   **units**: 128 é bom. 256 é mais "inteligente" mas mais lento.
    *   **window_size**: Quantos jogos passados ele olha? 10 é curto prazo. 20 é médio prazo. Tente variar.

```bash
# Pergunte à Random Forest (foco em contexto e regras de decisão)
# Dica: Use n_estimators mais alto para maior precisão (padrão é 100)
preloto megasena --model rf --model-args n_estimators:1000
```

*   **Nota sobre Calibragem RF**: `n_estimators:100` é rápido para testes. Para o "Tira-Teima" final, prefira **500** ou **1000**. Mais árvores = decisão mais estável (demora uns segundos a mais, mas vale a pena).
*   *Anote esses números.* Eles são suas apostas em "tendências".

## 4. A Convergência (O Tira-Teima)

O seu jogo final deve ser a intersecção desses mundos.

1.  Pegue os números do **Monte Carlo** (Base sólida).
2.  Veja quais deles TAMBÉM apareceram no **LSTM** ou **RF**.
3.  Esses são seus **Números de Ouro**.

### Exemplo Prático

*   **MC diz**: 04, 10, 33, 41, 52, 58
*   **LSTM diz**: 04, 15, 22, 33, 49, 60
*   **RF diz**: 04, 05, 10, 33, 42, 55

**Conclusão**:
*   **04 e 33**: Apareceram em TODOS. São obrigatórios.
*   **10**: Apareceu em MC e RF. Forte candidato.
*   **Restante**: Preencha com sua intuição ou análise do passo 1.

---

## Nota sobre "Garantias"

Se alguém te prometer garantia de vitória na loteria, é mentira. O que o **Preloto** garante é que **você não vai jogar dinheiro fora em apostas estúpidas** (como [1,2,3,4,5,6] ou jogos com Soma 40). Você está jogando no "centro da curva de sino" (Bell Curve), onde a grande maioria dos sorteios acontece.
