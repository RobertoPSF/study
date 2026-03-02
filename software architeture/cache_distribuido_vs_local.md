# Cache Distribuído vs Cache Local

## Introdução

Cache é uma cópia temporária de dados armazenada em um local mais rápido
para evitar recomputação ou novas consultas externas.

Seu objetivo é: - Reduzir latência - Reduzir carga - Reduzir custo -
Aumentar throughput

Cache não é apenas sobre velocidade. É sobre trade-offs entre
performance e consistência.

------------------------------------------------------------------------

## Cache Local

Cache local vive dentro da própria instância da aplicação.

Exemplos: - Dicionário em memória (Python dict) - LRUCache - Cache em
memória da própria aplicação

Ele está no mesmo processo e na mesma memória, sem rede envolvida.

### Funcionamento

Request → aplicação consulta cache local →\
Se existir → responde\
Se não existir → busca dado externo → salva em memória → responde

Latência extremamente baixa (nanosegundos a microssegundos).

### Vantagens

-   Muito rápido
-   Simples de implementar
-   Sem dependência externa
-   Zero latência de rede
-   Excelente para dados pequenos e leitura frequente

### Problemas

-   Não compartilha estado entre instâncias
-   Escala horizontal ruim
-   Consistência difícil entre múltiplas instâncias
-   Perde dados ao reiniciar

### Quando usar

-   Sistema pequeno
-   Baixa escala
-   Dados quase imutáveis
-   Apenas uma instância
-   Cache interno de cálculo repetitivo

------------------------------------------------------------------------

## Cache Distribuído

Cache distribuído é externo à aplicação e compartilhado por todas as
instâncias.

Exemplos: - Redis - Memcached - Hazelcast

Vive em outro processo ou servidor e é acessado via rede.

### Funcionamento

Request → aplicação → consulta cache distribuído →\
Se existir → responde\
Se não → busca dado → salva no cache → responde

### Vantagens

-   Compartilhamento global
-   Escala horizontalmente
-   Invalidação centralizada
-   Pode persistir dados (dependendo da configuração)

### Problemas

-   Latência de rede
-   Novo ponto de falha
-   Complexidade operacional
-   Custo adicional

------------------------------------------------------------------------

## Comparação

  Aspecto                Cache Local   Cache Distribuído
  ---------------------- ------------- -------------------
  Latência               Muito baixa   Baixa
  Escalabilidade         Ruim          Excelente
  Consistência           Difícil       Melhor
  Complexidade           Baixa         Alta
  Compartilhamento       Não           Sim
  Ponto único de falha   Não           Pode ser

------------------------------------------------------------------------

## Invalidação de Cache

É um dos problemas mais difíceis da computação.

Estratégias: - TTL (Time To Live) - Cache Aside - Write-through -
Write-back - Invalidação por eventos

------------------------------------------------------------------------

## Problemas Avançados

### Cache Stampede

Múltiplas requisições quando cache expira.

Soluções: - Lock - Early refresh - Backoff

### Cache Avalanche

Muitas chaves expiram ao mesmo tempo.

Solução: - TTL aleatório

### Cache Penetration

Consultas repetidas para chaves inexistentes.

Solução: - Cache de valores nulos - Bloom filter

------------------------------------------------------------------------

## Consistência vs Performance

Cache sempre envolve aceitar dados levemente desatualizados em troca de
velocidade e resiliência.

------------------------------------------------------------------------

## Conclusão

Cache local é simples e extremamente rápido, mas não escala
horizontalmente.

Cache distribuído adiciona complexidade e latência, mas permite
compartilhamento global, melhor escalabilidade e controle centralizado.

A escolha depende de: - Escala do sistema - Requisitos de consistência -
Custo operacional aceitável
