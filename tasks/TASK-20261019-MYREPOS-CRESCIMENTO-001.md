---
id: TASK-20261019-MYREPOS-CRESCIMENTO-001
tipo: task
estado: elenco leva 1 no ar (v0.3.25, 25/11); código em origin/jaaz @ dc557de
projeto: jaaz / myrepos
responsavel: Claude Opus 5.5 (elenco, 24–25/11); Codex 20/10–23/11
pedido_por: Paolo (19/10: "temos que conseguir mais seguidores, temos que ser criativos" → "podemos avançar")
branch: feat/MYREPOS-CRESCIMENTO-001 @ dc557de (enviada; origin/jaaz = dc557de; worktree /root/work/claude/MYREPOS-CRESCIMENTO-001)
---

# MyRepos: crescer seguidores com base em 3 perfis de referência

## Benchmark (19/10, Graph API Business Discovery, dados públicos)

| | @gittrend.io | @baroi.ai (fase repos) | @githubsignals | @myrepos |
|---|---|---|---|---|
| Seguidores | 162.579 | 6.728 | 56.730 | 91 |
| Posts/dia | 4,5 | 1 (horário fixo) | 4,5 | 2,3 (todos 18h UTC) |
| Curtidas (mediana) | 641 | 106 | 261 | 3 |
| Comentários (mediana) | 74 | 25 | 7 | 0 |
| Link na legenda | não | não | não | **sim** |

Lições: escolher o repo pelo apelo ao público geral (economiza dinheiro, útil, visual); abrir pelo benefício;
legenda curta sem link; palavra curta para comentar; hashtags do assunto; horários fixos e espaçados.
Dados brutos (fora do git): scratchpad da sessão 2ab77fa3 (`gt_all.json`, `ba_all.json`, `gs_all.json`, `mine_all.json`).

## Feito (código, @ d3cf562)

- `services/myrepos_editorial.py`: uma chamada N1 escolhe o repo entre até 8 candidatos novos e escreve série
  (`pare_de_pagar` | `achei_no_github`), gancho na tela, ângulo do roteiro, benefício, palavra curta (2–8) e 4 hashtags.
  Tudo validado; falha do N1 ou JSON ruim → plano determinístico (1º candidato, palavra curta, sem link).
- Legenda: gancho → benefício → `Comente "PALAVRA"` → `Open source: dono/repo` → `#github #opensource` + 4 do assunto. Sem URL.
- OpenReply (`link_in_caption`): reconhece `dono/repo` como texto, com as mesmas fronteiras (`a/rea` ≠ `a/reactor`);
  legendas antigas com URL continuam valendo.
- DM: convite para seguir no fim.
- Roteiro: `script_angle` vai para o prompt do gancho; gancho na tela = `hook` do plano.
- Agenda: `postiz_schedule_slots` ["12:00","19:00"] em `postiz_timezone` America/Sao_Paulo; próximo slot livre, nunca repetido.
  Lista vazia volta ao `postiz_schedule_time` antigo.
- Sem repost: se todos os repos em alta já foram publicados, o ciclo é pulado.
- Bugs corrigidos: histórico guardava os 50 **mais antigos** (último item era de 11/10, quebrando o "já publicado");
  `dict(DEFAULT_STATE)` compartilhava a lista `history` entre instâncias.

## Testes

- 31 novos em `tests/test_myrepos_crescimento.py`.
- Suíte completa em container descartável da imagem v0.3.12 (JUnit): branch 297 testes, base 266; nas duas, as mesmas
  3 falhas antigas (`test_check_ai_policy`, `test_n1_call`, `test_forced_media_call`).
- **Não verificado ao vivo:** o plano com o N1 real. A tentativa pelo `docker exec` não tem a chave do OmniRoute, e carregar o
  ambiente do app foi bloqueado (mapa de acessos). Verificar depois do deploy: `history[0].editorial.source == "llm"`.

## Deploy (pendente: usuário roda)

`! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0313.sh`
→ imagem `opensuite-jaaz:v0.3.13-n1-myrepos-crescimento`, rollback automático para v0.3.12. Não mexe em banco.
Rollback manual: `cd /root/opensuite && docker compose -f docker-compose.yml -f /root/deploy/jaaz-compose-v0312.yml up -d --no-deps jaaz`.

## Deploy v0.3.13: feito (19/10, 23:36 UTC)

Usuário rodou `deploy-jaaz-v0313.sh`: build ok, /health 200, piloto com `postiz_schedule_slots` 12:00/19:00 America/Sao_Paulo.
Primeiro ciclo com o código novo: 20/10 06:42 UTC → post às 12h BRT de 20/10. Conferir `history[0].editorial.source`.

## Fase 1: relatório (@ 0a9a7ff, aguardando deploy)

- Medido em 19/10 (Graph API): reel da MyRepos com **5,5 s de tempo médio assistido em 36 s**; o gancho é o gargalo.
- Meta não dá `follows` por reel e devolve vazio para `follower_count`/`follows_and_unfollows` abaixo de 100 seguidores
  (MyRepos: 91). Por isso o piloto tira uma foto diária de `followers_count` (`user_data/files/myrepos_followers.json`).
- `GET /api/video/autonomy/report?days=7`: por reel (alcance, views, assistido, compart., salvos, coment.) e por série; JSON + `markdown`.
- `OpenReplyService._find_account` extraído de `create_automation` (mesma busca), usado por `instagram_id_for_postiz_channel`.
- Testes: 40 dos arquivos ligados passam; suíte completa 303, mesmas 3 falhas antigas.
- Deploy: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0314.sh` (rollback automático para v0.3.13).
- Verificar depois: `curl -s 127.0.0.1:57988/api/video/autonomy/report` no CT100 e o arquivo de fotos no dia seguinte.

## v0.3.14 no ar e primeiro relatório real (19/10)

- Endpoint ok; foto de seguidores gravada (91 em 2026-10-19).
- 16 reels em 7 dias, todos formato antigo: alcance mediano 147,5, **assistido médio 6,0 s**, 46 comentários.
  Melhores: tester-army/e2e (1.449), ghidra (1.076), diagram-design (1.026).
- **morluto/rea publicado 5 vezes e AnyPS5 2 vezes**: os 25 do trending semanal já tinham sido usados e o código antigo
  repostava o 1º. A v0.3.13 pula o ciclo; mas então o scheduler tentaria de novo a cada 30 s.

## v0.3.15 (@ 9d717b1, aguardando deploy, de preferência antes de 20/10 06:42 UTC)

- Candidatos: categoria configurada → trending semana → dia → mês, URLs normalizadas, até 8.
- Ciclo agendado que falha tenta de novo em 1 h.
- Testes: 41 ligados; suíte 304, mesmas 3 falhas antigas.
- Deploy: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0315.sh` (rollback automático para v0.3.14).

## v0.3.16 (@ 820c23e) substitui a v0.3.15 (script removido do CT100)

- Inclui a v0.3.15 (candidatos dia/mês, retry 1 h).
- Vídeo: quando o README tem imagem de demonstração, ela abre os primeiros 3,5 s (screenshot_zoom, com o gancho);
  depois página do GitHub e terminal. Narração mira 22 s (antes 28 s; saía ~36 s). Roteiro para o público geral,
  1ª frase = benefício em até 10 palavras.
