---
projeto: jaaz
caminho: /root/jaaz
remote: git@github.com:neurodata-solutions/estudio-visual.git
branch: jaaz
tags: [video-studio]
---

# Jaaz (Estúdio Visual / Video Studio)

Produto principal do Video Studio. Repositório real: `estudio-visual`
(nome do repo no GitHub), rodando no host como `/root/jaaz` e em produção
como container `opensuite-jaaz` dentro do CT100 (Proxmox).

## Pontos de entrada

- `package.json` — scripts do frontend/build
- `Dockerfile.local` — build local da imagem de produção
- `server/` — backend/worker Python
- `react/` — frontend
- `electron/` — empacotamento desktop
- `docs/` — documentação própria do repositório (não duplicada aqui)

## Depende de

- `opensuite` (ver `[[opensuite]]`) para renderização (Remotion) e
  pipelines de dublagem/geração — roda como stack separada no CT100.

## Tasks relacionadas

Ver `tasks/` filtrando `projeto: jaaz` no frontmatter (busca do Obsidian
ou `grep -l "projeto: jaaz" tasks/*.md`).
