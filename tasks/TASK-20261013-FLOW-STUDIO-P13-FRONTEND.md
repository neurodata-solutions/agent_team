---
id: TASK-20261013-FLOW-STUDIO-P13-FRONTEND
estado: entregue — falta teste real no CT103
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

Tarefa: TASK-20261013-FLOW-STUDIO-P13-FRONTEND  
Estado: parcial — implementação e gates de código concluídos; gate visual/end-to-end bloqueado pelo sandbox desta sessão.  
Escopo verificado: `/root/flow-studio-mvp`, frontend Vite/React e bridge local `server/provider-api.mjs`; backend apenas lido em `/root/flow-studio-api`. Nenhuma alteração no backend, CT103 ou produção.

### Alterações

- `vite.config.ts`: proxy `/api` para `process.env.FLOW_API_TARGET ?? 'http://127.0.0.1:8791'`.
- `src/App.tsx`: substituição do storyboard/render simulado pelo fluxo real de `/api/projects`: briefing com teto/voz, plano editável, personagem e edição, grade de frames com refação/feedback, narração com player, quote, aprovação explícita dos shots, polling até `busy == null`, exibição de `error`/409 e corte/download.
- `src/providers.ts`: Google Flow inicia como `offline`/desconhecido; somente resposta real `connected: true` muda para `ready`.
- `src/App.css`: estados de erro, processamento, assets, frames, quote e player.
- `server/provider-api.mjs`: remoção do `FlowMcpClient` e das chamadas stdio duplicadas; o processo não inicia outra instância do flow-mcp. O arquivo de cliente obsoleto `server/flow-mcp-client.mjs` foi removido.

### Validação

- `npm run build`: passou.
- `npm run lint`: passou; permanece apenas warning não bloqueante `react(set-state-in-effect)` em `src/App.tsx:37`.
- `node --check server/provider-api.mjs`: passou.
- Busca estática: não há timer simulando etapa; o único `setTimeout` é o intervalo de polling de `GET /api/projects/{id}`. Não há `google-flow` inicializado como `ready`.
- Nenhuma chamada paga ao Flow/Gemini foi feita.
- Tentativa de backend mock local e Vite: bloqueada por `listen EPERM` ao abrir sockets no sandbox.
- Tentativa de Playwright com Chromium local: bloqueada por `setsockopt EPERM`/falha do crashpad; não foi possível exercitar o fluxo real nem gravar `/root/qa/ui-evidence/.../evidence.json` porque essa raiz não é gravável nesta sessão.

### O que ficou de fora / riscos

- Gate Playwright e evidência QA-UI-001 continuam pendentes e são obrigatórios antes de declarar concluída.
- O warning de `useEffect` é de lint não bloqueante e não altera o fluxo.
- O bridge legado ainda pode ser iniciado pelo script local na porta 8788, mas não possui mais cliente stdio nem rota de provider; o backend real em 8791 é a fonte do `/api`.


## Verificação independente (Claude, 13/10)

- `npm run build` passa; `npm run lint` passa, com 1 aviso (`set-state-in-effect`, `App.tsx:37`).
- **Ponta a ponta no navegador** (Chromium headless; o gate que o sandbox do Codex bloqueou):
  - backend real `flow-studio-api` na 8791 com o flow-mcp, o OmniRoute e o Gemini falsos da suíte (`tests/test_studio.py`), sem nenhuma chamada paga; Vite na 5199 com o proxy novo;
  - Briefing → Plano → Personagem → Imagens → Narração → Orçamento → aprovar → Vídeos → Corte → "Baixar vídeo": todas as etapas concluídas, 0 erro no console, 45/45 créditos no fake, `final.mp4` servido por `/files/final.mp4`;
  - cada etapa bateu na rota certa (`POST /api/projects`, `PUT /plan`, `/character`, `/frames`, `/narration`, `GET /quote`, `/shots`, `/cut`).
- **Observações (não bloqueiam):**
  - a tela de entrega mostra um cartão "final.mp4" com ▶, mas não há `<video>` tocando o arquivo;
  - "Minha conta / Google AI Pro" na barra lateral é texto fixo;
  - `App.tsx` tem 71 linhas, sendo 19 com mais de 300 caracteres (JSX em linha única), o que dificulta revisar e manter.
- **Falta:** o teste real no CT103 (login do Google no Chrome via noVNC + as chaves do OmniRoute e do Gemini).
