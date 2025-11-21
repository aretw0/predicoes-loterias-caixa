# Documentação Técnica das Modalidades de Loteria da Caixa

Este documento detalha as características técnicas das principais modalidades de loteria da Caixa Econômica Federal, com base nos dados históricos coletados. A compreensão dessas particularidades é fundamental para o desenvolvimento e treinamento de modelos preditivos específicos para cada jogo.

## 1. Mega-Sena

A Mega-Sena é uma das loterias mais populares do Brasil, conhecida por seus grandes prêmios. O jogo consiste na escolha de números em um universo predefinido.

### 1.1. Características Principais

* **Números a serem sorteados:** 6 dezenas.
* **Universo de números:** De 1 a 60.
* **Formato dos dados:** Os dados históricos incluem o número do concurso, data do sorteio, dezenas sorteadas (em ordem de sorteio e crescente), informações sobre premiações (faixas, ganhadores, valor do prêmio), se acumulou, e dados do próximo concurso.

### 1.2. Estrutura do Jogo

Os jogadores escolhem de 6 a 20 números dentre os 60 disponíveis no volante. Ganha o prêmio principal quem acerta as 6 dezenas sorteadas. Há também premiações para quem acerta 4 (Quadra) ou 5 (Quina) números.

## 2. Quina

A Quina é conhecida por seus sorteios diários e pela possibilidade de ganhar com 2, 3, 4 ou 5 acertos.

### 2.1. Características Principais

* **Números a serem sorteados:** 5 dezenas.
* **Universo de números:** De 1 a 80.
* **Formato dos dados:** Os dados históricos incluem número do concurso, data, dezenas sorteadas, premiações (Duque, Terno, Quadra, Quina), acumulação e próximo concurso.

### 2.2. Estrutura do Jogo

Os jogadores escolhem de 5 a 15 números dentre os 80 disponíveis no volante. Ganha quem acerta 2 (Duque), 3 (Terno), 4 (Quadra) ou 5 (Quina) números.

## 3. Lotofácil

A Lotofácil, como o próprio nome sugere, é uma loteria com maior probabilidade de acerto, o que a torna bastante atrativa.

### 3.1. Características Principais

* **Números a serem sorteados:** 15 dezenas.
* **Universo de números:** De 1 a 25.
* **Formato dos dados:** Similar à Mega-Sena, os dados históricos da Lotofácil contêm o número do concurso, data, dezenas sorteadas, detalhes das premiações, acumulação e informações do próximo sorteio.

### 3.2. Estrutura do Jogo

Para jogar na Lotofácil, o apostador deve escolher entre 15 e 20 números dentre os 25 disponíveis no volante. Ganha quem acerta 11, 12, 13, 14 ou 15 números.

## 4. Mais Milionária

A Mais Milionária é uma modalidade de loteria mais recente, que oferece prêmios ainda maiores e com uma estrutura de jogo diferenciada.

### 4.1. Características Principais

* **Números a serem sorteados:** 6 dezenas e 2 trevos.
* **Universo de números:** 6 dezenas de 1 a 50, e 2 trevos de 1 a 6.
* **Formato dos dados:** Os dados históricos incluem o número do concurso, data, dezenas sorteadas, trevos sorteados, informações de premiação, acumulação e detalhes do próximo concurso.

### 4.2. Estrutura do Jogo

Na Mais Milionária, o apostador escolhe 6 números de 1 a 50 e 2 trevos de 1 a 6. Para ganhar o prêmio principal, é preciso acertar as 6 dezenas e os 2 trevos. Existem diversas faixas de premiação para acertos parciais das dezenas e/ou trevos.

## Considerações para Modelagem Preditiva

As diferenças nas características de cada loteria (universo de números, quantidade de dezenas sorteadas, e a inclusão de "trevos" na Mais Milionária) exigem abordagens de modelagem distintas. Modelos desenvolvidos para a Mega-Sena, por exemplo, não podem ser diretamente aplicados à Lotofácil ou à Mais Milionária sem adaptações significativas. A análise da distribuição de frequência, a identificação de padrões e a aplicação de algoritmos de aprendizado de máquina devem levar em conta essas especificidades para cada modalidade.
