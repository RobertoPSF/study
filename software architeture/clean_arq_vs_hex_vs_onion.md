# Clean Architecture vs Hexagonal vs Onion

## Introdução

Clean Architecture, Hexagonal Architecture e Onion Architecture são variações do mesmo problema: como impedir que regras de negócio sejam contaminadas por detalhes externos, como banco de dados, framework, API HTTP, mensageria ou UI. As três arquiteturas surgiram em momentos diferentes, com autores diferentes, mas compartilham a mesma ideia central: o domínio deve estar no centro, e as dependências devem apontar para dentro.

A maior parte da confusão existe porque muita gente trata essas arquiteturas como concorrentes, quando na prática elas são parentes muito próximas. A diferença real está na forma de organizar camadas, no vocabulário utilizado e em como as fronteiras são explicitadas.

---

# O problema que elas tentam resolver

Em aplicações tradicionais, principalmente as construídas rapidamente com frameworks web, o código costuma seguir esta direção:

```text
Controller -> Service -> Repository -> Banco de Dados
```

O problema parece pequeno no início, mas rapidamente o domínio começa a depender de tudo:

* Entidades conhecem ORM
* Regras de negócio conhecem SQL
* Casos de uso dependem de HTTP
* Framework passa a controlar toda a estrutura da aplicação

O resultado é previsível: o sistema fica difícil de testar, difícil de trocar tecnologia e difícil de evoluir sem efeito cascata.

As três arquiteturas tentam inverter isso. Em vez de o negócio depender do framework, o framework passa a depender do negócio.

---

# A Dependency Rule

A regra mais importante é a chamada Dependency Rule.

Ela diz:

> Código de camadas internas nunca pode depender de código de camadas externas.

Ou seja, as dependências sempre apontam para dentro.

```text
Externo -> Interno
```

Nunca:

```text
Interno -> Externo
```

Por exemplo:

```text
Correto:
API -> Application -> Domain
Infra -> Application -> Domain
```

```text
Errado:
Domain -> Database
Domain -> FastAPI
Domain -> SQLAlchemy
```

Se uma regra de negócio precisa salvar algo em banco, ela não conhece o banco diretamente. Em vez disso, ela depende de uma abstração.

```python
class UserRepository:
    def save(self, user):
        pass
```

A implementação concreta fica do lado de fora:

```python
class SqlAlchemyUserRepository(UserRepository):
    def save(self, user):
        session.add(user)
```

O domínio conhece apenas a interface. A infraestrutura conhece a implementação.

Essa inversão normalmente é feita com Dependency Inversion Principle, interfaces, portas, adapters ou injeção de dependência.

---

# Hexagonal Architecture

Hexagonal Architecture foi proposta por Alistair Cockburn. Também é chamada de Ports and Adapters.

A ideia principal é simples: o sistema possui um núcleo isolado e tudo que está fora conversa com esse núcleo através de portas.

```text
        [ API REST ]
              |
        [ Adapter ]
              |
         [ Port ]
              |
         [ Domain ]
              |
         [ Port ]
              |
        [ Adapter ]
              |
         [ Database ]
```

O nome “hexagonal” existe apenas para reforçar que o sistema pode ter vários pontos de entrada e saída. O formato de hexágono não tem significado técnico.

## Componentes principais

### Domain

Contém entidades, regras de negócio e casos de uso centrais.

### Ports

São interfaces que definem como o domínio conversa com o exterior.

Existem dois tipos:

* Incoming Ports: algo chama o sistema
* Outgoing Ports: o sistema chama algo externo

Exemplo:

```python
class CreateOrderUseCase:
    def execute(self, data):
        pass
```

Esse pode ser um incoming port.

```python
class PaymentGateway:
    def charge(self, amount):
        pass
```

Esse pode ser um outgoing port.

### Adapters

São implementações concretas das portas.

