---
name: team-investigar-bug
description: Investigue falhas ambíguas ou intermitentes antes de propor correções, mantendo hipótese separada de causa confirmada.
---

# Team — investigar bug

## Objetivo e entradas

Explicar um sintoma por mecanismo comprovável. Receba relato, versão, caminho,
condição de ocorrência, logs seguros e limite de reprodução.

## Procedimento e decisões

1. Registre sintoma observável e expectativa, sem assumir causa.
2. Confirme versão/ambiente e reproduza com o menor caso; preserve um baseline.
3. Trace entradas, estados, fronteiras de ownership e saída de erro.
4. Liste hipóteses ranqueadas por evidência e falsificação barata; use
   `investigate-first` e descarte hipóteses com observações reproduzíveis.
5. Nomeie causa confirmada somente quando uma mudança/condição explicar o
   sintoma e houver prova independente; caso contrário, mantenha hipóteses.

## Limites e dependências

Diagnóstico não autoriza correção. Não exponha secrets, faça deploy ou altere
serviços. Pode usar `verify-and-stop` para encerrar quando a evidência bastar.

## Entrega e evidências

Entregue reprodução, comando, versão, logs redigidos, causa confirmada ou
hipóteses ranqueadas, correção proposta e prova necessária, no formato do
contrato.

## Impedimentos

Registre ambiente não reproduzível, logs insuficientes ou ausência de versão
como bloqueio específico; não converta silêncio em causa.
