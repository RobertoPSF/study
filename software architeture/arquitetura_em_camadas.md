Arquitetura em camadas é um padrão de organização estrutural onde o sistema é dividido em partes horizontais, cada uma com uma responsabilidade clara e delimitada. A ideia central não é estética, é controle de complexidade. Sistemas crescem, regras mudam, dependências externas falham. Se você mistura responsabilidades, você perde previsibilidade e capacidade de evolução. Camadas existem para evitar isso.

A premissa básica é simples:
cada camada depende apenas da camada imediatamente inferior. Nada de saltos. Nada de atalhos.

O fluxo clássico é:

Controller → Service → Repository → Infraestrutura

Mas isso é apenas a forma mais conhecida. O que importa não é o nome, é a responsabilidade.

Vamos decompor isso de forma estrutural.

A camada de apresentação (Controller ou API Layer) é responsável por comunicação externa. Ela recebe requisições HTTP, valida dados básicos, transforma input em algo que o domínio entende e transforma a resposta do domínio em formato de saída (JSON, por exemplo). Essa camada não contém regra de negócio. Se contém regra de negócio, você já está errado. Controller bom é magro. Ele orquestra, não decide.

Exemplo mental:
Se amanhã você trocar REST por GraphQL, a regra de negócio não deveria mudar. Se muda, você acoplou errado.

A camada de serviço (Service Layer) contém a regra de negócio. Aqui mora a inteligência do sistema. É onde decisões são tomadas. É onde agregações acontecem. É onde validações complexas vivem.

Se o controller é tradutor, o service é o cérebro.

Essa camada:

- Decide fluxos
- Coordena chamadas a repositórios
- Lida com exceções de negócio
- Aplica políticas
- Ela não deveria saber detalhes de banco ou detalhes HTTP. Se sabe, está contaminada.

A camada de repositório (Repository / Data Access Layer) é responsável por persistência. Ela sabe como falar com banco de dados. Ela conhece SQL, ORM, conexões, queries.

Ela não sabe o que é HTTP.
Ela não sabe regra de negócio.
Ela só sabe buscar e salvar dados.

A regra de ouro:
Se amanhã você trocar PostgreSQL por MongoDB, apenas o repositório deveria mudar.

A camada de infraestrutura engloba detalhes técnicos externos:

- Banco
- Cache
- Serviços externos
- Mensageria
- File system

Ela é a parte mais volátil do sistema. Justamente por isso deve estar isolada.

Agora vamos falar da razão real por trás das camadas.

Arquitetura em camadas não é sobre organização visual.
É sobre direção de dependência.

O sistema deve depender do que é estável, não do que é volátil.

Regra de negócio muda menos que tecnologia.
Domínio muda menos que framework.

Se seu service depende diretamente de FastAPI ou de um ORM específico, você amarrou o sistema à tecnologia.

Camadas mal implementadas criam uma falsa sensação de organização. Camadas bem implementadas criam independência.

Agora vamos entrar em pontos mais avançados.

Existe uma diferença entre:

Layered Architecture tradicional e Clean Architecture / Onion Architecture

- Arquitetura em camadas clássica geralmente permite que camadas superiores dependam das inferiores diretamente.
- Clean Architecture inverte a dependência usando abstrações. O domínio não depende da infraestrutura. A infraestrutura depende do domínio.

Em entrevista, você pode dizer algo como:

“Uso arquitetura em camadas para separar responsabilidades, mas prefiro que a regra de negócio não dependa de detalhes técnicos, seguindo princípios de inversão de dependência.”

Isso demonstra maturidade.

Falando em princípios: Arquitetura em camadas conversa diretamente com o SOLID.

Especialmente:

Single Responsibility Principle
Cada camada tem uma responsabilidade clara.

Dependency Inversion Principle
Camadas internas não devem depender de implementações externas.

Se você mencionar isso numa entrevista, você sai do nível júnior.

Vamos falar agora dos benefícios reais.

Testabilidade
Se o service não depende diretamente de banco, você consegue mockar o repositório.
Testes ficam simples e rápidos.

