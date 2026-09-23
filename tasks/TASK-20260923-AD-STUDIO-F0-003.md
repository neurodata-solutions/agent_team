---
id: TASK-20260923-AD-STUDIO-F0-003
tipo: operacao
estado: concluida_com_ressalvas
projeto: jaaz
responsavel: coordenador
data: '2026-09-23'
dependencias:
- RELATORIO_VPS_R2
paralelo_com:
- TASK-20260923-AD-STUDIO-F0-002
tags:
- ad-studio
- f0
- baseline
- ops
modo_escolhido: padrão
justificativa_modo: Ações operacionais pequenas e autorizadas; cada uma é independente e reversível ou de baixo risco.
autorizacao: D-06 — Paolo, 2026-09-23 (A2, A3, prune do build cache, parar o moneyprinterturbo-api)
refs:
- SPEC_AD_STUDIO.md §0.1, §0.2 (D-05, D-06), REQ-CFG-05
- ROADMAP_AD_STUDIO.md T0.0, T0.6, T0.10
- RELATORIO_VPS_R2.md §1.5, §2.2, §4, §6
checkout_reservado: /root/jaaz (host), branch baseline/2026-09-23
---

# Tarefa F0-003 — linha de base, busca teste e limpeza autorizada

## Objetivo

Deixar o repositório numa linha de base commitada e testável, medir os bancos
de vídeo e executar as duas limpezas autorizadas.

## Fora do escopo

- Push para o remoto; alterações na branch `jaaz`.
- Migração ou rotação de segredos (a rotação foi adiada pela D-05).
- Remover containers, imagens ou volumes; `docker image prune`; limpar o `cache_videos` do MPT.
- Rebuild, recreate ou redeploy de qualquer serviço.

## Critérios de aceitação

1. A branch `baseline/2026-09-23` existe com commits por tema; `.loki/` está ignorado; nenhum segredo commitado (gitleaks limpo ou achados reportados e excluídos).
2. `scripts/test.sh` roda num container efêmero; os resultados estão registrados.
3. A busca teste foi feita nos dois provedores, com as métricas pedidas e sem vazar chave.
4. Build cache limpo, com os números de antes e depois.
5. `moneyprinterturbo-api` parado com `restart=no`, serviços principais saudáveis e reversão documentada.

## Histórico de execução

Executada inicialmente numa sessão Antigravity (18:03–18:26), interrompida por
cota esgotada (HTTP 429) antes de limpar temporários e escrever este relatório.
Retomada pelo coordenador em sessão Claude Code (18:46+), que auditou o
transcript, encontrou os problemas abaixo e reabriu a verificação dos critérios
1 e 2 com o `team-tester`.

## Resultado por parte

| Parte | Critério | Estado |
|---|---|---|
| 1 — Linha de base | 1 | ✅ commits ok; gitleaks na baseline: só 1 falso positivo introduzido; 4 achados herdados do histórico |
| 2 — Testes efêmeros | 2 | ⚠️ roda em container efêmero; 182/187 passam, 5 falhas; `test.sh` padrão quebra por `server/main.py:5-6` |
| 3 — Busca Pexels/Pixabay | 3 | ❌ métricas ok, mas **chaves vazaram** (ver Incidente) |
| 4 — Build cache | 4 | ✅ executado; 0 B recuperado |
| 5 — MPT legado | 5 | ✅ parado, reversão documentada, reverificado 18:5x |

### Parte 1 — Linha de base

Branch `baseline/2026-09-23` criada no host a partir de `b4b863d`, sem push:

| Commit | Tema |
|---|---|
| `d519882` | chore(baseline): gitignore and config |
| `d8a87da` | chore(baseline): docs and policies |
| `5f18c9e` | chore(baseline): ai services and utilities |
| `dfe27e4` | chore(baseline): scripts |
| `0605b78` | chore(baseline): test suite |
| `7677bf3` | chore(baseline): modified source files |
| `37e47ae` | chore(test): dev test runner |

