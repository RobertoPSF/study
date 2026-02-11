Escalabilidade começa com uma pergunta que quase ninguém faz: o que exatamente vai crescer? Usuários? Requisições por segundo? Volume de dados? Tamanho das respostas? Dependências externas? Cada uma dessas dimensões cresce de forma diferente e quebra o sistema em lugares diferentes. Um erro clássico é falar “precisamos escalar” sem definir qual eixo está sob pressão.

Existem dois tipos fundamentais de escalabilidade: vertical e horizontal. Escalar verticalmente significa aumentar recursos da mesma máquina: mais CPU, mais memória, disco mais rápido. É simples, rápido e caro. Funciona até um limite físico e cria dependência de máquinas grandes. Escalar horizontalmente significa adicionar mais instâncias do sistema e distribuir a carga entre elas. É mais complexo, exige arquitetura preparada, mas praticamente não tem teto teórico. Sistemas modernos assumem que escalar verticalmente é paliativo e horizontalmente é estratégia.

A partir disso surge o primeiro conceito-chave: stateless vs stateful. Um sistema só escala horizontalmente bem se for majoritariamente stateless. Stateless significa que a instância não guarda estado de sessão relevante na memória local. Se você precisa que o usuário volte sempre para a mesma instância, você matou a escalabilidade horizontal. Por isso sessões vão para Redis, banco ou tokens como JWT. Estado local é conforto do desenvolvedor e inimigo da escala.

Outro ponto crítico é entender onde está o gargalo. Gargalos raramente estão onde você acha. CPU costuma ser o gargalo menos comum em backends modernos. Muito mais frequente é I/O: chamadas de rede, banco de dados, APIs externas, disco. Um backend “simples” pode lidar com dezenas de milhares de requisições se fizer pouca coisa. O mesmo backend cai com poucas centenas se cada request fizer múltiplas chamadas bloqueantes. Escalabilidade é, em grande parte, gestão de latência externa.

Daí surge a importância de concorrência e paralelismo. Concorrência é lidar com várias tarefas intercaladas; paralelismo é executar várias tarefas ao mesmo tempo. Em backend, especialmente com I/O, concorrência é mais importante que paralelismo. Um servidor assíncrono bem escrito escala melhor que um servidor síncrono mal configurado, mesmo com menos threads. Escalar não é “mais threads”, é melhor uso do tempo ocioso.

Cache entra como uma das ferramentas mais poderosas de escalabilidade. Cache reduz carga repetitiva, encurta latência e protege dependências. Mas cache não é trivial. Toda estratégia de cache precisa responder três perguntas: o que cachear, por quanto tempo (TTL) e como invalidar. A regra prática é: cachear leitura cara e relativamente estável. Cache mal invalidado causa bugs piores que lentidão. Por isso muitos sistemas preferem TTL curto a invalidação complexa.

Escalabilidade também exige entender acoplamento. Sistemas muito acoplados escalam mal porque tudo cresce junto. Um pequeno aumento em um fluxo explode o sistema inteiro. Separação de responsabilidades, camadas bem definidas e contratos claros reduzem acoplamento. Não é “arquitetura bonita”, é sobrevivência sob carga.

Banco de dados é quase sempre o maior ponto de falha de escalabilidade. Um banco centralizado vira gargalo rapidamente. Índices corretos fazem diferença absurda; índices errados matam escrita. Escalar leitura é mais fácil (replicas), escalar escrita é difícil. Por isso decisões como “normalizar tudo” ou “desnormalizar um pouco” são decisões de escalabilidade, não de estética. Em sistemas grandes, duplicar dados é comum porque leitura barata vale mais que escrita elegante.

Outro conceito essencial é backpressure. Um sistema escalável sabe dizer “não” de forma controlada. Quando a carga excede a capacidade, ele degrada graciosamente em vez de colapsar. Isso envolve rate limiting, filas, rejeição antecipada e timeouts agressivos. Um sistema que aceita tudo até cair não é escalável, é irresponsável.

Filas são uma ferramenta central aqui. Elas desacoplam produtores e consumidores, absorvem picos e permitem processamento assíncrono. Sempre que algo não precisa ser síncrono para o usuário, colocar atrás de uma fila melhora escalabilidade. Mas filas introduzem latência e complexidade operacional. De novo: trade-off explícito.

Escalabilidade não é só performance, é resiliência sob crescimento. À medida que o sistema cresce, falhas se tornam estatisticamente inevitáveis. Mais máquinas = mais falhas. Por isso padrões como timeout, retry com backoff e circuit breaker não são “detalhes”, são pré-requisitos. Sem eles, escalar aumenta a frequência de quedas.

Observabilidade fecha o ciclo. Você não escala o que não mede. Métricas como latência p95, taxa de erro, throughput e saturação são mais importantes que média. Média mente. Escalabilidade real é manter p95 e p99 sob controle quando a carga cresce. Logs estruturados e métricas permitem encontrar gargalos antes que usuários encontrem.

Um ponto que separa júnior de sênior: não existe sistema infinitamente escalável. Toda decisão empurra o problema para outro lugar. Cache empurra inconsistência, filas empurram latência, replicas empurram consistência, sharding empurra complexidade. Escalabilidade é escolher conscientemente qual problema você prefere ter.

