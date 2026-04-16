# Service Mesh (Istio, Linkerd, Sidecar Pattern)

## Introdução

Service Mesh surge quando a complexidade de comunicação entre serviços passa a ser um problema maior do que a própria lógica de negócio. Em sistemas distribuídos simples, você consegue lidar com chamadas HTTP diretas, retries básicos e algum nível de logging. À medida que o sistema cresce, isso se torna insuficiente.

Você começa a precisar de controle fino sobre tráfego, observabilidade detalhada, políticas de segurança consistentes, retries inteligentes, circuit breaking e versionamento de comunicação entre serviços. Se cada serviço implementar isso por conta própria, você cria duplicação, inconsistência e acoplamento.

Service Mesh resolve esse problema movendo essas responsabilidades para uma camada de infraestrutura dedicada à comunicação entre serviços.

## O problema antes do Service Mesh

Sem um Service Mesh, cada serviço precisa lidar diretamente com comunicação de rede. Isso significa que lógica de infraestrutura começa a vazar para dentro do código de aplicação.

Na prática, você começa a ver bibliotecas específicas sendo usadas em cada serviço para implementar:

* retries
* timeouts
* métricas
* tracing
* autenticação entre serviços

O problema não é só técnico, é organizacional. Cada equipe pode implementar isso de forma diferente, com configurações diferentes e comportamentos inconsistentes.

O resultado é um sistema difícil de operar e ainda mais difícil de debugar.

## O conceito de Service Mesh

Service Mesh é uma camada dedicada a gerenciar comunicação entre serviços.

Em vez de cada serviço implementar lógica de rede, essa lógica é extraída para a infraestrutura. O serviço continua focado em regras de negócio, enquanto o mesh controla como os serviços se comunicam.

A ideia central é separar completamente:

* lógica de negócio
* lógica de comunicação distribuída

Essa separação é feita através de um padrão chamado sidecar.

## Sidecar Pattern

O sidecar pattern é a base operacional do Service Mesh.

Para cada instância de serviço, existe um proxy rodando ao lado dele, no mesmo ambiente (geralmente no mesmo pod em Kubernetes). Esse proxy intercepta todo o tráfego de entrada e saída.

O serviço não fala diretamente com outros serviços. Ele fala com o proxy local. O proxy então decide como encaminhar a requisição.

Esse proxy pode:

* aplicar retries
* fazer load balancing
* coletar métricas
* aplicar políticas de segurança
* fazer tracing distribuído

O ponto crítico aqui é que o serviço não precisa saber de nada disso.

Isso muda completamente o modelo mental. Em vez de escrever código para lidar com falhas de rede, você configura comportamento no mesh.

## Plano de dados e plano de controle

Service Mesh normalmente é dividido em dois componentes: data plane e control plane.

O data plane é composto pelos sidecars, que lidam com o tráfego real.

O control plane define como esses proxies devem se comportar. Ele distribui configurações, políticas e regras de roteamento.

Essa separação permite alterar comportamento de rede sem alterar código ou redeployar serviços.

## Istio

Istio é um dos Service Mesh mais completos e também um dos mais complexos.

Ele utiliza proxies Envoy como sidecars e possui um control plane robusto que permite configurar praticamente qualquer aspecto da comunicação entre serviços.

Com Istio, você consegue implementar:

* roteamento avançado (canary, blue-green)
* controle de tráfego por versão
* autenticação mTLS automática
* autorização baseada em políticas
* observabilidade completa (metrics, logs, tracing)

O problema é que essa flexibilidade tem custo. Istio é pesado, exige conhecimento operacional e pode ser difícil de manter se o time não tiver maturidade.

## Linkerd

Linkerd é uma alternativa mais leve e focada.

Ele também utiliza proxies sidecar, mas prioriza simplicidade e facilidade de operação.

Linkerd cobre o essencial:

* observabilidade
* mTLS automático
* retries e timeouts
* load balancing

Mas evita a complexidade extrema de configuração que o Istio permite.

A escolha entre Istio e Linkerd normalmente não é técnica no sentido puro, mas organizacional. Times que precisam de controle fino e já possuem maturidade operacional tendem a preferir Istio. Times que querem simplicidade e previsibilidade tendem a escolher Linkerd.

## O que muda na prática

Adotar um Service Mesh muda onde você resolve problemas.

Sem mesh, você resolve no código.
Com mesh, você resolve na infraestrutura.

Isso tem implicações importantes.

Primeiro, desenvolvedores precisam parar de implementar lógica de rede manualmente e confiar na infraestrutura.

Segundo, times de plataforma passam a ter mais responsabilidade, porque agora comportamento de comunicação está centralizado.

Terceiro, debugging muda. Problemas podem estar no serviço, no proxy ou na configuração do mesh.

## Trade-offs reais

Service Mesh não é uma solução universal. Ele adiciona uma camada significativa de complexidade.

Você passa a ter:

* mais componentes rodando
* mais consumo de recursos (cada sidecar consome CPU e memória)
* maior complexidade operacional

Se o sistema ainda é pequeno ou possui poucos serviços, o custo não compensa.

Além disso, você precisa de maturidade em observabilidade e operação. Sem isso, o mesh vira uma caixa preta difícil de entender.

Outro ponto crítico é latência. Cada chamada passa por proxies adicionais, o que adiciona overhead.

## Quando usar

Service Mesh faz sentido quando:

* você tem muitos serviços
* comunicação entre serviços é complexa
* precisa de controle avançado de tráfego
* precisa de segurança consistente (mTLS)
* precisa de observabilidade distribuída madura

Se você ainda está tentando organizar seu domínio ou sua arquitetura básica, Service Mesh é distração.