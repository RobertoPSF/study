REST não é um framework, não é uma biblioteca e não é um protocolo novo. REST é um estilo arquitetural, definido por Roy Fielding, que descreve como sistemas distribuídos devem se comportar para serem simples, escaláveis, evolutivos e previsíveis. Quando alguém fala “API REST”, na prática está dizendo: “eu sigo (ou deveria seguir) esse conjunto de princípios ao expor recursos via HTTP”. O erro mais comum é achar que REST é apenas “usar JSON com HTTP”. Isso é superficial.

O ponto central do REST é o conceito de recurso. Um recurso é qualquer coisa que faça sentido ser identificada e manipulada: um usuário, um pedido, um pagamento, um relatório. Cada recurso possui um identificador único, normalmente uma URL. Essa URL identifica o recurso, não a ação. Em REST você não modela verbos na URL, você modela substantivos. A ação é representada pelo método HTTP, não pelo caminho.

Por isso, /users/123 faz sentido e /getUser?id=123 não é RESTful. No primeiro caso, você está apontando para um recurso (“o usuário 123”) e usando o método HTTP para dizer o que quer fazer com ele. No segundo, você está descrevendo uma ação, o que quebra a semântica do HTTP.

Os métodos HTTP não são apenas convenções; eles carregam semântica forte. GET significa recuperar uma representação do recurso. Ele deve ser seguro (não causar efeitos colaterais) e idempotente (chamar uma vez ou dez vezes tem o mesmo efeito). POST é usado para criar recursos ou executar operações não idempotentes. PUT substitui completamente um recurso existente, enquanto PATCH o modifica parcialmente. DELETE remove um recurso. Em entrevistas, o detalhe importante não é decorar isso, mas entender as consequências: caches, proxies e clientes confiam nessas propriedades.

Falando em idempotência: esse é um conceito central. Um método idempotente é aquele que, quando executado múltiplas vezes, produz o mesmo resultado final. PUT e DELETE são idempotentes por definição; POST não é. Isso importa porque sistemas distribuídos falham. Se um cliente não sabe se a requisição chegou, ele pode reenviar. Se sua API não respeita idempotência onde deveria, você cria bugs difíceis de rastrear. Em entrevistas backend, isso aparece o tempo todo.

REST também exige statelessness. Isso significa que cada requisição deve conter toda a informação necessária para ser processada. O servidor não deve depender de estado de sessão armazenado entre requisições. Isso não é um detalhe acadêmico; isso é o que permite escalabilidade horizontal. Se qualquer instância pode atender qualquer requisição, você pode adicionar e remover servidores sem dor. Autenticação via token, por exemplo, é uma consequência direta desse princípio.

Outro pilar é o uso correto de status codes HTTP. Eles não são cosméticos. Eles são parte do contrato. Um 200 OK indica sucesso genérico. 201 Created indica que um recurso foi criado, geralmente acompanhado de um header Location apontando para o novo recurso. 204 No Content indica sucesso sem corpo de resposta, muito comum em deletes. Códigos 4xx indicam erro do cliente (requisição inválida, falta de permissão, recurso inexistente). 5xx indicam erro do servidor. Em uma API REST bem feita, o cliente consegue entender o que aconteceu sem ler a documentação, apenas pelo status code.

Versionamento é outro tema que separa amador de profissional. APIs evoluem. Quebrar clientes em produção é caro. REST não define como versionar, mas práticas comuns existem. Versionar pela URL (/v1/users) é simples e explícito. Versionar por header é mais elegante, mas mais complexo. O importante é: não versionar é erro, e mudar comportamento sem mudar versão é ainda pior. Em entrevistas, o que importa é você conseguir explicar por que escolheu uma estratégia, não qual.

REST também fala de representações. Um recurso não é o JSON em si; o JSON é apenas uma representação do estado do recurso naquele momento. Amanhã você poderia oferecer a mesma API em XML ou outro formato via Accept header (content negotiation). Na prática, quase todo mundo usa JSON, mas entender que recurso ≠ representação ajuda a pensar corretamente sobre design.

Outro conceito frequentemente ignorado é o uso de HATEOAS (Hypermedia as the Engine of Application State). Em REST “puro”, o servidor deveria guiar o cliente através de links, informando quais ações são possíveis a partir daquele estado. Na prática, quase nenhuma API comercial implementa HATEOAS completamente. Em entrevistas, não é esperado que você implemente, mas é bom saber o que é e saber dizer: “conheço o conceito, mas geralmente não aplico por custo-benefício”. Isso mostra maturidade.

Paginação, filtros e ordenação também fazem parte do design REST. Você não cria endpoints novos para cada variação; você usa query parameters. /users?page=2&limit=20&sort=created_at é RESTful. /getUsersByPage não é. A URL identifica o recurso, os parâmetros refinam a representação. Esse detalhe costuma cair em entrevistas práticas.

Por fim, REST não é sobre “ficar bonito”, é sobre contrato claro e previsvel. Uma boa API REST permite que outro time a consuma sem conversar com você. Uma API ruim exige alinhamento humano constante. Em produção, isso é custo. Em entrevista, isso é sinal de imaturidade.

## Idempotência — o conceito real (não a definição rasa)