Manutenção
Você sabe onde procurar código.
Erro de regra? Service.
Erro de query? Repository.

Evolução
Você consegue trocar infraestrutura sem reescrever regra de negócio.

Escalabilidade organizacional
Times conseguem trabalhar em paralelo.

Agora vamos falar dos problemas.

Arquitetura em camadas pode virar burocracia se mal aplicada.

Erros comuns:

- Controller gordo
- Service vazio
- Repository cheio de regra
- Dependência circular
- Service chamando HTTP diretamente
- Camadas pulando níveis

Outro erro comum: superengenharia. Criar interface para tudo, abstração para tudo, sem necessidade real.

Se o sistema é pequeno, simplicidade vence.

Vamos aplicar isso ao seu projeto da API de agregação.

Controller:

- Recebe GET /aggregate
- Valida parâmetros
- Chama AggregationService
- Retorna JSON

Service:

- Chama ClientA
- Chama ClientB
- Aplica timeout
- Aplica retry
- Decide fallback
- Retorna resultado agregado
- Clients (infraestrutura):
- Fazem HTTP real
- Lidam com detalhes da API externa

Cache:

- Isolado como componente técnico

Percebe?
Regra de negócio (como agregar e quando usar fallback) não está no controller.
E cliente HTTP não sabe nada sobre regra de negócio.

Isso é arquitetura em camadas aplicada corretamente.

Agora uma visão mais estratégica.

Por que entrevistadores perguntam isso?

Porque código todo mundo escreve.
Mas organização define senioridade.

Quando você fala em camadas, o entrevistador quer saber:

- Você entende separação de responsabilidades?
- Você sabe onde colocar lógica?
- Você sabe evitar acoplamento?
- Você entende direção de dependência?

Vamos elevar um pouco mais.

Arquitetura em camadas funciona muito bem para sistemas CRUD, APIs tradicionais, sistemas administrativos.

Ela começa a ficar limitada quando:

domínio é extremamente complexo

sistema é altamente distribuído

eventos são o centro da arquitetura

Nesses casos entram:

- Arquitetura hexagonal
- Event-driven
- CQRS
- Microservices

Mas para 80% dos sistemas backend de empresas comuns, arquitetura em camadas é suficiente.

Saber aplicar bem já te coloca acima da média.

Agora a parte que quase ninguém fala.

Arquitetura em camadas não é sobre código.
É sobre disciplina.

Se você começar a permitir exceções:
“Ah, só dessa vez vou colocar essa regra no controller”

Em seis meses o sistema vira caos.

Arquitetura é decisão repetida com consistência.

Como ela se relaciona com SOLID?

Boa pergunta.
Se você não souber responder isso em entrevista, arquitetura em camadas vira só “organização bonitinha”.

Vou conectar diretamente Arquitetura em Camadas com SOLID, sem floreio.

Primeiro: visão estrutural

Arquitetura em camadas organiza módulos do sistema.
SOLID organiza classes e dependências internas.

Um atua no nível macro.
O outro no nível micro.

Quando combinados corretamente, você tem:

- estrutura previsível
- código coeso
- baixo acoplamento
- alta testabilidade

Se usados isoladamente, você tem meia solução.

S — Single Responsibility Principle

Uma classe deve ter um único motivo para mudar.

Arquitetura em camadas é praticamente a materialização estrutural desse princípio.

Cada camada tem uma responsabilidade distinta:

- Controller → lidar com HTTP
- Service → regra de negócio
- Repository → persistência
- Infra → detalhes técnicos

Se você coloca regra de negócio no controller, você viola SRP.
Se você coloca SQL no service, você viola SRP.

Camadas são um mecanismo organizacional para forçar SRP em nível de sistema.

Mas cuidado:
Mesmo dentro de uma camada, você ainda pode violar SRP.

Exemplo ruim:
AggregationService que:

- faz agregação
- faz retry
- faz cache
- faz logging
- faz parsing
- faz validação

Isso é um monstro.

