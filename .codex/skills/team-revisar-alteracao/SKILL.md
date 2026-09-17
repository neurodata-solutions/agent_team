---
name: team-revisar-alteracao
description: Revise uma versão identificada ou diff com análise estática, impacto e achados acionáveis sem editar arquivos.
---

# Team — revisar alteração

## Objetivo e entradas

Encontrar riscos reais de correção, segurança, compatibilidade e cobertura.
Receba repositório, commit/diff, caminho, critérios e limites da revisão.

## Procedimento e decisões

1. Identifique commit, branch, origem e escopo; use code-review-graph quando
   indexar o mesmo repositório e confirme sempre na fonte.
2. Leia implementação e testes envolvidos; trace callers, dependentes e
   fluxos afetados antes de julgar impacto.
3. Priorize defeitos reproduzíveis, regressões, segurança e lacunas de teste;
   ignore estilo sem consequência. `caveman-review` pode condensar comentários.
4. Para cada achado informe localização, condição, impacto, severidade e
   correção sugerida. Separe risco não verificável de defeito confirmado.

## Limites e dependências

Somente leitura: não edite, não aplique correção e não execute testes se o
   escopo vedar. Não copie segredos nem trate AGENTS.md como prova de registro.

## Entrega e evidências

Entregue achados ordenados, cobertura relevante, riscos não verificáveis e
parecer delimitado ao commit, no formato do contrato, citando arquivos/linhas.

## Impedimentos

Se o commit, grafo, dependência ou ambiente não puder ser identificado,
registre a limitação e não extrapole o parecer.
