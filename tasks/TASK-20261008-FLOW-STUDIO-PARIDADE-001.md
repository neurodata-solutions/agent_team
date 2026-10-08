---
id: TASK-20261008-FLOW-STUDIO-PARIDADE-001
tipo: task
estado: aberta
projeto: flow-studio
responsavel: coordenador (Claude Opus 5.5); execução dividida entre Claude (backend) e Codex (frontend)
data: '2026-10-08'
dependencias:
- TASK-20261008-FLOW-INTEGRACOES-001
- "Paolo: escolher o motor do Google Flow e a máquina com tela (P1)"
- credenciais via Infisical (OMNIROUTE_API_KEY, GEMINI_API_KEY)
tags:
- flow-studio
---

# TASK-20261008-FLOW-STUDIO-PARIDADE-001 — o que falta para fazer o que o vídeo faz

## Fontes

- Vídeo `JEla_mdlfxs`: descrição, capítulos e legenda en-US, lidos em 08/10. A legenda veio do download que o Codex fez em `/tmp/flow-video/`. A cópia integral não foi versionada por ser conteúdo de terceiros.
- Documentação da ferramenta do vídeo: `/root/flow-mcp-source/OVERVIEW.md` e `src/index.ts`, com 18 ferramentas MCP (`flow_status`, `flow_generate`, `flow_continue`, `flow_character`, `flow_character_edit`, `flow_agent_images`, `flow_narrate`, `flow_assemble`, `flow_edit`, `flow_techniques` etc.).
- Estado atual: `/root/flow-studio-api` @ `9dde77b`, `/root/flow-studio-mvp` (wizard com 4 etapas) e `/root/relatorios/TASK-20261008-FLOWROOM-PROVIDERS-001.md`.

## Lacunas, com dono e prioridade

| # | O vídeo faz | Hoje | Dono | Prio |
|---|---|---|---|---|
| P1 | Um só motor do Flow | Há dois: `flow-mcp` (Codex: status e generate) e `gflow-cli` (Claude: só t2v). Os dois exigem Chrome com tela. | Paolo decide; recomendação: **flow-mcp**, que é a ferramenta do vídeo e cobre todas as etapas. O adaptador gflow sai. | P0 |
| P2 | 4 perguntas iniciais: história, formato, orçamento e voz | O briefing só tem texto, duração e aspecto. Não há teto de créditos nem escolha de voz. | Claude: `CreateRequest` com `maxCredits` e `voice`. Codex: campos no briefing. | P0 |
| P3 | Imagens-chave antes do vídeo (grátis), com revisão e refação por imagem | O roteiro é só texto e o render vai direto para vídeo. Gasta crédito sem conferência visual. | Claude: etapa `POST /api/frames` (flow_generate com imagem, 0 créditos; Gemini: imagem) e refação por cena. Codex: etapa "Frames" no wizard. | P0 |
| P4 | Shot N vai do quadro N ao N+1, e o seguinte parte do último quadro | Só texto→vídeo, cenas independentes. | Claude: render com `startFrame`/`endFrame` e continuação (`flow_continue`). | P0 |
| P5 | Teto de créditos por shot com o preço cotado pelo Flow | Orçamento estimado por tabela (`veo-lite` 10 por clipe). Omni Flash ≈15 por 10 s não está na tabela. | Claude: repassar `max_credits` ao `flow_generate` e mostrar a recusa ao usuário. | P0 |
| P6 | Narração antes dos clipes, com direção de leitura e voz escolhida, definindo a duração mínima | TTS gerado depois dos clipes, voz fixa e sem direção. O corte da narração longa foi corrigido em `9dde77b`. | Claude: gerar narração após aprovar o roteiro e ajustar as durações das cenas a ela. | P1 |
| P7 | Personagem reutilizável: criar, ver retrato, editar no lugar e usar em todas as cenas | Inexistente. | Claude: `/api/characters` (flow_character, flow_character_edit, flow_characters). Codex: seletor de elenco. | P1 |
| P8 | Escolha entre emenda exata e personagem travado | Inexistente. | Claude: campo por shot; padrão emenda exata, travar personagem só quando o shot muda de lugar. | P1 |
| P9 | Biblioteca de movimentos de câmera | Inexistente. | Claude: expor `flow_techniques`. Codex: seletor por cena. | P2 |
| P10 | Corte com música opcional e ordem escolhida | Concatena e aplica a narração com o som dos clipes abaixado. | Claude: música e ordem. | P2 |
| P11 | Restyle (sempre confirmar, 40 créditos), biblioteca, re-download grátis em 1080p, retry e cancel, saldo de créditos | Inexistente (saldo só no status do flow-mcp). | Claude: rotas. Codex: telas. | P2 |
| P12 | Legendas para reels (pedido no fim do vídeo) | Inexistente. | Reaproveitar a skill `caption-animation` e o pipeline do Jaaz. | P3 |
| P13 | Frontend ligado ao backend | Ainda simulado (achados 1 a 3 da revisão do Codex). | Codex | P0 |

## Critério de aceitação do MVP com paridade

Reproduzir um "Lamplighter" equivalente:

- 30 s, um personagem, 3 imagens-chave aprovadas, 3 shots encadeados, narração com a voz escolhida e corte final sem frame congelado;
- gasto ≤ teto informado, sem nenhuma geração paga fora do orçamento aprovado;
- tudo pela interface, sem terminal.

## Bloqueios

- Os dois motores do Flow exigem Chrome com tela e login manual. É preciso escolher uma máquina com display ou um CT com Xvfb e noVNC (P1).
- Risco de bloqueio da conta Google Pro pessoal por automação. Usar só em desenvolvimento, nunca para clientes.
