# Throttling

Throttling é uma técnica de controle de carga utilizada para limitar ou regular a taxa de processamento de requisições em um sistema. Diferente de simplesmente bloquear requisições excedentes, como ocorre em muitos casos de rate limiting, o throttling atua de forma mais controlada, reduzindo gradualmente a velocidade com que requisições são aceitas ou processadas. Seu objetivo principal é proteger o sistema contra sobrecarga, garantindo estabilidade e previsibilidade mesmo sob alta demanda.

Em sistemas reais, a carga de entrada nem sempre é constante. Picos de tráfego podem ocorrer de forma imprevisível, seja por aumento legítimo de usuários, falhas em sistemas downstream que geram retries em cascata ou até ataques maliciosos. Sem mecanismos de controle, esses picos podem saturar recursos como CPU, memória, conexões de banco de dados ou largura de banda, levando à degradação do sistema ou até indisponibilidade total. O throttling atua como uma camada de proteção contra esse tipo de cenário.

O funcionamento do throttling geralmente envolve a definição de limites de capacidade do sistema e a aplicação de regras que controlam como requisições são tratadas quando esses limites são atingidos. Em vez de aceitar todas as requisições imediatamente, o sistema pode atrasar, enfileirar ou até rejeitar parte delas. Esse comportamento permite suavizar picos de carga e evitar que o sistema ultrapasse sua capacidade máxima de processamento.

Uma das formas mais comuns de throttling é o uso de filas. Quando a taxa de entrada de requisições excede a capacidade de processamento, as requisições são colocadas em uma fila e processadas gradualmente. Esse modelo desacopla a taxa de entrada da taxa de processamento, permitindo que o sistema absorva picos temporários sem falhar imediatamente. No entanto, filas também introduzem latência adicional, e seu tamanho precisa ser controlado para evitar crescimento indefinido.

Outra abordagem é o throttling baseado em delay, onde o sistema introduz atrasos artificiais no processamento de requisições quando detecta alta carga. Esse atraso reduz a taxa efetiva de processamento e pode desencorajar clientes a enviar requisições em excesso, especialmente quando combinado com mecanismos de retry.

O throttling também pode ser aplicado de forma adaptativa. Em vez de limites fixos, o sistema ajusta dinamicamente sua taxa de aceitação com base em métricas como uso de CPU, latência ou taxa de erro. Por exemplo, se a latência começa a aumentar além de um limite aceitável, o sistema pode reduzir automaticamente o número de requisições que aceita, protegendo sua estabilidade.

É importante entender a diferença entre throttling e rate limiting. Enquanto o rate limiting define limites rígidos de requisições por cliente ou por período de tempo, geralmente resultando em rejeições imediatas (como HTTP 429), o throttling é mais focado em proteger o sistema como um todo, controlando a taxa global de processamento. Em muitos casos, ambos são utilizados em conjunto: rate limiting para controle por cliente e throttling para controle interno do sistema.

O throttling está fortemente relacionado ao conceito de backpressure. Backpressure é o mecanismo pelo qual um sistema sinaliza para seus produtores que ele não consegue processar mais dados naquele momento. O throttling pode ser visto como uma forma de implementar backpressure, limitando a entrada de novas requisições ou desacelerando o fluxo de dados.

Outro ponto importante é a interação entre throttling e experiência do usuário. Aplicar throttling de forma agressiva pode proteger o sistema, mas também pode degradar a experiência do usuário, introduzindo latência ou falhas. Por isso, é necessário equilibrar proteção e usabilidade, muitas vezes priorizando requisições críticas ou implementando diferentes níveis de serviço.

Em sistemas distribuídos, o throttling pode ser aplicado em diferentes camadas, como gateways de API, load balancers ou serviços internos. Aplicar throttling próximo à entrada do sistema pode evitar que requisições desnecessárias consumam recursos internos. Por outro lado, aplicar throttling em serviços internos pode proteger componentes específicos que possuem capacidade limitada.

O throttling também desempenha um papel importante em cenários de falha. Quando um serviço downstream está lento ou indisponível, o número de requisições pendentes pode crescer rapidamente. Sem throttling, isso pode levar a um efeito cascata, onde múltiplos serviços ficam sobrecarregados. Ao limitar a taxa de requisições, o sistema consegue se estabilizar e evitar propagação de falhas.

Além disso, o throttling pode ser combinado com outras estratégias, como circuit breaker e retry com backoff. Quando um serviço começa a falhar, o circuit breaker pode interromper chamadas, enquanto o throttling controla a taxa de novas tentativas. Isso reduz pressão sobre o sistema e aumenta a probabilidade de recuperação.

Outro aspecto relevante é a priorização de requisições. Em sistemas mais avançados, o throttling pode ser aplicado de forma diferenciada, permitindo que requisições mais importantes sejam processadas com prioridade, enquanto requisições menos críticas são atrasadas ou rejeitadas. Isso é comum em sistemas que oferecem diferentes níveis de serviço.

Do ponto de vista de implementação, o throttling pode ser realizado utilizando contadores, tokens (como no token bucket), filas ou algoritmos adaptativos. A escolha depende do tipo de sistema e dos requisitos de controle de carga.

Em resumo, throttling é uma técnica essencial para manter a estabilidade de sistemas sob carga variável. Ele não apenas protege contra sobrecarga, mas também permite que o sistema degrade de forma controlada em situações de alta demanda. Compreender e aplicar corretamente o throttling é fundamental para construir sistemas resilientes, previsíveis e capazes de operar sob condições reais de uso.