- Testes: 47 ligados; suíte 306, mesmas 3 falhas antigas.
- Deploy: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0316.sh`. Depois: vídeo de teste via `POST /api/video/repo-reels`
  (não publica) com um repo já postado, e conferir quadros antes do ciclo de 06:42 UTC.

## Teste de vídeo na v0.3.16 (job repo-455f16c9, diagram-design, não publicado)

- Abertura pela imagem de demonstração funciona (0–3,5 s), depois GitHub e terminal.
- **O gancho nunca apareceu em nenhum reel:** `RepoExplainerVideo.tsx` (renderizador) ignora a prop `hook`;
  `HookOverlay.tsx` existe e é usado só pela `ShortVideo`. Fonte: CT100 `/root/opensuite/services/openshorts/remotion`,
  com mudanças sem commit de outro agente (Root, BrowserScrollScene, Subtitles, captions, types, 3 componentes novos).
  Rebuild do renderizador levaria esse trabalho junto: decisão do Paolo.
- Imagem de demonstração com `objectFit: contain` fica pequena com faixas pretas (renderizador também).
- Duração: alvo 22 s saiu 34,2 s (60 palavras, comando lido em voz alta) → v0.3.17 (@ 80cad7e): 1,8 palavra/s e
  proibido ler comandos/URLs. Deploy: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0317.sh`.

## v0.3.17 no ar (20/10 00:11 UTC)

- Teste repo-f7611863 (diagram-design, não publicado): 27,7 s (antes 34,2 s); a IA ainda escreveu 59 palavras,
  15 delas no CTA fixo do `locale_rules` pt. Próximo: CTA curto e `hook_animation` "spring" (o "bounce" do piloto
  não existe no esquema do renderizador).

## Renderizador: gancho e fundo desfocado (aguardando Paolo)

- Conferido (só leitura): `services/openshorts/remotion/src` e `render-service` (src, package.json, lock) idênticos ao
  container em produção, apesar de não commitados. Rebuild só acrescenta a mudança.
- `RepoExplainerVideo.tsx`: `<HookOverlay config={hook}/>` e cópia desfocada da imagem de demonstração ao fundo
  (imagem maior, sem faixas pretas). `tsc --noEmit` em container descartável: 0 erros.
- Instalar o script no CT100 foi bloqueado no auto mode (Production Deploy). Script para o usuário:
  `! bash /tmp/claude-0/-root/2ab77fa3-2eb5-4193-9482-ed15764a8807/scratchpad/renderer-hook-host.sh`
  (backup do arquivo e tag `opensuite-renderer:pre-hook-<stamp>`, rollback automático).

## 20/10 00:20–00:40 UTC: disco cheio no CT100 (incidente)

- 1º deploy do renderizador (rebuild do zero) passou do tempo limite do `!`; script restaurou a fonte. Rebuild do zero
  instalaria Chromium mais novo (cache apagado em 13/10) → trocado por imagem derivada (`FROM opensuite-renderer:latest` + 1 arquivo).
- 2º deploy subiu, mas todo render deu "Page crashed!"; rollback feito pelo usuário e **continuou falhando** (até render mínimo).
  Causa real: **disco do CT100 100% (182 MB livres)**; Chromium não grava em /tmp. Contribuíram as 5 imagens do Jaaz desta noite
  e o build do renderizador. Usuário rodou `docker builder prune -f`: 8,5 GB liberados, 6,5 GB livres (96%). Render mínimo ok.
- Gancho testado num container isolado (`renderer-hook-test`, porta interna, removido depois): gancho visível e some aos 3,5 s,
  fundo desfocado, imagem de demonstração com `width: 96%`. Arquivo final sha256 cd2920e8….
- Pendente: usuário rodar `! bash …/scratchpad/renderer-hook-host.sh` (hash atualizado); depois teste real via `/repo-reels`.
- A fazer: scripts de deploy do Jaaz removerem versões intermediárias; alerta de disco no CT100 (encheu em 13/10 e 20/10).

## Renderizador com gancho no ar (20/10 00:34 UTC)

- Imagem derivada `opensuite-renderer:latest` (backup `pre-hook-20261020-003412`). Teste real repo-2f496bd2 (não publicado):
  gancho na tela sobre a imagem de demonstração grande, depois GitHub e terminal. Duração 29,9 s (CTA fixo de 15 palavras).

## v0.3.18 (@ 98abaa3, aguardando deploy)

