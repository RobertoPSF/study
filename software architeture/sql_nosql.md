SQL e NoSQL diferem antes de tudo na forma como modelam dados e garantem consistência.
SQL é baseado no modelo relacional: dados organizados em tabelas, com colunas bem definidas, tipos fixos, chaves primárias, chaves estrangeiras e relacionamentos explícitos. NoSQL é um conjunto de abordagens que abandonam parte ou toda essa rigidez para ganhar flexibilidade, escala ou disponibilidade.

Em SQL, o esquema vem antes dos dados. Você define a estrutura, depois insere os registros. Em NoSQL, na maioria dos casos, os dados vêm antes do esquema, ou o esquema é implícito e flexível.

Isso já diz muito sobre quando usar cada um.

No mundo SQL, o pilar é o ACID: Atomicidade, Consistência, Isolamento e Durabilidade.

Atomicidade significa que uma transação acontece por completo ou não acontece.
Consistência significa que o banco nunca entra em um estado inválido segundo suas regras.
Isolamento garante que transações concorrentes não se interfiram indevidamente.
Durabilidade garante que, uma vez confirmada, a transação não será perdida.

Esse conjunto é o que torna bancos SQL excelentes para dados críticos, como:

sistemas financeiros

pedidos

estoque

qualquer coisa que não pode “ficar errada nem por um segundo”

Em troca disso, SQL cobra um preço: escala horizontal é mais difícil, especialmente quando você precisa manter fortes garantias transacionais entre muitos nós.

NoSQL surge quando o problema muda.

Quando o volume cresce demais, quando a estrutura dos dados muda frequentemente, quando você precisa responder rápido mesmo com falhas, as garantias rígidas do SQL passam a ser um gargalo.

NoSQL geralmente relaxa alguma garantia do ACID para ganhar:

escalabilidade horizontal

disponibilidade

flexibilidade de modelo

Aqui entra o CAP Theorem, que não é opcional saber.

Em sistemas distribuídos, você só pode garantir dois de três:

Consistência (todos veem o mesmo dado ao mesmo tempo)

Disponibilidade (o sistema sempre responde)

Tolerância a partições (continua funcionando mesmo com falhas de rede)

Bancos SQL tradicionais priorizam Consistência + Partição, sacrificando disponibilidade em alguns cenários.
Muitos bancos NoSQL priorizam Disponibilidade + Partição, aceitando consistência eventual.

Esse é o ponto que separa júnior de pleno em entrevista.

Agora, NoSQL não é uma coisa só. Ele se divide em categorias, e confundir isso é erro grave.

Existem quatro famílias principais:

- Key-Value
Você tem uma chave e um valor opaco. Extremamente rápido, extremamente simples. Ótimo para cache, sessões, contadores. Horrível para consultas complexas.

- Documentos
Armazenam documentos JSON. Flexíveis, fáceis de evoluir, bons para dados sem estrutura fixa. Consultas mais ricas que key-value, mas ainda longe da expressividade do SQL.

- Colunar (Wide Column)
Modelados para leitura massiva e escrita distribuída. Ótimos para grandes volumes e alta disponibilidade, ruins para joins e consultas ad-hoc.

- Grafos
Otimizados para relacionamentos complexos e profundos. Excelentes para redes, recomendações, fraudes. Não são substitutos gerais de bancos relacionais.

Saber isso mostra maturidade.

Agora vamos ao ponto que mais reprova candidatos: joins e normalização.

SQL foi feito para dados normalizados. Você evita duplicação, mantém integridade referencial e usa joins para recompor a informação.

NoSQL normalmente trabalha com dados desnormalizados. Você aceita duplicação para ganhar leitura rápida.
Isso significa que escrita é mais complexa, porque atualizar um dado pode exigir atualizar múltiplos documentos.

Se você diz em entrevista que NoSQL “simplifica tudo”, você está errado.
Ele simplifica leitura e escala, mas complica consistência e manutenção.

Outro ponto crítico: consultas.

SQL tem uma linguagem declarativa poderosa. Você diz o que quer, não como obter. O otimizador decide o plano de execução.

NoSQL geralmente exige que você modele o dado para a consulta.
Se sua consulta muda depois, muitas vezes o modelo precisa mudar junto.

Por isso, NoSQL funciona melhor quando:

padrões de acesso são bem conhecidos

consultas são previsiveis

leitura é muito mais frequente que escrita

Agora, um erro comum: achar que NoSQL é sempre mais rápido.

Isso é falso.

SQL é extremamente rápido quando bem indexado e bem modelado.
NoSQL é rápido quando você faz exatamente o que ele foi projetado para fazer.

Usar NoSQL para simular SQL é uma das piores decisões arquiteturais possíveis.

Em entrevista, a pergunta real não é “qual é melhor?”, mas sim:

“Por que você escolheu esse banco para esse problema?”

Uma resposta madura soa assim:

“Escolhi SQL porque preciso de transações fortes, integridade referencial e consultas complexas. O volume é previsível e a consistência é crítica.”

Ou:

“Escolhi NoSQL porque o volume é alto, o esquema é flexível e priorizo disponibilidade e leitura rápida, aceitando consistência eventual.”

Isso mostra que você entende o custo da escolha, não só o benefício.

Agora, a parte que quase ninguém fala: na prática, sistemas modernos usam os dois.

É comum ver:

SQL para dados transacionais

NoSQL para cache, busca, eventos ou leitura massiva

Isso se chama poliglot persistence, e mencionar isso em entrevista é ponto extra.

SQL é previsível, seguro, consistente e expressivo — ideal para dados críticos.
NoSQL é flexível, escalável e disponível — ideal para grandes volumes e padrões bem definidos.
Nenhum substitui o outro. Quem tenta usar um como se fosse o outro normalmente paga caro depois.