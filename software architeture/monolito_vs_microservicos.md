Monolito e microsserviços não são escolhas ideológicas, são respostas diferentes a contextos diferentes. O erro comum — e recorrente em entrevistas e na vida real — é tratar microsserviços como “evolução natural” do monolito. Não são. São uma troca consciente de problemas.

Comecemos pelo monolito.

Um sistema monolítico é aquele em que toda a aplicação roda como uma única unidade de deploy. Isso não significa “código bagunçado” nem “sistema pequeno”. Um monolito bem feito pode ter milhões de linhas de código, desde que mantenha organização interna clara: camadas, módulos, fronteiras explícitas. O ponto central é que tudo é compilado, versionado, testado e publicado junto.

As principais vantagens do monolito são simplicidade operacional e coerência técnica. Existe apenas um processo rodando, uma stack de logs, uma estratégia de deploy, uma topologia de rede. Comunicação entre partes do sistema ocorre em memória, via chamadas diretas de função ou método, o que é rápido, previsível e fácil de debugar. Transações envolvendo múltiplos módulos são triviais de implementar, porque tudo compartilha o mesmo contexto transacional e o mesmo banco de dados, se você assim decidir.

Essa simplicidade tem consequências práticas enormes. Times pequenos conseguem evoluir rápido porque não gastam energia com infraestrutura, observabilidade distribuída, versionamento de contratos ou problemas de latência de rede. Debugar um bug geralmente envolve abrir um stack trace e seguir o fluxo. Em entrevistas, isso se traduz em respostas como: “comecei com monolito porque o domínio ainda estava instável e o time precisava aprender rápido”.

O monolito começa a sofrer quando três forças aparecem juntas: crescimento de time, crescimento de domínio e crescimento de carga. À medida que mais pessoas trabalham no mesmo código, surgem conflitos de merge, deploys ficam mais arriscados e o tempo de build cresce. À medida que o domínio cresce, módulos passam a ter ciclos de mudança muito diferentes, mas continuam presos ao mesmo ritmo de deploy. À medida que a carga cresce, você passa a escalar o sistema inteiro mesmo quando apenas uma parte precisa de mais recursos.

Importante: esses problemas não surgem automaticamente. Eles surgem quando o monolito é mal modularizado. Um monolito bem estruturado pode escalar surpreendentemente bem por muito tempo. Muitas empresas grandes rodam sistemas críticos monolíticos há décadas.

Agora, microsserviços.

Microsserviços são uma arquitetura onde o sistema é dividido em serviços independentes, cada um com seu próprio ciclo de vida: código, deploy, escalabilidade e, idealmente, dados. Cada serviço é responsável por um subdomínio claro e se comunica com outros serviços por meio de rede, geralmente via HTTP ou mensageria.

O ganho central aqui é independência. Times diferentes podem trabalhar em serviços diferentes, fazer deploys em horários diferentes, escolher linguagens diferentes e escalar apenas o que precisa. Isso reduz acoplamento organizacional, não apenas técnico. Microsserviços são, antes de tudo, uma solução para coordenação de times, não para performance.

Mas essa independência vem com um custo brutal.

Quando você transforma chamadas locais em chamadas de rede, você introduz latência, falha parcial e indeterminação. Uma função chamada nunca “cai”. Um serviço remoto pode demorar, retornar erro, cair no meio da resposta ou responder com dados inconsistentes. Isso obriga você a lidar com timeout, retry, circuit breaker, fallback e versionamento de contrato. Se você não faz isso, o sistema parece funcionar… até o dia em que falha de forma catastrófica.

Além disso, microsserviços tornam transações distribuídas difíceis. Você perde a possibilidade de um simples BEGIN / COMMIT envolvendo múltiplos módulos. Surge a necessidade de consistência eventual, sagas, compensações e aceitação explícita de estados intermediários. Isso exige maturidade técnica e mental do time. Muitos times dizem aceitar consistência eventual, mas entram em pânico quando veem dados “temporariamente errados”.

Operacionalmente, microsserviços exigem uma base sólida: automação de deploy, observabilidade distribuída, tracing, métricas, gestão de configuração, descoberta de serviços, controle de versão de APIs. Sem isso, o sistema vira um pesadelo impossível de debugar. Um bug simples pode atravessar cinco serviços e três bancos de dados.

Aqui está o ponto que poucos dizem claramente: microsserviços aumentam a complexidade total do sistema. Eles apenas redistribuem essa complexidade para onde ela é mais tolerável — geralmente para times grandes, maduros e com necessidades claras de independência.

Por isso, a pergunta correta nunca é “monolito ou microsserviços?”. A pergunta correta é:

Quantas pessoas trabalham nesse sistema?

O domínio já está estável ou ainda muda muito?

Quais partes realmente precisam escalar de forma independente?

O time sabe operar sistemas distribuídos?

O custo operacional é aceitável para o negócio agora?

Em 90% dos casos iniciais, a resposta honesta leva ao monolito.

Uma prática madura é começar com um monolito modular, desenhado com fronteiras claras entre domínios, de forma que, se um dia fizer sentido, certos módulos possam ser extraídos para serviços independentes. Isso não é “monolito sujo esperando virar microsserviço”. É um design consciente que adia decisões irreversíveis até que haja dados reais.

Em entrevistas, respostas ruins são absolutas: “microsserviços escalam melhor” ou “monolito é ultrapassado”. Respostas boas falam de trade-offs. Respostas excelentes deixam claro que você entende que arquitetura é uma ferramenta de negócio, não uma bandeira técnica.

Uma resposta madura seria algo como:
“Eu começaria com um monolito bem modularizado. Microsserviços só fazem sentido quando o custo de coordenação dentro do monolito supera o custo operacional de sistemas distribuídos. Antes disso, eles mais atrapalham do que ajudam.”