- CTA pt: "Comente {KEYWORD} que eu te mando o link no direct!"; piloto com `hook_animation="spring"`.
- Depois do OK, o script apaga imagens/contextos v0.3.13, v0.3.14, v0.3.16 e o cache de build.
- Deploy: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0318.sh`.

## Próximas fases

1. Entrega semanal do relatório (onde: e-mail, Telegram, Notion? decidir com Paolo).
2. Post em colaboração / aviso ao autor do repo.
3. Carrossel "Top 5 da semana"; reels de teste; YouTube Shorts/TikTok.
4. Vídeo abrindo no resultado (não na página do GitHub) — exige captura do projeto rodando ("Testei pra você").
5. Segurança: reconectar o Instagram da MyRepos na Postiz (token vazou na sessão de 19/10).


## Handoff para o Codex (20/10, ~00:45 UTC)

Pedido do Paolo: "repasse as infos para o codex, continuar depois dessa última verificação".
O Codex não viu a conversa; tudo o que importa está nesta nota.

### Estado em produção (CT100)

- Jaaz: `opensuite-jaaz:v0.3.17-n1-myrepos-narracao` (rollback: `jaaz-compose-v0316.yml`).
- Renderizador: `opensuite-renderer:latest` = imagem derivada com o gancho (backup `opensuite-renderer:pre-hook-20261020-003412`;
  rollback manual no fim de `/root/deploy/renderer-hook/deploy.log`). A fonte em
  `/root/opensuite/services/openshorts/remotion/src/compositions/RepoExplainerVideo.tsx` acompanha a imagem; o original está em
  `/root/deploy/renderer-hook/RepoExplainerVideo.orig.tsx`.
- Código: branch `feat/MYREPOS-CRESCIMENTO-001` (worktree `/root/work/claude/MYREPOS-CRESCIMENTO-001`, sem push), HEAD `98abaa3`.
  A mudança do renderizador **não está commitada** em nenhum repo (a pasta `services/openshorts` tem trabalho sem commit de outro agente).
- Disco do CT100: 6,4 GB livres (96%) depois de `docker builder prune -f`.

### "Última verificação" (fazer primeiro)

1. Se o Paolo ainda não rodou: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0318.sh` (CTA curto + `spring`; rollback automático
   para v0.3.17; no fim apaga imagens/contextos v0.3.13, v0.3.14, v0.3.16 e o cache de build). Conferir saída `OK:` e `df -h /`.
2. Ciclo do piloto em 20/10 06:42 UTC (03:42 BRT). Conferir via `curl -s 127.0.0.1:57988/api/video/autonomy/status` no CT100:
   - `history[0].editorial.source == "llm"` (se `fallback`, o N1 falhou: ver logs `[MyReposEditorial]`);
   - `history[0].caption` sem `github.com`/`http`, com `Open source: dono/repo`, palavra curta e 4 hashtags do assunto;
   - `postiz_scheduled_date` = `2026-10-20T15:00:00Z` (12h BRT) e `status` do job `completed`;
   - vídeo do job (`/app/server/user_data/files/video_jobs/<job>/output.mp4`): gancho no topo nos primeiros 3,5 s, ~25 s.
   - Se o ciclo falhar, o próximo é em 1 h (não a cada 30 s).
3. Depois das 12h BRT: comentar no reel e conferir que o DM do OpenReply traz o link certo (casamento por `dono/repo` na legenda).
4. Relatório: `curl -s "127.0.0.1:57988/api/video/autonomy/report?days=7"`; foto diária de seguidores em
   `/app/server/user_data/files/myrepos_followers.json` (1ª: 91 em 2026-10-19).

### Como trabalhamos aqui (aprendido nesta sessão)

- Testes: `tar` de `server/` → CT100 → `docker run --rm` da imagem atual do Jaaz com `pip install pytest pytest-asyncio` e
  `POSTIZ_API_KEY=test-only POSTGRES_PASSWORD=test-only`; suíte completa com `--junitxml` (o stdout fecha). Base atual: 306 testes,
  3 falhas antigas conhecidas (`test_check_ai_policy`, `test_n1_call`, `test_forced_media_call`).
