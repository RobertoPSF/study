# Aula Completa: Rate Limit

Rate limiting é um mecanismo de controle de tráfego que define quantas
requisições um cliente pode fazer a um sistema dentro de um determinado
intervalo de tempo. Ele existe por três motivos principais: proteção
contra abuso, proteção contra sobrecarga e garantia de justiça entre
consumidores. Se você não entende profundamente rate limit, você não
entende sistemas em produção.

## O Problema

Todo sistema backend tem recursos finitos: CPU, memória, I/O, conexões
de banco, threads e sockets. Se um único cliente --- seja malicioso, mal
configurado ou simplesmente muito ativo --- fizer requisições demais,
ele pode degradar ou derrubar o sistema para todos os outros. Rate
limiting é uma forma de impor governança sobre o uso desses recursos.

Existem dois grandes contextos: - **Entrada**: proteger sua API de
clientes externos. - **Saída**: proteger serviços externos que você
consome.

## Modelo Básico

"N requisições a cada T segundos".

Exemplo: 100 requisições por minuto por usuário.

Perguntas críticas: - O que define um usuário? IP? API Key? Conta
autenticada? - Qual a granularidade? Global? Por endpoint?

## Algoritmos Clássicos

### 1. Fixed Window Counter

Divide o tempo em janelas fixas. Simples, mas sofre com efeito de borda.

### 2. Sliding Window Log

Armazena timestamp de cada requisição. Preciso, mas caro em memória.

### 3. Sliding Window Counter

Versão otimizada do anterior. Reduz custo e suaviza picos.

### 4. Token Bucket (Mais Importante)

Um "balde" com tokens que são repostos a uma taxa fixa. Cada requisição
consome um token. Permite bursts controlados.

### 5. Leaky Bucket

Controla saída em taxa constante. Modela vazão estável.

## Onde Implementar

-   Load Balancer
-   API Gateway
-   Aplicação

Em sistemas distribuídos, use armazenamento compartilhado (ex: Redis)
para manter consistência.

## Redis e Atomicidade

Use operações atômicas como `INCR` + `EXPIRE` ou scripts Lua para
garantir que múltiplas requisições simultâneas não ultrapassem o limite.

## Granularidade

Pode ser aplicado: - Global - Por usuário - Por endpoint - Por plano
(tier)

## Código de Resposta

-   **429 Too Many Requests**
-   Headers recomendados:
    -   `Retry-After`
    -   `X-RateLimit-Limit`
    -   `X-RateLimit-Remaining`
    -   `X-RateLimit-Reset`

## Segurança

Ajuda contra: - Brute force - Credential stuffing - Scraping

Não substitui mecanismos de segurança completos.

## Hard vs Soft Limit

-   **Hard limit**: bloqueia imediatamente.
-   **Soft limit**: permite temporariamente com degradação gradual.

## Observabilidade

Monitorar: - Número de bloqueios - Picos de requisições - Impacto na
experiência do usuário

## Trade-offs

-   Muito restritivo → prejudica usuários legítimos.
-   Muito permissivo → risco de sobrecarga.
-   Centralizado → consistente, mas pode virar gargalo.
-   Descentralizado → rápido, mas inconsistente.

## Aplicação no Projeto

No projeto de API de agregação resiliente:

1.  Proteger o backend contra abuso externo.
2.  Não exceder limites das APIs consumidas.

## Perguntas Clássicas de Entrevista

**Como implementar rate limit distribuído?**\
Redis com operações atômicas ou script Lua + Token Bucket.

**Como evitar gargalo?**\
Aplicar rate limit no edge (CDN/API Gateway) e usar cluster/sharding.

## Conceitos Relacionados

-   **Rate Limit**: define limite máximo permitido.
-   **Throttling**: desacelera progressivamente ao invés de bloquear.

------------------------------------------------------------------------

## Resumo Final

-   Rate limit controla consumo de recursos.
-   Token bucket é o algoritmo mais equilibrado.
-   Redis resolve consistência distribuída.
-   429 é o status correto.
-   Limites devem ser baseados na capacidade real do sistema.
-   Rate limit protege, mas não substitui segurança.
