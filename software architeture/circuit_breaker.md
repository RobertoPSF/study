# Circuit Breaker --- Entendendo de Verdade

Circuit breaker é um padrão de resiliência usado para evitar que falhas
em serviços externos derrubem o seu sistema.

Ele existe para responder a uma pergunta muito simples:

> O que acontece com meu backend quando uma dependência começa a falhar
> lentamente?

Se sua resposta for "ele espera até dar timeout", você tem um problema
sério.

------------------------------------------------------------------------

## O problema que ele resolve

Imagine seu endpoint chamando um serviço externo que começa a: -
responder lentamente - retornar erro 500 - ou parar completamente

Sem proteção: 1. Threads ficam ocupadas esperando timeout 2. Pool de
conexões esgota 3. Latência explode 4. Seu sistema cai junto

Isso se chama falha em cascata.

O circuit breaker existe para cortar essa cascata.

------------------------------------------------------------------------

## A analogia elétrica

Funciona como um disjuntor elétrico.

Quando há sobrecarga: - o disjuntor desarma - a corrente é
interrompida - o sistema é protegido

No software: - quando muitas falhas acontecem - o circuito abre - você
para de chamar o serviço externo - responde imediatamente com fallback

------------------------------------------------------------------------

## Os três estados

### Closed (Fechado)

Estado normal. As chamadas passam e o sistema monitora falhas.

### Open (Aberto)

Nenhuma chamada externa é feita. Responde com fallback ou erro imediato.

### Half-Open (Meio-aberto)

Após um tempo, o sistema permite chamadas de teste. Se funcionar →
fecha. Se falhar → abre novamente.

------------------------------------------------------------------------

## Componentes importantes

### Failure threshold

Quantidade de falhas para abrir o circuito.

### Timeout duration

Tempo que o circuito permanece aberto antes de testar novamente.

### Sliding window

Janela de tempo ou número de requisições para medir taxa de erro.

------------------------------------------------------------------------

## Relação com Retry

Retry tenta novamente. Circuit breaker decide quando parar de tentar.

Ordem correta: 1. Timeout 2. Retry com backoff 3. Circuit breaker

------------------------------------------------------------------------

## Trade-offs

Abrir o circuito pode significar: - dados desatualizados - resposta
parcial - erro controlado

Você troca consistência perfeita por disponibilidade controlada.

------------------------------------------------------------------------

## Erros comuns

-   Contador simples que nunca reseta
-   Abrir circuito para qualquer erro
-   Não diferenciar erro 4xx de 5xx
-   Não logar estado do breaker

------------------------------------------------------------------------

## Quando usar

Use quando: - Dependência externa é instável - Latência variável -
Serviço crítico - Alto volume de requisições

------------------------------------------------------------------------

## Aplicação prática

Fluxo típico: 1. Requisição chega 2. Verifica estado do breaker 3. Se
Open → fallback 4. Se Closed → chama serviço 5. Atualiza métricas 6. Se
threshold ultrapassado → Open

------------------------------------------------------------------------

## Como explicar em entrevista

"Implementei circuit breaker para evitar falha em cascata quando
dependências externas apresentavam alta taxa de erro ou latência. O
breaker abre após threshold configurado em janela deslizante e permanece
aberto por período definido antes de permitir chamadas de teste em
half-open, garantindo fail-fast e preservação de recursos."
