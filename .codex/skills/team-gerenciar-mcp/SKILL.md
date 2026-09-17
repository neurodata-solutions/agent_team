---
name: team-gerenciar-mcp
description: Gerencie catálogo e ciclo de vida de MCPs, distinguindo descoberta, configuração, acesso e verificação.
---

# Team — gerenciar MCP

## Objetivo e entradas

Manter inventário decisório de MCPs sem alterar permissões. Receba nome,
origem, versão, ambiente, owner, transporte, dependências e matriz de acesso.

## Procedimento e decisões

1. Registre identidade, origem, versão e responsável com data e escopo.
2. Classifique cada item como encontrado, configurado, acessível, verificado,
   indisponível ou desativado; cada estado exige evidência própria.
3. Mapeie clientes, ferramentas/recursos, autorização e dependências sem ler
   valores secretos.
4. Registre mudanças de ciclo de vida, risco, rollback e próximo responsável.
5. Verifique o catálogo contra fontes identificadas e pare quando o critério
   estiver provado (`verify-and-stop`).

## Limites e dependências

Não conceda permissões, habilite serviços, instale servidores ou trate um
   registro declarado como funcionamento verificado.

## Entrega e evidências

Entregue catálogo, ownership, matriz de acesso, estado, data/origem,
pendências e riscos no formato do contrato; redija secrets.

## Impedimentos

Marque não verificado quando owner, origem, versão, acesso ou evidência faltar;
indique a fonte que precisa ser confirmada.
