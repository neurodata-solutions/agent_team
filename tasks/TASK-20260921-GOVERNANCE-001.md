---
id: TASK-20260921-GOVERNANCE-001
tipo: task
estado: concluida
projeto: agent-team-meta
responsavel: coordenador (sessão Claude Code)
data: '2026-09-21'
dependencias: []
tags: []
---

# TASK-20260921-GOVERNANCE-001

## Objetivo

Corrigir três falhas recorrentes relatadas pelo usuário: agentes não lêem log real antes de hipótese, agentes trabalham sem saber escopo/estado do projeto, e o mesmo erro se repete entre sessões sem virar checagem permanente. Diagnóstico feito por evidência (grep/stat/diff), não suposição.

## Escopo

editar TEAM_CONTRACT.md, README.md, agents/*.md, .codex/skills/team-investigar-bug/SKILL.md, adapters/antigravity/subagents.json, third_party/**, /root/.mcp.json; nenhuma alteração em código de produto, container ou serviço

## Resultado

Diagnóstico com evidência de arquivo antes de qualquer edição:
(1) todas as menções a "log" em agents/*.md e .codex/skills/*/SKILL.md tratavam log só
    como evidência a entregar, nunca como leitura obrigatória no início;
(2) STATUS.md ("leia isto primeiro") não era referenciado em README.md nem TEAM_CONTRACT.md
    — README.md datado de 17/09, STATUS.md atualizado em 20/09, nunca linkado de volta;
(3) improvement-loop/ continha só templates, zero registros reais — único lugar onde
    causa recorrente virou regra permanente foi o checklist de deploy, escrito à mão;
(4) 44 arquivos .md/.toml/.json definem papel/contrato; o papel "debug" sozinho duplicado
    em 4 lugares, com paráfrase já divergente no system_prompt do Antigravity vs. o texto
    canônico de agents/debug.md.
Correções aplicadas: passo 0 de leitura de log real + instrumentação de runtime (debug-mode)
+ verificação em navegador real (browser-testing-with-devtools/Chrome DevTools MCP) em
team-investigar-bug/SKILL.md; passo obrigatório de leitura de STATUS.md/TASK_REGISTER.md em
README.md; regra de enforcement do ciclo de melhoria em TEAM_CONTRACT.md; subagents.json
reescrito para apontar aos arquivos canônicos em vez de reparafrasear; nova seção "Uso de
skills" em TEAM_CONTRACT.md com mapeamento superpowers por papel; bug-hunter (codexstar69,
commit 3be6973), debug-mode (doraemonkeys, commit c34f9e3) e browser-testing-with-devtools +
debugging-and-error-recovery (addyosmani/agent-skills, commit dc27a9c) incorporados em
third_party/ com licença MIT preservada, sem CLI/instalador/scripts executáveis, sem modo
autônomo; chrome-devtools MCP registrado em /root/.mcp.json em modo --isolated.

## Evidências

- grep -rniE 'journalctl|docker logs|/var/log|log' agents/*.md .codex/skills/*/SKILL.md -> só 'preservar/entregar log', nunca 'ler log'
- grep -n STATUS README.md TEAM_CONTRACT.md team-coordenador.md -> zero ocorrências
- find improvement-loop -iname '*.json' -not -name '*.template.json' -> vazio
- diff agents/debug.md vs. system_prompt do Antigravity -> texto reformulado, não idêntico
- git ls-remote dos 3 repos terceiros para fixar commit antes de copiar; WebFetch do SKILL.md real de cada um antes de confiar no conteúdo
- python3 -c 'import json; json.load(...)' em subagents.json apos as 9 edições -> JSON válido

## Arquivos alterados

- TEAM_CONTRACT.md
- README.md
- .codex/skills/team-investigar-bug/SKILL.md
- agents/debug.md, agents/desenvolvedor.md, agents/code-reviewer.md, agents/coordenador.md, agents/qa.md, agents/tester.md
- adapters/antigravity/subagents.json
- third_party/bug-hunter/** (novo)
- third_party/debug-mode/** (novo)
- third_party/agent-skills/** (novo)
- /root/.mcp.json (novo server chrome-devtools)

## Verificações

- passou (JSON validado, arquivos lidos antes de editar); não executada (nenhuma sessão real de agente rodou o fluxo novo ainda pra confirmar comportamento em produção)

## Limitações

- chrome-devtools MCP só ativa de fato na próxima vez que uma sessão carregar /root/.mcp.json; não foi exercitado nesta tarefa
- agents/ambiente-linux-devops.md, engenheiro-mcp.md e gestor-mcp.md não receberam referência a superpowers/third_party por não terem mapeamento direto — decisão deliberada, não omissão
- STATUS.md em si não foi atualizado nesta tarefa (é convenção do coordenador, não obrigação desta correção específica)

## Próximo passo

na próxima tarefa real de debug, confirmar que o passo 0 (log real) e o mapeamento de skills estão sendo seguidos na prática, não só documentados

## Outros campos

- **caminho:** /root/agent-team, /root/.claude/agents, /root/.mcp.json
- **checkout_reservado:** liberado
- **criterios_aceitacao:**   - team-investigar-bug/SKILL.md exige leitura de log real como passo 0
  - README.md exige leitura de STATUS.md/TASK_REGISTER.md antes de delimitar escopo
  - TEAM_CONTRACT.md torna obrigatória a conversão de causa recorrente/bloqueio em checklist ou eval-case
  - subagents.json não reafirma regras do contrato por paráfrase — aponta pros arquivos canônicos
  - mentalidade de skills (superpowers na superfície Claude + skills da equipe em toda superfície) documentada com mapeamento por papel
  - bug-hunter, debug-mode e 2 skills de agent-skills (Addy Osmani) incorporados com commit fixado, licença preservada, sem instalador automático de terceiro e sem modo de correção autônoma
- **entrega_esperada:** arquivos editados + third_party/ novos + chrome-devtools MCP registrado
- **integrador:** coordenador
- **maquina:** host /root
- **skills_referencias:**   - investigate-first (usado para o próprio diagnóstico)
- **versao_estado:** CORRIGIDO em 2026-09-22: esta afirmação estava errada. agent-team já era repositório git desde 2026-09-16 (16 commits, HEAD f114d48..2a32f2b), só sem remote e sem commits desde 17/09 — não checado antes de escrever este registro. Achado ao rodar `git init` durante a Task 1 do plano do vault Obsidian.
