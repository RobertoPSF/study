# Escalar Leitura vs Escrita

## Introdução

Quase todo sistema enfrenta a pergunta: o gargalo está na leitura ou na
escrita?

Leitura e escrita possuem comportamentos físicos diferentes:

-   Leitura pode ser replicada.
-   Escrita precisa manter integridade.
-   Leitura tolera atraso.
-   Escrita não tolera inconsistência silenciosa.

Se você não entende isso, toma decisões arquiteturais erradas.

------------------------------------------------------------------------

## Padrão de Carga: Read-heavy vs Write-heavy

### Sistemas Read-heavy

Exemplos: - Feed de redes sociais - Catálogo de e-commerce - Portal de
notícias - APIs públicas

Normalmente: - 90% leitura - 10% escrita

### Sistemas Write-heavy

Exemplos: - Sistema de logs - Telemetria - Plataforma de eventos - Chat
em tempo real

Aqui a escrita é o gargalo.

Sem medir padrão de carga, você está arquitetando no escuro.

------------------------------------------------------------------------

# Escalando Leitura

Escalar leitura é mais simples porque leitura pode ser distribuída.

## 1. Read Replicas

Banco principal recebe escrita. Réplicas recebem cópia assíncrona e
respondem leitura.

Arquitetura típica:

Master → Réplicas

Vantagem: - Escala leitura quase linearmente.

Problema: - Replication lag. - Possível inconsistência temporária.

Consistência eventual pode ser aceitável dependendo do domínio.

------------------------------------------------------------------------

## 2. Cache

Ferramenta mais poderosa para escalar leitura.

Tipos: - Cache local (memória da aplicação) - Cache distribuído
(Redis) - CDN (nível HTTP)

Problemas: - Invalidação é difícil. - Pode servir dado desatualizado. -
Pode mascarar problema de modelagem.

Cache é otimização, não solução para design ruim.

------------------------------------------------------------------------

## 3. Índices

Antes de escalar horizontalmente: - Verifique queries. - Crie índices
corretos. - Analise plano de execução.

Muitas vezes o gargalo não é infraestrutura, é query mal feita.

------------------------------------------------------------------------

## 4. CQRS

Separar modelo de leitura do modelo de escrita.

Escrita: - Normalizada - Consistência forte

Leitura: - Denormalizada - Otimizada para consulta

Permite escalabilidade independente, mas aumenta complexidade.

------------------------------------------------------------------------

# Escalando Escrita

Escrita envolve: - Locks - Transações - Ordem - Consistência

Você não pode simplesmente replicar escrita como leitura.

------------------------------------------------------------------------

## 1. Escala Vertical

Mais CPU, mais memória, mais IOPS.

Simples, mas possui limite físico.

------------------------------------------------------------------------

## 2. Sharding

Dividir dados por chave.

Exemplo: Usuários A--M → Shard 1\
Usuários N--Z → Shard 2

Vantagens: - Distribui carga de escrita.

Problemas: - Consultas cruzadas complexas. - Transações distribuídas
difíceis. - Rebalanceamento caro.

Sharding aumenta complexidade operacional.

------------------------------------------------------------------------

## 3. Particionamento Interno

Partition by range ou hash.

Reduz contenção e melhora throughput.

------------------------------------------------------------------------

## 4. Append-only / Event Sourcing

Ao invés de atualizar estado, apenas adiciona eventos.

Exemplo: Registrar transações ao invés de atualizar saldo.

Vantagens: - Reduz lock. - Melhora throughput.

Desvantagem: - Leitura fica mais complexa.

------------------------------------------------------------------------

## 5. Filas

Fluxo:

Cliente → API → Fila → Worker → Banco

Vantagens: - Absorve pico. - Controla taxa de escrita.

Desvantagens: - Introduz consistência eventual. - Aumenta complexidade.

------------------------------------------------------------------------

# Consistência vs Escalabilidade

Relaciona-se ao CAP Theorem:

-   Consistência
-   Disponibilidade
-   Tolerância a partição

Não é possível maximizar os três simultaneamente.

Leitura tolera consistência eventual. Escrita normalmente exige
consistência forte.

------------------------------------------------------------------------

# Aplicação prática

Sistemas com 95% leitura: - Read replicas - Cache - Índices - CDN

Sistemas com 95% escrita: - Medir gargalo - Otimizar lock e transações -
Particionamento - Filas - Event sourcing quando necessário

------------------------------------------------------------------------

# Conclusão

Escalar leitura é problema de distribuição. Escalar escrita é problema
de coordenação.

Distribuição é relativamente simples. Coordenação exige controle
rigoroso de consistência e transações.
