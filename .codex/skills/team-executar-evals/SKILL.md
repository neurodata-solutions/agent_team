---
name: team-executar-evals
description: Execute avaliações controladas de agentes quando explicitamente autorizado, mantendo o gabarito separado do agente avaliado.
---

# Team — executar evals

## Objetivo e entradas

Medir comportamento de um agente em cenários controlados. Receba protocolo,
cenários, versão, orçamento, critérios prévios, gabarito protegido e formato
de evidência.

## Procedimento e decisões

1. Congele versão, prompt, ferramentas, permissões, seed quando aplicável e
   critérios antes da execução; registre o que fica fora do contexto avaliado.
2. Mantenha gabarito/oráculo em arquivo ou processo separado e entregue apenas
   a entrada necessária ao agente.
3. Execute somente cenários autorizados, isolando efeitos e capturando
   transcript, artefatos, tempo, erros e exit code sem secrets.
4. Compare resultados ao gabarito prévio; classifique erro de tarefa, agente,
   ferramenta ou ambiente sem mover a meta após ver a saída.
5. Pare no orçamento/critério definido e preserve os artefatos para auditoria.

## Limites e dependências

Não executar evals nesta etapa sem autorização explícita. Não vazar gabarito,
   criar amostras após o resultado ou ampliar campanha; use `verify-and-stop`.

## Entrega e evidências

Entregue protocolo, versão, matriz cenário→resultado, métricas, falhas,
artefatos e limitações; declare claramente o que não foi executado.

## Impedimentos

Bloqueie se critérios, gabarito separado, isolamento ou versão não puderem ser
garantidos; não substitua o oráculo por julgamento informal.