- Deploy do Jaaz: scripts `CT100:/root/deploy/deploy-jaaz-v03NN.sh` derivados do anterior (contexto copiado, hash dos arquivos,
  checagens `grep` no container, rollback automático). Conferir antes que os arquivos do contexto anterior batem com a base da branch.
- Teste de vídeo sem publicar: `POST /api/video/repo-reels` com `auto_open_reply:false` e um repo já postado (cria pasta em
  `video_jobs`, então o piloto passa a considerar esse repo como usado).
- Mudança no renderizador: testar antes num container isolado (`docker run` da imagem derivada na rede
  `opensuite_opensuite-network`, `POST /render` direto) e só então deploy. **Nunca** rebuild do zero (cache apagado; viria Chromium novo).
- Auto mode bloqueia: ler env de containers de produção, instalar deploy de serviço sem pedido explícito. Ver `docs/ACESSOS-E-PERMISSOES.md`.
- Token da Meta: nunca imprimir JSON de erro cru (a Meta repete o token). **Pendente de segurança:** o Paolo precisa reconectar o
  Instagram da MyRepos na Postiz (token vazou nos logs da sessão de 19/10).

### Próximos passos (depois da verificação), em ordem

1. Medir: comparar no relatório o tempo assistido dos posts novos com os 6,0 s de mediana do formato antigo (alcance mediano 147).
2. Duração: a IA ainda escreve ~59 palavras para alvo de 39; considerar cortar o roteiro no código (limite de palavras) se passar de 25 s.
3. Deploys do Jaaz devem sempre limpar versões intermediárias; propor alerta de disco no CT100 (encheu em 13/10 e 20/10).
4. Commitar a mudança do renderizador quando o dono de `services/openshorts` commitar o trabalho pendente (coordenar).
5. Fases de conteúdo seguintes: legenda com menos palavras por vez; série com vinheta própria; carrossel "Top 5 da semana";
   post em colaboração com autor do repo; YouTube Shorts/TikTok. Painel/entrega do relatório: depois (Paolo: "depois criaremos um painel").


## 20/10 ~10:10 UTC: incidente de conteúdo (Claude, a pedido do Paolo)

- Ciclo de 06:43 UTC: N1 respondeu `OmniRoute HTTP 500`; o plano caiu no padrão e agendou `YuJunZhiXue/dsh-purge` (jailbreak de modelos,
  descrição em chinês) para 20/10 15:00Z no IG e no FB (Postiz `cmvgblw6i000smk85ukd1rpb6`, `cmvgblw6v000tmk854dh9hpr3`).
- Cancelamento: pela tela da Postiz (o `deletePost` também encerra o workflow no Temporal; só marcar `deletedAt` no banco não basta,
  e a chave da API só existe no processo do Jaaz).
- Correção (@ 22f07bb, v0.3.19 substitui a v0.3.18): sem plano da IA o ciclo é adiado (nada publicado); `is_publishable` bloqueia
  jailbreak/bypass/crack/pirataria/adulto/evasão e descrição majoritariamente não latina antes da IA e do fallback; prompt proíbe os temas.
  Trending de hoje: só o dsh-purge bloqueado (13+12+21 candidatos publicáveis). Testes: 58 ligados; suíte 317, mesmas 3 falhas antigas.