`.gitignore`: `.env` → `.env*`; adicionados `.loki/`, `*.mp4`, `*.mov`, `*.wav`,
`config.toml` (`server/data/` já estava). `config/` revisado: só YAMLs de
política, sem segredos.

**Gitleaks — primeira execução inválida.** Os scans `--no-git` (4 achados, em
`server/data_backup/config.toml` e `react/dist/`) e de histórico (20 achados)
montaram `/root/jaaz` **dentro do CT100**, que é outro clone (branch `jaaz`,
HEAD `e96ac719`, com alterações não commitadas), não a baseline do host.

**Gitleaks — reverificação na baseline (team-tester, 19:xx).** O snapshot foi feito com `git clone --no-local` da
`baseline/2026-09-23` (HEAD `37e47ae`) e enviado para `/root/f0003-verify` no CT100 (sha256 do tar conferido); tudo foi
removido no fim. Gitleaks v8.30.1 com `--redact`:
(a) árvore rastreada (`git archive HEAD`, porque o `--no-git` ignora o `.gitignore`): 1 achado;
(b) histórico (890 commits): 5 achados.

| Arquivo | Regra | Linha | Commit | Classificação |
|---|---|---|---|---|
| server/tests/test_redaction.py | private-key | 12 | 0605b78 (baseline) | Falso positivo: PEM sintético de teste |
| server/tools/social/postiz_client.py | generic-api-key | 18 | dd221bdc (2026-09-13) | Herdado: o valor fixo saiu em 029c827, mas continua no histórico. **Rotacionar a chave Postiz** |
| react/dist/assets/index-pJQPpaE3.js | gcp-api-key | 242 | b9c01174 | Herdado; não está rastreado no HEAD |
| react/dist/assets/percentages-BXMCSKIN-CEQXNO4i.js | gcp-api-key | 17 | 3a972946 | Herdado; não está rastreado no HEAD |
| react/dist/assets/index-BQlOUjYj.js | gcp-api-key | 242 | 8680a23b | Herdado; não está rastreado no HEAD |

Os commits da baseline não introduziram segredo real. Se o repositório for publicado, o histórico precisa
ser reescrito ou as chaves herdadas rotacionadas.

### Parte 2 — Testes efêmeros

`requirements-dev.txt` e `scripts/test.sh` commitados em `37e47ae`.

**Primeira execução inválida**: rodou em `python:3.12-slim` efêmero, mas sobre
o clone do CT100 (mesmo problema acima); a sessão copiou `requirements-dev.txt`,
`scripts/test.sh` e `scripts/run_tests_ephemeral.sh` para dentro daquele clone.
A suíte inteira quebrou na coleta (`ValueError: I/O operation on closed file`
no capture do pytest); o runner por arquivo mostrou 6 erros de coleta e 1 falha
(`test_message_history.py::test_duplicate_handoffs_are_reduced_to_one`), mas
esses números não se referem à baseline.

**Reverificação na baseline (team-tester).** Container `python:3.12-slim` com `--rm`, snapshot montado.
Com `scripts/test.sh` no modo padrão, a suíte quebra com `ValueError: I/O operation on closed file`.
**Causa confirmada:** `server/main.py:5-6` troca `sys.stdout`/`sys.stderr` por `io.TextIOWrapper` no momento do
import, o que fecha o arquivo de capture do pytest. `test_character_animation` e `test_video_queue_and_delete`
importam `main`. É um efeito colateral no produto, e não dependência faltando. Com `-s`: **187 testes, 182 passam,
5 falham, 0 erros de coleta**.

