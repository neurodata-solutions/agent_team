# Equipe compartilhada de agentes

Versão inicial: 1.0 (2026-09-15).

Este diretório é a fonte central das definições de papéis e do contrato de
coordenação para Codex, Claude e futuras adaptações. Ele não substitui as
instruções específicas de cada ferramenta.

## Uso

1. Ler `TEAM_CONTRACT.md`.
2. Selecionar um papel em `agents/`.
3. Delimitar escopo, evidências e critério de aceitação.
4. Entregar resultado com o formato do contrato.

O adaptador Claude confirmado está em `/root/.claude/agents/team-*.md`.
O adaptador Gemini/Antigravity está em `/root/agent-team/adapters/antigravity/`
(baseado nas ferramentas nativas `define_subagent` e `invoke_subagent` do Antigravity CLI 1.2.4).

## Acionamento

No Codex, peça: `Leia /root/agent-team/TEAM_CONTRACT.md e atue como
<papel>; registre a tarefa <id>`. O papel coordenador delega especialistas
somente com os campos obrigatórios do contrato. No Claude, use os agentes
`team-coordenador`, `team-ambiente-linux-devops`, `team-desenvolvedor`,
`team-debug`, `team-code-reviewer`, `team-tester`, `team-qa`,
`team-engenheiro-mcp` ou `team-gestor-mcp`. No Gemini/Antigravity, carregue
as definições de `/root/agent-team/adapters/antigravity/subagents.json` via
`define_subagent` e acione os subagentes via `invoke_subagent`.

Skills associadas: `investigate-first` (debug), `surgical-patch` e
`safe-refactor` (desenvolvimento), `caveman-review`/code-review-graph (review),
`verify-and-stop` (tester/QA) e `cavecrew` quando delegação comprimida for
explicitamente solicitada.

Skills próprias da equipe ficam em `.codex/skills/` e são referenciadas pelas
definições centrais em `agents/`. Os adaptadores Codex carregam essas skills
por `[[skills.config]]`; Antigravity chega às mesmas referências por
`definition_ref`, enquanto Claude recebe a referência textual nos arquivos
`/root/.claude/agents/team-*.md` e lê a definição central. A associação de arquivo acessível
não é, por si só, prova de carregamento em uma sessão nova.

## Limitações conhecidas

- Não há coordenação automática entre ferramentas.
- O checkout do host e o checkout do CT100 podem divergir.
- Grafos e memória não são presumidos como globais.
- Esta configuração não altera aplicações, containers, infraestrutura,
  segredos ou serviços de produção.
