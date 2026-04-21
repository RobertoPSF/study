# Event Sourcing (Event Store, Replay, Trade-offs)

## Introdução

Event Sourcing parte de uma mudança de perspectiva que muita gente subestima. Em vez de armazenar apenas o estado atual de uma entidade, você passa a armazenar todos os eventos que levaram a esse estado. O sistema deixa de ser definido pelo “valor atual” e passa a ser definido pela sequência de fatos que aconteceram ao longo do tempo.

Isso não é apenas uma escolha de persistência. É uma mudança de modelo mental. Você deixa de perguntar “qual é o estado agora?” e passa a perguntar “como chegamos até aqui?”.

## O modelo tradicional vs Event Sourcing

No modelo tradicional, você tem algo assim:

```text
Order {
  id: 1
  status: "PAID"
}
```

Você não sabe como esse estado foi alcançado, apenas qual é o resultado final.

Com Event Sourcing, você armazena algo como:

```text
OrderCreated
PaymentAuthorized
PaymentCaptured
```

O estado atual é derivado desses eventos. Ele não é a fonte de verdade, apenas uma projeção.

Isso tem implicações profundas em auditoria, rastreabilidade e flexibilidade.

## Event Store

O Event Store é o componente central dessa arquitetura. Ele é responsável por armazenar eventos de forma imutável e ordenada.

Cada evento representa algo que aconteceu no passado e não pode ser alterado. Se algo precisa ser corrigido, você não modifica o evento antigo, você adiciona um novo evento que representa a correção.

Isso significa que o banco de dados deixa de ser uma coleção de estados mutáveis e passa a ser um log de eventos.

Esse log normalmente é append-only. Você só adiciona novos eventos.

O Event Store precisa garantir:

* ordenação correta dos eventos
* consistência na gravação
* capacidade de leitura sequencial

Ele pode ser implementado com bancos específicos (como EventStoreDB) ou adaptado sobre bancos tradicionais.

## Reconstrução de estado (Replay)

Como o estado não é armazenado diretamente, ele precisa ser reconstruído a partir dos eventos.

Esse processo é chamado de replay.

Você pega todos os eventos de uma entidade e os aplica em ordem para reconstruir o estado atual.

Exemplo conceitual:

```python
state = Order()
for event in events:
    state.apply(event)
```

Esse processo pode ser feito em tempo real ou pode gerar snapshots intermediários para evitar custo alto de reconstrução.

## Snapshots

Snapshots são otimizações.

Em vez de sempre reconstruir o estado desde o primeiro evento, você armazena estados intermediários.

Na prática, você reduz o custo de replay aplicando apenas eventos mais recentes.

Mas isso introduz complexidade adicional, porque agora você precisa manter consistência entre eventos e snapshots.

## Projeções

Event Sourcing raramente existe sozinho. Ele normalmente é combinado com CQRS.

Os eventos gerados no lado de escrita são usados para construir modelos de leitura, chamados de projeções.

Essas projeções podem ser:

* tabelas desnormalizadas
* views otimizadas
* índices específicos

Elas são atualizadas a partir dos eventos, normalmente de forma assíncrona.

Isso reforça o modelo de consistência eventual.

## Benefícios reais

O principal benefício é rastreabilidade completa. Você sabe exatamente tudo que aconteceu no sistema.

Isso é extremamente valioso em domínios como finanças, auditoria e sistemas críticos.

Outro benefício é a capacidade de reconstruir estado em diferentes formas. Você pode criar novas projeções a partir de eventos antigos sem alterar o fluxo de escrita.

Também permite debugging avançado. Você consegue reproduzir cenários aplicando eventos históricos.

## Flexibilidade de evolução

Com Event Sourcing, você pode evoluir o sistema sem perder histórico.

Se você precisa de uma nova visão dos dados, basta reprocessar eventos.

Isso é poderoso, mas também perigoso se você não gerenciar versões de eventos corretamente.

## Versionamento de eventos

Eventos são contratos imutáveis.

Quando o modelo muda, você precisa lidar com versões diferentes de eventos.

Isso pode ser feito com:

* versionamento explícito
* transformações durante replay

Ignorar isso leva a sistemas impossíveis de evoluir.

## Trade-offs reais

Event Sourcing adiciona complexidade significativa.

Você passa a lidar com:

* reconstrução de estado
* versionamento de eventos
* consistência eventual
* múltiplas projeções

Debugging pode ser mais difícil, especialmente sem ferramentas adequadas.

Também há custo cognitivo. Desenvolvedores precisam entender um modelo menos intuitivo.

Outro ponto crítico é performance. Replay de muitos eventos pode ser caro sem otimizações.

## Quando usar

Event Sourcing faz sentido quando:

* histórico completo é crítico
* auditoria é obrigatória
* o domínio é altamente orientado a eventos
* você precisa reconstruir estado de diferentes formas

Se você só precisa armazenar estado atual, isso é overkill.

## O que muda na prática

Você deixa de modelar apenas entidades e passa a modelar eventos como primeira classe.

As regras de negócio passam a gerar eventos, não apenas modificar estado.

O banco deixa de ser fonte de verdade direta e passa a ser um log.

Isso muda profundamente como você pensa o sistema.