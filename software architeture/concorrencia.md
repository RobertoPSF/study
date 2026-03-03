# Concorrência --- Aula Completa

Concorrência é a capacidade de um sistema lidar com múltiplas tarefas
que progridem no mesmo intervalo de tempo. Isso não significa que elas
estão executando simultaneamente. Isso é paralelismo. Concorrência é
sobre estrutura; paralelismo é sobre execução física.

Um programa concorrente organiza o trabalho de forma que múltiplas
operações possam avançar de maneira intercalada ou simultânea,
dependendo do ambiente.

## Concorrência vs Paralelismo

Concorrência: - Várias tarefas em progresso - Pode acontecer com um
único núcleo de CPU - Usa troca de contexto

Paralelismo: - Execução simultânea real - Múltiplos núcleos - Foco em
performance bruta

Concorrência é sobre estrutura correta sob múltiplos fluxos de
execução.\
Paralelismo é sobre escala de CPU.

------------------------------------------------------------------------

## Por que concorrência é difícil?

Porque o estado compartilhado é perigoso.

Quando múltiplas threads ou processos acessam o mesmo dado, surgem
problemas como: - Race condition - Deadlock - Livelock - Starvation -
Inconsistência

Concorrência é essencialmente o problema de controlar acesso a estado
compartilhado.

------------------------------------------------------------------------

## Modelos de Concorrência

### 1. Threads (Shared Memory)

Múltiplas threads compartilham memória no mesmo processo.

Problemas comuns: - Necessidade de sincronização - Race conditions

Ferramentas: - Mutex - Semaphore - RWLock - Operações atômicas

------------------------------------------------------------------------

### 2. Processos

Cada processo tem memória isolada.

Vantagens: - Mais seguro - Isolamento natural

Desvantagem: - Comunicação mais cara (IPC)

------------------------------------------------------------------------

### 3. Modelo Assíncrono / Event Loop

Baseado em operações não bloqueantes e cooperativas (async/await).

Ideal para: - Workloads I/O-bound - Servidores web

Erro clássico: usar operação bloqueante dentro de função async.

------------------------------------------------------------------------

## I/O-bound vs CPU-bound

I/O-bound: - Espera rede - Espera banco - Espera disco

CPU-bound: - Cálculo pesado - Compressão - Criptografia

Async ajuda I/O-bound.\
Multiprocess ajuda CPU-bound.

------------------------------------------------------------------------

## Problemas Clássicos

### Race Condition

Resultado depende da ordem de execução.

### Deadlock

Duas threads esperando uma à outra indefinidamente.

### Starvation

Uma thread nunca executa.

### Livelock

Threads reagem entre si sem progresso real.

------------------------------------------------------------------------

## Sincronização

-   Mutex: exclusão mútua
-   Semaphore: limite de acessos simultâneos
-   Read-Write Lock: múltiplos leitores, um escritor
-   Operações atômicas

Melhor estratégia: evitar estado compartilhado.

------------------------------------------------------------------------

## Python e GIL

Python possui Global Interpreter Lock (GIL): - Apenas uma thread executa
bytecode por vez - Threads não escalam CPU-bound - Funcionam bem para
I/O-bound

Para CPU-bound: - Multiprocessing - Extensões em C

------------------------------------------------------------------------

## Concorrência em Backend

Aparece em: - Múltiplas requisições simultâneas - Cache compartilhado -
Chamadas paralelas a APIs externas

Perguntas comuns em entrevista: - Seu cache é thread-safe? - Como evitar
cache stampede? - Como garantir consistência sob concorrência?

------------------------------------------------------------------------

## Nível Sênior

Concorrência não é criar threads. É controlar complexidade sob múltiplas
execuções.

Boas práticas: - Reduzir estado compartilhado - Usar imutabilidade -
Isolar responsabilidades - Aceitar consistência eventual quando
necessário

------------------------------------------------------------------------

## Aplicação no Projeto

No projeto de API de agregação resiliente: - Usar async gather para
chamadas paralelas - Implementar cache thread-safe - Evitar múltiplos
refresh simultâneos - Garantir logs consistentes
