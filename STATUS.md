# Status do projeto agent-team

Resumo executivo. Não substitui as notas individuais em `tasks/` (histórico
completo, evidências e critérios por tarefa) — este documento é um preview de
leitura rápida para qualquer sessão (Codex, Claude, Gemini/Antigravity) que
retome o projeto. Atualizado por: coordenador (sessão Claude Code). Data:
2026-09-21.

## Sessão 21/09 — Governança do contrato de agentes

Ver `tasks/TASK-20260921-GOVERNANCE-001.md` pra detalhes completos.

Três falhas recorrentes relatadas pelo usuário (agente não lê log real antes de
hipótese; agente trabalha sem saber escopo/estado do projeto; mesmo erro se
repete entre sessões sem virar checagem permanente) foram diagnosticadas por
evidência de arquivo (não suposição) e corrigidas:

- **Log-first**: `team-investigar-bug/SKILL.md` ganhou passo 0 obrigatório —
  ler log real do serviço (`journalctl`/`docker logs`/arquivo de log) antes de
  formar hipótese.
- **Escopo/estado**: `README.md` (onboarding) agora exige ler `STATUS.md` (este
  arquivo) + a entrada relevante em `tasks/` antes de delimitar qualquer
  tarefa — antes disso não estava referenciado em lugar nenhum do onboarding.
- **Não repetir erro**: `TEAM_CONTRACT.md` § Ciclo de melhoria agora exige que
  tarefa `bloqueada` ou com causa recorrente vire checklist/eval-case antes de
  poder ser dada por encerrada — antes disso `improvement-loop/` só tinha
  templates, zero registros reais.
- **Duplicação entre ferramentas**: `adapters/antigravity/subagents.json`
  parafraseava as regras do contrato (já tinha divergido do texto canônico);
  agora aponta pros arquivos em vez de reafirmar.
- **Mentalidade de skills**: nova seção em `TEAM_CONTRACT.md` mapeando
  `superpowers` (Claude, já instalado, escopo `user`) por papel, com a mesma
  disciplina aplicada via skills próprias em Codex/Antigravity.
- **3 integrações `third_party/` novas**, commit fixado, licença preservada,
  sem instalador automático nem modo de correção autônoma: `bug-hunter`
  (achado por análise estática, complementa `bug-hunt`), `debug-mode`
  (confirmação de causa por instrumentação de runtime) e
  `browser-testing-with-devtools` + `debugging-and-error-recovery`
  (Addy Osmani/`agent-skills`, MCP `chrome-devtools` registrado em modo
  `--isolated` em `/root/.mcp.json`).

**Não verificado ainda**: nenhuma sessão real de agente exercitou o fluxo
novo em produção — a próxima tarefa de debug real precisa confirmar que o
passo 0 e o mapeamento de skills estão sendo seguidos na prática.

## 0. Sessão 20/09 — Estúdio Visual Multi-Painel, TTS, título de repo, comentários

Ver `tasks/TASK-20260920-001.md` a `tasks/TASK-20260920-004.md` pra detalhes
completos. Resumo do que mudou e por quê:

- **Editor multi-painel**: arrastar painel/texto, duplo-clique editar texto,
  Del apagar, seleção exclusiva, fundo de imagem real (não só gradiente),
  fontes de verdade (Montserrat/Poppins/Bebas Neue/Anton/Oswald via
  `@remotion/google-fonts` — o renderer só tinha DejaVu instalada antes
  disso), cor de fonte. Corrigido em `jaaz` (frontend + worker) e no
  renderer (`opensuite/services/openshorts/remotion`).
- **Piloto Automático GitHub Reels**: narração não usava sotaque nativo
  pt-BR de verdade (normalizador fonético de termos técnicos tinha sido
  removido por engano no commit `bd4ea0d`); nome de projeto podia vir errado
  se o README começasse com um H1 diferente do nome real do repo (ex.:
  "Agent Canvas" pro repo OpenHands); automação de resposta de comentário
  tinha um bug clássico de asyncio (tarefa de fundo sem referência guardada,
  podia ser destruída pelo garbage collector sem log nenhum). Todos
  corrigidos e testados isoladamente.
- **⚠️ Novo checklist obrigatório de deploy** em `TEAM_CONTRACT.md` § "Ações
  operacionais" — nasceu de 2 incidentes reais de produção nesta sessão
  (crash-loop por regex de env-var, queda de DNS interno por perda de
  network alias ao reconectar rede manualmente). Ler antes de qualquer
  rebuild/recreate de container nesta stack.
- **Automação de resposta de comentário** (fix do poller) ainda não
  confirmada em produção real — precisa de um comentário novo depois do
  deploy pra ver funcionando sozinha, sem chamada manual.

