# Aula Completa: Cache

## O que é Cache

Cache é uma camada temporária de armazenamento usada para reduzir
latência, carga e custo ao evitar recomputação ou reconsulta de dados
que já foram obtidos anteriormente.

A definição mais importante não é "armazenar rápido". Cache troca
consistência absoluta por performance previsível.

------------------------------------------------------------------------

## Por que Cache existe?

Três coisas são caras em sistemas:

1.  I/O de rede (chamar API externa)
2.  I/O de disco (consultar banco)
3.  Computação pesada

Cache reduz qualquer um desses custos.

------------------------------------------------------------------------

## Hit vs Miss

**Cache Hit**\
O dado está no cache. Resposta rápida.

**Cache Miss**\
O dado não está no cache. É necessário buscar na origem e depois
armazenar.

A eficiência do cache depende da taxa de hit.

------------------------------------------------------------------------

## TTL (Time To Live)

TTL é o tempo que um dado permanece válido no cache.

Exemplo: TTL = 60 segundos.

Trade-off: - TTL alto → menos chamadas externas, mas dados mais
desatualizados. - TTL baixo → mais consistência, menos ganho de
performance.

A escolha do TTL depende de: - Frequência de mudança do dado - Impacto
de dados desatualizados - Custo da chamada externa

------------------------------------------------------------------------

## Dados Stale

Cache não garante que o dado seja o mais recente.

É necessário decidir: - Pode retornar dado antigo? - Quanto tempo de
defasagem é aceitável?

------------------------------------------------------------------------

## Cache Invalidation

Invalidar cache é difícil porque você precisa saber quando o dado deixou
de ser válido.

Estratégias comuns: - Baseado em tempo (TTL) - Baseado em evento -
Manual

------------------------------------------------------------------------

## Tipos de Cache

### Cache em Memória Local

Exemplo: dicionário Python, LRUCache.

Vantagens: - Muito rápido - Simples

Desvantagens: - Não compartilhado entre instâncias - Perde dados ao
reiniciar o processo

------------------------------------------------------------------------

### Cache Distribuído

Exemplo: Redis, Memcached.

Vantagens: - Compartilhado entre instâncias - Escalável

Desvantagens: - Infraestrutura adicional - Latência de rede

------------------------------------------------------------------------

## Estratégias de Cache

### Cache-Aside (mais comum)

Fluxo: 1. Checa cache 2. Se miss → busca origem 3. Armazena no cache 4.
Retorna

------------------------------------------------------------------------

### Write-Through

Atualiza cache e banco ao mesmo tempo.

------------------------------------------------------------------------

### Write-Back

Escreve no cache e atualiza banco depois. Alta performance, maior
complexidade.

------------------------------------------------------------------------

## Problemas Reais

### Cache Stampede

Muitas requisições simultâneas após expiração do TTL causam sobrecarga
na origem.

### Cache Poisoning

Dados incorretos armazenados e servidos repetidamente.

### Consistência

Cache pode introduzir eventual consistency.

------------------------------------------------------------------------

## Quando NÃO usar Cache

-   Dados críticos que mudam constantemente
-   Sistemas pequenos sem problema de performance
-   Baixa repetição de requisições

------------------------------------------------------------------------

## Aplicação Prática

Para um projeto backend:

1.  Implementar cache em memória
2.  Definir TTL (ex: 60 segundos)
3.  Logar hits e misses
4.  Documentar trade-offs no README

------------------------------------------------------------------------

## Modelo de Resposta para Entrevista

"Implementei cache no padrão cache-aside para reduzir latência e
dependência de APIs externas. Defini TTL baseado na frequência de
mudança do dado e aceitei eventual consistency como trade-off. Em caso
de escala horizontal, migraria para Redis."
