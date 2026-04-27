# Embeddings & Vector Databases (ANN, HNSW, Similaridade Semântica)

## Introdução

Embeddings e bancos vetoriais resolvem um problema que modelos tradicionais de dados não conseguem atacar bem: como encontrar similaridade entre informações que não são idênticas, mas semanticamente próximas. Em sistemas clássicos, você busca por igualdade ou por filtros bem definidos. Em sistemas modernos, você quer buscar por “significado”.

Isso muda completamente a forma como você modela dados e constrói queries. Em vez de comparar strings ou IDs, você compara vetores numéricos de alta dimensão.

## O que são embeddings

Embeddings são representações vetoriais de dados, normalmente geradas por modelos de machine learning. Um texto, imagem ou até um usuário pode ser transformado em um vetor de números.

A propriedade importante é que itens semanticamente semelhantes ficam próximos nesse espaço vetorial.

Por exemplo, frases com significados parecidos terão vetores próximos, mesmo que não compartilhem palavras exatas.

Isso permite buscas como:

* “textos parecidos com este”
* “produtos similares”
* “documentos relacionados”

Sem depender de matching exato.

## Similaridade semântica

Uma vez que você tem embeddings, o problema vira matemático: como medir proximidade entre vetores.

As métricas mais comuns são:

* cosine similarity
* distância euclidiana
* produto escalar

Essas métricas permitem ordenar resultados por “quão próximos” estão de um vetor de consulta.

Na prática, você transforma a query em embedding e busca os vetores mais próximos.

## O problema da busca em alta dimensão

Aqui está o ponto onde a teoria encontra a realidade.

Buscar o vizinho mais próximo exato (Nearest Neighbor) em espaços de alta dimensão é caro. O custo cresce rapidamente com o número de vetores e dimensões.

Fazer isso de forma exata em tempo real não escala bem para milhões ou bilhões de vetores.

É por isso que surge o conceito de ANN.

## Approximate Nearest Neighbor (ANN)

ANN troca precisão absoluta por performance.

Em vez de garantir o resultado exato, o sistema retorna um resultado “muito próximo do melhor” com custo muito menor.

Essa troca é aceitável na maioria dos casos de busca semântica, porque a diferença entre o melhor resultado e um muito próximo raramente é perceptível para o usuário.

O ganho de performance é o que torna sistemas vetoriais viáveis em produção.

## HNSW (Hierarchical Navigable Small World)

HNSW é um dos algoritmos mais usados para ANN.

A ideia central é construir um grafo onde cada vetor é conectado a outros vetores próximos. Esse grafo é organizado em múltiplos níveis, criando uma estrutura hierárquica.

Durante a busca, você navega por esse grafo, começando de níveis mais altos (mais conectados e menos detalhados) e descendo para níveis mais específicos.

Isso permite encontrar vizinhos próximos de forma muito eficiente, sem precisar comparar com todos os vetores.

O resultado é uma busca extremamente rápida, com alta qualidade de aproximação.

## Vector Databases

Bancos vetoriais existem para armazenar e indexar embeddings de forma eficiente.

Eles combinam:

* armazenamento de vetores
* indexação ANN
* operações de busca por similaridade

Diferente de bancos tradicionais, eles são otimizados para consultas como “top-k vetores mais próximos”.

Muitos também permitem combinar filtros estruturados com busca vetorial, como:

* categoria = “livros”
* similaridade com vetor X

Isso é essencial para casos reais.

## Pipeline típico

Um sistema baseado em embeddings normalmente segue este fluxo:

Você gera embeddings para seus dados e os armazena no banco vetorial. Quando uma query chega, você gera o embedding da query e busca os vetores mais próximos.

Opcionalmente, você pode reordenar resultados com um modelo mais caro (reranking) para melhorar qualidade.

Esse pipeline aparece em:

* busca semântica
* sistemas de recomendação
* RAG (retrieval augmented generation)

## Trade-offs reais

Embeddings não são mágicos. Eles dependem fortemente do modelo que os gera. Um modelo ruim gera representações ruins.

ANN sacrifica precisão. Em alguns casos críticos, isso pode ser um problema.

HNSW consome memória significativa, porque mantém estruturas de grafo complexas.

Bancos vetoriais adicionam uma nova camada de infraestrutura e exigem tuning de parâmetros.

Outro ponto crítico é atualização. Inserir e remover vetores pode ser mais complexo do que em bancos tradicionais.

## Quando usar

Embeddings fazem sentido quando o problema envolve similaridade semântica.

Se você precisa de matching exato ou filtros simples, bancos tradicionais são mais simples e eficientes.

Vector databases são úteis quando:

* há grande volume de embeddings
* latência de busca importa
* queries de similaridade são frequentes

Se você tem poucos dados, uma solução simples pode ser suficiente.

## O que muda na prática

Você deixa de modelar dados apenas como entidades e passa a modelar representações numéricas.

Queries deixam de ser determinísticas e passam a ser probabilísticas.

Isso exige mudança de mentalidade: você não busca o “resultado correto”, mas o “resultado mais relevante”.