---
id: TASK-20261019-MYREPOS-CRESCIMENTO-001
tipo: task
estado: v0.3.17 no ar (20/10 00:11 UTC); renderizador com gancho aguardando o usuário rodar
projeto: jaaz / myrepos
responsavel: Claude Opus 5.5
pedido_por: Paolo (19/10: "temos que conseguir mais seguidores, temos que ser criativos" → "podemos avançar")
branch: feat/MYREPOS-CRESCIMENTO-001 @ d3cf562 (worktree /root/work/claude/MYREPOS-CRESCIMENTO-001, base fix/OPENREPLY-LINK-001 @ 94a61d4 = produção v0.3.12)
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

## Próximas fases

1. Entrega semanal do relatório (onde: e-mail, Telegram, Notion? decidir com Paolo).
2. Post em colaboração / aviso ao autor do repo.
3. Carrossel "Top 5 da semana"; reels de teste; YouTube Shorts/TikTok.
4. Vídeo abrindo no resultado (não na página do GitHub) — exige captura do projeto rodando ("Testei pra você").
5. Segurança: reconectar o Instagram da MyRepos na Postiz (token vazou na sessão de 19/10).
