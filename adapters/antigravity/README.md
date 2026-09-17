# Adaptador Antigravity / Gemini CLI

Este diretório contém o adaptador da equipe de agentes compartilhada para o ambiente **Google Antigravity CLI (`agy`)**.

## Informações do Ambiente
- **Ferramenta:** Google Antigravity CLI (`agy`)
- **Versão:** `1.2.4`
- **Engine / Modelos:** Gemini (ex.: Gemini 3.8 Flash / Pro)
- **Diretório de Configuração:** `/root/.gemini/antigravity-cli/`

## Arquitetura de Subagentes no Antigravity

Diferente do Claude Code (que descobre subagentes a partir de arquivos `.claude/agents/*.md`), o Antigravity CLI 1.2.4 utiliza um modelo dinâmico baseado em ferramentas nativas disponibilizadas para o agente orquestrador:
1. **`define_subagent`**: Define dinamicamente o tipo de subagente para a sessão, com nome, descrição, prompt de sistema e concessão de grupos de ferramentas (`enable_write_tools`, `enable_subagent_tools`, `enable_mcp_tools`).
2. **`invoke_subagent`**: Dispara a execução concorrente em background de um ou mais subagentes registrados, com retorno assíncrono e canais de mensagens (`send_message`).
3. **`manage_subagents`**: Lista, inspeciona e encerra subagentes em execução (`list`, `kill`, `kill_all`).

As instruções centrais dos 9 papéis permanecem exclusivamente em `/root/agent-team/agents/*.md` e `/root/agent-team/TEAM_CONTRACT.md`, evitando duplicação de regras.

## Registro dos 9 Papéis
As definições formais para registro de cada papel estão declaradas em `subagents.json`:
- `team-coordenador` (escrita: sim, subagentes: sim, mcp: sim)
- `team-desenvolvedor` (escrita: sim, subagentes: não, mcp: não)
- `team-tester` (escrita: sim, subagentes: não, mcp: não)
- `team-code-reviewer` (escrita: não, subagentes: não, mcp: sim)
- `team-qa` (escrita: não, subagentes: não, mcp: não)
- `team-debug` (escrita: não, subagentes: não, mcp: não)
- `team-ambiente-linux-devops` (escrita: sim, subagentes: não, mcp: não)
- `team-engenheiro-mcp` (escrita: sim, subagentes: não, mcp: sim)
- `team-gestor-mcp` (escrita: não, subagentes: não, mcp: sim)

## Como utilizar a equipe no Antigravity

Em uma nova sessão de chat no Antigravity CLI:
1. **Instruir o agente principal a registrar a equipe:**
   > "Leia `/root/agent-team/adapters/antigravity/subagents.json` e registre os subagentes usando a ferramenta `define_subagent`."
2. **Acionar um especialista por tarefa:**
   > "Atue como Coordenador e acione o subagente `team-code-reviewer` para revisar o repositório X."
3. **Execução direta:**
   O agente chama `invoke_subagent(TypeName="team-code-reviewer", Prompt="...", Workspace="inherit")`. A execução corre em segundo plano e notifica automaticamente ao terminar.

## Orquestração do Modo de Contestação Independente (Bug Hunt)

Como os subagentes especialistas (`team-debug`, `team-code-reviewer`, `team-qa`) possuem `enable_subagent_tools: false`, a orquestração sequencial do modo de contestação de `team-investigar-bug` é conduzida pelo agente principal (ou `team-coordenador`):
1. **Etapa 1 (Hunter)**: `invoke_subagent(TypeName="team-debug", Prompt="... [instruções de hunter.md + escopo delimitado] ...")`.
2. **Gate de corte**: Se a resposta do Hunter indicar `TOTAL DE CANDIDATOS: 0`, encerra imediatamente sem disparar subagentes adicionais.
3. **Etapa 2 (Skeptic)**: `invoke_subagent(TypeName="team-code-reviewer", Prompt="... [instruções de skeptic.md + lista estruturada de candidatos] ...")`.
4. **Etapa 3 (Referee)**: `invoke_subagent(TypeName="team-qa", Prompt="... [instruções de referee.md + achados estruturados e contestações] ...")`.
5. **Consolidação**: O agente principal apresenta o relatório final e encaminha achados sustentados ao Desenvolvedor conforme escopo.

## Limitações e Observações
- O Antigravity CLI 1.2.4 não carrega automaticamente subagentes customizados a partir de diretórios estáticos na inicialização fria da CLI sem o passo de registro via `define_subagent`.
- As chamadas são assíncronas; a comunicação bidirecional ocorre via `send_message`.