```text
REST Controller -> Incoming Adapter
PostgreSQL Repository -> Outgoing Adapter
Kafka Consumer -> Incoming Adapter
Stripe Client -> Outgoing Adapter
```

## Força da arquitetura hexagonal

A arquitetura hexagonal deixa explícito que tudo externo é intercambiável. Você pode trocar REST por gRPC, PostgreSQL por MongoDB ou Stripe por outro gateway sem alterar o núcleo.

Ela é especialmente forte quando a aplicação possui muitas integrações externas.

Por exemplo:

* APIs
* Mensageria
* Banco de dados
* Serviços externos
* CLI
* Jobs

## Fraqueza da arquitetura hexagonal

A principal desvantagem é que, se levada ao extremo, ela gera excesso de interfaces e adapters.

Em times inexperientes, surge este padrão ruim:

```text
1 interface para cada classe
1 adapter para cada método
1 camada extra sem motivo
```

Isso aumenta a complexidade sem ganho real.

Outro problema é que a arquitetura hexagonal não define com clareza várias camadas internas. Ela separa muito bem “dentro” e “fora”, mas deixa menos explícito onde ficam application services, use cases e entidades.

---

# Onion Architecture

Onion Architecture foi proposta por Jeffrey Palermo.

Ela organiza a aplicação em anéis concêntricos.

```text
+-------------------------+
| Infrastructure          |
| +---------------------+ |
| | Application Layer   | |
| | +-----------------+ | |
| | | Domain Layer    | | |
| | +-----------------+ | |
| +---------------------+ |
+-------------------------+
```

Quanto mais próximo do centro, mais importante e mais estável é o código.

## Camadas típicas

### Centro: Domain

O centro contém:

* Entidades
* Value Objects
* Regras de negócio puras
* Domain Services

Esse núcleo não conhece nada externo.

### Camada intermediária: Application

Contém:

* Use Cases
* Orquestração
* Serviços de aplicação
* Interfaces de repositórios

Ela coordena o domínio, mas ainda não conhece detalhes concretos.

### Camada externa: Infrastructure

Contém:

* Banco de dados
* Framework web
* Repositórios concretos
* APIs externas
* Filas

## Dependência na Onion

A regra continua igual:

```text
Infrastructure -> Application -> Domain
```

Nunca o contrário.

## Força da Onion

A Onion deixa mais claro o papel das camadas internas. Ela é melhor para sistemas onde existe muita lógica de domínio e onde você quer separar nitidamente:

* Regras de negócio
* Casos de uso
* Infraestrutura

Ela também costuma ser mais intuitiva para times vindos de DDD.

## Fraqueza da Onion

A Onion é muito forte no centro da aplicação, mas menos explícita sobre os pontos de entrada e saída.

Ela não enfatiza tanto adapters e portas quanto a arquitetura hexagonal. Em aplicações muito integradas, isso pode gerar ambiguidade.

Exemplo: fica menos óbvio quais componentes são interfaces de entrada, quais são de saída e como cada integração deve ser tratada.

---

# Clean Architecture

Clean Architecture foi proposta por Robert C. Martin (Uncle Bob).

Ela basicamente combina ideias da Hexagonal, Onion, DCI e outras arquiteturas anteriores.

A organização clássica possui quatro camadas:

```text
+-----------------------------+
| Frameworks & Drivers        |
+-----------------------------+
| Interface Adapters          |
+-----------------------------+
| Use Cases                   |
+-----------------------------+
| Entities                    |
+-----------------------------+
```

## Entities

São as regras mais centrais e estáveis do negócio.

## Use Cases

Contêm a lógica específica da aplicação.

Por exemplo:

* Criar pedido
* Aprovar pagamento
* Calcular frete

## Interface Adapters

Transformam dados entre o mundo externo e o interno.

Exemplo:

```text
HTTP Request -> DTO -> Use Case
```

ou

```text
Entity -> Presenter -> JSON Response
```

## Frameworks & Drivers

Tudo que é externo:

