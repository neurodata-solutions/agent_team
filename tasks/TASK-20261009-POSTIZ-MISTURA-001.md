---
id: TASK-20261009-POSTIZ-MISTURA-001
tipo: incidente
estado: diagnosticado (correção aguardando aprovação do Paolo)
projeto: jaaz
responsavel: Claude Opus 5.5
data: '2026-10-09'
tags:
- postiz
- historiador
- myrepos
---

# Reels do MyRepos publicados nos canais do Historiador

## Regra (Paolo; já registrada em TASK-20260930-HISTORIAN-POSTIZ-MANUAL-001)

O **Historiador do Mundo / Contando História do Mundo** nunca recebe conteúdo de outro canal, em especial os reels automáticos de repositórios do GitHub, que são do **MyRepos**. Cada piloto automático publica só nas contas dele, sempre por **ID de integração** e nunca por nome de rede.

## Evidência (leitura no Postiz, 09/10 09:40)

O mesmo post do piloto automático vai para 4 contas: `myrepos | Open Source e Automação` (IG), `MyRepos` (FB), **`Historiador do Mundo` (IG)** e **`Contandohistoriadomundo` (FB)**.

| Conteúdo | Criado | Estado |
|---|---|---|
| t3code | 04/10 | publicado em 05/10 18:00 |
| OpenShell | 08/10 | publicado em 08/10 18:00 |
| raddebugger | 08/10 18:36 | na fila para 09/10 18:00 |
| laya | 09/10 06:36 | na fila para 09/10 18:00 |

## Causa raiz

- `opensuite-jaaz:/app/server/user_data/files/autonomy_state.json` tem `postiz_channels = ["instagram", "facebook"]`, com `enabled = true`.
- `server/services/autonomy_service.py:421` repassa esse valor ao `postiz_client.create_social_post`.
- `server/tools/social/postiz_client.py:104-118`, quando recebe nomes de rede, seleciona **todas** as integrações ativas daquela rede na organização.
- Quando os canais do Historiador foram ativados no Postiz, entraram automaticamente na lista.
- Efeito colateral: o registro do OpenReply (`autonomy_service.py:447`) itera os mesmos "canais" (`instagram`, `facebook`), que não são IDs de conta.

## IDs (Postiz)

| Conta | Rede | ID |
|---|---|---|
| myrepos \| Open Source e Automação | instagram | `cmu86xrbr0001mk8cqt3xn1v1` |
| MyRepos | facebook | `cmultrpgv0005mkmg73x0u6dz` |
| Historiador do Mundo | instagram | `cmultr3sm0003mkmgbzs6dnll` |
| Contandohistoriadomundo | facebook | `cmultqigt0001mkmgnwacqogw` |

## Correção proposta (produção: precisa de OK explícito)

1. **Até 09/10 18:00:** tirar da fila os 2 posts (raddebugger e laya) **só** nas contas do Historiador, pelo próprio Postiz (UI ou API), para que o workflow agendado também seja cancelado. Apagar direto no banco não garante isso.
2. **Configuração do piloto automático:** `postiz_channels = ["cmu86xrbr0001mk8cqt3xn1v1", "cmultrpgv0005mkmg73x0u6dz"]`, aplicado via `update_config`, com backup do JSON antes.
3. **Código (branch, sem deploy imediato):** o piloto automático recusa nomes de rede genéricos e exige IDs de integração. Assim, conta nova nunca entra sozinha. Teste de regressão incluído.
4. **Já publicados** (t3code em 05/10 e OpenShell em 08/10) nas contas do Historiador: remover manualmente no Instagram e no Facebook, decisão do Paolo.

## Execução (09/10, aprovada pelo Paolo: "sim, temos que separar bem as coisas")