| Arquivo | Passou | Falhou |
|---|---|---|
| test_generate_video_by_moneyprinter | 16 | 0 |
| test_media_manifest | 3 | 1 (`test_manifest_rejects_traversal_and_adds_timeline_tool`: `ensure_timeline_tool` devolve um item a mais, provider `local`) |
| test_message_history | 3 | 1 (`RemoveMessage` não é subscriptable: contrato de `guard_handoff_calls` mudou) |
| test_timeline_studio_bridge | 7 | 3 (POST `/inspect` extra; provider `local` ≠ `system`; `Circular reference` em `timeline_studio_bridge.py:648`, ainda hipótese) |
| outros 24 arquivos | 153 | 0 |

Nada foi corrigido. Ficou como tarefa de desenvolvimento: mover a reconfiguração de stdout para
`if __name__ == "__main__"` (ou usar `sys.stdout.reconfigure`) e alinhar teste e código em
`ensure_timeline_tool`, provider e `guard_handoff_calls`.

### Parte 3 — Busca teste nos bancos

Chaves lidas de `/MoneyPrinterTurbo/config.toml` no container
`opensuite-moneyprinter` (não existe `config.toml` no repo Jaaz). Nenhum vídeo
baixado. Busca `fashion model`, retrato, 5 por página:

| Métrica | Pexels | Pixabay |
|---|---|---|
| HTTP | 200 | 200 |
| Total de resultados | 8.000 | 500 |
| Retrato com lado curto ≥ 1080 (de 5) | 4 | 5 |
| Duração média | 18,2 s | 7,8 s |
| Rate limit | 25.000/mês | 100/min |
| Restante | 24.914 | 99 |

### Parte 4 — Build cache

Sem build em andamento. `docker builder prune -f` (sem `--all`): **0 B
recuperado** — os 11,59 GB (23 entradas) estão todos marcados como ativos.
`--all` não foi usado (precisa de nova autorização, conforme a tarefa).

| Métrica | Antes | Depois |
|---|---|---|
| `/` do CT100 | 36G usados / 54G livres (41%) | igual |
| Imagens | 85,61 GB (220,6 MB recuperáveis) | igual |
| Containers | 2,573 GB (257,3 MB recuperáveis) | igual |
| Volumes | 13,89 GB (0) | igual |
| Build cache | 11,59 GB (0 recuperável) | igual |

### Parte 5 — `moneyprinterturbo-api` legado

- Antes: restart `always`, compose `moneyprinterturbo` / serviço `api`, imagem `moneyprinterturbo-api`, criado 2026-08-27.
- `docker update --restart=no` + `docker stop`: saiu com código 0; container e imagem preservados.
- Reverificado pelo coordenador: `moneyprinterturbo-api exited restart=no`; `opensuite-jaaz`, `opensuite-moneyprinter`, `opensuite-moneyprinter-worker` e `postiz` em `running`; GET `http://opensuite-moneyprinter:8080/` de dentro do `opensuite-jaaz` → **200**.
- Reversão: `pct exec 100 -- docker start moneyprinterturbo-api && pct exec 100 -- docker update --restart=always moneyprinterturbo-api`

## Incidente — cópias e vazamento das chaves do MPT

Para a Parte 3, o subagente Antigravity executou (21:07Z):

```
pct exec 100 -- docker cp opensuite-moneyprinter:/MoneyPrinterTurbo/config.toml /tmp/config.toml \
  && pct pull 100 /tmp/config.toml /tmp/jaaz_config.toml
```

e, antes disso, `docker exec ... cat config.toml | grep -i 'pexels\|pixabay'`.

Consequências confirmadas:

1. `/tmp/jaaz_config.toml` no host (modo 644, legível por todos) — mesmo hash do original. **Removido com `shred`** pelo coordenador.
2. `/tmp/config.toml` no CT100 (modo 600; o mtime 11:04Z herdado do original via `docker cp` fazia parecer mais antigo) — mesmo hash do original. **Removido com `shred`**.
3. Os valores das chaves **Pexels (56 caracteres) e Pixabay (34)** aparecem em texto puro nos passos 34–35 do transcript Antigravity `brain/2b463430-322a-442c-bdbe-d7a0e8be7d7c/.system_generated/logs/transcript.jsonl` — portanto também foram enviados ao provedor do modelo. O critério 3 ("sem vazar chave") **não foi atendido**.

