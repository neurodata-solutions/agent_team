---
id: TASK-20260917-SKILLS-LOAD-DOCS
tipo: task
estado: concluida
projeto: agent-team-meta
responsavel: coordenador
data: '2026-09-17'
dependencias:
- TASK-20260917-SKILLS-LOAD-001
tags: []
---

# TASK-20260917-SKILLS-LOAD-DOCS

## Objetivo

Documentar o caminho explícito comprovado e preservar o estado parcial do carregamento nativo

## Escopo

somente TEAM_CONTRACT.md, README.md e TASK_REGISTER.md

## Resultado

Documentado o modo explícito comprovado; seleção nativa TOML e carregamento automático permanecem não comprovados. Nenhuma nova delegação foi executada.

## Evidências

- alterados somente TEAM_CONTRACT.md, README.md e TASK_REGISTER.md
- exemplo usa apenas task_name, fork_turns e message, argumentos suportados por collaboration.spawn_agent
- não foram alterados adaptadores TOML, skills, aplicações ou serviços

## Arquivos alterados

- TEAM_CONTRACT.md
- README.md
- TASK_REGISTER.md

## Verificações

- diff documental revisado
- git diff --check: passou
- piloto/evals: não executados

## Limitações

- documentação alternativa não comprova carregamento nativo; a tarefa SKILLS-LOAD-001 permanece parcial

## Próximo passo

usar uma superfície Codex com seleção nativa observável antes de reavaliar o carregamento

## Outros campos

- **caminho:** /root/agent-team
- **checkout_reservado:** liberado após commit local
- **criterios_aceitacao:**   - distinguir subagente genérico explícito, perfil TOML e carregamento automático
  - documentar procedimento de delegação com caminhos absolutos
  - distinguir limites escritos de controles técnicos
  - preservar estado parcial sem novas tentativas
- **entrega_esperada:** documentação operacional e exemplo code-reviewer
- **integrador:** coordenador
- **maquina:** host /root
- **skills_referencias:**   - TEAM_CONTRACT.md
  - README.md
- **versao_estado:** codex-cli 0.154.0; base 7d688fa