Idempotência vem da matemática e significa, essencialmente, que aplicar a mesma operação várias vezes produz o mesmo estado final do sistema. Em sistemas distribuídos, isso não é luxo, é mecanismo de sobrevivência. Redes falham, timeouts acontecem, conexões caem depois que o servidor já processou a requisição, mas antes do cliente receber a resposta. Quando isso acontece, o cliente não sabe se o servidor executou a operação ou não. A única reação segura é reenviar.

Agora entra o ponto crítico: o que acontece se a mesma requisição for processada duas vezes?

Se o estado final for o mesmo, não há problema. Se não for, você cria inconsistência, duplicação e efeitos colaterais difíceis de detectar. Isso é exatamente o problema que idempotência resolve.

Por que PUT é idempotente

PUT significa substituir completamente o estado de um recurso por uma nova representação. Se você envia o mesmo payload para o mesmo recurso, não importa quantas vezes, o estado final será igual.

Exemplo:
Você faz:

```
PUT /users/123
{
  "name": "Roberto",
  "email": "roberto@email.com"
}
```


- A primeira chamada cria ou atualiza o usuário.
- A segunda chamada não muda nada.
- A terceira também não.

O estado final do recurso /users/123 é exatamente o mesmo após 1 ou 100 requisições. Isso é idempotência. É por isso que PUT é ideal quando o cliente conhece o identificador do recurso e quer definir o estado dele explicitamente.

Por que DELETE é idempotente

DELETE significa “garantir que o recurso não exista mais”. Se você apaga um recurso uma vez, ele deixa de existir. Se você apaga de novo, ele continua não existindo.

O efeito colateral acontece só na primeira chamada. As seguintes não alteram o estado do sistema. O resultado final é sempre o mesmo: o recurso não existe.

Mesmo que o servidor responda 404 Not Found em chamadas posteriores, a intenção semântica continua sendo idempotente: o estado final não muda.

Por que POST não é idempotente

POST é usado para criar novos recursos ou executar operações não determinísticas. Cada chamada pode gerar um novo efeito colateral.

Exemplo clássico:

```
POST /orders
{
  "product_id": 10,
  "quantity": 1
}
```


- Primeira chamada → cria pedido #101
- Segunda chamada → cria pedido #102
- Terceira chamada → cria pedido #103

O estado final do sistema muda a cada requisição, mesmo com o mesmo payload. Isso viola idempotência por definição.

É por isso que POST é perigoso em sistemas distribuídos. Se o cliente não recebe a resposta e reenvia, você pode criar pedidos duplicados, cobranças duplicadas, eventos duplicados. Em produção, isso é fonte clássica de bugs financeiros.

Idempotência “forçada” em POST (detalhe avançado)

Apesar de POST não ser idempotente por padrão, você pode torná-lo idempotente por contrato usando uma chave de idempotência. O cliente envia um identificador único (por exemplo, um UUID) no header. O servidor registra essa chave e garante que requisições com a mesma chave produzam o mesmo efeito.

Isso é comum em APIs de pagamento. Em entrevista, mencionar isso mostra maturidade real.

HATEOAS — o que é de verdade (e por que quase ninguém usa)

HATEOAS significa Hypermedia as the Engine of Application State. A ideia é que o servidor não apenas retorne dados, mas também informe ao cliente quais ações são possíveis a partir daquele estado, através de links.

Exemplo conceitual:

```
GET /orders/123


Resposta:

{
  "id": 123,
  "status": "PAID",
  "_links": {
    "cancel": { "href": "/orders/123/cancel", "method": "POST" },
    "refund": { "href": "/orders/123/refund", "method": "POST" }
  }
}
```

O cliente não precisa saber previamente quais operações são válidas. Ele descobre isso dinamicamente. O servidor controla o fluxo da aplicação.

Isso é REST “puro”. O problema é custo. Implementar HATEOAS bem exige:

- contratos mais complexos
- clientes mais inteligentes
- versionamento mais cuidadoso

Na prática, a maioria das APIs REST ignora HATEOAS ou usa apenas parcialmente. Em entrevista, a resposta madura é: “Conheço o conceito, mas raramente aplico completamente por custo-benefício. Uso links apenas quando agregam valor real.”

Cache em HTTP — por que isso importa tanto

HTTP foi desenhado desde o início para ser cacheável. Cache não é um hack; é parte do protocolo. Quando bem usado, reduz latência, custo e carga no backend.

O princípio é simples: se uma resposta pode ser reutilizada, não há motivo para recalcular ou buscar novamente.

O controle de cache acontece principalmente via headers. O mais importante é Cache-Control. Ele define se e por quanto tempo uma resposta pode ser cacheada.

Exemplo:

Cache-Control: max-age=60


Isso diz que a resposta é válida por 60 segundos. Durante esse tempo, clientes ou proxies podem reutilizá-la sem chamar o servidor.

Outro conceito importante é cache validation. Em vez de reenviar o conteúdo inteiro, o cliente pode perguntar: “isso mudou?”. Isso é feito com ETag ou Last-Modified. O cliente envia o valor que tem, o servidor responde 304 Not Modified se nada mudou. Isso economiza banda e processamento.

Importante: GET é cacheável por padrão, desde que o servidor permita. POST, PUT e DELETE não são cacheáveis, porque mudam estado. Por isso, respeitar semântica HTTP influencia diretamente desempenho.