---
id: TASK-20261019-MYREPOS-CRESCIMENTO-001
tipo: task
estado: aguardando deploy (usuário roda)
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

## Próximas fases

1. Relatório semanal: seguidores ganhos e alcance por post e por série (Graph API insights).
2. Post em colaboração / aviso ao autor do repo.
3. Carrossel "Top 5 da semana"; reels de teste; YouTube Shorts/TikTok.
4. Vídeo abrindo no resultado (não na página do GitHub) — exige captura do projeto rodando ("Testei pra você").
5. Segurança: reconectar o Instagram da MyRepos na Postiz (token vazou na sessão de 19/10).
