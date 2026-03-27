# Resumo de Arquitetura de Software (Versão Consolidada)

## ACID e Transações
ACID define as garantias fundamentais de transações em bancos de dados: atomicidade garante que tudo acontece ou nada acontece, consistência assegura que o banco nunca entra em estado inválido, isolamento controla interferência entre transações concorrentes e durabilidade garante persistência mesmo após falhas. Essas propriedades são essenciais em sistemas críticos, mas vêm com custo de performance e escalabilidade.

## Anti-patterns
Anti-patterns são soluções aparentemente válidas que geram problemas no longo prazo, como acoplamento excessivo, complexidade desnecessária ou baixa escalabilidade. Reconhecê-los é tão importante quanto conhecer boas práticas, pois evita decisões que degradam o sistema com o tempo.

## APIs e Timeouts
Timeouts definem o tempo máximo de espera por uma resposta externa, evitando que threads ou recursos fiquem bloqueados indefinidamente. São essenciais para resiliência, especialmente quando combinados com retry e circuit breaker.

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

## Concorrência
Execução simultânea de operações exige controle rigoroso para evitar inconsistências. Problemas comuns incluem race conditions, deadlocks e contenção de recursos.

## Consistência Distribuída
Garante que múltiplos nós mantenham uma visão coerente dos dados. Pode variar entre consistência forte e eventual, dependendo dos trade-offs entre latência, disponibilidade e complexidade.

## Escalabilidade
Capacidade de lidar com aumento de carga. Pode ser vertical (mais recursos) ou horizontal (mais instâncias), sendo esta última a base de sistemas distribuídos modernos.

## Escalar Leitura vs Escrita
Leitura é mais fácil de escalar com réplicas. Escrita exige coordenação, particionamento ou estratégias mais complexas devido à necessidade de manter consistência.

## Event-Driven Architecture
Baseada em eventos, permite desacoplamento entre componentes. Producers geram eventos e consumers reagem, aumentando escalabilidade e resiliência, mas dificultando rastreabilidade e consistência.

## Idempotência
Garante que executar a mesma operação múltiplas vezes resulta no mesmo estado final. É essencial em sistemas com retries, filas e processamento distribuído.

## Load Distribution
Distribui carga entre múltiplas instâncias para evitar gargalos e melhorar utilização de recursos. Estratégias variam de simples round robin até algoritmos baseados em estado.

## Lost Update
Ocorre quando múltiplas operações sobrescrevem dados umas das outras sem coordenação, resultando em perda de informação. É um problema clássico de concorrência.

## Monolito vs Microserviços
Monolito é simples e fácil de desenvolver inicialmente. Microserviços oferecem escalabilidade e independência, mas aumentam complexidade operacional, comunicação e consistência.

## Observabilidade
Capacidade de entender o comportamento interno do sistema via métricas, logs e traces. Essencial para debugging, performance e tomada de decisão.

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

## SQL vs NoSQL
SQL prioriza consistência e estrutura rígida. NoSQL prioriza escalabilidade e flexibilidade, geralmente aceitando consistência eventual.

## Task Leasing
Atribui tarefas a workers com tempo limitado. Se o worker falhar, a tarefa volta para a fila, garantindo confiabilidade com risco de duplicação.

## Throughput vs Latency
Throughput mede volume de processamento; latency mede tempo de resposta. Melhorar um geralmente impacta o outro, exigindo trade-offs.

## Trade-offs
Toda decisão arquitetural envolve abrir mão de algo para ganhar outra propriedade. Entender esses trade-offs é essencial para projetar sistemas corretos.

## Tratamento de Erros
Define como o sistema reage a falhas, incluindo retries, fallback, logging e recuperação, sendo essencial para resiliência.

## Horizontal Scaling
Horizontal scaling é a capacidade de aumentar a capacidade de um sistema adicionando mais instâncias e distribuindo a carga entre elas. Ele melhora escalabilidade e disponibilidade ao eliminar pontos únicos de falha, mas exige sistemas stateless, uso de load balancing e, frequentemente, particionamento de dados. Em troca, introduz complexidade relacionada à consistência, coordenação e comunicação distribuída.

## Observalidade
Observabilidade é a capacidade de entender o comportamento interno de um sistema através de métricas, logs e traces. Diferente de monitoramento, ela permite investigar problemas desconhecidos e analisar sistemas distribuídos de forma profunda. É essencial para debugging, performance e operação, mas exige boa instrumentação, correlação de dados e controle de custo.