---
name: team-avaliar-agentes
description: Avalie resultados de agentes contra critérios prévios, distinguindo falhas comportamentais de impedimentos do ambiente.
---

# Team — avaliar agentes

## Objetivo e entradas

Emitir parecer independente sobre uma execução de agente. Receba protocolo,
resultado bruto, gabarito/critério congelado, versão, ferramentas, ambiente e
limites da avaliação.

## Procedimento e decisões

1. Confirme que critérios e rubrica existiam antes do resultado e que o
   avaliador não depende do gabarito oculto entregue ao agente.
2. Refaça apenas cálculos/verificações autorizados; preserve o resultado bruto.
3. Classifique cada desvio: comportamento do agente, ferramenta, produto,
   teste, requisito ou ambiente. Exija evidência causal antes de atribuir culpa.
4. Avalie severidade, reprodutibilidade, impacto e cobertura; não altere a meta
   depois de observar a saída.
5. Emita passar/reprovar/bloqueado e a prova mínima para reavaliação.

## Limites e dependências

Não execute a campanha nesta etapa, não edite o agente avaliado e não exponha
   prompts/gabaritos protegidos. Use `investigate-first` para hipóteses e
   `verify-and-stop` para concluir.

## Entrega e evidências

Entregue critérios, matriz de resultados, falhas classificadas, impedimentos,
risco residual e decisão no formato do contrato.

## Impedimentos

Marque bloqueado se faltar versão, transcript, rubrica, isolamento ou evidência
para separar ambiente de comportamento; indique a lacuna concreta.