Arquitetura em camadas não garante SRP automaticamente.
Ela só cria o ambiente onde você pode aplicá-lo corretamente.

O — Open/Closed Principle

Entidades devem estar abertas para extensão e fechadas para modificação.

Em arquitetura em camadas, isso aparece quando você usa abstrações entre camadas.

Exemplo:

Service depende de uma interface:
- ExternalClient

Você pode trocar:

- Cliente real
- Cliente mock
- Cliente com cache
- Cliente com retry

Sem alterar o service.

Se seu service depende diretamente de uma implementação concreta (ex: HTTPXClient), você violou OCP.

Arquitetura em camadas bem feita favorece OCP porque:

você separa responsabilidades

você pode substituir implementações em camadas inferiores

Mal feita, ela acopla tudo e destrói o princípio.

L — Liskov Substitution Principle

Subtipos devem poder substituir seus tipos base sem quebrar comportamento esperado.

Isso aparece principalmente na camada de abstração.

Se seu Service depende de:

PaymentRepository (interface)

E você cria:
- PostgresPaymentRepository
- MongoPaymentRepository

Ambos devem respeitar o mesmo contrato.

Se um deles retorna null inesperadamente ou lança exceção diferente, você viola LSP.

Arquitetura em camadas cria os pontos onde LSP precisa ser respeitado:
principalmente entre Service ↔ Repository e Service ↔ Clients externos.

Se você não entende LSP, suas abstrações viram armadilha.

I — Interface Segregation Principle

Não forçar clientes a depender de interfaces que não usam.

Erro comum em arquitetura em camadas:

Criar uma interface gigante de repositório:

UserRepository com:

- save
- delete
- findAll
- findById
- findByEmail
- updateStatus
- deactivate
- exportCSV

E o service usa só dois métodos.

Você criou acoplamento desnecessário.

Boa arquitetura em camadas favorece interfaces pequenas e específicas.

Exemplo melhor:
- UserReadRepository
- UserWriteRepository

Isso melhora testabilidade e reduz impacto de mudança.

D — Dependency Inversion Principle

Esse é o mais importante na conexão com arquitetura em camadas.

Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações.

Em arquitetura em camadas tradicional, Service depende de Repository concreto.

Isso é dependência direta.

Em uma arquitetura mais madura (inspirada em Clean Architecture), você faz:

- Service depende de InterfaceRepository
- Infra implementa InterfaceRepository

Ou seja:
A camada de regra de negócio não depende de detalhes técnicos.

Essa é a evolução natural da arquitetura em camadas.

Se você quiser parecer mais experiente em entrevista, diga algo como:

“Uso arquitetura em camadas, mas aplico inversão de dependência para que a regra de negócio não dependa diretamente de infraestrutura.”

Isso mostra que você não está preso à forma superficial do padrão.

Conexão real entre os dois

Arquitetura em camadas fornece:

- separação macro de responsabilidades
- fluxo previsível
- estrutura organizacional

SOLID fornece:

- coesão interna
- baixo acoplamento
- extensibilidade
- substituibilidade

Sem SOLID, arquitetura em camadas vira uma pasta com nomes bonitos.
Sem arquitetura em camadas, SOLID vira disciplina isolada dentro de um caos estrutural.

Os dois se reforçam.

Onde as pessoas erram

Acham que separar em pastas já é arquitetura.

Acham que usar interface automaticamente resolve acoplamento.

Criam abstrações desnecessárias.

Confundem camadas com níveis de complexidade.

Arquitetura em camadas não é:
“controller → service → repository porque todo mundo faz”

É:
“separar responsabilidades para proteger regra de negócio e reduzir impacto de mudança”

Como responder isso em entrevista (versão madura)

Resposta enxuta e forte:

“A arquitetura em camadas organiza responsabilidades em níveis distintos, enquanto SOLID garante que as dependências e classes dentro dessas camadas permaneçam coesas e pouco acopladas. Especialmente o princípio da inversão de dependência é fundamental para evitar que a regra de negócio dependa de detalhes técnicos.”