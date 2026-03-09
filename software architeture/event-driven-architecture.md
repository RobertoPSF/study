# Event-Driven Architecture (EDA) --- Explicação Completa

Event-Driven Architecture (EDA) é um modelo de arquitetura de software
em que sistemas se comunicam e reagem a acontecimentos chamados eventos.
Um evento representa algo que já ocorreu no sistema, ou seja, uma
mudança de estado relevante. Exemplos comuns de eventos incluem
situações como um usuário ter sido registrado, um pedido ter sido
criado, um pagamento ter sido aprovado ou um produto ter ficado sem
estoque. A ideia central é que, em vez de um serviço chamar diretamente
outro serviço para executar uma ação, ele publica um evento informando
que algo aconteceu. Outros serviços que tenham interesse nesse evento
podem reagir a ele de forma independente.

Essa abordagem é diferente da arquitetura tradicional baseada em
requisição e resposta. Em sistemas tradicionais, um serviço chama
diretamente outro serviço, que por sua vez pode chamar um terceiro,
criando cadeias de dependência. Isso aumenta o acoplamento entre
componentes, aumenta a latência acumulada das chamadas e pode provocar
falhas em cascata quando um serviço intermediário falha. Já na
arquitetura orientada a eventos, um serviço publica um evento em um
barramento ou broker de eventos e não precisa conhecer os consumidores
desse evento. Os serviços interessados simplesmente se inscrevem para
receber determinados tipos de eventos e executam suas próprias ações
quando eles ocorrem.

Uma arquitetura orientada a eventos normalmente possui três componentes
principais: produtores de eventos, um broker ou barramento de eventos, e
consumidores de eventos. O produtor é o componente responsável por gerar
o evento. Por exemplo, um serviço de pedidos pode publicar um evento
chamado OrderCreated quando um novo pedido é criado. Esse evento é
enviado para um sistema intermediário chamado event broker ou event bus,
cuja função é receber eventos e distribuí‑los para os serviços
interessados. Entre as tecnologias mais usadas para esse papel estão
Apache Kafka, RabbitMQ, Google Pub/Sub, AWS SNS, AWS EventBridge e NATS.
Os consumidores são os serviços que recebem e processam os eventos. Um
único evento pode ser consumido por vários serviços diferentes, como um
serviço de e‑mail, um serviço de analytics, um serviço de estoque ou um
sistema de recomendação.

Um exemplo simples ajuda a entender esse fluxo. Imagine que um usuário
cria um pedido em uma loja online. O serviço de pedidos salva o pedido
no banco de dados e publica um evento chamado OrderCreated. Esse evento
é enviado para um broker de eventos. A partir desse ponto, diversos
serviços podem reagir a ele: um serviço de pagamento pode iniciar o
processo de cobrança, um serviço de e‑mail pode enviar uma confirmação
ao cliente, um serviço de analytics pode registrar o evento para análise
de dados e um serviço de estoque pode reservar os itens comprados. Todos
esses processos acontecem de forma desacoplada, permitindo que cada
serviço evolua independentemente.

Eventos podem ser classificados em diferentes categorias. Os chamados
domain events representam acontecimentos importantes do domínio de
negócio, como OrderCreated, UserRegistered ou PaymentConfirmed. Já os
integration events são usados para comunicação entre sistemas
diferentes, por exemplo quando um sistema externo precisa ser informado
de uma mudança de dados. Também existem eventos de sistema, que
representam ocorrências técnicas internas, como inicialização de um
serviço ou invalidação de cache.

Outro aspecto importante da arquitetura orientada a eventos é o modelo
de entrega das mensagens. Em alguns sistemas, um evento pode ser
entregue no máximo uma vez, o que significa que ele pode ser perdido
caso ocorra algum erro. Em outros casos, o modelo garante que o evento
será entregue pelo menos uma vez, mas pode ser entregue mais de uma vez.
Esse é o modelo mais comum em sistemas distribuídos, pois é mais simples
de garantir. Para lidar com isso, os consumidores precisam ser
idempotentes, ou seja, capazes de processar o mesmo evento repetidas
vezes sem causar efeitos duplicados. Existe também o modelo chamado
exactly once, em que o sistema tenta garantir que cada evento será
processado exatamente uma vez, mas isso é muito mais difícil de
implementar corretamente em ambientes distribuídos.

Para garantir idempotência, muitos sistemas armazenam identificadores
únicos de eventos que já foram processados. Antes de executar a lógica
de negócio, o consumidor verifica se aquele evento já foi tratado
anteriormente. Se o identificador já estiver registrado, o evento é
ignorado. Isso evita problemas como duplicação de pedidos, pagamentos
repetidos ou envio múltiplo de notificações.

Eventos também precisam ter uma estrutura bem definida, chamada de
schema. Normalmente um evento contém campos como um identificador único
do evento, o tipo do evento, o timestamp indicando quando ele ocorreu, a
versão do evento e um payload com os dados relevantes. Definir um schema
consistente é importante porque diferentes serviços dependerão dessa
estrutura para processar corretamente os eventos.

Com o tempo, o schema de um evento pode evoluir. Novos campos podem ser
adicionados ou alguns podem deixar de existir. Por isso, estratégias de
versionamento de eventos são necessárias. Uma abordagem comum é incluir
um campo de versão no próprio evento. Outra possibilidade é versionar o
próprio tópico ou canal de eventos, criando versões como
order.created.v1 ou order.created.v2. Em sistemas maiores, é comum usar
ferramentas de schema registry para controlar a evolução desses formatos
de dados, utilizando tecnologias como Avro ou Protobuf.

