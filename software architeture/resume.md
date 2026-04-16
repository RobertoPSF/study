# Resumo de Arquitetura de Software (Versão Consolidada)

## ACID e Transações
ACID define as garantias fundamentais de transações em bancos de dados: atomicidade garante que tudo acontece ou nada acontece, consistência assegura que o banco nunca entra em estado inválido, isolamento controla interferência entre transações concorrentes e durabilidade garante persistência mesmo após falhas. Essas propriedades são essenciais em sistemas críticos, mas vêm com custo de performance e escalabilidade.

## Anti-patterns
Anti-patterns são soluções aparentemente válidas que geram problemas no longo prazo, como acoplamento excessivo, complexidade desnecessária ou baixa escalabilidade. Reconhecê-los é tão importante quanto conhecer boas práticas, pois evita decisões que degradam o sistema com o tempo.

## APIs e Timeouts
Timeouts definem o tempo máximo de espera por uma resposta externa, evitando que threads ou recursos fiquem bloqueados indefinidamente. São essenciais para resiliência, especialmente quando combinados com retry e circuit breaker.

## API Gateway e BFF
API Gateway e Backend for Frontend resolvem problemas diferentes dentro de sistemas distribuídos. O API Gateway centraliza preocupações transversais e funciona como ponto único de entrada, devendo permanecer livre de lógica de negócio. O BFF adapta o backend para necessidades específicas de cada cliente, orquestrando serviços e ajustando respostas.

Quando usados juntos, o gateway cuida da infraestrutura e o BFF da experiência do cliente. O uso correto depende do nível real de complexidade do sistema. Usar cedo demais adiciona custo sem benefício; usar tarde demais gera acoplamento difícil de corrigir.

## Arquitetura em Camadas
Organiza o sistema em camadas com responsabilidades bem definidas, separando regras de negócio de infraestrutura. Isso melhora manutenção, testabilidade e evolução do sistema, mas pode introduzir overhead e rigidez se mal aplicado.

## Cache Distribuído vs Local
Cache local oferece baixa latência e simplicidade, mas não é compartilhado entre instâncias. Cache distribuído resolve isso, permitindo consistência entre nós, porém com maior complexidade, latência e desafios de invalidação.

## Cache
Cache reduz latência e carga em sistemas downstream armazenando dados frequentemente acessados. O maior desafio está em manter consistência e evitar dados desatualizados.

## CAP Theorem
Em sistemas distribuídos, é impossível garantir simultaneamente consistência forte, disponibilidade total e tolerância a partições. Na prática, sistemas precisam escolher trade-offs dependendo do contexto.

## Capacity Planning
Processo de estimar e ajustar recursos para suportar carga atual e futura. Envolve entender throughput, latência, uso de recursos e padrões de tráfego, evitando tanto gargalos quanto desperdício.

## Circuit Breaker
Protege o sistema interrompendo chamadas para serviços que estão falhando, evitando efeito cascata. Após um período, permite tentativas controladas para verificar recuperação.

## Clean Architeture vs Hexagonal vs Onion

Hexagonal, Onion e Clean Architecture defendem a mesma ideia central: regras de negócio não devem depender de detalhes externos. A Dependency Rule obriga as dependências a apontarem para dentro, protegendo o domínio.

Hexagonal enfatiza portas e adapters, sendo forte para integrações. Onion enfatiza camadas concêntricas e separação do domínio. Clean Architecture combina as duas e adiciona uma divisão mais explícita entre entidades, casos de uso, adapters e frameworks.

Nenhuma é universalmente melhor. O melhor desenho depende do tamanho do sistema, da quantidade de regras de negócio, da quantidade de integrações e do nível de complexidade que realmente precisa ser controlado.

## Concorrência
Execução simultânea de operações exige controle rigoroso para evitar inconsistências. Problemas comuns incluem race conditions, deadlocks e contenção de recursos.

## Consistência Distribuída
Garante que múltiplos nós mantenham uma visão coerente dos dados. Pode variar entre consistência forte e eventual, dependendo dos trade-offs entre latência, disponibilidade e complexidade.

## Dead Letter Queue
Dead Letter Queue é uma fila onde mensagens que falharam após várias tentativas são armazenadas para análise ou reprocessamento. Ela evita que mensagens problemáticas travem o sistema, melhora resiliência e observabilidade, mas exige tratamento adequado para não se tornar apenas um acúmulo de erros ignorados.

## Deadlock Prevention
Deadlock prevention consiste em evitar ciclos de espera entre processos concorrentes, eliminando condições como espera circular ou hold and wait. Técnicas incluem ordenação de recursos, aquisição antecipada, timeouts e preempção. O objetivo é garantir que o sistema continue progredindo mesmo sob alta concorrência.

## Domain Driven-Design
Domain-Driven Design é uma abordagem para alinhar código ao domínio de negócio. Ubiquitous Language garante que todos falem a mesma língua. Bounded Context separa onde cada modelo é válido, evitando conflitos de significado. Aggregates protegem invariantes e controlam consistência dentro de um contexto.

DDD não é sobre arquitetura em si, mas sobre modelagem correta. Ele introduz complexidade intencional para controlar sistemas complexos. Se aplicado sem necessidade, vira sobrecarga. Se ignorado quando necessário, o sistema se torna caótico.


## Escalabilidade
Capacidade de lidar com aumento de carga. Pode ser vertical (mais recursos) ou horizontal (mais instâncias), sendo esta última a base de sistemas distribuídos modernos.