* FastAPI
* Django
* PostgreSQL
* Kafka
* Redis

## Força da Clean Architecture

A Clean Architecture é a mais didática e a mais explícita sobre o fluxo completo.

Ela mostra claramente:

* Onde ficam entidades
* Onde ficam casos de uso
* Onde ficam adapters
* Onde entram frameworks

Por isso ela costuma ser a arquitetura mais fácil de ensinar e padronizar.

## Fraqueza da Clean Architecture

Ela tende a criar muitas camadas, DTOs, interfaces e objetos intermediários.

Em aplicações pequenas, isso pode gerar excesso de boilerplate.

É comum encontrar projetos simples com:

```text
Controller
DTO de entrada
Use Case
DTO interno
Entity
Repository Interface
Repository Concrete
DTO de saída
Presenter
```

Tudo isso para uma operação trivial.

Nesse ponto, a arquitetura deixa de proteger o sistema e passa a atrasar o desenvolvimento.

---

# Comparação direta

| Aspecto                    | Hexagonal                       | Onion                     | Clean Architecture                      |
| -------------------------- | ------------------------------- | ------------------------- | --------------------------------------- |
| Foco principal             | Ports e Adapters                | Camadas concêntricas      | Separação completa de responsabilidades |
| Centro do sistema          | Domínio                         | Domínio                   | Entities + Use Cases                    |
| Ênfase em integrações      | Muito alta                      | Média                     | Alta                                    |
| Ênfase em camadas internas | Média                           | Alta                      | Alta                                    |
| Clareza didática           | Média                           | Média                     | Alta                                    |
| Quantidade de boilerplate  | Média                           | Média                     | Alta                                    |
| Melhor para                | Sistemas com muitas integrações | Sistemas ricos em domínio | Times que querem estrutura explícita    |

---

# O que realmente muda na prática

Na prática, quase todo projeto sério mistura as três.

Exemplo comum:

* Organização interna inspirada em Onion
* Use Cases e Adapters inspirados em Clean Architecture
* Integrações modeladas como Ports and Adapters da Hexagonal

Estrutura típica:

```text
src/
 ├── domain/
 │    ├── entities/
 │    ├── value_objects/
 │    └── services/
 │
 ├── application/
 │    ├── use_cases/
 │    ├── ports/
 │    └── dto/
 │
 ├── infrastructure/
 │    ├── persistence/
 │    ├── messaging/
 │    └── external_services/
 │
 └── interfaces/
      ├── api/
      ├── cli/
      └── jobs/
```

Esse modelo já é, ao mesmo tempo:

* Onion, porque existe um núcleo central
* Hexagonal, porque existem portas e adapters
* Clean, porque há separação clara entre use cases, adapters e framework

---

# Trade-offs reais

A discussão importante não é “qual é melhor”, e sim “quanto isolamento vale a pena para este sistema”.

Se você aplicar essas arquiteturas em excesso em um CRUD pequeno, estará criando custo sem retorno. Você terá dezenas de arquivos para encapsular regras que poderiam caber em uma única classe.

Por outro lado, se você ignorar essas arquiteturas em um sistema que terá muitos módulos, integrações e regras complexas, o custo virá depois: acoplamento, dificuldade de testes, medo de mudar e refactors caros.

A regra prática é:

* Sistema pequeno e simples: use poucas camadas
* Sistema médio com crescimento esperado: use Onion ou Clean simplificada
* Sistema grande, rico em domínio e integrações: combine Onion + Hexagonal + Clean

O erro mais comum é copiar a estrutura de uma grande empresa em um projeto pequeno. O segundo erro mais comum é fazer o oposto: manter uma arquitetura improvisada mesmo quando o sistema já se tornou complexo.

Arquitetura não é um objetivo. É um mecanismo para controlar complexidade. Se a complexidade ainda não existe, simplifique. Se ela já existe, modularize cedo antes que o sistema fique caro demais para evoluir.