# Data Lakes vs Data Warehouses vs Lakehouse

## Introdução

Quando sistemas começam a produzir grandes volumes de dados, surge uma pergunta inevitável: onde e como armazenar esses dados para extrair valor? Data Lakes, Data Warehouses e Lakehouses são três respostas diferentes para esse problema, cada uma com premissas distintas.

A confusão comum é tratá-los como alternativas diretas, quando na prática eles representam evoluções e tentativas de resolver limitações uns dos outros. Para entender bem, você precisa olhar para o tipo de dado, o tipo de uso e o nível de governança necessário.

## Data Warehouse

O Data Warehouse é a abordagem mais tradicional para análise de dados. Ele foi projetado para armazenar dados estruturados, organizados e limpos, prontos para consulta.

Antes de chegar ao warehouse, os dados passam por processos de transformação, normalmente ETL (Extract, Transform, Load). Isso significa que os dados são estruturados antes de serem armazenados.

O resultado é um ambiente altamente confiável para análise. Queries são rápidas, consistentes e baseadas em um modelo bem definido.

O problema é rigidez. Qualquer mudança no esquema exige trabalho de transformação. Além disso, ele não lida bem com dados não estruturados, como logs brutos, arquivos ou eventos complexos.

## Data Lake

O Data Lake surge como resposta à rigidez do warehouse. Em vez de transformar dados antes de armazenar, você armazena dados brutos, no formato original.

Aqui o modelo é “schema-on-read”. Você define a estrutura apenas quando vai consumir o dado, não quando armazena.

Isso permite armazenar qualquer tipo de dado:

* estruturado
* semi-estruturado
* não estruturado

A flexibilidade é enorme, mas vem com custo. Sem governança, o data lake vira um “data swamp”, onde dados existem, mas ninguém sabe o que são ou como usar.

Outro problema é performance. Consultar dados brutos pode ser mais lento e mais complexo.

## Lakehouse

O Lakehouse surge como uma tentativa de unir o melhor dos dois mundos.

Ele mantém a flexibilidade do data lake, permitindo armazenar dados brutos, mas adiciona camadas de organização, governança e performance semelhantes ao data warehouse.

Isso é feito com tecnologias que trazem:

* controle de schema
* transações (ACID)
* versionamento de dados
* otimizações para query

Na prática, você consegue usar o mesmo storage para:

* ingestão de dados brutos
* processamento
* análise

Isso reduz a necessidade de múltiplos sistemas separados.

## Diferenças fundamentais

A principal diferença está em quando e como o schema é aplicado.

No Data Warehouse, o schema é definido antes do armazenamento. Isso garante consistência, mas reduz flexibilidade.

No Data Lake, o schema é aplicado na leitura. Isso aumenta flexibilidade, mas exige mais disciplina e tooling.

No Lakehouse, você tenta equilibrar os dois, aplicando estrutura progressivamente sem perder flexibilidade inicial.

## Governança e qualidade

Data Warehouses têm governança forte por definição. Dados entram já tratados e validados.

Data Lakes exigem governança ativa. Sem isso, qualidade se degrada rapidamente.

Lakehouses tentam trazer governança para o lake, permitindo controle sem perder flexibilidade.

## Performance

Data Warehouses são altamente otimizados para queries analíticas.

Data Lakes podem ser mais lentos, dependendo do formato e do processamento.

Lakehouses utilizam formatos e engines que melhoram performance sem exigir transformação completa antecipada.

## Trade-offs reais

Data Warehouse oferece confiabilidade e performance, mas com custo de flexibilidade e maior esforço de transformação.

Data Lake oferece flexibilidade e baixo custo de ingestão, mas exige governança e pode sofrer com performance e organização.

Lakehouse reduz a necessidade de escolher entre os dois, mas adiciona complexidade tecnológica e dependência de ferramentas específicas.

## Quando usar

Se o foco é análise estruturada e relatórios confiáveis, Data Warehouse continua sendo uma escolha sólida.

Se você precisa armazenar grandes volumes de dados variados sem saber ainda como serão usados, Data Lake faz sentido.

Se você quer consolidar ingestão, processamento e análise em uma arquitetura unificada, Lakehouse é uma opção moderna.

## O que muda na prática

Você deixa de pensar apenas em banco de dados e passa a pensar em pipelines de dados.

Dados fluem por diferentes estágios:

* ingestão
* processamento
* consumo

Cada abordagem organiza esses estágios de forma diferente.

A escolha impacta diretamente custo, performance, governança e velocidade de evolução.
