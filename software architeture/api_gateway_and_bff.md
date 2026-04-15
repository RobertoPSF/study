# API Gateway + Backend for Frontend (BFF)

## Introdução

API Gateway e Backend for Frontend (BFF) resolvem um problema que aparece inevitavelmente quando sistemas começam a crescer: múltiplos clientes, como web, mobile e parceiros externos, consumindo múltiplos serviços backend. Sem um desenho adequado, cada cliente precisa conhecer todos os serviços, lidar com autenticação, fazer agregação de dados e ainda se adaptar a mudanças de contrato. Isso cria um acoplamento distribuído difícil de evoluir e praticamente impossível de governar com consistência.

Esses dois padrões surgem para controlar esse cenário, mas é aqui que muita gente erra: eles não são a mesma coisa e não resolvem o mesmo problema. Quando você mistura os papéis, você não simplifica a arquitetura — você só move a complexidade para outro lugar.

## O problema sem Gateway ou BFF

Em uma arquitetura ingênua, o frontend conversa diretamente com vários serviços. Isso pode parecer eficiente no começo, mas rapidamente se torna um problema estrutural. O cliente passa a conhecer detalhes internos do backend, a lógica de agregação de dados vai parar no frontend e qualquer mudança em um serviço começa a quebrar múltiplos clientes. Além disso, preocupações como autenticação, rate limiting e observabilidade acabam sendo replicadas ou mal implementadas.

O resultado é simples: você perde controle sobre o sistema.

## API Gateway

O API Gateway surge como um ponto único de entrada para o sistema. Em vez de o cliente falar diretamente com vários serviços, ele fala com o gateway, que então encaminha a requisição para o destino correto. Essa camada não existe para implementar lógica de negócio, mas para centralizar preocupações transversais.

Na prática, o gateway atua como um proxy inteligente. Ele decide para onde cada requisição vai, aplica autenticação e autorização, controla taxa de requisições, coleta métricas e pode fazer transformações simples de request e response. Esse tipo de responsabilidade é transversal ao sistema inteiro, então centralizar faz sentido.

O erro clássico acontece quando o gateway começa a crescer além desse papel. Quando você começa a colocar lógica de negócio nele, como combinar respostas de múltiplos serviços ou aplicar regras específicas do domínio, você cria um acoplamento perigoso. O gateway deixa de ser infraestrutura e vira um monólito escondido. Isso é especialmente problemático porque agora você tem lógica crítica em um ponto que deveria ser genérico e altamente estável.

O gateway funciona melhor quando é fino, previsível e focado em controle de tráfego e políticas globais. Ele deve ser boring por definição.

## Backend for Frontend (BFF)

O Backend for Frontend resolve um problema completamente diferente. Ele existe porque diferentes clientes têm necessidades diferentes. Um aplicativo mobile, por exemplo, costuma precisar de respostas menores, menos chamadas de rede e estruturas mais otimizadas. Já um frontend web pode lidar com mais dados e mais requisições.

Se você tentar atender todos os clientes com a mesma API genérica, você acaba criando endpoints complexos, difíceis de manter e cheios de parâmetros condicionais. Alternativamente, você pode empurrar essa lógica para o frontend, o que é pior, porque agora você espalha regras de orquestração entre múltiplos clientes.

O BFF resolve isso criando um backend específico para cada tipo de cliente. Esse backend conhece as necessidades do cliente e orquestra chamadas para os serviços internos, agregando dados e retornando exatamente o formato esperado. Diferente do gateway, o BFF pode conter lógica de orquestração e até uma camada leve de lógica de domínio, desde que isso não replique regras críticas que deveriam estar nos serviços centrais.

A diferença aqui é fundamental: o BFF não é genérico, ele é intencionalmente acoplado ao cliente.

## API Gateway e BFF juntos

Quando você usa os dois padrões juntos, a separação de responsabilidades precisa ser clara. O cliente fala com o API Gateway, que aplica políticas globais e roteia a requisição para o BFF correto. O BFF então orquestra os serviços internos e retorna uma resposta adaptada.

Esse fluxo funciona bem porque cada camada resolve um problema específico. O gateway cuida da infraestrutura e da governança do tráfego. O BFF cuida da experiência do cliente e da adaptação dos dados. Quando você respeita essa divisão, o sistema se mantém organizado mesmo com crescimento.

Se você mistura essas responsabilidades, por exemplo colocando lógica de orquestração no gateway ou criando um único BFF genérico para todos os clientes, você perde os benefícios e recria os problemas originais com mais camadas.

## Trade-offs reais

Esses padrões não são gratuitos. O API Gateway introduz um ponto central que pode se tornar gargalo ou ponto único de falha se não for bem implementado. Ele também exige maturidade operacional, especialmente em observabilidade e escalabilidade.

O BFF, por sua vez, aumenta o número de serviços e pode levar à duplicação de lógica entre diferentes clientes. Se você não for disciplinado, começa a replicar regras de negócio em múltiplos BFFs, o que é um erro grave.

A combinação dos dois aumenta o controle e a flexibilidade, mas também aumenta a complexidade do sistema. Se você não tem um problema claro que justifique essa estrutura, você está apenas antecipando complexidade sem necessidade.

## Regra prática

A distinção mais útil é pensar em natureza do problema. Quando o problema é infraestrutura, como autenticação, roteamento e controle de tráfego, o API Gateway é a solução. Quando o problema é adaptação para diferentes clientes, agregação de dados e redução de acoplamento no frontend, o BFF é a ferramenta correta.

Se você não consegue justificar claramente por que precisa de cada um, é um sinal de que provavelmente ainda não precisa deles.