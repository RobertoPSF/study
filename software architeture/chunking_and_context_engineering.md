# Chunking & Context Engineering (Overlap, Metadata, Re-ranking)

## Introdução

Se você chegou até RAG e embeddings, já percebeu um ponto desconfortável: a qualidade do sistema raramente depende só do modelo. Na prática, o gargalo quase sempre está em como você prepara e organiza o contexto.

Chunking e Context Engineering existem exatamente para resolver isso. Eles tratam de uma pergunta central: como transformar dados brutos em contexto útil para o modelo tomar decisões melhores.

A maioria dos sistemas falha aqui porque trata essa etapa como detalhe técnico, quando na verdade ela é o principal determinante de qualidade.

## O problema do contexto mal construído

Modelos de linguagem têm uma limitação clara: eles só conseguem raciocinar sobre o que está dentro do contexto fornecido.

Se o contexto está incompleto, fragmentado ou poluído, o modelo vai errar — não por incapacidade, mas por falta de informação adequada.

Isso significa que não adianta ter o melhor modelo se:

* o chunk não contém a informação completa
* partes relevantes foram separadas
* há muito ruído irrelevante

Contexto ruim gera resposta ruim. Isso é determinístico.

## Chunking

Chunking é o processo de dividir documentos em partes menores que serão indexadas e recuperadas.

Essa divisão parece simples, mas é onde decisões erradas começam a comprometer todo o pipeline.

O objetivo não é apenas “quebrar texto”, mas preservar unidades semânticas.

Um chunk ideal deve ser autocontido. Ele precisa fazer sentido sozinho, sem depender fortemente de partes externas.

Se você corta no meio de uma ideia, você cria ambiguidade.

Se você agrupa demais, você dilui relevância.

Esse equilíbrio é o ponto central do chunking.

## Tamanho de chunk

Chunks muito pequenos aumentam precisão, mas perdem contexto.

Chunks muito grandes preservam contexto, mas dificultam recuperação precisa.

Não existe tamanho universal. O correto depende do domínio e do tipo de query.

Em textos técnicos, por exemplo, manter parágrafos completos costuma funcionar melhor do que cortes arbitrários por número de tokens.

A abordagem madura é iterativa: você ajusta com base em avaliação real, não em regra fixa.

## Overlap

Overlap é uma técnica usada para reduzir o problema de cortes artificiais.

Você permite que chunks consecutivos compartilhem uma parte do conteúdo.

Isso aumenta a chance de que informações importantes não sejam perdidas na divisão.

Mas isso tem custo.

Overlap excessivo gera redundância, aumenta o tamanho do índice e pode poluir o contexto com repetições.

Overlap insuficiente pode cortar informação crítica.

O objetivo não é maximizar overlap, é usá-lo de forma controlada para preservar continuidade sem gerar ruído.

## Metadata

Metadata é o que permite sair de uma busca puramente semântica para uma busca mais controlada.

Cada chunk pode carregar informações adicionais, como:

* fonte do documento
* data
* tipo de conteúdo
* categoria
* autor

Isso permite aplicar filtros antes ou durante a busca.

Sem metadata, você depende apenas de similaridade vetorial, que nem sempre é suficiente.

Por exemplo, duas respostas podem ser semanticamente próximas, mas uma pode estar desatualizada.

Metadata permite evitar esse tipo de erro.

Ela também melhora explicabilidade. Você consegue rastrear de onde veio a informação.

## Context Engineering

Context Engineering é o processo de montar o contexto final que será enviado ao modelo.

Isso vai além de simplesmente pegar os top-k resultados e concatenar.

Você precisa decidir:

* quais chunks incluir
* em que ordem
* com que formatação
* com quais instruções

Essa etapa define o que o modelo realmente “vê”.

Erros aqui são comuns e silenciosos.

## Ordenação e seleção

Nem todo resultado recuperado deve entrar no contexto.

Você precisa selecionar e ordenar.

Ordenação por similaridade é o ponto de partida, mas nem sempre é suficiente.

Às vezes, diversidade de contexto é mais importante do que proximidade extrema.

Outras vezes, você precisa priorizar fontes mais confiáveis.

Isso exige heurísticas ou modelos adicionais.

## Re-ranking

Re-ranking é uma etapa onde você pega os resultados iniciais (geralmente obtidos por ANN) e reordena usando um modelo mais preciso.

A busca vetorial é rápida, mas aproximada.

O re-ranking usa um modelo mais caro (por exemplo, um cross-encoder) para avaliar melhor a relevância.

Isso melhora significativamente a qualidade dos resultados finais.

O trade-off é latência e custo.

Re-ranking não deve ser aplicado cegamente. Ele faz sentido quando qualidade é mais crítica do que tempo de resposta.

## Construção do prompt

Context Engineering também inclui como você apresenta os dados ao modelo.

Você pode:

* separar chunks com delimitadores claros
* indicar fontes
* estruturar em formato consistente

Isso ajuda o modelo a interpretar corretamente o contexto.

Prompts mal estruturados podem fazer o modelo ignorar partes relevantes.

## Trade-offs reais

Chunking fino melhora precisão, mas aumenta custo de indexação.

Overlap melhora continuidade, mas gera redundância.

Metadata melhora controle, mas exige manutenção.

Re-ranking melhora qualidade, mas aumenta latência.

Context Engineering melhora respostas, mas adiciona complexidade ao pipeline.

Não existe configuração ideal universal. Existe ajuste contínuo baseado em avaliação.

## Quando isso importa

Se você está construindo qualquer sistema baseado em RAG ou busca semântica, isso não é opcional.

Se você ignora chunking e contexto, você está limitando o sistema antes mesmo do modelo entrar em ação.

## O que muda na prática

Você deixa de pensar apenas em “armazenar dados” e passa a pensar em “como esses dados serão consumidos pelo modelo”.

Isso exige:

* entender queries reais
* ajustar chunking
* testar diferentes estratégias

A qualidade final passa a depender mais dessas decisões do que do modelo em si.