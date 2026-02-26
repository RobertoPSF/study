O CAP Theorem (ou Teorema de Brewer) foi proposto por Eric Brewer em 2000 e formalizado depois por Gilbert e Lynch. Ele afirma que, em um sistema distribuído, é impossível garantir simultaneamente três propriedades em presença de falhas de rede: Consistência (Consistency), Disponibilidade (Availability) e Tolerância a Partição (Partition Tolerance). Em qualquer sistema distribuído real, você só pode escolher duas das três.

Primeiro precisamos definir essas três propriedades com precisão técnica, porque quase todo mundo entende errado.

Consistência, no contexto do CAP, não significa “dados corretos” ou “integridade referencial”. Significa que todas as leituras retornam o valor mais recente escrito. Ou seja, após uma escrita bem-sucedida, qualquer leitura subsequente, em qualquer nó do sistema, deve retornar esse valor atualizado. Isso é consistência linearizável (forte).

Disponibilidade significa que todo pedido recebido por um nó não falho deve retornar uma resposta, mesmo que a resposta não contenha o dado mais recente. Não é “alta disponibilidade” percentual; é garantia formal de resposta.

Tolerância a Partição significa que o sistema continua funcionando mesmo que ocorram falhas de comunicação entre partes do cluster — ou seja, a rede pode se dividir em partições isoladas e o sistema deve continuar operando.

Aqui está o ponto central: em sistemas distribuídos reais, partições de rede não são hipótese teórica. Elas acontecem. Timeout, perda de pacote, falha de switch, latência imprevisível — tudo isso é partição. Portanto, em prática, você não escolhe entre CP ou CA. Você escolhe entre CP ou AP, porque P é obrigatório.

Imagine dois nós replicando um banco de dados. O cliente escreve no nó A. Antes que o nó A replique para o nó B, a rede entre eles cai. Agora há uma partição.

Se você optar por Consistência, o nó B deve recusar leituras ou escritas porque ele não tem certeza se possui o valor mais recente. Logo, o sistema sacrifica Disponibilidade. Esse é um sistema CP.

Se você optar por Disponibilidade, o nó B continuará respondendo requisições, mesmo sem ter o valor atualizado. Você sacrifica Consistência. Esse é um sistema AP.

É impossível ter os dois ao mesmo tempo durante uma partição.

Agora vamos aprofundar o que isso significa na prática.

Sistemas CP garantem que você nunca verá dado antigo, mas podem ficar indisponíveis durante falhas de rede. Exemplos clássicos incluem bancos de dados como HBase, MongoDB (em determinadas configurações com majority write concern) e sistemas baseados em consenso como aqueles que usam Raft ou Paxos.

Sistemas AP continuam respondendo mesmo com falhas de rede, mas podem retornar dados inconsistentes temporariamente. Exemplos incluem Cassandra, DynamoDB (em modo eventual) e CouchDB.

Agora uma nuance importante: o CAP Theorem só fala sobre o comportamento durante partições. Fora delas, você pode ter consistência e disponibilidade ao mesmo tempo. Esse é um erro comum — achar que CAP é uma escolha constante. Não é. É uma escolha que se manifesta quando a rede falha.

Outra confusão comum é misturar CAP com ACID. ACID trata de propriedades transacionais dentro de um único sistema, especialmente consistência no sentido de regras de integridade. CAP trata de consistência de leitura em ambiente distribuído. São conceitos diferentes.

Outro ponto avançado: CAP não fala nada sobre latência. Porém, na prática, quanto mais você força consistência forte, maior a latência, porque precisa de coordenação síncrona entre nós. Isso nos leva ao conceito de quorum. Sistemas CP frequentemente usam quorum para decidir se uma operação pode ser considerada válida. Se maioria responde, operação é aceita. Se não, falha.

Agora vamos conectar com engenharia real.

Imagine um sistema de pagamento. Se houver partição, você prefere que o sistema:

- Continue aceitando pagamentos possivelmente duplicados ou inconsistentes?
- Pare temporariamente até garantir estado correto?

Para pagamentos, você escolhe CP. Para feed de rede social, você escolhe AP.

Essa escolha é estratégica. É alinhamento com risco de negócio.

Existe também o conceito de consistência eventual. Em sistemas AP, você aceita que os dados podem divergir temporariamente, mas eventualmente convergem. Isso funciona porque a maioria das aplicações tolera atraso de sincronização.

Agora uma camada mais profunda: CAP é um modelo binário simplificado. Na prática, sistemas modernos trabalham em um espectro. Não é simplesmente CP ou AP; você pode configurar níveis diferentes por operação.

Exemplo: MongoDB permite ajustar write concern e read concern. Cassandra permite configurar consistência por requisição (ONE, QUORUM, ALL). Isso cria flexibilidade para escolher consistência ou disponibilidade dependendo do contexto.

Outro conceito crítico é que partição não significa apenas “cabo cortado”. Latência extrema pode ser indistinguível de falha. Um timeout de 5 segundos pode ser considerado partição lógica.

Também é importante entender que replicação síncrona favorece consistência, enquanto replicação assíncrona favorece disponibilidade.

Existe ainda o teorema PACELC, que estende CAP. Ele diz: se houver Partição (P), você escolhe entre Availability (A) e Consistency (C); Else (E), quando não há partição, você escolhe entre Latency (L) e Consistency (C). Ou seja, mesmo sem falhas, existe trade-off entre latência e consistência. Sistemas que priorizam latência tendem a usar replicação assíncrona.