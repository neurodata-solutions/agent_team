---
projeto: flow-studio
caminho: /root/flow-studio-mvp (frontend) + /root/flow-studio-api (backend)
remote: nenhum (git local só em flow-studio-api)
tags: [video-studio, flow-studio]
---

# Flow Studio (Flowroom MVP)

Produto novo e isolado do Jaaz: uma "fábrica simples de vídeos" inspirada no vídeo
[I Fully Automated Google Flow Using Claude Code](https://www.youtube.com/watch?v=JEla_mdlfxs)
(Guney Topcu, 07/10/2026). A ferramenta do vídeo é o [GTAI-1/flow-mcp](https://github.com/GTAI-1/flow-mcp),
clonado em `/root/flow-mcp-source`. O nicho Achadinhos entra depois, pelo mesmo fluxo
(`/root/relatorios/TASK-20261008-ACHADINHOS-MVP-001.md`).

## Onde vive cada parte

| Parte | Local | Dono |
|---|---|---|
| Interface (wizard Briefing → Cenas → Render → Exportar) | `/root/flow-studio-mvp` (Vite/React, sem git) | Codex |
| Contrato de provedores | `/root/flow-studio-mvp/docs/PROVIDER_CONTRACT.md` | Codex |
| Backend de integrações (roteiro, orçamento, render, jobs, narração, corte) | `/root/flow-studio-api` (FastAPI, porta 8791) | Claude |
| Motor Google Flow | `/root/flow-mcp-source` (Node, MCP stdio + Chrome via CDP) | a decidir (ver tarefa de paridade) |

## O fluxo do vídeo, que é a referência de produto

| Tempo | Etapa | Regra que o vídeo ensina |
|---|---|---|
| 1:30 | 4 perguntas iniciais | Tipo de história, formato (aspecto e duração), orçamento em créditos e voz. Nada é gerado antes disso. |
| 2:05 | Personagem | Criado uma vez (nome, aparência, personalidade, voz) e reutilizado em todas as cenas. Editado no próprio personagem, de graça, sem recriar. |
| 3:00 | Imagens-chave primeiro | Imagens no Flow custam 0 créditos. Primeiro o plano descrito, depois as imagens. Revisar e refazer as imagens antes de gastar com vídeo. Modo em lote: até 50 imagens. |
| 3:55 | Imagem → vídeo | Omni Flash, 10 s, 720p, cerca de 15 créditos por shot. O shot N começa na imagem N e termina na N+1. O shot seguinte parte do último quadro do anterior. Os prompts de shot são escritos pela IA a partir das imagens. |
| 3:55 | Teto de créditos por shot | Antes de gerar, lê o preço que o próprio Flow cota. Se passar do teto, não gera e explica o motivo. |
| 4:30 | Movimentos de câmera | Biblioteca de 39 técnicas: órbita, crash zoom, drone, match cut, loop… |
| 5:10 | Emenda exata × personagem travado | Para continuação direta, usar a emenda exata no último quadro. Travar o personagem só quando o shot muda de lugar. Na emenda exata, o rosto precisa estar visível no último quadro. |
| 6:10 | Narração grátis | Texto escrito para a história com uma linha de direção de leitura. A narração é gravada antes dos clipes e define a duração mínima do filme. Voz escolhida (ex.: Charon). Usa a chave grátis do Google AI Studio. |
| 7:15 | Corte com FFmpeg | Clipes na ordem, narração por cima, música opcional, som dos clipes mais baixo e sem frame congelado no fim. 0 créditos. |
| 8:45 | Extras | Restyle (40 créditos, sem preço prévio, então sempre pedir confirmação), biblioteca, re-download grátis com upscale para 1080p, lote de imagens, painel sem IA com 7 abas. |

Custo do filme de 30 s: 45 créditos Flow. O plano grátis dá 50 créditos por dia.

Backlog de paridade: [TASK-20261008-FLOW-STUDIO-PARIDADE-001](../tasks/TASK-20261008-FLOW-STUDIO-PARIDADE-001.md).

## Ideia futura (Paolo, 2026-10-08)

Reaproveitar o CT 103 "flow-browser" (Chrome logado, Xvfb e noVNC) como **navegador de serviço** para outros modelos e ferramentas que só existem como site, no mesmo padrão MCP do flow-mcp.

- Um perfil de Chrome por conta ou ferramenta.
- Uma fila por perfil.
- Ritmo humano, para reduzir o risco de bloqueio.
- Preferir a API oficial sempre que existir.
