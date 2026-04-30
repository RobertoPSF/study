# LLM System Design (Orquestração, Caching, Agentes vs Pipelines)

## Introdução

Projetar sistemas com LLMs não é sobre escolher um modelo e chamar uma API. Isso é o equivalente moderno de escrever um script, não de construir um sistema. O desafio real aparece quando você precisa de previsibilidade, custo controlado, latência aceitável e qualidade consistente em produção.

LLMs são componentes probabilísticos inseridos em sistemas determinísticos. Isso cria uma tensão fundamental. O restante da sua arquitetura quer previsibilidade e repetibilidade; o LLM introduz variabilidade. O papel do system design é controlar essa variabilidade sem perder o valor que o modelo oferece.

Três decisões estruturais definem quase tudo: como você orquestra chamadas, como você usa caching e se você modela o fluxo como pipeline ou como agente.

## Orquestração

Orquestração é como você organiza múltiplas etapas envolvendo LLMs e outros serviços. Em sistemas reais, raramente existe uma única chamada. Você tem etapas como classificação, recuperação, geração, verificação e formatação.

Uma orquestração ingênua encadeia chamadas de forma linear e rígida. Isso funciona no começo, mas rapidamente se torna frágil. Pequenas mudanças em uma etapa impactam todo o fluxo, e você perde capacidade de adaptar comportamento dinamicamente.

Uma orquestração madura trata o fluxo como um grafo de decisões. Em vez de sempre executar tudo, você decide quais etapas executar com base no contexto. Por exemplo, você pode classificar a intenção primeiro e só executar RAG se a pergunta exigir conhecimento externo. Isso reduz custo e latência.

Outro ponto crítico é observabilidade. Você precisa saber o que cada etapa recebeu, produziu e quanto custou. Sem isso, você não consegue depurar nem otimizar.

Orquestração também envolve controle de erros. LLMs falham de formas não determinísticas. Você precisa de estratégias como retries controlados, fallback para respostas mais simples ou até short-circuit quando a confiança é baixa.

## Caching

Caching em sistemas com LLM é frequentemente negligenciado, mas tem impacto direto em custo e latência.

O primeiro tipo é caching de resposta. Se a mesma pergunta aparece com frequência, você pode armazenar a resposta e evitar nova chamada ao modelo. Isso parece óbvio, mas exige cuidado com variações de input. Perguntas semanticamente iguais podem ter formas diferentes, então você precisa de normalização ou até embeddings para detectar similaridade.

O segundo tipo é caching intermediário. Em pipelines com múltiplas etapas, você pode cachear resultados de classificação, retrieval ou até partes do contexto. Isso evita recomputação e estabiliza o sistema.

O terceiro tipo é caching de embeddings. Gerar embeddings tem custo. Reutilizar embeddings para documentos e queries recorrentes reduz significativamente esse custo.

O problema é invalidação. Dados mudam, contexto muda, comportamento desejado muda. Cache sem estratégia de invalidação vira fonte de inconsistência.

Caching também pode esconder problemas. Se você cacheia respostas ruins, você só acelera a propagação de erro.

## Pipelines

Pipelines são fluxos estruturados e previsíveis. Cada etapa tem responsabilidade clara e ordem definida. Esse modelo é mais fácil de testar, debugar e operar.

Um pipeline típico pode ser: classificar intenção, recuperar contexto, gerar resposta, validar saída.

A vantagem é controle. Você sabe exatamente o que acontece em cada etapa. Isso facilita medir qualidade, custo e latência.

A desvantagem é rigidez. Se o fluxo precisa variar muito dependendo do contexto, o pipeline começa a acumular condicionais e perde clareza.

Pipelines funcionam melhor quando o problema é bem definido e repetitivo.

## Agentes

Agentes são sistemas onde o LLM decide quais ações tomar. Em vez de um fluxo fixo, você dá ao modelo ferramentas e ele escolhe quando e como usá-las.

Isso permite comportamento mais flexível. O sistema pode adaptar o fluxo dinamicamente, chamar APIs diferentes, iterar até chegar a uma resposta.

O problema é controle. Você está delegando decisões para um componente probabilístico. Isso torna o sistema mais difícil de prever, testar e limitar em custo.

Agentes também introduzem loops. Sem limites claros, você pode ter múltiplas chamadas desnecessárias, aumentando latência e custo.

Debugging se torna mais difícil porque o caminho de execução não é fixo.

## Agentes vs Pipelines

Essa não é uma escolha binária, mas um espectro.

Pipelines oferecem previsibilidade e são preferíveis quando você precisa de controle e consistência.

Agentes oferecem flexibilidade e são úteis quando o problema exige exploração ou decisões dinâmicas.

Na prática, sistemas maduros combinam os dois. Você usa pipelines para estrutura principal e agentes para partes específicas onde flexibilidade agrega valor.

O erro comum é usar agentes para tudo. Isso geralmente resulta em sistemas caros, lentos e difíceis de manter.

## Trade-offs reais

Orquestração complexa melhora qualidade, mas aumenta custo operacional.

Caching reduz custo e latência, mas introduz risco de inconsistência.

Pipelines são previsíveis, mas podem se tornar rígidos.

Agentes são flexíveis, mas difíceis de controlar.

A decisão correta depende do tipo de problema e do nível de maturidade do sistema.

## O que muda na prática

Você deixa de pensar em “chamar um modelo” e passa a pensar em compor um sistema com múltiplos componentes.

O LLM vira apenas uma peça dentro de um fluxo maior que inclui dados, regras e controle.

A qualidade final depende tanto da arquitetura quanto do modelo.
