# Bug Hunter incorporado

Origem: https://github.com/codexstar69/bug-hunter
Commit fixado: `3be69733a27aa04d4f5620df203c05350d162067`

## Atribuição e Licença

- Autor: codexstar69 (https://github.com/codexstar69)
- Licença: MIT (preservada integralmente em `LICENSE`)

## Arquivos incorporados do commit fixado

- `SKILL.md`
- `prompts/hunter.md`
- `prompts/skeptic.md`
- `prompts/referee.md`
- `prompts/recon.md`
- `prompts/threat-model.md`
- `LICENSE`

Não incorporados, deliberadamente: `bin/`, `scripts/*.cjs`, `schemas/`,
`evals/`, `modes/`, `templates/subagent-wrapper.md`, `prompts/fixer.md`,
`prompts/doc-lookup.md`. São a camada executável (CLI, loop autônomo,
correção automática, lookup em API externa) que este time não usa — ver
delimitação abaixo.

## Delimitação de uso

Esta cópia preserva o conteúdo original do repositório fixado (prompts de
papel Hunter/Skeptic/Referee + recon + threat-model) para fins de referência,
licença e insumo metodológico. Não inclui nem autoriza a execução do CLI
(`bin/bug-hunter`), do instalador (`npx ... install --agent codex`), nem
ativa carregamento automático.

**O modo `--autonomous`/`--auto-commit` da origem nunca é usado aqui.**
Diagnóstico é somente leitura por padrão (`TEAM_CONTRACT.md`); achados
seguem para o Desenvolvedor apenas sob autorização explícita da tarefa,
igual ao `bug-hunt` (`danpeg/bug-hunt`) já incorporado.

Este material é adicional ao `bug-hunt` já integrado, não substituto: os
papéis Hunter (Debug) / Skeptic (Code Reviewer) / Referee (QA) do time
continuam regidos exclusivamente por
`/root/agent-team/TEAM_CONTRACT.md` e
`/root/agent-team/.codex/skills/team-investigar-bug/SKILL.md`, sob
delimitação estrita de escopo (nunca varredura cega ou ilimitada).
