# Conectar seu Obsidian a este vault

Este repositório (`agent_team`) é o vault. O servidor onde ele vive é
headless — o Obsidian roda no seu dispositivo, não aqui.

## Passos

1. Clonar o repositório no seu computador/celular:
   ```
   git clone git@github.com:neurodata-solutions/agent_team.git
   ```
2. No Obsidian: "Open folder as vault" e escolher a pasta clonada.
3. Instalar o plugin comunitário `obsidian-git` (Configurações → Plugins
   comunitários → Procurar → "Git").
4. Configurar no `obsidian-git`: intervalo de auto-commit/pull (ex.: a
   cada 10 min) e "Pull on boot" ligado, pra sempre abrir com o estado
   mais recente.

## O que NÃO fazer

- Não editar `tasks/*.md` fora do padrão de frontmatter (`id`, `tipo`,
  `estado`, `projeto`, `responsavel`, `data`, `dependencias`, `tags`) —
  agentes e buscas dependem desses campos existirem.
- Não copiar código-fonte de `jaaz`/`opensuite`/`neuro-studio-mvp` pra
  dentro deste vault — as notas em `projects/` só linkam pra lá.
