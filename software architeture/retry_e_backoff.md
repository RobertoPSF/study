# Retry e Backoff --- Aula Completa

## 1. O problema real que o retry tenta resolver

Em sistemas distribuídos, falha não é exceção, é regra.

Quando seu backend chama:

-   outro microserviço\
-   banco remoto\
-   API externa\
-   serviço de pagamento\
-   fila

essa chamada pode falhar por:

-   timeout
-   instabilidade momentânea
-   pico de carga
-   rede intermitente
-   deploy do outro lado
-   DNS lento
-   throttling

Muitas dessas falhas são transientes (temporárias).\
E aqui nasce o retry.

Retry é a decisão de:

> "Se falhou agora, talvez funcione daqui a pouco."

Mas aqui começa o perigo.

------------------------------------------------------------------------

## 2. O que é Retry

Retry é simplesmente repetir uma operação após falha, sob condições
controladas.

Estrutura básica:

    tentar
    se falhar:
        esperar
        tentar novamente

Sem regras claras, retry vira:

-   loop infinito
-   explosão de tráfego
-   efeito cascata
-   DDoS involuntário

Retry não é repetir.\
Retry é repetir com política explícita.

------------------------------------------------------------------------

## 3. Quando usar Retry

Use retry quando a falha for:

-   Intermitente
-   Não determinística
-   Externa ao seu controle

Exemplos bons:

-   Timeout de rede
-   HTTP 503
-   Conexão resetada
-   Erro de DNS temporário

Não use retry quando:

-   Erro 400
-   Falha de validação
-   Credencial inválida
-   Erro lógico
-   Erro determinístico

------------------------------------------------------------------------

## 4. O problema do retry imediato

Imagine milhares de requisições simultâneas.\
Uma API externa cai por 2 segundos.\
Todas falham.\
Todas fazem retry imediato.

Você acabou de criar um **retry storm**.

------------------------------------------------------------------------

# Backoff --- O controle da agressividade

Backoff é a política de espera antes da próxima tentativa.

------------------------------------------------------------------------

## 5. Tipos de Backoff

### Backoff Fixo

Sempre espera o mesmo tempo.

Problema: sincronização de falhas.

### Backoff Linear

Aumenta de forma linear.

Melhor que fixo, mas ainda previsível.

### Backoff Exponencial

Aumenta exponencialmente.

Fórmula:

    delay = base * 2^tentativa

Reduz carga progressivamente.

------------------------------------------------------------------------

## 6. O problema da sincronização

Mesmo exponencial pode sincronizar clientes.

Solução: **Jitter**

------------------------------------------------------------------------

# Jitter --- O caos que salva o sistema

Jitter adiciona aleatoriedade ao tempo de espera.

Exemplo:

    delay = random(0, 8)

Amazon recomenda Exponential Backoff + Jitter.

------------------------------------------------------------------------

# 7. Limites obrigatórios

Retry precisa de:

-   Número máximo de tentativas
-   Tempo máximo total
-   Timeout por requisição

Sem limite → sistema pode travar.

------------------------------------------------------------------------

# 8. Idempotência

Retry só é seguro se a operação for idempotente.

Idempotência significa:

> Executar a mesma operação várias vezes produz o mesmo efeito final.

GET é idempotente.\
POST geralmente não é.

Cuidado com duplicação de efeitos.

------------------------------------------------------------------------

# 9. Retry na arquitetura

Retry pode existir:

-   No client HTTP
-   No service
-   No gateway

Nunca implemente retry em todas as camadas.

Isso causa **retry amplification**.

------------------------------------------------------------------------

# 10. Retry + Circuit Breaker

Retry tenta de novo.\
Circuit Breaker para de tentar quando já está falhando demais.

Essa combinação protege o sistema.

------------------------------------------------------------------------

# 11. Trade-offs

Retry melhora:

-   Disponibilidade
-   Robustez

Mas piora:

-   Latência
-   Uso de recursos
-   Complexidade

Sempre há troca entre tempo de resposta e probabilidade de sucesso.

------------------------------------------------------------------------

# 12. Quando NÃO usar retry

-   Operações não idempotentes
-   Erros lógicos
-   Falhas previsíveis

Retry é ferramenta cirúrgica.

------------------------------------------------------------------------

# 13. Como explicar em entrevista

Resposta madura:

> "Aplicaria retry apenas em falhas transientes, com limite de
> tentativas, timeout por requisição e exponential backoff com jitter.
> Garantiria idempotência antes de permitir retry e avaliaria circuit
> breaker para evitar amplification."

------------------------------------------------------------------------

# 14. Aplicação no projeto

No projeto da API agregadora:

-   Timeout de 2s
-   Máximo 3 tentativas
-   Exponential backoff com jitter
-   Logs por tentativa
-   Fallback se todas falharem

------------------------------------------------------------------------

# 15. Erros clássicos

-   Retry infinito
-   Sem limite
-   Sem timeout
-   Retry para erro 400
-   Retry em múltiplas camadas
-   Sem jitter

Evitar isso já coloca você acima da média.
