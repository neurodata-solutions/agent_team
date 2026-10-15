# TASK-20261015-OPENREPLY-LINK-001: comentário no MyRepos recebe link de outro repositório

## Problema (relatado por Paolo, 15/10)
Ao comentar num reel do MyRepos, o DM trazia um link diferente do anunciado no post.

## Evidência (banco `openreply`, só leitura)
- 42 automações ativas na conta MyRepos, nenhuma com `postId`; todas com `matchAnyPost=true`.
- 26 automações "Vídeo … (*)" de 15–25/09 com `matchAnyWord=true`: respondem a qualquer comentário em qualquer post.
- Comentários "DiagramViz"/"🙌" (09–15/10) foram respondidos por "Vídeo repo-d6e40c8c (*)" com `github.com/cloudflare/security-audit-skill`: 6 DMs errados em 14 dias.
- Piloto (`autonomy_service.py`) acrescentava `QUERO/LINK/REPO` e cortava a palavra do CTA em 10 letras (`DIAGRAMDES`).

## Regra decidida (Paolo)
Qualquer comentário pode disparar o DM, mas o link tem que ser o do repositório do vídeo comentado.

## Correção
Branch `fix/OPENREPLY-LINK-001` (worktree `/root/work/claude/OPENREPLY-LINK-001`, base `fix/POSTIZ-MISTURA-001` @ `4834192`), commit `94a61d4`:
- `openreply_service.automations_for_media`: uma automação só responde no post a que está presa (`postId`) ou no post cuja legenda contém o link dela. Sem correspondência, nada é enviado. A legenda vem do scanner ou de `GET /{media_id}?fields=caption` no webhook.
- Piloto: `match_any_word=True`, só a palavra do repositório, sem corte em 10 letras.
- Premissa conferida: todos os posts do MyRepos IG dos últimos 10 dias têm `github.com/…` na legenda.
- Testes: 7 novos (`test_openreply_link_per_post.py`); suíte em container 266 → 273, mesmas 3 falhas pré-existentes (`test_forced_media_call`, `test_check_ai_policy`, `test_n1_call`).

## Deploy (pendente: usuário roda)
`CT100:/root/deploy/deploy-jaaz-v0312.sh` → imagem `opensuite-jaaz:v0.3.12-n1-openreply-link`, rollback automático para v0.3.11; depois faz backup da tabela `Automation` e põe `matchAnyWord=true` nas 13 automações "Autonomia:".
Rollback manual: `cd /root/opensuite && docker compose -f docker-compose.yml -f /root/deploy/jaaz-compose-v0311.yml up -d --no-deps jaaz`.