A arquitetura orientada a eventos frequentemente aparece associada ao
padrão chamado Event Sourcing. Nesse modelo, em vez de armazenar apenas
o estado atual de uma entidade no banco de dados, o sistema registra
todos os eventos que levaram àquele estado. Por exemplo, uma conta
bancária pode ser representada por uma sequência de eventos como
AccountOpened, MoneyDeposited e MoneyWithdrawn. O saldo da conta pode
ser reconstruído a qualquer momento aplicando todos os eventos em ordem.
Isso oferece vantagens como histórico completo e auditabilidade, além da
possibilidade de reproduzir eventos passados para reconstruir sistemas
derivados.

Essa capacidade de reproduzir eventos é chamada de event replay. Se
todos os eventos forem armazenados em um log persistente, um sistema
pode processá‑los novamente para reconstruir índices de busca,
recomputar métricas ou atualizar caches. Tecnologias como Kafka são
particularmente eficientes nesse tipo de operação, pois tratam eventos
como um log imutável que pode ser percorrido novamente quando
necessário.

Outro conceito importante é o de event streaming. Em vez de tratar
eventos apenas como mensagens isoladas, eles podem ser vistos como
fluxos contínuos de dados. Ferramentas de processamento de stream, como
Kafka Streams, Apache Flink ou Apache Spark Streaming, permitem analisar
e transformar esses fluxos em tempo real. Isso possibilita construir
aplicações de análise em tempo real, detecção de fraude, monitoramento
de métricas ou agregações baseadas em janelas de tempo.

Diversos padrões arquiteturais surgem nesse contexto. O padrão
publish‑subscribe permite que múltiplos consumidores recebam eventos
publicados por um produtor. O padrão event notification consiste em
publicar um evento apenas para informar que algo mudou, deixando que os
consumidores consultem os dados adicionais se necessário. Já no padrão
event‑carried state transfer, o próprio evento carrega os dados
necessários para o processamento, reduzindo a necessidade de chamadas
adicionais. Também existe o padrão competing consumers, em que vários
workers consomem mensagens de uma mesma fila para processar tarefas em
paralelo. Outro padrão frequentemente utilizado é o CQRS, que separa o
modelo de escrita do modelo de leitura, permitindo que eventos atualizem
visões otimizadas para consulta.

Entre as tecnologias mais usadas para implementar EDA, Apache Kafka é
frequentemente considerado o padrão da indústria para sistemas de alto
throughput, oferecendo um log distribuído com retenção de eventos e
capacidade de replay. RabbitMQ é bastante usado para filas de tarefas e
processamento assíncrono tradicional. Em ambientes de nuvem, serviços
gerenciados como AWS SNS, SQS, EventBridge ou Kinesis também são
amplamente utilizados.

Apesar de suas vantagens, a arquitetura orientada a eventos também traz
desafios significativos. Um deles é a dificuldade de depuração, pois os
fluxos deixam de ser lineares e passam a envolver múltiplos serviços
reagindo a eventos. Ferramentas de observabilidade e tracing
distribuído, como OpenTelemetry, Jaeger ou Zipkin, tornam‑se essenciais
para entender o fluxo completo de processamento. Outro problema possível
é o chamado event storm, em que um evento dispara vários outros eventos
em cascata, criando um sistema difícil de controlar. A evolução de
schemas também pode causar problemas se mudanças não forem feitas de
forma compatível com consumidores existentes.

Além disso, muitos sistemas baseados em eventos trabalham com
consistência eventual. Isso significa que diferentes partes do sistema
podem levar algum tempo para refletir a mesma informação. Por exemplo,
um pedido pode ter sido criado, mas o serviço de estoque ainda não
processou o evento correspondente. Esse tipo de comportamento precisa
ser considerado no design da aplicação.

Por essas razões, EDA não é sempre a melhor escolha. Sistemas simples
com poucos serviços e requisitos de consistência forte podem ser mais
bem atendidos por arquiteturas tradicionais. Entretanto, quando há
muitos serviços, alto volume de dados e necessidade de processamento
assíncrono, a arquitetura orientada a eventos se torna extremamente
poderosa.

Grandes empresas de tecnologia utilizam intensivamente esse modelo.
Plataformas de streaming como Netflix processam eventos de reprodução
para alimentar sistemas de recomendação e analytics. Empresas como Uber
utilizam eventos para coordenar estados de corridas, pagamentos e
notificações. Sistemas de comércio eletrônico como os da Amazon também
utilizam eventos para gerenciar pedidos, pagamentos, envios e
atualizações de inventário.

Em sistemas distribuídos complexos, também é comum o uso do padrão Saga
para coordenar transações entre múltiplos serviços. Em vez de uma única
transação distribuída, uma sequência de eventos coordena as etapas do
processo. Por exemplo, a criação de um pedido pode gerar um evento que
inicia o pagamento. Quando o pagamento é confirmado, outro evento
reserva o estoque. Se alguma etapa falhar, eventos compensatórios podem
desfazer ações anteriores.

No fim das contas, Event‑Driven Architecture representa mais do que
apenas um padrão técnico. Ela muda a forma como os sistemas são
projetados. Em vez de um fluxo centralizado de chamadas, temos múltiplos
componentes reagindo a acontecimentos distribuídos. Essa abordagem
permite construir sistemas altamente escaláveis e resilientes, capazes
de processar grandes volumes de dados em tempo real, mas também exige
maior maturidade em design de sistemas distribuídos, observabilidade e
gerenciamento de complexidade.
