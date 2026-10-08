---
id: TASK-20261008-FLOW-INTEGRACOES-001
tipo: task
estado: parcial
projeto: flow-studio
responsavel: Claude Opus 5.5 (integrações); Codex (frontend, sessão interativa 2026-10-08 19:09)
data: '2026-10-08'
dependencias:
- credenciais via Infisical (OMNIROUTE_API_KEY, GEMINI_API_KEY)
- decisão sobre onde roda o Google Flow (máquina com tela)
tags:
- flow-studio
- integracoes
---

# TASK-20261008-FLOW-INTEGRACOES-001

## Divisão por subtarefa (sem checkout compartilhado)

| Área | Dono | Local |
|---|---|---|
| Frontend, design e contrato de provedores | Codex | `/root/flow-studio-mvp` (sem git) |
| Backend de integrações: roteiro, orçamento, render, jobs, narração e montagem | Claude | `/root/flow-studio-api` (git local `main`, HEAD `fdc5142`, sem push) |

O Claude não edita `/root/flow-studio-mvp`. O Codex não edita `/root/flow-studio-api`.

## Entregue (Claude)

- A API implementa `docs/PROVIDER_CONTRACT.md` do Codex. As rotas estão no `README.md` do repositório.
- Integrações:
  - roteiro via OmniRoute `codigo-gratis`;
  - Veo 3.1 lite via Gemini API, com preço oficial de US$ 0,05/s;
  - Google Flow via gflow-cli 0.83.1 (MIT), estimado em 10 créditos por clipe;
  - narração via Gemini TTS;
  - montagem via FFmpeg.
- O servidor obriga: aprovação e orçamento recalculado igual ao aprovado (senão 409), provedor conectado, e falha sem perder o storyboard nem os clipes.
- Validação: `pytest` com 7 testes passando (FFmpeg real; Veo, TTS, OmniRoute e gflow simulados). Smoke na 127.0.0.1:8791: `/api/providers` mostra os três provedores como desconectados, o que é honesto porque não há credenciais.
- Não houve chamada paga nem uso de credencial de produção.

## Sobreposição a resolver

O Codex criou `server/provider-api.mjs` (porta 8788, só `GET /api/providers`) e `server/flow-mcp-client.mjs` (status do Flow via `/root/flow-mcp-source`). Isso duplica o `status()`.

Proposta: um único backend. O Vite passa a apontar `/api` para a 8791. A checagem de status do flow-mcp é portada para dentro do adaptador `google-flow` ou descartada, ficando um só motor do Flow.

## Bloqueio comum aos dois motores do Flow

- gflow-cli: Chrome com interface; headless é recusado pelo reCAPTCHA.
- flow-mcp: testado só em macOS/Windows, com tela ligada.
- Nenhum dos dois roda no host Proxmox headless. É preciso escolher entre uma máquina do Paolo com tela ou um CT com Xvfb e noVNC.
- Há risco de bloqueio da conta Pro pessoal (ver `gflow docs account-safety`). Uso apenas em desenvolvimento.

## Revisão independente (Codex, `codex exec -s read-only`, 2026-10-08)

- Relatório completo: `/root/flow-studio-api/docs/review-codex-2026-10-08.md`.
- Achados 4 a 9, no backend: corrigidos no commit `67759ed`.
  - IDs de cena únicos e sequenciais.
  - TTS que devolve PCM cru é convertido em WAV.
  - Jobs interrompidos por reinício passam a "failed", mantendo os clipes.
  - Erro HTTP no polling do Veo é tratado.
  - O envelope JSON do gflow é validado.
  - O arquivo temporário do job tem nome único.
- Testes de regressão adicionados: 10 passam.
- O pytest do revisor travou no sandbox read-only, que não tem TMPDIR gravável. É limitação do ambiente; no host, a suíte termina em cerca de 6 s.
- Achados 1 a 3, no frontend (dono: Codex), continuam em aberto:
  - o proxy do Vite ainda aponta para a 8788;
  - `App.tsx` simula storyboard e render com `setTimeout`;
  - o fallback de `/api/providers` mostra o `google-flow` como `ready`.