## 1. Piloto HH:MM:SS — concluído

Função `seconds_to_hhmmss` implementada e verificada por dois métodos
independentes (suíte do Tester + reexecução/oráculo do QA), 0 defeitos de
produto. Persistida em `pilots/hhmmss/` (não mais no scratchpad temporário
original). Revisada duas vezes: subagentes Claude e, depois, um subagente
nativo do Antigravity. Serviu para provar que o protocolo de delegação cega
(Desenvolvedor não vê testes, Tester não vê implementação) funciona dentro de
uma única ferramenta.

## 2. Infraestrutura da equipe — concluída, com limitações registradas

- Adaptadores nativos: Codex (`.codex/agents/*.toml`, 9 papéis) e Antigravity
  (`adapters/antigravity/`). Claude usa `/root/.claude/agents/team-*.md`.
- 11 skills próprias em `.codex/skills/`, associadas às definições centrais em
  `agents/`.
- **Carregamento automático de skill/perfil TOML nunca foi comprovado** na
  superfície Codex avaliada (`TASK-20260917-SKILLS-LOAD-001`, estado
  `parcial`). O caminho comprovado é sempre delegação explícita com caminhos
  absolutos — ver `TEAM_CONTRACT.md` § "Modo operacional comprovado no
  Codex".
- code-review-graph registrado para `/root/agent-team`, mas historicamente
  relatado como *stale* em pelo menos uma verificação — confirmar a revisão
  antes de confiar nela.

## 3. Terceiros integrados de forma delimitada — concluído

- **Bug Hunt**: modo de contestação (Hunter/Skeptic/Referee) ligado a
  Debug/Code Reviewer/QA existentes, sem novos agentes permanentes.
- **Ponytail**: duas skills ligadas a Desenvolvedor e Code Reviewer.
- Ambos com os arquivos de origem preservados byte a byte em `third_party/`,
  licença e commit de origem registrados.

## 4. Avaliação técnica — concluída

`browser-use/video-use`: **rejeitado como dependência**. Cinco das sete
capacidades anunciadas já existem na nossa fonte (Jaaz/OpenMontage); as duas
genuinamente novas (remoção de filler words, autoverificação de qualidade)
não compensam a exigência de chave paga ElevenLabs sem fallback, quando já
rodamos faster-whisper de graça em produção. Detalhe em
`TASK-20260917-VIDEOUSE-EVAL-001`.

Descoberta lateral importante: a árvore de produção real do
OpenMontage/MoneyPrinter é no **CT100** (`/root/opensuite`), não no host; os
dois pipelines de dublagem (Bloco 1 literal, Bloco 2 adaptação criativa)
existem lá — mas na época da investigação viviam *untracked* na camada
mutável do container, sem sobreviver a um `recreate`. Ver
`TASK-20260917-VIDEOUSE-TREE-001` para o status daquele risco.

## 5. Trabalho direto no produto (Jaaz / Video Studio) — concluído, verificado nesta sessão

`TASK-20260917-001..003`: utilitário `gitvideo-push`, segredos no Infisical,
correção de timeout falso e travamento do Remotion no Multi-Painel, player de
vídeo in-canvas, correção de erro 405 e `[Errno 21]`.

**Verificado independentemente em 2026-09-19** (não apenas copiado do
registro): `git -C /root/jaaz log/status` confirma que os commits `d8eccbe` e
`a8f115d` citados existem de fato no histórico do host, a branch `jaaz`
rastreia `origin/jaaz`, e a árvore está limpa (HEAD atual `ae79334a`, mais
novo que os dois commits — houve trabalho adicional depois). O alerta de
outra sessão (`root-e6`) sobre 17 arquivos não commitados antes de um rebuild
do container CT100 foi resolvido nesse meio-tempo.

## 6. Pontos em aberto / não verificados por mim

- Nenhum eval comportamental de Bug Hunt ou Ponytail foi executado.
- code-review-graph pode estar desatualizado; confirmar antes de usar em
  revisão real.
- Carregamento automático de skill/agente continua não comprovado em Codex e
  Antigravity — sempre delegar de forma explícita.
- `/root/opensuite` no host é uma pasta solta sem git; o repositório real do
  CT100 tem HEAD próprio sem remote configurado — sem linhagem confirmável
  além do histórico local.

## Como usar este documento

Leia isto primeiro para orientação rápida; para evidência, critérios de
aceitação e detalhes por tarefa, vá à nota correspondente em `tasks/` pelo
`id` citado acima. Este arquivo é atualizado por convenção quando o
coordenador considerar o preview desatualizado — não há sincronização
automática.
