Quando falamos em APIs externas, estamos falando de qualquer serviço que não está sob o seu controle operacional. Pode ser uma API pública, um serviço de um parceiro, um gateway interno de outro time ou até um microserviço “vizinho”. O ponto central é sempre o mesmo: você não controla latência, disponibilidade, nem comportamento em falha. Esse fato muda completamente como um backend sério deve ser construído.

O erro mais comum de desenvolvedores iniciantes é tratar chamadas externas como se fossem chamadas de função locais. Elas não são. Uma chamada externa é, por definição, uma operação de I/O remota, sujeita a atraso, falha parcial, falha total e comportamento imprevisível. Se você não parte dessa premissa, seu sistema vai quebrar em produção.

Quando seu backend chama uma API externa, três coisas ruins podem acontecer. Primeiro, ela pode responder lentamente. Segundo, ela pode não responder nunca. Terceiro, ela pode responder errado ou inconsistente. O timeout existe principalmente para lidar com o segundo caso, mas influencia todos os outros.

Timeout é, tecnicamente, o limite máximo de tempo que você está disposto a esperar por uma resposta. Conceitualmente, ele é uma afirmação de negócio disfarçada de detalhe técnico. Quando você define um timeout, você está dizendo:

“Depois desse ponto, o custo de esperar é maior do que o valor da resposta.”

Sem timeout, uma chamada externa pode ficar pendurada indefinidamente. Isso não é só um problema daquela requisição específica. Em servidores backend, threads, workers ou event loops são recursos finitos. Uma requisição travada consome memória, conexões e, dependendo do modelo de concorrência, bloqueia o processamento de outras requisições. Em efeito cascata, uma API externa lenta pode derrubar todo o seu sistema, mesmo que seu código esteja correto.

Por isso, timeout não é opcional. É uma regra básica de sobrevivência.

Existem diferentes tipos de timeout, e isso é algo que quase ninguém menciona, mas diferencia quem entende de quem só “usa biblioteca”.

O primeiro é o timeout de conexão, que limita quanto tempo você aceita gastar tentando abrir a conexão com o servidor remoto. Se esse tempo estourar, significa que o serviço está fora do ar, inacessível ou com problemas graves de rede.

O segundo é o timeout de leitura, que define quanto tempo você espera entre pacotes de dados depois que a conexão já foi estabelecida. Isso é importante porque alguns serviços aceitam a conexão rápido, mas demoram muito para responder de fato.

Em entrevistas, quando você diz “timeout”, o entrevistador espera que você saiba que não é uma coisa única e mágica, mas um conjunto de limites bem definidos.

Agora vem um ponto crítico: qual valor escolher para o timeout?

Não existe valor universal. Quem responde “2 segundos” ou “5 segundos” sem contexto está chutando. Timeout é definido por três fatores principais: expectativa do usuário, SLA do serviço externo e custo de degradação do seu sistema.

Se o seu endpoint faz parte de uma resposta síncrona ao usuário, você geralmente tem um orçamento total de latência. Por exemplo, se a página precisa responder em até 1 segundo, e você depende de duas APIs externas, você não pode permitir que cada uma consuma 1 segundo. Você precisa dividir esse orçamento.

Aqui aparece um conceito importante: latência composta. Se você faz chamadas externas em sequência, os tempos se somam. Se faz em paralelo, você paga pelo pior caso. Em ambos os cenários, timeout mal configurado destrói SLA.

Outro erro clássico é confundir timeout com retry. Timeout não resolve falha, ele apenas impede que você espere demais. Depois que o timeout acontece, você precisa decidir o que fazer. E essa decisão é arquitetural, não técnica.

Você pode tentar novamente (retry), pode devolver um erro, pode usar cache, pode devolver dados parciais. O timeout é só o gatilho que te força a tomar uma decisão.

Falando em retry, aqui existe uma armadilha importante: retry sem timeout é inútil, e timeout sem critério de retry é incompleto. Mas retry mal feito é pior do que não ter retry.

Se a API externa está lenta porque está sobrecarregada, fazer retry agressivo só piora o problema. Por isso, retry geralmente vem acompanhado de backoff exponencial, que aumenta o tempo entre tentativas, e de um limite máximo de tentativas.

Timeout define quando desistir de uma tentativa. Retry define quantas vezes vale a pena tentar novamente. Eles são complementares, mas independentes.

Voltando ao seu projeto: quando você consome APIs externas, a chamada não deve ficar espalhada pelo código. Ela deve estar encapsulada em um “client” ou “adapter”. Isso serve para três coisas: centralizar timeout, centralizar política de retry e facilitar testes.

Se cada parte do sistema chama a API externa de um jeito diferente, você perde controle operacional. Em entrevista, isso é visto como falta de maturidade.

Outro ponto avançado, mas importante: timeout não é só técnico, é de negócio. Às vezes, devolver um dado parcialmente desatualizado é melhor do que devolver erro. Às vezes, devolver erro rápido é melhor do que devolver resposta lenta. Isso depende do contexto.

Por exemplo, um sistema de cotação financeira pode preferir erro a dados antigos. Um sistema de recomendação pode preferir dados antigos a erro. O timeout é o ponto onde você escolhe qual dessas coisas acontece.

Existe também o conceito de timeout agressivo vs timeout conservador. Timeout agressivo melhora latência média, mas aumenta chance de falhas percebidas. Timeout conservador reduz falhas, mas aumenta latência e risco de saturação. Não existe escolha “certa”, existe escolha assumida conscientemente.

“Chamadas a APIs externas são operações não confiáveis. Timeout é obrigatório para proteger recursos internos, preservar SLA e forçar decisões de degradação controlada. Ele deve ser definido com base no orçamento de latência do sistema, no comportamento esperado do serviço externo e no impacto de falha para o negócio.”