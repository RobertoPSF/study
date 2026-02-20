# Aula Completa -- Observabilidade

Observabilidade não é sobre logs. Não é sobre monitoramento. Não é sobre
dashboards bonitos. Observabilidade é a capacidade de entender o que
está acontecendo dentro de um sistema apenas olhando suas saídas
externas. Em termos simples: se algo quebrar às 3h da manhã, você
consegue descobrir o motivo sem precisar "adivinhar"?

Monitoramento responde perguntas conhecidas. Observabilidade permite
responder perguntas que você ainda não sabe que precisa fazer.

Essa distinção é crítica. Monitoramento tradicional funciona com
métricas fixas e alertas pré-definidos. Exemplo: CPU acima de 80%. Isso
é útil, mas limitado. Se o problema não estiver previsto no alerta, você
fica cego. Observabilidade moderna permite investigar sistemas
complexos, especialmente distribuídos, onde falhas não são lineares e
causas não são óbvias.

Em sistemas backend modernos --- especialmente quando você tem chamadas
externas, cache, retries, filas --- a complexidade aumenta rapidamente.
Quanto mais serviços interagem, mais difícil se torna responder
perguntas como: "por que essa requisição demorou 4 segundos?" ou "por
que só alguns usuários estão recebendo erro?"

Observabilidade se sustenta em três pilares clássicos: logs, métricas e
traces.

Logs são registros detalhados de eventos que aconteceram no sistema. São
ricos em contexto, mas pobres em agregação. Você consegue saber
exatamente o que aconteceu, mas precisa procurar. Logs são ótimos para
investigar casos específicos.

Métricas são dados numéricos agregados ao longo do tempo. Elas são
eficientes para detectar padrões e anomalias. Exemplos: número de
requisições por segundo, tempo médio de resposta, taxa de erro. Métricas
são leves, rápidas e boas para alertas.

Traces (ou tracing distribuído) acompanham o caminho de uma requisição
ao longo de múltiplos serviços. Eles respondem a pergunta: "por onde
essa requisição passou e quanto tempo gastou em cada etapa?" Em
arquiteturas distribuídas, isso é essencial.

Esses três pilares não competem. Eles se complementam.

## Aplicação no Projeto

Imagine que seu endpoint chama duas APIs externas. Às vezes a resposta
demora. Às vezes falha. Às vezes o cache entra em ação. Como você sabe o
que aconteceu em cada requisição?

Sem observabilidade adequada, você só verá: "demorou". Com
observabilidade, você verá: "a API A demorou 1.8s, a API B falhou com
timeout, ativamos retry, o cache foi usado, tempo total 2.4s".

Isso é maturidade técnica.

## Logs Estruturados

Logs devem ser estruturados (chave-valor), por exemplo:

-   level=error\
-   service=aggregator\
-   endpoint=/aggregate\
-   external_service=sourceA\
-   status=timeout\
-   duration_ms=2100

Logs estruturados podem ser filtrados e analisados automaticamente.

É essencial incluir um **correlation ID (request ID)** em toda
requisição para rastrear ponta a ponta.

## Métricas Importantes

-   Latência (tempo de resposta)
-   Throughput (requisições por segundo)
-   Taxa de erro
-   Tempo de chamada externa
-   Cache hit/miss

Use percentis (p95, p99), não apenas média.

## Tracing Distribuído

Tracing acompanha o caminho completo da requisição entre serviços. Em
projetos maiores, ferramentas como OpenTelemetry são usadas.

## Golden Signals (Google SRE)

-   Latência
-   Tráfego
-   Erros
-   Saturação

Esses quatro sinais cobrem a maioria dos problemas operacionais.

## Cardinalidade

Evite métricas com labels de alta cardinalidade (ex: user_id). Isso pode
comprometer performance do sistema de métricas.

## SLO (Service Level Objective)

Exemplo: 99% das requisições devem responder em até 300ms.

Sem SLO, métricas são apenas números.

## Alertas

Alertas devem ser acionáveis e evitar fadiga. Exemplo melhor: "Taxa de
erro acima de 5% por 5 minutos"

## Aplicação Prática no Seu Projeto

Você deve implementar:

1.  Logs estruturados
2.  Request ID por requisição
3.  Logs de início/fim de requisição
4.  Logs de chamadas externas e retries
5.  Métricas de latência total e por dependência
6.  Taxa de erro
7.  Cache hit/miss

## Resumo Mental

Observabilidade é capacidade investigativa.

-   Logs mostram eventos\
-   Métricas mostram tendências\
-   Traces mostram fluxo\
-   SLOs dão contexto\
-   Alertas devem ser acionáveis\
-   Cardinalidade precisa controle\
-   Correlation ID é obrigatório

Pergunta para reflexão:

Se sua API começar a responder lentamente apenas para 3% das
requisições, qual métrica você analisaria primeiro e por quê?
