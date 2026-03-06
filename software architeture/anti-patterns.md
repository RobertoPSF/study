# Anti-Patterns em Backend

## O que são Anti-Patterns

Anti-patterns são soluções recorrentes que parecem boas no começo, mas geram problemas estruturais no médio e longo prazo.

Eles não são erros óbvios. São decisões “convenientes” que acumulam dívida técnica silenciosa.

Um padrão resolve um problema.  
Um anti-pattern cria um problema futuro disfarçado de solução.

Se você não reconhece anti-patterns, você:

- escreve código que escala mal
- cria sistemas frágeis
- vira gargalo técnico na empresa
- perde entrevistas para quem enxerga trade-offs melhor

---

# Categoria 1 – Anti-patterns de Arquitetura Backend

## 1. God Object / God Class

Uma classe que faz tudo:

- valida
- chama API
- salva no banco
- loga
- trata erro
- transforma dados

Parece produtivo no começo, mas depois vira impossível de testar e manter.

Sinais claros:

- arquivos muito grandes
- múltiplas responsabilidades

Impacto:

- alto acoplamento
- testes difíceis
- mudanças perigosas

Correção:

- separar responsabilidades
- `controller ≠ service ≠ repository`

---

## 2. Tight Coupling (Acoplamento Forte)

O código depende diretamente de detalhes da infraestrutura.

Exemplo:

- lógica de negócio depende diretamente de biblioteca HTTP ou banco.

Impacto:

- difícil trocar banco
- difícil mockar dependências
- manutenção complicada

Correção:

- abstrações claras
- inversão de dependência

---

## 3. Premature Microservices

Criar microserviços antes de existir necessidade real.

Motivações comuns:

- copiar empresas grandes
- parecer mais sofisticado

Problemas:

- complexidade operacional
- deploy distribuído
- latência de rede
- observabilidade mais difícil

Regra prática:

> Se você não tem problema real de escala ou organização, microserviços são desperdício.

---

## 4. Shared Database Between Services

Múltiplos serviços acessando o mesmo banco ou tabela.

Impactos:

- schema vira contrato implícito
- mudanças quebram vários serviços
- independência entre serviços desaparece

---

## 5. Big Ball of Mud

Sistema sem arquitetura clara que cresce de forma desorganizada.

Características:

- dependências circulares
- lógica espalhada
- difícil entender onde alterar código

Esse anti-pattern geralmente surge gradualmente.

---

# Categoria 2 – Anti-patterns de Resiliência

## 6. Retry Sem Critério

Retry mal implementado pode:

- sobrecarregar APIs externas
- amplificar falhas
- causar cascatas de erro

Retry precisa definir:

- quando tentar novamente
- quantas tentativas
- intervalo entre tentativas (backoff)

---

## 7. Swallowing Exceptions

Ignorar erros silenciosamente.

Exemplo:

```python
try:
    process()
except:
    pass