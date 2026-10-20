# Status do projeto agent-team

Resumo executivo. Não substitui as notas individuais em `tasks/` (histórico
completo, evidências e critérios por tarefa) — este documento é um preview de
leitura rápida para qualquer sessão (Codex, Claude, Gemini/Antigravity) que
retome o projeto. Atualizado por: Claude (coordenador AVATAR-QUALIDADE-001). Data: 2026-09-24.

## Sessão 19–20/10 — TASK-20261019-MYREPOS-CRESCIMENTO-001 — repassada ao Codex

Ver `tasks/TASK-20261019-MYREPOS-CRESCIMENTO-001.md`, seção "Handoff para o Codex".

- MyRepos (IG): benchmark com @gittrend.io, @baroi.ai, @githubsignals; plano editorial por N1, legenda sem link, palavra curta,
  horários 12h/19h BRT, sem repost, relatório `/api/video/autonomy/report`, vídeo abrindo na imagem de demonstração com gancho.
- Produção: Jaaz v0.3.17 + renderizador com gancho; v0.3.18 (CTA curto + limpeza) pronta em `CT100:/root/deploy/deploy-jaaz-v0318.sh`.
- Incidente: disco do CT100 a 100% em 20/10 ~00:25 UTC; resolvido com `docker builder prune -f`.
- Próximo (Codex): verificar o ciclo de 20/10 06:42 UTC e o post das 12h BRT; depois seguir os próximos passos da nota.

## Sessão 24/09 — TASK-20260924-AVATAR-QUALIDADE-001 (Q0 + Q0b) — parcial

Ver `tasks/TASK-20260924-AVATAR-QUALIDADE-001.md` e `/root/tarefas/AVATAR-QUALIDADE-001/handoff.md` (host).

- Branch `feature/avatar-qualidade` (base `feature/avatar-voice-sync` @ `8f43909`), worktree
  `/root/work/claude/AVATAR-QUALIDADE-001`, HEAD `1cf77bf`. Sem push; produção e staging intocados.
- **Q0 (`22781dd`)**: os 9 `except` silenciosos do pipeline de avatar viram estado explícito
  (`quality`/`warnings`/`degraded` em `status.json`), com código de log e aviso na UI. Sem motor de sincronia,
  o vídeo é declarado "apresentador estático"; `/capabilities` diz `avatarLipsync: static`.
- **Q0b (`1cf77bf`)**: `sample_avatar.jpg` (foto real) removida; padrões são placeholders desenhados por código;
  `DELETE /api/video/avatars/{id}`; `/api/file/avatar_*` só para o dono (`JAAZ_OWNER_TOKEN`, falha fechada);
  rótulo "voz e rosto gerados por IA" no MP4.
- Validação: 241 testes passaram (base 214); gitleaks sem vazamentos; tsc 0 erros; Playwright não executado.
- Próximo: verificação da Q0 pelo Codex → Q2 em sessão nova. Pendentes de decisão do Paolo: auth do dono
  (sem ela, miniaturas de avatar ficam ocultas), `release/0.3.1` (BUG-007), TTS pago p/ medição, Rhubarb, kit.

## Sessão 24/09 — TASK-20260924-AVATAR-VOICE-SYNC: Trava Estrita de Gênero (Avatar ↔ Voz) e Sincronização de Reels

Ver `/root/relatorios/TASK-20260924-AVATAR-VOICE-SYNC.md` no CT100 (`192.168.0.200`) para o relatório oficial.

- **Status:** Concluído com UI Gate e Testes Unitários Aprovados.
- **Branch:** `feature/avatar-voice-sync` (alvo: `v0.3.1`), baseada em `release/0.3.0` (commit `230b31c`), HEAD `8f439090fa9f3f7600461574703a0d11349b0a9f`.
- **Produção mantida intocada:** O container `opensuite-jaaz` no CT100 não foi modificado.
- **Trava Estrita de Gênero (Hard Lock):**
  - **Feminino (`female`):** Vozes permitidas restritas a `openai:nova` (Expressiva), `openai:shimmer` (Suave) e `pt-BR-FranciscaNeural` (Edge Clara). Qualquer voz masculina é removida da interface e bloqueada/auto-corrigida no backend.
  - **Masculino (`male`):** Vozes permitidas restritas a `openai:echo` (Jovem/Creator), `openai:onyx` (Cinema) e `pt-BR-AntonioNeural` (Edge Firme). Qualquer voz feminina é removida da interface e bloqueada/auto-corrigida no backend.
  - **Badge Visual:** `🔒 Trava: ♀ Feminina` / `🔒 Trava: ♂ Masculina` exibido nos dois locais (Radar GitHub manual e Piloto Automático).
  - **Backend Defense-in-depth:** Função `resolve_gender_locked_voice` em `video_router.py` e validação em `AutonomyService.update_config` forçam a voz correta caso payloads externos tentem burlar.
- **Validação:**
  - **Unitários:** 6 testes passando em `server/tests/test_avatar_voice_sync.py` (0.83s).
  - **Playwright UI Gate:** `/root/qa/bin/ui_gate.sh` aprovado para commit `8f43909` (fluxos `UI-06`, `UI-11` e `UI-12` com 0 erros de console e 0 erros HTTP).
  - **Smoke Test MP4:** Vídeo gerado com avatar em `1080x1920` e exatamente 1 faixa de áudio sincronizada (`repo-40f03112.mp4`).

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

## 6. Ad Studio F0 — atualização 2026-09-23