Por fim, a regra mais importante: não escale antes de precisar, mas construa para escalar quando precisar. Isso significa código simples, estado fora da aplicação, contratos claros, dependências isoladas e decisões documentadas. Escalabilidade não nasce de frameworks ou buzzwords, nasce de respeito aos limites do sistema.

Stateless e stateful não são categorias absolutas; são propriedades de componentes dentro de um sistema. Um sistema real quase nunca é 100% stateless ou 100% stateful. A pergunta correta não é “meu sistema é stateless?”, mas onde o estado vive e quem é responsável por ele.

Um componente é stateful quando seu comportamento futuro depende de informações armazenadas localmente de interações passadas. Em backend, isso normalmente significa estado em memória: sessão de usuário, cache local, conexão persistente, contadores, flags temporárias. O ponto crítico é que esse estado não é compartilhado automaticamente com outras instâncias.

Um componente é stateless quando cada requisição contém tudo o que o componente precisa para processá-la, ou quando o estado necessário está em um repositório externo acessível por todas as instâncias. Stateless não significa “sem estado nenhum”; significa sem estado local relevante.

Essa distinção é crucial para escalabilidade horizontal. Quando você adiciona instâncias atrás de um load balancer, o tráfego começa a ser distribuído. Se a aplicação for stateless, qualquer instância pode atender qualquer requisição. Se for stateful, você cria dependência entre usuário e instância. A partir daí surgem soluções artificiais como sticky sessions, que resolvem um problema local e criam um problema estrutural: você transformou um cluster em vários monolitos pequenos.

Sticky session é um ótimo exemplo de antipadrão tolerável no início e tóxico em escala. Funciona enquanto o tráfego é pequeno e as instâncias são poucas. Em escala, dificulta balanceamento, reduz tolerância a falhas e complica deploy. Se uma instância cai, todo o estado associado a ela morre. Um sistema verdadeiramente escalável assume que instâncias são descartáveis.

A noção de “instâncias descartáveis” é central aqui. Em arquitetura moderna, você deve ser capaz de matar qualquer instância a qualquer momento sem impacto funcional grave. Isso só é possível quando o estado crítico vive fora da aplicação: banco, cache distribuído, fila, storage externo. Stateless é menos sobre conforto de código e mais sobre liberdade operacional.

Sessões de usuário ilustram bem isso. Em aplicações stateful tradicionais, a sessão fica em memória. Em aplicações stateless, a sessão vai para Redis ou vira um token auto-contido como JWT. Cada abordagem tem trade-offs. Redis centraliza estado e facilita invalidação, mas vira dependência crítica. JWT elimina lookup central, mas dificulta revogação e aumenta tamanho de requisição. Nenhuma é “melhor”; cada uma empurra a complexidade para um lugar diferente.

Outro ponto importante: cache local torna um sistema parcialmente stateful. Cache em memória melhora latência, mas cria inconsistência entre instâncias. Isso pode ser aceitável se o cache for apenas otimização e nunca fonte de verdade. O erro comum é esquecer disso e depender do cache local para lógica de negócio. A partir daí, bugs aparecem só em produção e só sob carga.

Statefulness também aparece em conexões persistentes, como WebSockets. Aqui, stateful é inevitável. A solução não é “evitar estado”, mas isolar onde ele existe. Sistemas que usam WebSocket em escala normalmente têm um gateway stateful na borda e um core stateless atrás, comunicando via eventos. Você não elimina estado; você o empurra para camadas controladas.

Um detalhe sutil: stateful não é só memória. Pode ser filesystem local, variáveis de ambiente mutáveis, locks locais, até ordem de processamento implícita. Qualquer coisa que faça duas instâncias se comportarem de forma diferente para a mesma entrada é estado relevante. Escalabilidade exige determinismo sob repetição.

Do ponto de vista de deploy, aplicações stateless permitem estratégias seguras como rolling update, blue-green e auto scaling. Stateful torna deploy mais delicado: você precisa drenar conexões, preservar estado, migrar sessões. Isso aumenta custo operacional e risco. Por isso equipes experientes pagam o preço de externalizar estado cedo.

Há também um custo cognitivo. Sistemas stateful são mais fáceis de escrever no começo porque você “lembra das coisas”. Sistemas stateless exigem pensar em contratos, dados explícitos, idempotência. O custo aparece no início, mas o benefício vem com escala. É um clássico trade-off curto prazo vs longo prazo.

Um ponto que entrevistadores gostam de ouvir: stateless favorece idempotência. Se uma requisição pode ser repetida sem efeitos colaterais inesperados, retries ficam seguros. Em sistemas stateful, retries mal feitos causam duplicação, inconsistência e corrupção de dados. Por isso sistemas distribuídos valorizam tanto operações idempotentes.

Por fim, a conclusão prática: você não deve eliminar estado, você deve centralizá-lo, torná-lo explícito e tratá-lo como recurso compartilhado. Aplicação backend bem escalável é aquela onde a lógica é stateless, o estado é externo, e as instâncias são intercambiáveis.