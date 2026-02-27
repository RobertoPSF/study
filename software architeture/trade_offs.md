# Trade-offs em Arquitetura de Software

## O que é um Trade-off?

Trade-off é escolher conscientemente perder algo para ganhar outra coisa
mais importante dentro de um contexto específico.

Não existe arquitetura "boa" de forma absoluta. Existe arquitetura
adequada às restrições do problema.

Todo ganho tem um custo invisível.

------------------------------------------------------------------------

## As 4 Grandes Restrições

Todo sistema vive sob quatro forças:

-   Tempo
-   Dinheiro
-   Complexidade
-   Risco

Você nunca reduz as quatro ao mesmo tempo.

Exemplos:

-   Mais escalável → mais complexo\
-   Mais consistente → menos disponível\
-   Mais desacoplado → mais latência\
-   Mais flexível → menos performance

------------------------------------------------------------------------

## Trade-offs Clássicos em Backend

### Consistência vs Disponibilidade (CAP)

Em sistemas distribuídos você não pode garantir simultaneamente:

-   Consistência forte
-   Disponibilidade total
-   Tolerância a partição

Você sempre escolhe dois.

Exemplos:

-   Sistema bancário → Consistência \> Disponibilidade\
-   Feed de rede social → Disponibilidade \> Consistência

------------------------------------------------------------------------

### Performance vs Legibilidade

Código extremamente otimizado tende a:

-   Ser menos claro
-   Mais difícil de manter

Código simples tende a:

-   Ser mais sustentável
-   Possivelmente menos performático

Regra madura: não otimizar antes de medir.

------------------------------------------------------------------------

### Escalabilidade vs Simplicidade

Monolito: - Simples - Fácil deploy - Fácil debug

Microsserviços: - Escaláveis - Isolamento de falhas - Complexidade
operacional alta

Pergunta-chave: você está pagando complexidade cedo demais?

------------------------------------------------------------------------

### Cache vs Consistência

Cache melhora:

-   Latência
-   Custo

Mas introduz:

-   Dados desatualizados
-   Complexidade de invalidação

Se o dado muda pouco → cache faz sentido.\
Se muda constantemente → pode virar problema.

------------------------------------------------------------------------

### Síncrono vs Assíncrono

Síncrono: - Simples - Previsível

Assíncrono: - Melhor uso de I/O - Mais difícil de raciocinar

Você troca simplicidade por escalabilidade.

------------------------------------------------------------------------

## Trade-offs Invisíveis

### Complexidade Cognitiva

Cada nova abstração reduz repetição, mas aumenta carga mental.

Arquitetura serve ao time, não ao ego técnico.

------------------------------------------------------------------------

### Flexibilidade Futura vs Entrega Rápida

Projetar para todos os cenários futuros geralmente é desperdício.

Otimize para mudanças frequentes, não para possibilidades remotas.

------------------------------------------------------------------------

### Generalização vs Especificidade

Código genérico: - Reutilizável - Abstrato - Difícil de entender

Código específico: - Claro - Limitado - Fácil de evoluir

Clareza quase sempre vence genialidade.

------------------------------------------------------------------------

## Como Pensar Trade-offs como Sênior

Sempre responda:

1.  Qual problema estou resolvendo?
2.  Quais são as restrições?
3.  O que estou sacrificando?
4.  O custo do sacrifício é aceitável?

Se você não sabe o que está sacrificando, você não entendeu sua decisão.

------------------------------------------------------------------------

## Aplicação Prática (Projeto API Agregadora)

### Cache Local vs Redis

Cache local: - Simples - Rápido - Não compartilhado

Redis: - Compartilhado entre instâncias - Mais infraestrutura

Se não há múltiplas instâncias, Redis pode ser overengineering.

------------------------------------------------------------------------

### Retry Agressivo vs Proteção do Sistema

Retry melhora disponibilidade, mas pode causar tempestade de
requisições.

Você troca disponibilidade local por estabilidade global.

------------------------------------------------------------------------

### Timeout Curto vs Experiência do Usuário

Timeout curto: - Resposta rápida - Mais falhas

Timeout longo: - Mais sucesso - UX pior

Escolha depende da prioridade do negócio.

------------------------------------------------------------------------

## Estrutura Ideal para Responder em Entrevista

1.  Contexto
2.  Opções disponíveis
3.  Critério de decisão
4.  Sacrifício assumido
5.  Justificativa

Exemplo:

Escolhi cache local em vez de Redis porque o sistema não precisava de
múltiplas instâncias. Isso reduziu complexidade operacional, mesmo
sacrificando compartilhamento entre instâncias.

------------------------------------------------------------------------

## Conclusão

Arquitetura não é sobre fazer certo.

É sobre escolher errado de forma consciente.

Todo sistema é um conjunto de perdas aceitáveis.

Se você consegue enxergar, explicar e justificar essas perdas, você
demonstra maturidade técnica real.
