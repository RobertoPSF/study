# Data Modeling Moderno (OLTP vs OLAP, Desnormalização)

## Introdução

Modelagem de dados moderna começa com uma decisão que muita gente evita enfrentar: você está otimizando para transações ou para análise? OLTP e OLAP têm objetivos diferentes, padrões de acesso diferentes e, consequentemente, modelos de dados diferentes. Tentar usar o mesmo desenho para ambos é uma das causas mais comuns de sistemas lentos, complexos e difíceis de evoluir.

A abordagem madura não é escolher um “melhor modelo”, mas aceitar que você provavelmente precisará de mais de um, cada um otimizado para um tipo de uso.

## OLTP (Online Transaction Processing)

OLTP é o modelo clássico de sistemas operacionais. Ele é otimizado para escrita frequente, consistência e integridade de dados. Aqui você está lidando com operações como criar pedidos, atualizar saldo, registrar pagamentos.

Nesse contexto, o modelo tende a ser normalizado. A normalização reduz redundância, evita inconsistências e facilita garantir invariantes do domínio. Você quebra dados em múltiplas tabelas relacionadas e usa chaves estrangeiras para manter integridade.

Esse desenho funciona bem para escrita porque evita duplicação e mantém uma única fonte de verdade. No entanto, ele cobra um preço em leitura. Queries começam a exigir múltiplos joins, e isso escala mal quando o volume cresce.

OLTP é sobre garantir que o dado esteja correto no momento da escrita.

## OLAP (Online Analytical Processing)

OLAP é otimizado para leitura, especialmente leitura pesada e agregada. Aqui você está respondendo perguntas como relatórios, dashboards, análises históricas e métricas de negócio.

Nesse cenário, normalização se torna um problema. Queries com múltiplos joins ficam lentas e complexas. O modelo OLAP tende a ser desnormalizado, muitas vezes organizado em formatos como star schema ou wide tables.

Você duplica dados intencionalmente para tornar consultas mais simples e rápidas. Em vez de montar uma resposta com vários joins, você já tem os dados pré-combinados.

OLAP é sobre responder perguntas rapidamente, mesmo que isso custe mais espaço e complexidade na ingestão.

## A tensão entre OLTP e OLAP

O conflito entre OLTP e OLAP é inevitável. Um quer consistência e escrita eficiente, o outro quer leitura rápida e agregação simples.

Se você tenta usar um banco OLTP para analytics pesado, você sobrecarrega o sistema operacional. Se tenta usar um modelo OLAP para transações, você perde integridade e controle.

A solução moderna é separar esses mundos.

## Separação de responsabilidades

Sistemas maduros normalmente possuem:

* um banco OLTP para operações transacionais
* um sistema OLAP para análise

Os dados fluem do OLTP para o OLAP através de pipelines, como ETL ou streaming.

Isso permite otimizar cada lado de forma independente.

O OLTP continua consistente e seguro.
O OLAP se torna rápido e flexível para análise.

Essa separação conversa diretamente com conceitos como CQRS, onde leitura e escrita também são tratadas separadamente.

## Desnormalização

Desnormalização é frequentemente mal interpretada. Não é “fazer bagunça”, é uma decisão consciente de duplicar dados para otimizar leitura.

No mundo OLAP, isso é padrão. Você pré-calcula, agrega e armazena dados de forma redundante para evitar custo em tempo de query.

Mesmo em sistemas OLTP, desnormalização pode aparecer de forma controlada. Por exemplo, armazenar um campo derivado para evitar joins frequentes.

O ponto crítico é saber onde aplicar.

Desnormalização sem controle leva a inconsistência.
Desnormalização bem aplicada reduz latência e simplifica queries.

## Modelagem orientada a acesso

Modelagem moderna não começa pelo “modelo ideal”. Começa pelos padrões de acesso.

Você precisa saber:

* quais queries são críticas
* qual é o volume de leitura vs escrita
* quais são os SLAs de latência

A partir disso, você decide o formato dos dados.

Isso é especialmente importante em bancos NoSQL, onde você modela dados baseado em como eles serão consumidos, não apenas em relações.

## Trade-offs reais

Normalização melhora integridade, mas piora leitura.
Desnormalização melhora leitura, mas aumenta risco de inconsistência.

Separar OLTP e OLAP melhora performance geral, mas aumenta complexidade operacional.

Manter múltiplos modelos exige pipelines de dados confiáveis.

Ignorar esses trade-offs leva a sistemas que parecem simples no início, mas se tornam caros de manter e escalar.

## Quando aplicar cada abordagem

Se o sistema é pequeno e o volume é baixo, um único banco relacional bem modelado resolve.

À medida que leitura analítica cresce, faz sentido introduzir um modelo OLAP separado.

Desnormalização deve ser aplicada quando há necessidade clara de performance em leitura, não por hábito.

Se você não sabe quais queries precisa otimizar, ainda não está no momento de desnormalizar agressivamente.

## O que muda na prática

Você deixa de pensar em “um banco que resolve tudo” e passa a pensar em fluxos de dados.

Dados são escritos em um lugar, transformados e consumidos em outro.

Modelos deixam de ser únicos e passam a ser especializados.

Isso exige mais engenharia, mas reduz acoplamento e melhora performance em escala.
