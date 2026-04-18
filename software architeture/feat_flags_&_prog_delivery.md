# Feature Flags & Progressive Delivery (Canary, Blue/Green, A/B)

## Introdução

Feature Flags e Progressive Delivery existem para resolver um problema recorrente em sistemas em produção: como mudar comportamento sem assumir risco desnecessário. Deploy não deveria ser um momento de tensão, mas na prática ainda é, porque muitas vezes deploy e release estão acoplados. Você sobe código novo e automaticamente expõe isso para todos os usuários.

Esses conceitos quebram essa ligação. Você passa a separar duas coisas diferentes: disponibilizar código e ativar comportamento. Isso muda completamente a forma como você evolui um sistema.

## O problema sem controle de release

Sem Feature Flags ou estratégias de rollout, o fluxo é simples e perigoso. Você desenvolve, faz deploy e todos os usuários recebem a nova versão ao mesmo tempo. Se houver problema, rollback vira a única saída, o que pode ser lento, arriscado e nem sempre possível.

Além disso, você perde a capacidade de testar comportamento em produção de forma controlada. Tudo vira “big bang”.

## Feature Flags

Feature Flags são condicionais que permitem ativar ou desativar funcionalidades em tempo de execução, sem necessidade de redeploy.

Na prática, você escreve código que pode seguir caminhos diferentes dependendo de uma configuração externa.

Em vez de:

```python
if new_logic:
    execute_new()
else:
    execute_old()
```

Você controla isso via flag:

```python
if feature_flag("new_logic"):
    execute_new()
else:
    execute_old()
```

A decisão deixa de estar hardcoded e passa a ser controlada externamente.

Isso permite ativar uma feature para uma porcentagem de usuários, para um grupo específico ou até para um único usuário.

## Tipos de Feature Flags

Nem todas as flags são iguais, e aqui existe um ponto importante que muita gente ignora. Existem flags temporárias e flags permanentes.

Flags de release são usadas para liberar funcionalidades gradualmente e devem ser removidas depois.

Flags de experimentação são usadas para testes A/B.

Flags operacionais permitem ligar ou desligar comportamentos em produção, como desabilitar uma integração externa.

O erro comum é deixar flags acumularem. Isso cria dívida técnica invisível.

## Progressive Delivery

Progressive Delivery é a prática de liberar mudanças gradualmente, reduzindo risco e aumentando controle.

Feature Flags são uma ferramenta para isso, mas não a única. Estratégias de deploy também fazem parte.

A ideia central é simples: não exponha mudanças para todos de uma vez.

## Canary Release

No canary release, você libera uma nova versão para uma pequena porcentagem de usuários ou instâncias.

Se tudo funcionar bem, você aumenta gradualmente essa porcentagem.

Se algo der errado, o impacto é limitado.

Isso funciona bem quando você quer validar comportamento em produção com risco controlado.

O ponto crítico aqui é observabilidade. Sem métricas claras, você não sabe se o canary está funcionando ou falhando.

## Blue/Green Deployment

No blue/green, você mantém duas versões completas do sistema.

Uma versão está ativa (blue) e a outra está pronta para assumir (green). Quando você decide fazer o switch, o tráfego é redirecionado de uma para outra.

Isso permite rollback quase imediato.

A desvantagem é custo. Você precisa manter duas infraestruturas completas rodando.

Além disso, não há granularidade. Ou você muda tudo, ou não muda nada.

## A/B Testing

A/B testing é uma forma de experimentação onde diferentes versões são expostas para diferentes grupos de usuários.

Diferente de canary, o objetivo aqui não é apenas validar estabilidade, mas comparar comportamento.

Você pode medir conversão, retenção ou qualquer métrica relevante.

Isso normalmente é feito com Feature Flags que direcionam usuários para variações diferentes.

O ponto crítico é disciplina em métricas. Sem definição clara de sucesso, A/B testing vira achismo com estatística superficial.

## Relação entre os conceitos

Esses conceitos não competem entre si. Eles se complementam.

Feature Flags permitem controlar comportamento em nível de código.

Canary controla rollout em nível de tráfego.

Blue/Green controla versões em nível de infraestrutura.

A/B testing usa flags para experimentação.

Sistemas maduros combinam essas abordagens.

## O que muda na prática

Você passa a tratar deploy como um evento técnico e release como uma decisão de negócio.

Isso permite:

* deploy contínuo sem medo
* validação gradual
* rollback rápido sem redeploy
* experimentação controlada

Mas isso só funciona se houver disciplina.

## Trade-offs reais

Feature Flags adicionam complexidade ao código. Cada flag é um caminho alternativo que precisa ser mantido e testado.

Se você não remove flags antigas, o sistema vira um conjunto de ifs difíceis de entender.

Progressive Delivery exige maturidade em observabilidade. Sem métricas, você não sabe quando promover ou reverter mudanças.

Canary pode mascarar problemas que só aparecem em escala.

Blue/Green aumenta custo de infraestrutura.

A/B testing pode gerar decisões erradas se análise estatística for fraca.

## Quando usar

Se você faz deploys frequentes e quer reduzir risco, Feature Flags já são úteis.

Se seu sistema tem tráfego suficiente para validar comportamento gradualmente, canary faz sentido.

Se rollback rápido é crítico, blue/green ajuda.

Se você quer otimizar métricas de produto, A/B testing é essencial.

Se você não tem observabilidade básica, nenhum desses vale a pena ainda.

