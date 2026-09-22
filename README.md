# Equipe compartilhada de agentes

Versão inicial: 1.0 (2026-09-15).

Este diretório é a fonte central das definições de papéis e do contrato de
coordenação para Codex, Claude e futuras adaptações. Ele não substitui as
instruções específicas de cada ferramenta.

## Uso

1. Ler `TEAM_CONTRACT.md`.
2. Ler `STATUS.md` (orientação rápida) e as entradas relevantes do projeto/
   serviço em `tasks/` — sem isso a tarefa é delimitada sem saber
   o que já foi feito, o que está em aberto ou se a causa já é conhecida.
   Registrar essa leitura como evidência da tarefa.
3. Selecionar um papel em `agents/`.
4. Delimitar escopo, evidências e critério de aceitação.
5. Entregar resultado com o formato do contrato.
6. Para versionamento e commits rápidos e seguros no Video Studio e outros produtos, consulte [VCS_PLAYBOOK.md](file:///root/agent-team/VCS_PLAYBOOK.md).


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

Skills associadas: `investigate-first` e `bug-hunt` adaptado (debug), `surgical-patch` e
`safe-refactor` (desenvolvimento), `caveman-review`/code-review-graph e `ponytail-review` (review),
`verify-and-stop` (tester/QA) e `cavecrew` quando delegação comprimida for
explicitamente solicitada.

Skills próprias da equipe ficam em `.codex/skills/` e são referenciadas pelas
definições centrais em `agents/`. Os adaptadores Codex carregam essas skills
por `[[skills.config]]`; Antigravity chega às mesmas referências por
`definition_ref`, enquanto Claude recebe a referência textual nos arquivos
`/root/.claude/agents/team-*.md` e lê a definição central. A associação de arquivo acessível
não é, por si só, prova de carregamento em uma sessão nova.

## Modo operacional comprovado no Codex

O modo comprovado é delegar um subagente genérico e fornecer explicitamente o
papel, o contrato, a definição e a skill principal. A seleção nativa do perfil
TOML por nome e a descoberta automática das skills permanecem não comprovadas
na superfície avaliada. Não use uma opção inventada como `--agent` nem trate
`skills.config` como carregamento observado.

Exemplo pronto, usando apenas os argumentos suportados por
`collaboration.spawn_agent`:

```javascript
collaboration.spawn_agent({
  task_name: "code_reviewer_explicit",
  fork_turns: "all",
  message: """
  Revise somente o commit 5f3e687 em /root/agent-team, sem editar arquivos,
  instalar dependências ou executar piloto/evals. Antes de trabalhar, leia:
  - /root/agent-team/TEAM_CONTRACT.md
  - /root/agent-team/agents/code-reviewer.md
  - /root/agent-team/.codex/skills/team-revisar-alteracao/SKILL.md
  Use somente, se necessário, as referências auxiliares:
  - /root/.agents/skills/caveman-review/SKILL.md
  - /root/.agents/skills/verify-and-stop/SKILL.md
  Informe o identificador real, os arquivos lidos, achados por severidade,
  evidências e limitações no formato do TEAM_CONTRACT.md.
  """
})
```

O agente principal deve registrar quais arquivos foram realmente lidos. Esse
procedimento é uma alternativa operacional comprovada; não resolve nem prova o
carregamento nativo do perfil TOML ou das skills.

Limites escritos nas instruções são orientações. Não são, sem evidência
adicional, controles técnicos de sandbox, isolamento, permissões, modelo ou
aprovação.

## Limitações conhecidas

- Não há coordenação automática entre ferramentas.
- O checkout do host e o checkout do CT100 podem divergir.
- Grafos e memória não são presumidos como globais.
- Esta configuração não altera aplicações, containers, infraestrutura,
  segredos ou serviços de produção.
