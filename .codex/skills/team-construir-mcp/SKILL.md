---
name: team-construir-mcp
description: Construa ou diagnostique um MCP autorizado com contrato, compatibilidade, erros e controles de acesso verificáveis.
---

# Team — construir MCP

## Objetivo e entradas

Entregar uma integração MCP delimitada e compatível. Receba ferramentas/
recursos, transporte, esquema, cliente/servidor, autenticação/autorização,
versões e critérios de erro.

## Procedimento e decisões

1. Defina contrato de nomes, entradas, saídas, erros, idempotência e limites.
2. Confirme transporte e matriz cliente×servidor antes de implementar.
3. Implemente validação de entrada, erros seguros, timeouts e observabilidade
   sem registrar tokens ou dados sensíveis.
4. Diferencie autenticação de autorização e respeite ownership/escopo mínimo.
5. Valide handshake, ferramentas, recursos e falhas com versões identificadas;
   use `verify-and-stop` para a prova final.

## Limites e dependências

Não instale MCP, altere rede, habilite serviço ou conceda permissão por
descoberta. Não leia credenciais; use referências/variáveis já autorizadas.

## Entrega e evidências

Entregue contrato, implementação/arquivos, matriz de compatibilidade, erros,
autorização, comandos e riscos no formato do contrato.

## Impedimentos

Bloqueie se transporte, esquema, versão ou autoridade forem desconhecidos;
registre a decisão necessária sem presumir compatibilidade.
