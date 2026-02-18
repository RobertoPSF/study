# Tratamento de Erros em Backend

## 1. O que é um erro?

Erro não é simplesmente "algo deu errado".\
Erro é uma quebra de expectativa entre contrato e execução.

Sempre que existe um sistema, existem contratos: - Contrato entre função
e chamador\
- Contrato entre API e cliente\
- Contrato entre serviço e banco\
- Contrato entre seu sistema e outro externo

Erro é quando esse contrato não é cumprido.

### Categorias de erro:

1.  Erros de programação (bugs)
2.  Erros de domínio (regra de negócio)
3.  Erros de infraestrutura (rede, banco, latência, timeout)

Misturar todos em um único bloco `try/except` é perda de controle
arquitetural.

------------------------------------------------------------------------

## 2. Erro esperado vs erro inesperado

### Erro esperado

-   Input inválido
-   Recurso não encontrado
-   Autenticação inválida

Faz parte do fluxo normal e deve ser tratado explicitamente.

### Erro inesperado

-   NullPointer
-   Divisão por zero
-   Falha de conexão inesperada
-   Exceção não mapeada

Indica quebra estrutural do sistema.

------------------------------------------------------------------------

## 3. Tratamento por camada

Erro deve ser tratado na camada adequada:

-   **Controller** → Traduz erro para HTTP\
-   **Service** → Define regras de negócio\
-   **Client** → Lida com erros externos\
-   **Infra** → Trata detalhes técnicos

Nunca deixe detalhes técnicos vazarem entre camadas.

------------------------------------------------------------------------

## 4. Erro deve ser informativo

Erro deve responder: - O que aconteceu? - O que significa? - O que pode
ser feito?

### Exemplo ruim:

``` json
{ "error": "KeyError: 'id'" }
```

### Exemplo correto:

``` json
{
  "error": "invalid_request",
  "message": "Field 'id' is required."
}
```

------------------------------------------------------------------------

## 5. Códigos HTTP importantes

-   400 --- erro do cliente\
-   401 --- não autenticado\
-   403 --- proibido\
-   404 --- não encontrado\
-   409 --- conflito\
-   422 --- erro de validação\
-   500 --- erro interno\
-   503 --- indisponível temporariamente

Nunca responda tudo com 500.

------------------------------------------------------------------------

## 6. Captura vs propagação

Só capture erro quando: - Pode resolver - Pode enriquecer contexto -
Pode transformar em algo mais significativo

Nunca engula exceções silenciosamente.

------------------------------------------------------------------------

## 7. Encapsulamento de erro

Nunca exponha exceções técnicas cruas.

Exemplo: Timeout externo → transformar em `ExternalServiceTimeout`

Isso desacopla o sistema da biblioteca usada.

------------------------------------------------------------------------

## 8. Retry

Pergunta obrigatória: A operação é idempotente?

Retry deve ter: - Limite - Backoff exponencial - Critério claro

Retry infinito é autossabotagem.

------------------------------------------------------------------------

## 9. Timeout

Chamada externa sem timeout é risco sistêmico.

Timeout protege: - Threads - Pool de conexões - Estabilidade geral

------------------------------------------------------------------------

## 10. Fallback e degradação

Se dependência falhar: - Usar cache - Retornar parcial - Retornar versão
reduzida

Nunca mentir sobre estado dos dados.

------------------------------------------------------------------------

## 11. Logs

Erro sem log é erro invisível.

Logs devem conter: - Nível correto (warning, error, critical) - Contexto
(request_id, endpoint) - Mensagem clara

Nunca logar dados sensíveis.

------------------------------------------------------------------------

## 12. Erros de domínio

Exemplo: Saldo insuficiente não é erro técnico, é regra de negócio.

Modelar como exceção de domínio ou retorno estruturado.

------------------------------------------------------------------------

## 13. Fail Fast

Validar entrada na borda do sistema.\
Quanto mais cedo falha, menor o dano.

------------------------------------------------------------------------

## 14. Anti-patterns

-   Engolir exceção\
-   Retornar None silenciosamente\
-   Usar Exception genérica para tudo\
-   Misturar erro técnico com regra de negócio\
-   Retry cego\
-   Não diferenciar 500 de 503

------------------------------------------------------------------------

## 15. O que dizer em entrevista

1.  Diferencio erro esperado de inesperado\
2.  Trato erro na camada adequada\
3.  Encapsulo exceções externas\
4.  Uso timeout e retry com critério\
5.  Retorno HTTP adequado\
6.  Registro logs estruturados\
7.  Documento trade-offs

------------------------------------------------------------------------

## 16. Aplicação no projeto

Sua API de agregação deve ter:

-   Timeout nas APIs externas\
-   Retry controlado\
-   Exceção própria (`ExternalServiceError`)\
-   Fallback com cache\
-   Resposta parcial quando necessário\
-   Log estruturado com request_id\
-   HTTP 503 quando dependência indisponível

------------------------------------------------------------------------

## 17. Mentalidade final

Tratamento de erro não é evitar que o sistema quebre.\
É decidir **como ele quebra**.

Sistema imaturo quebra de forma imprevisível.\
Sistema maduro quebra de forma controlada.
