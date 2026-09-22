# Debug Mode incorporado

Origem: https://github.com/doraemonkeys/claude-code-debug-mode
Commit fixado: `c34f9e3ec806bc50b6f871b3c572a9772f489951`

## Atribuição e Licença

- Autor: doraemonkeys (https://github.com/doraemonkeys)
- Licença: MIT (preservada integralmente em `LICENSE`)

## Arquivos incorporados do commit fixado

- `SKILL.md` (originalmente em `debug-mode/SKILL.md` na origem)
- `LICENSE`

## Delimitação de uso

Skill de debug por instrumentação com hipótese: instrumenta código com
logging (`#region DEBUG`) gravando em `.agents/debug.log`, nunca usa
stdout/stderr solto, e para explicitamente pedindo confirmação do usuário
após reproduzir e após corrigir.

Conteúdo revisado nesta integração: sem `eval`, sem execução de comando
arbitrário, sem acesso a credenciais/segredos, sem chamada externa (o
caminho de browser usa um endpoint que o próprio usuário implementaria —
não se aplica ao uso deste time).

**Não instalado em `~/.claude/skills/` (carregamento automático global).**
Fica como referência fixada em `third_party/`, citada explicitamente por
`agents/debug.md` e `team-investigar-bug/SKILL.md`. A fase "Limpar" do
fluxo original (remover instrumentação e logs) é obrigatória para
considerar a tarefa `concluída`, conforme o campo `Arquivos alterados` da
entrega do `TEAM_CONTRACT.md`.
