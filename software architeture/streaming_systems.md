# Streaming Systems (Kafka: Partitions, Ordering, Guarantees)

## Introdução

Streaming systems existem porque o modelo tradicional de request/response e processamento em batch não escala bem quando você precisa reagir a eventos em tempo quase real. Em vez de tratar dados como algo que você consulta pontualmente, você passa a tratá-los como um fluxo contínuo.

Nesse contexto, Apache Kafka se tornou o padrão de fato não por ser “rápido”, mas por oferecer um modelo consistente de log distribuído, capaz de lidar com alto throughput, retenção de eventos e consumo desacoplado.

Para usar Kafka corretamente, você precisa entender três conceitos que definem quase todo o comportamento do sistema: partitions, ordering e delivery guarantees. Se você não entende esses três, você está operando Kafka no escuro.

## Modelo mental do Kafka

Kafka não é uma fila tradicional. Ele é um log distribuído e particionado.

Você escreve eventos em um tópico, e esse tópico é dividido em partições. Cada partição é um log ordenado e imutável. Consumidores leem esse log avançando um offset.

Esse detalhe muda tudo. Em vez de “consumir e remover”, você “consome e avança”. O dado continua lá por um período de retenção configurado.

Isso permite múltiplos consumidores independentes, replay e processamento desacoplado.

## Partitions

Partições são o mecanismo central de escalabilidade do Kafka.

Um tópico é dividido em múltiplas partições, e cada partição pode ser distribuída entre diferentes brokers. Isso permite paralelismo tanto na escrita quanto na leitura.

Quando você produz um evento, o Kafka precisa decidir em qual partição ele será escrito. Isso pode ser feito de forma round-robin ou baseado em uma chave.

A escolha da chave é crítica. Eventos com a mesma chave sempre vão para a mesma partição. Isso garante ordem local para aquela chave.

Se você não define uma chave, você perde controle sobre onde os eventos vão parar, o que pode quebrar requisitos de ordenação.

Por outro lado, usar uma chave ruim pode gerar hotspot em uma única partição, limitando throughput.

Esse é um trade-off inevitável entre paralelismo e ordenação.

## Ordering

Kafka garante ordenação apenas dentro de uma partição.

Isso é um ponto que muita gente ignora e depois descobre da pior forma.

Se você tem múltiplas partições, não existe ordem global garantida entre elas.

Exemplo: eventos A e B podem ser produzidos nessa ordem, mas se forem para partições diferentes, consumidores podem ver B antes de A.

Se seu domínio exige ordenação, você precisa modelar isso explicitamente através da chave de partição.

Na prática, isso significa que você define o que precisa ser ordenado. Normalmente isso é por entidade, como user_id, order_id ou account_id.

Você não tenta ordenar o sistema inteiro, você ordena dentro de um contexto específico.

## Consumer Groups

Consumer groups permitem escalar leitura.

Cada partição é consumida por apenas um consumidor dentro de um grupo. Isso garante que eventos não sejam processados em paralelo dentro da mesma partição, preservando ordenação.

Se você adiciona mais consumidores do que partições, alguns ficam ociosos.

Se você adiciona mais partições, você aumenta paralelismo.

Isso cria uma relação direta entre número de partições e capacidade de escala.

## Delivery Guarantees

Kafka oferece três tipos principais de garantia de entrega.

At-most-once significa que mensagens podem ser perdidas, mas nunca duplicadas. Isso acontece quando você confirma o consumo antes de processar.

At-least-once significa que mensagens nunca são perdidas, mas podem ser processadas mais de uma vez. Esse é o padrão mais comum.

Exactly-once é mais complexo. Kafka oferece mecanismos para isso, mas apenas dentro de certos limites e com custo adicional.

O ponto crítico é entender que “exactly-once” raramente é global. Normalmente ele é garantido dentro de um pipeline controlado.

Na prática, a maioria dos sistemas usa at-least-once e resolve duplicação na aplicação com idempotência.

## Offsets

Offsets representam a posição de leitura dentro de uma partição.

Consumidores controlam offsets para saber onde estão no log.

Você pode commitar offsets automaticamente ou manualmente.

Esse controle define o comportamento de entrega. Se você commita antes de processar, pode perder mensagens. Se commita depois, pode duplicar.

Novamente, isso é um trade-off.

## Retenção e Replay

Kafka mantém eventos por um período configurado, independentemente de terem sido consumidos.

Isso permite replay. Você pode reprocessar eventos desde o início ou de um ponto específico.

Isso é extremamente poderoso para:

* reconstruir estado
* corrigir bugs
* criar novas projeções

Mas exige cuidado. Reprocessar eventos pode gerar efeitos colaterais se sua aplicação não for idempotente.

## Trade-offs reais

Kafka resolve problemas de escala e desacoplamento, mas adiciona complexidade.

Você precisa lidar com:

* ordenação parcial
* duplicação de eventos
* consistência eventual
* gerenciamento de offsets

Debugging também muda. Problemas podem estar em produção, consumo ou na forma como offsets são gerenciados.

Outro ponto crítico é modelagem de eventos. Eventos mal definidos tornam o sistema difícil de evoluir.

## Quando usar

Kafka faz sentido quando você precisa de:

* alto throughput
* processamento assíncrono
* múltiplos consumidores independentes
* integração entre serviços

Se você só precisa de comunicação simples entre poucos serviços, Kafka pode ser exagero.

## O que muda na prática

Você deixa de pensar em chamadas síncronas e passa a pensar em fluxos de eventos.

Serviços deixam de depender diretamente uns dos outros e passam a reagir a eventos.

Isso aumenta desacoplamento, mas exige disciplina em modelagem e operação.