As tarefas `TASK-20260923-AD-STUDIO-F0-002`, `F0-004` e `F0-005` foram
registradas a partir do pacote F0 v0.5. F0-002 foi concluída: o portão G-01
aprovou o MoneyPrinter para cenas de duração uniforme, com áudio customizado
task-local e remoção posterior do stream silencioso quando necessário. F0-005
foi concluída: o host em `baseline/2026-09-23` é a fonte oficial recomendada;
o CT100 permanece apenas runtime com 52 alterações não commitadas. F0-004 foi
registrada como bloqueada e não iniciou, aguardando o cadastro das cinco
variáveis e da identidade `mpt-runtime` pelo Paolo.

Resultados entregues em `/root/relatorios/` no CT100:

- `TASK-20260923-AD-STUDIO-F0-002.md`
- `TASK-20260923-AD-STUDIO-F0-004.md`
- `TASK-20260923-AD-STUDIO-F0-005.md`
- `SPEC_AD_STUDIO.md`, `ROADMAP_AD_STUDIO.md`, `AGENTS.md` (F0 v0.5)

## 7. Feature reservada — GitHub Trending Radar (2026-09-24)

- Branch: `feature/video-studio-github-radar`
- Dono: Paolo Roberto Calvo
- Commit WIP: `27faeb5`
- Arquivos reservados: `react/src/components/video_studio/GitHubRepoExplorerModal.tsx`,
  `react/src/components/video_studio/GitHubTrendingRadar.tsx`,
  `server/routers/video_router.py`
- Estado: commit autorizado e branch publicada; não mergeada nem implantada.
- Catálogo F0-007: `/root/relatorios/TASK-20260924-AD-STUDIO-F0-007-GITHUB-RADAR.md`

## 8. Pontos em aberto / não verificados por mim

- Nenhum eval comportamental de Bug Hunt ou Ponytail foi executado.
- code-review-graph pode estar desatualizado; confirmar antes de usar em
  revisão real.
- Carregamento automático de skill/agente continua não comprovado em Codex e
  Antigravity — sempre delegar de forma explícita.
- `/root/opensuite` no host é uma pasta solta sem git; o repositório real do
  CT100 tem HEAD próprio sem remote configurado — sem linhagem confirmável
  além do histórico local.

## 9. BUG-004 — entrega estruturada de mídia (2026-09-24)

- Branch: `fix/BUG-004-media-delivery`
- Commits publicados: `e70f3e0`, `47dcad4`, `8db60ff`
- Release local preparada: `release/0.3.0`
- OpenReply separado em `feature/openreply-defaults`, commit `bf2e27d`
- Estado: implementação e staging focado passaram; homologação final bloqueada porque o Timeline MCP ainda retorna 502 para projeto inexistente.
- Relatório: `/root/relatorios/RELATORIO_BUG-004_V030_20260924.md`

## 10. TASK-20260924-AVATAR-VOICE-SYNC — Sincronização Avatar ↔ Voz & Renderização Reels (2026-09-24)

- Branch: `feature/avatar-voice-sync` (ramificada a partir de `release/0.3.0`, alvo release: `v0.3.1`)
- Commits no worktree: `acb5bc4`, `b40a6f5`
- Escopo entregue:
  1. Cadastro dinâmico de avatares no backend (`/api/video/avatars`) com `{id, name, gender, default_voice, voice_style, license_notice, voice_generated_notice}`.
  2. Frontend (`video_studio.tsx` e `GitHubAutonomySection.tsx`) sem nomes de arquivos fixos; consome dinamicamente a API.
  3. Pareamento automático de voz enérgica/expressiva por gênero:
     - Feminino: `openai:nova` / fallback `pt-BR-FranciscaNeural`
     - Masculino: `openai:echo` / fallback `pt-BR-AntonioNeural`
  4. Botões de override ♂ Masculino e ♀ Feminino em ambos os locais (Radar Manual e Piloto Automático).
  5. Autonomia persiste `avatar_id` + `voice_name` no backend via `/api/video/autonomy/config`.
  6. Pipeline de geração corrigido: `/api/video/repo-reels` quando `use_avatar=True` despacha `run_character_animation_pipeline` com avatar PiP iluminado, fundo escuro de repo, legendas sincronizadas e mapeamento de áudio dedicado.
  7. Avisos de "Voz gerada por IA (sintética neural)" e consentimento de licença exibidos na tela.
  8. Testes:
     - Unitários de mapeamento gênero→voz e persistência (`server/tests/test_avatar_voice_sync.py`) passaram 100%.
     - Playwright MCP UI Gate: fluxos `UI-06`, `UI-11` (Radar Manual) e `UI-12` (Autonomia) aprovados com 0 erros de console e 0 erros HTTP.
     - Smoke test no staging: MP4 gerado com stream de vídeo 1080x1920 (avatar na moldura) e exatamente 1 faixa de áudio (`smoke_evidence.json`).
- Gate: `/root/qa/bin/ui_gate.sh` aprovado para o commit `b40a6f5`.
- Relatórios oficiais: `/root/relatorios/TASK-20260924-AVATAR-VOICE-SYNC.md` e evidência em `/root/qa/ui-evidence/TASK-20260924-AVATAR-VOICE-SYNC/b40a6f5f4363866bc6e41903daba3263636c5d3a/`.
- Contêiner de produção (`opensuite-jaaz`): **preservado intacto**, nenhuma alteração direta realizada.

## Como usar este documento

Leia isto primeiro para orientação rápida; para evidência, critérios de
aceitação e detalhes por tarefa, vá à nota correspondente em `tasks/` pelo
`id` citado acima. Este arquivo é atualizado por convenção quando o
coordenador considerar o preview desatualizado — não há sincronização
automática.
