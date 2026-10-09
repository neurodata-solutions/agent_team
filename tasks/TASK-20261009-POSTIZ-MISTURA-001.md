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
