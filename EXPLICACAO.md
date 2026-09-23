## Solução

Este documento descreve a implementação, as fontes usadas como referência e como executar o projeto.

### Arquivos

- **`src/tokenizer.py`** — função `tokenize(line)` que quebra uma linha de texto em uma lista de palavras normalizadas (minúsculas, sem pontuação), sem usar bibliotecas externas de regex — implementado varrendo caractere por caractere.

- **`src/build_dictionary.py`** — Job 1: lê todos os documentos de `dataset/`, extrai o vocabulário único de palavras e gera `output/dictionary.txt`, no formato `palavra<TAB>word_id`, ordenado alfabeticamente.

- **`src/build_index.py`** — Job 2: constrói o índice invertido a partir do dicionário e dos documentos, seguindo o algoritmo **Blocked Sort-Based Indexing (BSBI)**:
  1. Os documentos são processados em blocos (`BLOCK_SIZE` documentos por vez).
  2. Para cada bloco, gera os pares `(word_id, document_id)`, ordena e grava um arquivo intermediário em `output/blocks/`.
  3. Um merge k-way (`heapq.merge`) combina todos os blocos ordenados em uma única sequência global ordenada.
  4. Durante o merge, os pares são agrupados por `word_id`, produzindo o índice final em `output/inverted_index.txt`, no formato `word_id<TAB>doc_id1,doc_id2,...`.

  Essa abordagem em blocos evita carregar o dataset inteiro em memória de uma vez, permitindo escalar para volumes de dados maiores que a RAM disponível.

### Como executar

Rode os comandos a partir da raiz do projeto, nesta ordem:

### Comando 1

```bash
python src/build_dictionary.py
```

### Comando 2

```bash
python src/build_index.py
```

O primeiro comando gera `output/dictionary.txt`. O segundo lê esse dicionário, processa o dataset em blocos e gera `output/inverted_index.txt`.

### Referências e apoio utilizado

Este desafio foi resolvido com apoio de:

- **["Inverted Index - The Data Structure Behind Search Engines"](https://www.youtube.com/watch?v=iHHqnyThrqE)** (YouTube) — vídeo explicando o conceito e a estrutura de dados do índice invertido.
- **["7 3 The Inverted Index 10 42"](https://www.youtube.com/watch?v=Wf6HbY2PQDw)** (YouTube) — vídeo aula sobre construção do índice invertido.
- **["Understanding inverted indexes: the key to faster and more accurate search results"](https://www.youtube.com/watch?v=JsJ_ZGMztVg&t=11s)** (YouTube) — vídeo explicando como índices invertidos aceleram buscas.
- **Assistência de IA** para tirar dúvidas de código e aprofundar temas específicos do algoritmo BSBI. O código foi escrito e testado por mim, com essa orientação da IA.