1. **Feito.** Os 4 posts errados na fila do Historiador (raddebugger e laya, IG e FB) foram marcados com `deletedAt`, que é o mesmo mecanismo do delete do Postiz.
   - Confirmado em `post.activity.js:84`: o agendador não publica post com `deletedAt`.
   - Os do MyRepos seguem em `QUEUE` para 18:00. Os 5 rascunhos do Historiador não foram tocados.
   - Backup em `/root/backup-postiz-historiador-fila-20261009.csv`.
2. **Feito.** O piloto automático passou a usar `postiz_channels = [cmu86xrbr…, cmultrpgv…]`, aplicado via `POST /api/video/autonomy/config` e conferido no arquivo. Backup em `autonomy_state.json.bak-20261009-mistura`, no container.
3. **Branch `fix/POSTIZ-MISTURA-001`** (worktree `/root/work/claude/POSTIZ-MISTURA-001`, base `003dbf1` = produção), commits `284b831` e `416d53e`, **sem deploy**:
   - `postiz_client` só aceita IDs explícitos. Nome de rede, lista vazia, ID desconhecido ou conta desativada geram `ValueError`, e a rota manual devolve 400.
   - Saíram os padrões `["instagram","facebook"]` do piloto automático, da rota e do esquema `PublishToSocialRequest`.
   - Modal: jobs que não são do Git abrem sem conta marcada; o modo Git nunca cai para "todas"; os botões genéricos instagram/facebook do fallback foram removidos.
   - Testes:
     - 8 novos, e 6 deles falham no código antigo;
     - suíte em container: base 259 testes contra fix 267, com as mesmas 3 falhas e 2 erros de coleta pré-existentes;
     - `tsc`: nenhum erro novo (o único erro no modal, `onOpenChange` sem tipo, já existia).
   - Revisão do Codex: `docs/reviews/codex-POSTIZ-MISTURA-001.md` na branch. Os 3 achados (1 🔴 e 2 🟡) foram corrigidos em `416d53e`.

Pendente:
- **Deploy da branch:** OK do Paolo.
- **Remoção manual** dos reels já publicados no Historiador (t3code em 05/10 e OpenShell em 08/10).

## Deploy (09/10 14:35 UTC, aprovado: "pode seguir")

- **Achado antes do deploy:**
  - A produção rodava `opensuite-jaaz:v0.3.10-n1-direct-video`, e não a v0.3.8.
  - Essa imagem = worktree `N1-OMNIROUTE-001` **com 5 alterações não commitadas** (verificado: 139/139 `.py` idênticos).
  - O overlay usado (`/tmp/jaaz-compose-v0310-n1-direct-video.yml`) tinha sumido.
- **Branch `fix/POSTIZ-MISTURA-001` @ `4834192`:** essas 5 alterações foram copiadas sem mudança (commit próprio), mais os 2 commits da correção. Diferença para a produção anterior: só `postiz_client.py`, `autonomy_service.py` e `video_router.py`.
- **Suíte:**
  - produção anterior: 261 testes, 4 falhas e 2 erros;
  - combinado: 269 testes, as mesmas 4 falhas e 2 erros.
  - A falha `test_forced_media_call::test_forced_video_call_reads_duration_from_request` **já existia na v0.3.10** (vem das alterações não commitadas do N1), e não da correção.
- **Script** `CT100:/root/deploy/deploy-jaaz-v0311.sh`: build `opensuite-jaaz:v0.3.11-n1-postiz-ids` (contexto `/root/deploy/jaaz-v0311`, overlay `jaaz-compose-v0311.yml`), checagem de `/health`, da trava de canais e da configuração do piloto automático, com rollback automático.
- **Resultado:** no ar. Conferido depois:
  - 139/139 arquivos iguais à branch;
  - piloto automático parado, com as contas do MyRepos;
  - `/api/video/social/channels` responde (Postiz ok);
  - fila das 18:00 intacta: MyRepos ativo e Historiador removido.
- **Rollback:**
  ```
  cd /root/opensuite && docker compose -f docker-compose.yml -f /root/deploy/jaaz-compose-v0310.yml up -d --no-deps jaaz
  ```
  A imagem v0.3.10 foi mantida.
