# Aula Completa: Idempotência

Idempotência é uma propriedade de uma operação onde executar a mesma
ação múltiplas vezes produz o mesmo efeito que executá-la uma única vez.
O ponto central não é retornar a mesma resposta, mas sim não produzir
efeitos colaterais adicionais após a primeira execução bem-sucedida.

Matematicamente, uma função `f` é idempotente se:

    f(f(x)) = f(x)

Essa é a origem do conceito.

## Idempotência em Backend

Considere um endpoint:

    POST /create-user

Se chamado duas vezes com o mesmo payload e criar dois usuários
diferentes, não é idempotente.

Agora:

    PUT /users/123

Se chamado várias vezes com os mesmos dados e o estado final continuar
igual, é idempotente.

Idempotência não significa resposta idêntica, mas estado final idêntico.

## Métodos HTTP e Idempotência

Segundo a especificação HTTP:

-   GET → idempotente\
-   PUT → idempotente\
-   DELETE → idempotente\
-   POST → não é idempotente por definição\
-   PATCH → geralmente não é garantido

Isso é semântico, não garantia prática.

## Por que Idempotência Importa

Sistemas distribuídos falham. Requisições podem ser repetidas
automaticamente por:

-   Retries do cliente\
-   Load balancers\
-   Timeouts\
-   Falhas de rede

Sem idempotência você pode ter:

-   Cobranças duplicadas\
-   Pedidos duplicados\
-   Inconsistência de estado

## Tipos de Idempotência

### 1. Natural

Operações que sobrescrevem estado.

Exemplo:

    PUT /users/123
    {
      "name": "Roberto"
    }

Executar várias vezes mantém o mesmo estado final.

### 2. Artificial (Forçada)

Quando você precisa impedir duplicação manualmente.

Exemplo clássico: pagamentos.

### Idempotency Key

-   Cliente gera UUID\
-   Envia no header\
-   Servidor armazena chave + resultado\
-   Se repetir, retorna resultado armazenado

Exemplo:

    Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000

## Relação com Retry

Retry pressupõe idempotência. Caso contrário, cada tentativa pode gerar
efeitos colaterais extras.

## Mensageria e Sistemas Distribuídos

Em sistemas "at-least-once", mensagens podem ser processadas mais de uma
vez. Sua lógica deve ser idempotente.

Exemplo: processar pagamento com ID único e ignorar se já processado.

## Idempotência ≠

-   Segurança\
-   Pureza\
-   Imutabilidade\
-   Cacheabilidade

DELETE é idempotente mesmo que a segunda chamada retorne 404.

## Banco de Dados

Implementação comum via:

-   Chaves únicas\
-   Constraints\
-   Upsert\
-   INSERT ... ON CONFLICT DO NOTHING

## Aplicação no Projeto (API de Agregação)

-   Se for apenas leitura → naturalmente idempotente\
-   Retry exige proteção contra efeitos colaterais externos\
-   Cache não quebra idempotência

## Idempotência de Requisição vs Efeito

Você pode retornar 200 na primeira chamada e 409 na segunda e ainda ser
idempotente se o estado final for igual.

## Perguntas Clássicas de Entrevista

Como tornar um POST idempotente?

-   Idempotency-Key\
-   Persistência da chave\
-   Retornar resultado armazenado\
-   TTL\
-   Garantir atomicidade

Como evitar duplicidade com retry?

-   Constraint no banco\
-   Chave única\
-   Controle transacional

## Custos

Idempotência exige:

-   Armazenamento extra\
-   Complexidade\
-   Controle transacional\
-   Latência potencial

Aplique onde faz sentido.

## Resumo Mental

Idempotência protege contra repetição involuntária de operações.

Essencial em:

-   Sistemas distribuídos\
-   Operações financeiras\
-   Processamento de eventos\
-   APIs públicas

Implementada via:

-   Design correto de métodos HTTP\
-   Idempotency keys\
-   Constraints de banco\
-   Deduplicação

Se você implementa retry sem garantir idempotência, você está criando um
bug futuro.
