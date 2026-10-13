---
id: TASK-20261013-FLOW-STUDIO-P13-FRONTEND
estado: enviada ao Codex
dono: Codex
pedido_por: Paolo (13/10: "envie ao codex")
checkout_reservado: /root/flow-studio-mvp
escopo_permitido: /root/flow-studio-mvp (exceto node_modules); leitura em /root/flow-studio-api
backup: /root/backups/flow-studio-mvp-20261013.tgz (o frontend não tem git)
---

# P13 — ligar o frontend do Flow Studio ao backend real

Origem: [TASK-20261008-FLOW-STUDIO-PARIDADE-001](TASK-20261008-FLOW-STUDIO-PARIDADE-001.md) (P13 e "Coordenação com o Codex"),
achados 1 a 3 de `/root/flow-studio-api/docs/review-codex-2026-10-08.md`.

## O que fazer

1. Proxy do Vite: `/api` → `process.env.FLOW_API_TARGET ?? 'http://127.0.0.1:8791'` (hoje 8788).
2. Remover a simulação do `App.tsx` (`setTimeout` no storyboard e no render).
3. O fallback de `/api/providers` nunca mostra `google-flow` como `ready`. Sem resposta = "desconhecido/offline".
4. Wizard no fluxo `/api/projects` (contrato: `/root/flow-studio-api/README.md`, seção "Fluxo do vídeo"):
   1. Perguntas (história, formato/aspecto, duração, teto de créditos `maxCredits`, voz) → `POST /api/projects` → Plano editável (`PUT .../plan`).
   2. Personagem: retrato e "editar" (`POST .../character`, `.../character/edit`).
   3. Imagens: grade com "refazer" e feedback por cena (`.../frames`, `.../frames/redo`).
   4. Narração com player (`.../narration`).
   5. Orçamento (`GET .../quote`) → aprovar explicitamente (`POST .../shots {approved:true, quote}`).
   6. Vídeos dos shots.
   7. Corte (`.../cut`) → download (`GET .../files/{nome}`).
   - Após cada ação: acompanhar `GET /api/projects/{id}` até `busy == null`; mostrar `error` quando houver; 409 = etapa em andamento.
5. `server/provider-api.mjs` não pode iniciar outra instância do flow-mcp por stdio: um único processo é dono do Chrome (o da porta 8792, via backend).

## Regras

- Nenhuma chamada paga real ao Flow/Gemini durante o desenvolvimento. Validar contra o backend local com flow-mcp falso (testes de `/root/flow-studio-api`) ou mocks.
- Não mexer em `/root/flow-studio-api`, CT103 nem produção. Se o backend precisar mudar, anotar aqui em "Pedidos ao backend".
- Sem segredos em arquivos.

## Aceite

- `npm run build` e `npm run lint` passam.
- Nenhum `setTimeout` simulando etapa; nenhum `ready` falso.
- Relatório no fim deste arquivo: arquivos alterados, como testou, o que ficou de fora.

## Relatório do Codex

(pendente)