Remediação (decisão do Paolo, 2026-09-23): **o próprio Paolo fará a rotação das
chaves**; a F0-004 só migra as chaves para o Infisical. Os valores vazados também
estavam em logs de outras sessões do Antigravity (057bb86d, 06a2a93b, bb0ee65d),
não só na 2b463430. Com autorização do Paolo, foram redigidos por substituição
**binária de mesmo tamanho** (`X`) em 21 arquivos de `brain/*/.system_generated/`
(transcripts, chunks, `steps/*/output.txt`). A validade JSON foi conferida antes e
depois e ficou idêntica (as linhas inválidas já existiam nos chunks). Restam 0
ocorrências. Os backups temporários foram destruídos com `shred`.

**Dano colateral causado pelo coordenador.** A primeira tentativa de redação abriu
os bancos SQLite `conversations/{057bb86d,06a2a93b,2b463430}.db` em modo texto
(conversão de newline e reescrita de bytes) e sem backup prévio. Os 3 bancos
ficaram **corrompidos sem recuperação**: não há snapshot, porque o LV root não tem
snapshot, e o `sqlite3 .recover` não recuperou o esquema, só fragmentos em
`lost_and_found`. Foram movidos para
`~/.gemini/antigravity-cli/conversations-quarentena-20260923/` (com LEIA-ME e os
fragmentos). O conteúdo das 3 conversas continua nos transcripts em `brain/`. O
que se perdeu foi só a possibilidade de retomar essas 3 sessões no Antigravity.

Checklist permanente derivado deste incidente:
1. Nunca extrair `config.toml` ou segredo para arquivo nem fazer `grep` em linhas de chave; ler a chave dentro do script, sem imprimir.
2. Redação de segredo em arquivo binário ou banco: **backup antes**, abrir em modo binário, substituir por valor do mesmo tamanho e rodar verificação de integridade (`pragma integrity_check`) antes de considerar concluído. Na dúvida, parar o processo dono do banco e redigir via SQL.
3. `glob('**')` ignora diretórios ocultos: para varrer segredos, use `os.walk` ou `find`.

## Temporários

- Removidos: `/root/jaaz/scripts/run_tests_ephemeral.sh` no host; os 3 arquivos não rastreados no clone `/root/jaaz` do CT100; `/tmp/jaaz_config.toml` no host e `/tmp/config.toml` no CT100 (os dois com `shred`); snapshots de verificação no host e no CT100.
- Restam no `/tmp` do host, sem valores de chave: `test-results*.txt`, `run_tests.sh`, `video_api_test.py`, `adstudio_r2_test.py`, `ad_studio_mpt_local_test.py`.

## Observação para a F0-002/F0-004

Os clones `/root/jaaz` do host (`b4b863d` + baseline) e do CT100 (`jaaz`,
`e96ac719` + alterações não commitadas) divergem. Antes de qualquer
build/deploy a partir da baseline, é preciso decidir qual deles é a fonte da
imagem `opensuite-jaaz`.

## Próximo passo

1. **F0-004 (T0.7):** migrar os segredos do MPT para o Infisical (a rotação das chaves Pexels e Pixabay fica com o Paolo; avaliar também a chave Postiz herdada no histórico).
2. Tarefa de desenvolvimento: corrigir `server/main.py:5-6` (reconfiguração de stdout no import) e alinhar as 5 falhas de teste/contrato.
3. Decidir qual clone do Jaaz é a fonte da imagem `opensuite-jaaz` (host baseline ou CT100 `jaaz`/`e96ac719`).
4. Retomar a F0-001: causa da duração de 3,03 s no render do MPT (a investigação foi interrompida).
