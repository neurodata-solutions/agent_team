---
id: TASK-20261008-FLOW-STUDIO-PARIDADE-001
tipo: task
estado: adiada
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

- Vídeo `JEla_mdlfxs`: descrição, capítulos e legenda en-US, lidos em 08/10. A legenda veio do download que o Codex fez em `/tmp/flow-video/`. A cópia integral não foi versionada por ser conteúdo de terceiros. Essa cópia se perdeu; em 13/10 a legenda foi baixada de novo para `/root/incoming/flow-video/` (`JEla_mdlfxs.en-US.vtt` e versão em texto `.txt`), fora do git.
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

## Atualização 2026-10-08 (Claude): decisão e backend

- **Decisão do Paolo:** fidelidade ao vídeo primeiro ("deixamos o simples funcional e vamos aplicando melhorias").
- **P1 decidido:** o motor do Flow é o **flow-mcp**. O adaptador gflow-cli foi removido de `/root/flow-studio-api`.
- **Backend `/root/flow-studio-api` @ `80d8a39`:** fluxo `/api/projects` cobrindo P2, P3, P4, P5, P6 e P7, com a parte de backend de P9 (campo `technique` por cena). Rotas no README.
  - Chama o flow-mcp via `POST http://127.0.0.1:$FLOW_MCP_PORT/api/<tool>` com o token, e busca os arquivos por `/media`.
  - Testes: 13 passam, incluindo o "Lamplighter" ponta a ponta contra um flow-mcp falso e FFmpeg real.
  - Esses testes provam a ordem das etapas, o personagem em todas as imagens, os shots encadeados (imagem N → N+1), o teto de 15 créditos por shot, a recusa acima do teto e a narração de 32 s sem corte.
- **P8:** só a emenda exata (`chain_previous`), que é o padrão recomendado no vídeo. "Travar personagem" fica para a fase de melhorias.
- **Não verificado ao vivo:** nenhuma chamada real ao Flow, porque não há tela nem login.

### Coordenação com o Codex (importante)

- O flow-mcp precisa ser iniciado com `FLOW_MCP_PORT=8792`. A porta 8787 é do gateway Caveman: com ela ocupada, o flow-mcp não sobe a API HTTP, e o backend fica sem acesso a ele.
- Só um processo pode ser dono do Chrome e da fila. Em vez de o `server/provider-api.mjs` iniciar a própria instância por stdio, o login e o status devem usar o mesmo processo `npm run studio` na 8792.
- **P13 (frontend):** trocar o wizard simulado pelo fluxo `/api/projects`:
  1. Perguntas → Plano (editável).
  2. Personagem (retrato e "editar").
  3. Imagens (grade com "refazer" e feedback por cena).
  4. Narração (player).
  5. Orçamento → aprovar.
  6. Vídeos.
  7. Corte → download.
  - Acompanhar `GET /api/projects/{id}` até `busy` virar `null`, mostrando `error` quando houver.
  - Apontar o proxy do Vite para a porta 8791.

### Revisão do Codex do fluxo (2026-10-08) → corrigido em `/root/flow-studio-api` @ HEAD

Relatório: `/root/flow-studio-api/docs/review-codex-2026-10-08-workflow.md`.

Corrigido no backend, com testes (17 passam):

- Narração obrigatória antes dos shots pagos e antes do corte.
- Troca de `busy` atômica: com 5 requisições simultâneas, uma é aceita (202) e quatro recusadas (409).
- Os ids dos jobs pagos são gravados antes de esperar. Após um reinício, o servidor **retoma** os mesmos jobs em vez de reenviar. Um job que o flow-mcp esqueceu vira falha com o aviso "confira a biblioteca do Flow". Um segundo `/shots` é recusado.
- A refação de imagem usa como referência a imagem real da cena anterior.
- Editar o personagem atualiza o `look` no plano e no flow-mcp.
- O texto do orçamento diz que o preço real é cotado pelo Flow em cada shot.
- O worker ignora projeto ilegível.

Em aberto: o frontend ainda é simulado (P13, Codex). Também falta repetir só os shots que falharam (hoje, uma falha parcial bloqueia novo envio; melhoria futura via `flow_retry`).

## Atualização 2026-10-19 (Paolo): projeto adiado

- Paolo: "esse projeto vai ficar pra frente, pois instalamos local". O Flow Studio do vídeo já está instalado localmente e em uso; a versão própria (`flow-studio-api` + `flow-studio-mvp`, CT103) fica em espera.
- Estado congelado: nenhuma geração real feita; `gemini.pending` não ativado no CT103; `OMNIROUTE_API_KEY` ausente no CT103; mudanças sem commit em `/root/flow-studio-api` (status simplificado do provedor e deploy CT103).
- Ao retomar: começar pelos passos 1–4 da comparação de 19/10 (ativar Gemini, OmniRoute, teste de US$ 0,20, "Lamplighter").
