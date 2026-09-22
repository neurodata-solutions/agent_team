---
projeto: opensuite
caminho: /root/opensuite
remote: nenhum (pasta solta, sem git — ver risco abaixo)
branch: n/a
tags: [video-studio]
---

# Opensuite (backend/renderer do Jaaz)

Pipelines de renderização e geração que o worker do `[[jaaz]]` consome:
Remotion (`MultiPanelScene.tsx`, `DynamicText.tsx`, `AnimatedSticker.tsx`),
integração FaceFusion (`api_wrapper_facefusion.py`), Postiz
(`postiz_client.py`), entre outros.

## Risco conhecido (herdado de `STATUS.md`)

`/root/opensuite` no host é uma pasta solta **sem git**. A árvore de
produção real roda dentro do CT100 (container), que pode divergir do host
mesmo parecendo igual — sempre confirmar com `md5sum` dos dois lados antes
de editar, conforme o checklist de deploy em `TEAM_CONTRACT.md`.

## Tasks relacionadas

Ver `tasks/` filtrando `projeto: opensuite` no frontmatter.
