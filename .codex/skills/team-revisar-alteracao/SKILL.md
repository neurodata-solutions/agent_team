---
name: team-revisar-alteracao
description: Revise uma versão identificada ou diff com análise estática, impacto e achados acionáveis sem editar arquivos.
---

# Team — revisar alteração

## Objetivo e entradas

Encontrar riscos reais de correção, segurança, compatibilidade e cobertura.
Receba repositório e um escopo identificável (commit, diff, conjunto de
arquivos ou versão), além de critérios e limites da revisão; não extrapole esse
escopo.

## Procedimento e decisões

1. Identifique commit, branch, origem e escopo; use code-review-graph somente
   quando indexar o mesmo repositório e referência. Se estiver indisponível,
   desatualizado ou incompatível, inspecione diretamente o diff e a fonte e
   registre a limitação; confirme sempre na fonte.
2. Leia implementação e testes envolvidos; trace callers, dependentes e
   fluxos afetados antes de julgar impacto.
3. Resolva cada skill auxiliar pelo respectivo `SKILL.md` antes de usá-la. Se
   estiver ausente ou indisponível, registre o impedimento e continue com o
   procedimento próprio. Priorize defeitos reproduzíveis, regressões,
   segurança e lacunas de teste; ignore estilo sem consequência.
   `ponytail-review` pode propor cortes de complexidade, mas é complementar e
   não substitui a revisão completa nem autoriza remover requisitos, testes,
   validações, segurança, acessibilidade ou tratamento de erros.
4. Para cada achado informe localização, condição, impacto, severidade e
   correção sugerida. Separe risco não verificável de defeito confirmado.

## Limites e dependências

Somente leitura: não edite, não aplique correção e não execute testes se o
   escopo vedar. Esse limite da tarefa não comprova isolamento técnico de
   shell ou MCP. Não copie segredos. `AGENTS.md`, quando aplicável, é contexto
   conceitual; não é caminho exigido nem prova de registro de agente.

## Entrega e evidências

Entregue achados ordenados, cobertura relevante, riscos não verificáveis e
parecer delimitado ao commit, no formato do contrato, citando arquivos/linhas.

## Impedimentos

Se o commit, grafo, dependência ou ambiente não puder ser identificado,
registre a limitação e não extrapole o parecer.
