# CQRS (Command Query Responsibility Segregation)

## Introdução

CQRS surge de uma constatação simples: leitura e escrita têm características diferentes, mas normalmente são tratadas da mesma forma. Em muitos sistemas, usamos o mesmo modelo, o mesmo banco e as mesmas estruturas para inserir dados e para consultá-los. Isso funciona bem no início, mas começa a quebrar quando o sistema cresce.

A ideia central do CQRS é separar explicitamente essas duas responsabilidades. Em vez de um único modelo que tenta servir a tudo, você passa a ter modelos diferentes para escrita (commands) e leitura (queries). Isso não é apenas uma decisão técnica, é uma forma de reduzir acoplamento e permitir otimizações específicas para cada tipo de operação.

## O problema do modelo único

Quando você usa um único modelo para leitura e escrita, você acaba fazendo concessões. O modelo precisa ser consistente para escrita, mas ao mesmo tempo eficiente para leitura. Isso leva a estruturas complexas, joins pesados, queries difíceis de manter e entidades inchadas com responsabilidades demais.

Além disso, regras de negócio e preocupações de leitura começam a se misturar. Você vê entidades que existem apenas para facilitar queries, ou queries que contornam o modelo de domínio porque ele não é eficiente para leitura.

Esse é o sinal clássico de que o modelo único está sendo forçado além do que deveria.

## O conceito de CQRS

CQRS separa o sistema em dois caminhos distintos.

O lado de escrita recebe comandos, aplica regras de negócio e altera o estado do sistema. Ele é focado em consistência e invariantes.

O lado de leitura responde queries e retorna dados já preparados para consumo. Ele é focado em performance e simplicidade de acesso.

Esses dois lados podem compartilhar o mesmo banco em casos simples, mas em arquiteturas mais maduras, eles possuem modelos e até bancos diferentes.

## Command Side (Escrita)

O lado de escrita é onde a lógica de negócio vive. Ele recebe comandos que representam intenções claras, como criar um pedido, cancelar uma compra ou registrar um pagamento.

Esses comandos passam por validação, aplicam regras de domínio e resultam em mudanças de estado.

Aqui você normalmente usa entidades ricas, aggregates e tudo que garante consistência.

O foco não é performance de leitura, é garantir que o estado seja correto.

## Query Side (Leitura)

O lado de leitura existe para responder perguntas. Ele não precisa respeitar as mesmas regras estruturais do domínio.

Você pode ter modelos totalmente diferentes, como tabelas desnormalizadas, projeções ou até bancos específicos para leitura.

O objetivo é responder rápido e de forma simples.

Não há regras de negócio complexas aqui, apenas transformação e entrega de dados.

## Sincronização entre escrita e leitura

Essa é a parte que define se sua implementação de CQRS é madura ou apenas superficial.

Quando você separa leitura e escrita, você precisa sincronizar os dois lados. Isso normalmente é feito com eventos.

Fluxo típico:

* Comando é executado
* Estado é alterado
* Evento é emitido
* Modelo de leitura é atualizado

Esse processo frequentemente é assíncrono, o que introduz consistência eventual.

Isso significa que, por um curto período, a leitura pode não refletir imediatamente a escrita.

## Consistência eventual

Consistência eventual é um dos trade-offs mais importantes do CQRS.

Você ganha escalabilidade e performance, mas perde consistência imediata entre leitura e escrita.

Se o seu sistema não pode tolerar esse tipo de atraso, CQRS completo pode não ser adequado.

Muitos sistemas adotam versões simplificadas exatamente para evitar esse problema.

## CQRS simples vs CQRS completo

CQRS não é binário. Existe um espectro.

Em uma forma simples, você apenas separa comandos e queries no código, mas ainda usa o mesmo banco.

Em uma forma mais avançada, você tem:

* modelos diferentes
* bancos diferentes
* sincronização por eventos

O erro comum é tentar implementar a versão mais complexa sem necessidade.

## Benefícios reais

Separar leitura e escrita permite otimizar cada lado de forma independente. Você pode escalar leitura sem impactar escrita, e vice-versa.

Também melhora clareza. Fica evidente o que é mutação de estado e o que é consulta.

Além disso, combina muito bem com DDD, especialmente com aggregates no lado de escrita.

## Trade-offs reais

CQRS adiciona complexidade significativa. Você passa a ter dois modelos, dois fluxos e um mecanismo de sincronização.

Debugging fica mais difícil, porque um problema pode estar no comando, no evento ou na projeção de leitura.

Consistência eventual pode gerar confusão para usuários se não for bem tratada.

Também existe custo operacional maior, principalmente se você usar múltiplos bancos.

## Quando usar

CQRS faz sentido quando:

* leitura e escrita têm requisitos muito diferentes
* o sistema possui alto volume de leitura
* o domínio é complexo
* há necessidade de escalar leitura separadamente

Se você tem um CRUD simples, CQRS completo é exagero.

## O que muda na prática

Você deixa de pensar em "modelos que fazem tudo" e passa a pensar em fluxos separados.

Comandos alteram estado.
Queries leem estado.

Essa separação força disciplina e clareza, mas exige maturidade para lidar com as consequências.
