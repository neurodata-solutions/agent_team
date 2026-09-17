---
name: team-validar-entrega
description: Valide uma entrega contra critérios, integrações e fluxos completos e emita parecer sustentado por evidências.
---

# Team — validar entrega

## Objetivo e entradas

Decidir passar, reprovar ou bloquear uma entrega. Receba critérios prévios,
versão/origem, evidências de testes, dependências, integrações e ambiente.

## Procedimento e decisões

1. Transforme cada critério em evidência observável e identifique lacunas.
2. Confirme versão e origem dos artefatos; não misture resultados de commits ou
   ambientes diferentes.
3. Verifique fluxos ponta a ponta e fronteiras entre componentes somente no
   escopo autorizado; coordene evidências do Tester.
4. Separe defeito do produto, teste, ambiente e requisito; bloqueie quando a
   prova depender de serviço não identificado ou não saudável.
5. Emita decisão com risco residual e condição objetiva de encerramento.

## Limites e dependências

QA não substitui testes nem autoriza deploy. Não altere código/serviços e não
   execute evals de agentes salvo autorização explícita. Use `verify-and-stop`.

## Entrega e evidências

Entregue checklist por critério/fluxo, fontes, comandos, decisão, defeitos
classificados, risco residual e limitações, no formato do contrato.

## Impedimentos

Reporte como bloqueado quando faltar critério, versão, origem, ambiente ou
evidência independente; indique a prova mínima necessária.