## Escalar Leitura vs Escrita
Leitura é mais fácil de escalar com réplicas. Escrita exige coordenação, particionamento ou estratégias mais complexas devido à necessidade de manter consistência.

## Event-Driven Architecture
Baseada em eventos, permite desacoplamento entre componentes. Producers geram eventos e consumers reagem, aumentando escalabilidade e resiliência, mas dificultando rastreabilidade e consistência.

## Fan-Out Pattern
Fan-out é um padrão onde uma única requisição ou evento é distribuído para múltiplos consumidores que processam em paralelo. Ele aumenta throughput e desacoplamento, sendo comum em arquiteturas orientadas a eventos, mas exige cuidados com consistência, idempotência e tratamento de falhas.

## Horizontal Scaling
Horizontal scaling é a capacidade de aumentar a capacidade de um sistema adicionando mais instâncias e distribuindo a carga entre elas. Ele melhora escalabilidade e disponibilidade ao eliminar pontos únicos de falha, mas exige sistemas stateless, uso de load balancing e, frequentemente, particionamento de dados. Em troca, introduz complexidade relacionada à consistência, coordenação e comunicação distribuída.

## Idempotência
Garante que executar a mesma operação múltiplas vezes resulta no mesmo estado final. É essencial em sistemas com retries, filas e processamento distribuído.

## Load Distribution
Distribui carga entre múltiplas instâncias para evitar gargalos e melhorar utilização de recursos. Estratégias variam de simples round robin até algoritmos baseados em estado.

## Lost Update
Ocorre quando múltiplas operações sobrescrevem dados umas das outras sem coordenação, resultando em perda de informação. É um problema clássico de concorrência.

## Monolito vs Microserviços
Monolito é simples e fácil de desenvolver inicialmente. Microserviços oferecem escalabilidade e independência, mas aumentam complexidade operacional, comunicação e consistência.

## Observalidade
Observabilidade é a capacidade de entender o comportamento interno de um sistema através de métricas, logs e traces. Diferente de monitoramento, ela permite investigar problemas desconhecidos e analisar sistemas distribuídos de forma profunda. É essencial para debugging, performance e operação, mas exige boa instrumentação, correlação de dados e controle de custo.

## Optimistic Lock
Permite concorrência assumindo poucos conflitos e valida alterações no commit. Em caso de conflito, a operação falha e deve ser reexecutada.

## Pessimistic Lock
Bloqueia recursos antecipadamente para evitar conflitos. Garante consistência forte, mas reduz concorrência e pode causar contenção e deadlocks.

## Producer–Consumer
Separa geração e processamento de tarefas usando filas. Permite escalabilidade e processamento assíncrono, sendo base de sistemas modernos.

## Race Conditions
Acontecem quando o resultado depende da ordem de execução de operações concorrentes. São difíceis de reproduzir e podem gerar inconsistências críticas.

## Rate Limit
Controla o número de requisições permitidas em um período, protegendo o sistema contra abuso e sobrecarga.

## REST
Estilo arquitetural baseado em recursos e HTTP, com comunicação stateless. Simples e amplamente utilizado, mas pode não ser ideal para todos os cenários.

## Retry e Backoff
Permite reexecutar operações falhas com intervalos crescentes, aumentando resiliência sem causar sobrecarga no sistema.

## Service Mesh
Service Mesh é uma camada de infraestrutura que gerencia comunicação entre serviços, removendo essa responsabilidade do código de aplicação. Ele utiliza o sidecar pattern para interceptar tráfego e aplicar políticas como retries, segurança e observabilidade.

Istio oferece controle avançado com alta complexidade operacional, enquanto Linkerd prioriza simplicidade com menos flexibilidade. O uso de Service Mesh desloca a complexidade do código para a infraestrutura e só faz sentido em sistemas distribuídos maduros.

## SQL vs NoSQL
SQL prioriza consistência e estrutura rígida. NoSQL prioriza escalabilidade e flexibilidade, geralmente aceitando consistência eventual.

## System Design
System Design é o processo de projetar sistemas completos considerando requisitos funcionais e não funcionais, integrando conceitos como escalabilidade, consistência, concorrência e resiliência. O foco está em tomar decisões baseadas em trade-offs e construir soluções que funcionem em produção, não apenas em teoria.

## Task Leasing
Atribui tarefas a workers com tempo limitado. Se o worker falhar, a tarefa volta para a fila, garantindo confiabilidade com risco de duplicação.

## Throttling
Throttling é o controle da taxa de processamento de requisições para evitar sobrecarga no sistema. Diferente de rate limiting, ele atua de forma mais gradual, podendo atrasar, enfileirar ou reduzir o fluxo de requisições. É essencial para estabilidade, funcionando como uma forma de backpressure e sendo frequentemente combinado com filas, retries e circuit breakers.

## Throughput vs Latency
Throughput mede volume de processamento; latency mede tempo de resposta. Melhorar um geralmente impacta o outro, exigindo trade-offs.

## Trade-offs
Toda decisão arquitetural envolve abrir mão de algo para ganhar outra propriedade. Entender esses trade-offs é essencial para projetar sistemas corretos.

## Tratamento de Erros
Define como o sistema reage a falhas, incluindo retries, fallback, logging e recuperação, sendo essencial para resiliência.

## Rate Limit vs Throttling
Enquanto o rate limiting define limites **rígidos** de requisições por cliente ou por período de tempo, geralmente resultando em rejeições imediatas (como HTTP 429), o throttling é mais focado em proteger o sistema como um todo, controlando a taxa global de processamento **progressivamente**.