- Deploy: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0319.sh` (inclui a limpeza de imagens intermediárias).
- Em aberto: causa do 500 do OmniRoute (sem registro no journal do CT102 nem no Jaaz). Se o N1 seguir fora, o piloto não publica.

### Causa do 500 do OmniRoute (CT102), 20/10 ~10:30 UTC

- `app.log` (`/var/lib/omniroute/data/logs/application/`): toda leitura do banco dá `disk I/O error` (sql.js, em memória);
  a requisição do Jaaz de 06:43:10 falhou em `Object.get` → 500. ~1.400 erros/hora.
- Linha do tempo: erros em 02–03/10, 09/10 até o restart de 13/10 04:37, nenhum em 14–16/10, voltou em 17/10 (último write do
  `storage.sqlite`: 17/10 22:52) e segue. **N1 fora desde 17/10.** Defeito do OmniRoute v16.3.1; restart resolve por alguns dias.
- Cópia do `storage.sqlite`: `integrity_check ok`, 130 tabelas. Disco do CT102 com 25 GB livres.
- Correção (usuário roda; restart no CT102 é bloqueado no auto mode):
  `! bash /tmp/claude-0/-root/2ab77fa3-2eb5-4193-9482-ed15764a8807/scratchpad/omniroute-recover.sh`
  backup em `data/db_backups/`, restart, contagem de erros pós-restart, e timer `omniroute-dbwatch` (10 min; ≥20 erros em 5 min
  → backup e restart, máx. 1/h, guarda 7 backups). O que só existia na memória desde 17/10 22:52 (logs de chamadas, edições na UI)
  se perde no restart.
- A investigar depois: por que o OmniRoute usa sql.js se `better-sqlite3` está instalado; atualizar o OmniRoute.

### 20/10 ~10:30 UTC: resultado

- OmniRoute: `omniroute-recover.sh` rodado; backup `db_backups/storage-20261020-072436.sqlite`; 0 `disk I/O error` depois de 10:25 UTC
  e `storage.sqlite` voltou a gravar. O passo 4 (vigia) falhou (`sh: 0: -c requires an argument`, script multilinha no `pct exec`):
  instalar com `! bash /tmp/claude-0/-root/2ab77fa3-2eb5-4193-9482-ed15764a8807/scratchpad/dbwatch/install.sh` (usa `pct push`).
- Jaaz v0.3.19: 1ª tentativa falhou por **disco cheio no CT100** (build completo sem cache, nova camada pip >3 GB; 1,8 GB livres).
  Produção intacta (v0.3.17, /health 200). Script reescrito: limpa cache/imagens/contextos intermediários e constrói **imagem
  derivada** (`FROM v0.3.17` + 3 arquivos), `compose up --no-build`. Padrão a seguir em todo deploy do Jaaz daqui em diante.

### 20/10 ~10:50 UTC: espaço e v0.3.19 no ar (autorizado pelo Paolo no chat)

- Limpeza do CT100 (`scratchpad/ct100-limpeza.sh`): removidos a pilha `openshorts` antiga (containers parados desde 29/08 + imagens),
  o renderizador de staging, imagens Jaaz v0.3.13/14/16/19-parcial, tags `pre-hook-001936`/`-002249`, cache e contextos.
  Disco: 1,8 GB → 22 GB livres (86%).
- Jaaz **v0.3.19-n1-myrepos-curadoria no ar** (imagem derivada da v0.3.17; rollback: `jaaz-compose-v0317.yml --no-build`).
- Postiz: posts `dsh-purge` (12h) apagados pelo Paolo; os de 15h (`scientific-agent-skills`) também ficaram apagados.
- Pendentes: vigia do OmniRoute (`scratchpad/dbwatch/install.sh`); etapa 2 (mover discos da VM 101 para `hdd-storage`,
  `mp0` de 200 GB no HDD para o CT100 e mover dados grandes) e etapa 3 (alerta de disco), aguardando janela do Paolo.
  Alerta: `local-lvm` com 362 GB alocados num pool de 348 GB (82%).

### 20/10 ~10:45 UTC: por partes
- Vigia do OmniRoute **instalado** (`omniroute-dbwatch.timer`, 10 min; teste a seco ok).
- Mover discos da VM 101 para `hdd-storage`: bloqueado no auto mode (Protected-Scope IaC Apply) com autorização genérica;
  comando para o Paolo: `qm move-disk 101 scsi0 hdd-storage && qm move-disk 101 scsi1 hdd-storage` (sem `--delete`; originais
  viram `unused` e só saem depois de conferir). VM 101 não tem backup.
- Alerta de disco: `scratchpad/disco-alerta.sh` (timer 30 min no host, limite 85%, e-mail root + journal `disco-alerta`).

## v0.3.21 — limpeza de vídeos publicados (28/10, @ 6444b5b, aguardando deploy)
- Pedido do Paolo (28/10): "depois de postar os videos nao temos necessidade de manter o video".
- Uma vez por dia a autonomia consulta `GET /public/v1/posts` do Postiz; reel com todos os posts `PUBLISHED` → `delete_job_files`
  (pasta do job + `files/<id>.*`). ERROR/QUEUE mantêm o vídeo. Histórico intacto. Primeira execução libera ~810 MB (26 reels).
- A v0.3.20 (trava de seguidor + abertura com resultado) **nunca foi ao ar**; a v0.3.21 a inclui (FROM v0.3.19 + 5 arquivos + follow-gate.sql).
- Testes: 91 ok (container descartável da imagem v0.3.19 + pytest).
- Deploy: `! pct exec 100 -- bash /root/deploy/deploy-jaaz-v0321.sh` (rollback automático para v0.3.19; remove imagem v0.3.17).
- Levantamento (não executado): Postiz tem 81 vídeos só de posts PUBLISHED (1,7 GB); ~30 jobs antigos fora do histórico.
- 28/10: Paolo aprovou tudo ("pode"). Auto mode bloqueou deploy e exclusões → scripts no CT100 para rodar com `!`:
  `deploy-jaaz-v0321.sh`, `postiz-purge-published.sh` (81 vídeos só de posts PUBLISHED, ~1,7 GB),
  `jaaz-old-purge.sh` (19 reels antigos confirmados PUBLISHED por dono/repo + 9 jobs com erro + MoneyPrinter/testes).
  Ficam: img-*, episódios do Historiador, char-*, repo-auto-f67cd018 (sem post no Postiz).

## 24/11: piloto parado desde 06/11 (incidente resolvido)

- Causa: combo `codigo-gratis` do OmniRoute (CT102) tinha `antigravity/gemini-3.7-flash-medium` em 1º desde 28/09.
  Até 06/11 ele dava 404/429 → lockout → fallback para Gemini/Codestral. Desde 07/11 08:22 UTC o Google responde
  **HTTP 200** com "This version of Antigravity is no longer supported…" → OmniRoute conta sucesso, sem fallback →
  `myrepos_editorial` sem JSON → ciclo adiado de hora em hora (~315 vezes).
- Correção: antigravity removido do `codigo-gratis` com `CT102:/root/omniroute-drop-antigravity-codigo.sh`
  (para o serviço, edita, sobe, testa, rollback automático). Backup: `CT102:/root/backup-omniroute-db-20261124-173156`.
  Editar `storage.sqlite` com o serviço rodando NÃO funciona (sql.js em memória regrava ao parar).
- Teste: ciclo manual 17:33 UTC, `editorial.source == "llm"`, job repo-auto-4b7b9a1e (mvanhorn/last30days-skill),
  vídeo 1080x1920 24,0 s, agendado na Postiz para 2026-11-24T22:00:00Z (19h BRT).
- Pendente: `imagem-gratis` ainda começa por antigravity; `docker logs` do opensuite-jaaz parado desde 20/11.

## 24/11: mascotes falantes Beto/Bia + narração animada (@ b73aeb3, aguardando deploy)

- Pedido do Paolo: "mascote do MyRepos ... quando o mascote for feminino, voz feminina; masculino, alternar também".
- Piloto alterna Beto (openai:echo) e Bia (openai:nova); reel que falhou não conta a vez; `mascot_rotation=false` desliga.
  Narração do piloto com preset `punchy` (instrução de criador de Reels no gpt-4o-mini-tts; `conversational` inalterado).
- Renderizador: `Mascot.tsx` (SVG original, boca pelos tempos das palavras, pisca, balança), à esquerda acima da legenda.
  Fonte em `deploy/renderer-mascote/` (branch) e `CT100:/root/deploy/renderer-mascote/` (originais em `orig/`).
  Teste isolado (container renderer-mascote-test): quadros conferidos para os dois.
- Testes: 16 novos; suíte 348 com `-s --continue-on-collection-errors` (stdout fecha sem `-s`), só as 3 falhas antigas.
- Amostras de voz (timbre, ainda com a instrução antiga): repo-2e41f993 (echo), repo-b5629fc1 (nova), não publicadas.
- Deploy (ordem): `pct exec 100 -- bash /root/deploy/renderer-mascote/deploy-renderer-mascote.sh` e depois
  `pct exec 100 -- bash /root/deploy/deploy-jaaz-v0322.sh` (= v0.3.21 nunca publicada + mascote; rollback automático p/ v0.3.19).
- **No ar 24/11 ~19:39 UTC** (Paolo rodou os dois `!`): renderizador com mascote (backup `opensuite-renderer:pre-mascote-20261124-193742`)
  e Jaaz `v0.3.22-n1-myrepos-mascote` (inclui v0.3.20/21: trava de seguidor ligada em 58 automações, backup
  `/root/deploy/backup-openreply-automation-20261124-193841.sql`; limpeza diária de vídeos publicados).
  Histórico real sem mascote → 1º reel automático (25/11 05:33 UTC) = Beto, depois Bia.

## 24/11: elenco de cartoon — leva 1 (no ar desde 24/11; v0.3.25 em 25/11)

- Design: `docs/superpowers/specs/2026-11-24-myrepos-elenco-design.md`; plano: `docs/superpowers/plans/2026-11-24-myrepos-elenco-leva1.md`.
- 4 personagens (Beto Bug, Bia Deploy, Capitão Commit, Dona Neide), sorteio em baralho (`services/myrepos_cast.py`),
  voz/estilo/velocidade por personagem, persona no roteiro, trilha de bocas (`tools/repo_explainer/visemes.py`),
  boneco retrô no renderizador (`deploy/renderer-elenco/`). Suíte 376, só as 3 falhas antigas.
- Render isolado: +12% a +20% de tempo com personagem. Quadros conferidos.
- Deploy (ordem obrigatória): `pct exec 100 -- bash /root/deploy/renderer-elenco/deploy-renderer-elenco.sh` e depois
  `pct exec 100 -- bash /root/deploy/deploy-jaaz-v0323.sh` (este confere o renderizador antes; rollback p/ v0.3.22).

## 24–25/11: elenco no ar, sincronia e roteiro curto

- 24/11: renderizador do elenco + Jaaz `v0.3.23-n1-myrepos-elenco`; depois `v0.3.24-n1-myrepos-sincronia`
  (Whisper recebia áudio que o PyAV não lia e caía em palavras igualmente espaçadas; agora decodifica com ffmpeg,
  boca fecha nos quadros sem voz, roteiro cita o nome do projeto e fatos do README). Concordância boca×fala 0,70 → 0,86.
- Lote de teste na v0.3.24 saiu longo: 23–38 s, 61–81 palavras (meta ~22 s / ~40 palavras).
- 25/11: `fit_script_length` reescreve uma vez o roteiro acima de 1,2× a meta; mantém o original se falhar, não encurtar
  ou perder a palavra do "Comente X". Jaaz **`v0.3.25-n1-myrepos-roteiro` no ar** (Paolo rodou o `!`; rollback p/ v0.3.24).
- Lote de teste v0.3.25 (não publicado): repo-fde92f88 Beto 15,2 s, repo-7575b49c Bia 16,5 s, repo-2cf6b56a Capitão 19,4 s,
  repo-eee907ce Dona Neide 19,8 s; 36–40 palavras, todos com /last30days e RESUMO. Aprovado pelo Paolo.
- Suíte 389, só as 3 falhas antigas.
- **Git (25/11):** branch `feat/MYREPOS-CRESCIMENTO-001` @ `dc557de` enviada e `origin/jaaz` (branch oficial do
  estudio-visual, ver `VCS_PLAYBOOK.md`) avançado por fast-forward `9b3c102..dc557de`. O `main` do remoto é outro histórico
  (ai-lab) — não usar para o Jaaz.
- Pendente: `Character.fallback_voice` definido mas não usado; Beto pode ficar curto (15 s) — subir meta p/ ~50 palavras se quiser.

