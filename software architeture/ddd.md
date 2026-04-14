# Domain-Driven Design (DDD)

## Introdução

Domain-Driven Design não é sobre tecnologia, frameworks ou padrões isolados. É sobre alinhar software com o negócio real. A premissa central é simples: sistemas complexos falham não por falta de código, mas por falta de entendimento do domínio.

DDD propõe que o modelo de domínio seja o centro do sistema e que ele seja construído em colaboração direta com especialistas do negócio. O código deixa de ser apenas uma implementação e passa a ser uma representação explícita das regras e conceitos do mundo real.

Os três pilares que mais causam impacto prático são: Ubiquitous Language, Bounded Contexts e Aggregates. Se você não entende esses três profundamente, você não está aplicando DDD — está apenas organizando pastas.

---

# Ubiquitous Language

## O problema

Em muitos sistemas, existe uma desconexão entre como o negócio fala e como o código é escrito.

Exemplo clássico:

* O negócio fala “Cliente Premium”
* O código chama de `UserType = 2`

Isso parece pequeno, mas escala mal. Com o tempo, cada parte do sistema usa termos diferentes para o mesmo conceito, ou pior, o mesmo termo para conceitos diferentes.

Resultado:

* Ambiguidade
* Bugs de interpretação
* Regras implementadas incorretamente

## O conceito

Ubiquitous Language é uma linguagem compartilhada entre:

* Desenvolvedores
* Product owners
* Especialistas de domínio

Essa linguagem deve aparecer em todos os lugares:

* Código
* Nomes de classes
* Métodos
* Documentação
* Conversas

Exemplo correto:

```python
class PremiumCustomer:
    def apply_discount(self, order):
        ...
```

Não existe tradução entre negócio e código. Eles são a mesma coisa.

## Implicações reais

Se o negócio muda o termo, o código muda junto.

Se existe dúvida sobre um conceito, o problema não é técnico — é de entendimento do domínio.

Se você está criando nomes genéricos como `Manager`, `Service`, `Helper`, você já perdeu a linguagem ubíqua.

---

# Bounded Context

## O problema

Em sistemas maiores, a mesma palavra pode ter significados diferentes dependendo do contexto.

Exemplo:

“Pedido” pode significar:

* Um carrinho ainda editável (checkout)
* Um pedido fechado (billing)
* Um envio em andamento (logística)

Se você tenta unificar tudo em um único modelo global, o sistema vira um monstro inconsistente.

## O conceito

Bounded Context define uma fronteira onde um modelo específico é válido.

Dentro de um contexto:

* Termos têm significado claro
* Regras são consistentes
* Modelo é coeso

Fora desse contexto, nada disso é garantido.

## Exemplo

```text
[ Checkout Context ]
Pedido = algo editável

[ Billing Context ]
Pedido = algo fechado e faturado

[ Shipping Context ]
Pedido = algo em transporte
```

Cada contexto pode ter:

* Modelos diferentes
* Estruturas diferentes
* Regras diferentes

E isso é correto.

## Integração entre contextos

Contextos se comunicam, mas não compartilham modelos diretamente.

Formas comuns de integração:

* APIs
* Eventos
* Anti-corruption layer (ACL)

Exemplo de ACL:

```text
Sistema A (Pedido)
    ↓
[ Tradução ]
    ↓
Sistema B (Order)
```

Você traduz conceitos em vez de compartilhar classes.

## Implicações reais

Se você tem um único modelo gigante para toda a empresa, você não tem DDD.

Se múltiplas equipes brigam pelo significado de uma entidade, você não tem boundaries claros.

Bounded Context é tanto uma decisão técnica quanto organizacional.

---

# Aggregates

## O problema

Sem limites claros, qualquer parte do sistema pode modificar qualquer entidade.

Exemplo ruim:

```python
order.customer.balance -= 100
order.items[0].price = 0
```

Isso permite estados inválidos e regras quebradas.

## O conceito

Aggregate é um conjunto de entidades tratadas como uma unidade de consistência.

Ele possui:

* Um Aggregate Root
* Regras de consistência internas
* Controle de acesso

Somente o Aggregate Root pode ser acessado diretamente.

## Exemplo

```python
class Order:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        if quantity <= 0:
            raise Exception("Invalid quantity")
        self.items.append((product, quantity))
```

Você não acessa `items` diretamente de fora.

Você usa métodos que garantem invariantes.

## Regras importantes

* Um Aggregate deve ser pequeno
* Deve proteger invariantes
* Deve ser carregado e salvo como unidade

## Consistência

Consistência forte acontece dentro do aggregate.

Entre aggregates, você normalmente usa consistência eventual.

Exemplo:

* Pedido criado
* Evento disparado
* Estoque atualizado depois

Você não tenta manter tudo sincronizado em uma única transação.

## Implicações reais

Se seu aggregate é gigante, você criou um monólito interno.

Se qualquer classe pode modificar qualquer entidade, você não tem aggregate.

Se você tenta garantir consistência global imediata, você vai travar escalabilidade.

---

# Como tudo se conecta

DDD não é um conjunto de peças isoladas. Elas se reforçam.

* Ubiquitous Language define como você fala
* Bounded Context define onde cada linguagem vale
* Aggregates definem como proteger consistência dentro desse contexto

Fluxo típico:

```text
Contexto definido
    ↓
Linguagem ubíqua estabelecida
    ↓
Modelo criado
    ↓
Aggregates protegem regras
    ↓
Contextos se integram via contratos
```

Se você pula qualquer etapa, o sistema degrada.

---

# Trade-offs reais

DDD tem custo alto.

Você está trocando velocidade inicial por:

* Clareza
* Manutenibilidade
* Escalabilidade organizacional

Se o sistema é simples, isso é desperdício.

Se o sistema é complexo e você ignora DDD, você paga depois com juros.

Erros comuns:

* Usar DDD para CRUD simples
* Criar aggregates gigantes
* Ignorar bounded contexts
* Tratar DDD como estrutura de pastas

DDD exige disciplina e entendimento contínuo do domínio. Não é algo que você "instala" no projeto.
