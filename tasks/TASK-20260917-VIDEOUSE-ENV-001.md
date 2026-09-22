---
id: TASK-20260917-VIDEOUSE-ENV-001
tipo: task
estado: concluida
projeto: opensuite
responsavel: ambiente-linux-devops (subagente team-ambiente-linux-devops)
data: '2026-09-17'
dependencias: []
tags:
- video-studio
---

# TASK-20260917-VIDEOUSE-ENV-001

## Objetivo

Determinar o que o video-use é (deps/licença/modelo de execução) e se host e CT100 satisfazem seus pré-requisitos, sem instalar nada

## Escopo

clone somente-leitura, leitura de arquivos, comandos de inspeção no host e CT100

## Resultado

Os cinco critérios verificados com evidência. video-use é MIT/Python>=3.10 com deps open-source; orquestração depende de agente lendo SKILL.md (Hard Rule 10 exige a ferramenta Agent), embora os helpers sejam CLI standalone; ElevenLabs Scribe obrigatória sem fallback e whisper local declarado anti-pattern; ffmpeg ausente em host e base do CT100; host já tem toolchains uv >=3.10; CT100 sem uv e com 86% de disco usado.

## Verificações

- 5/5 critérios: passou
- instalação: não executada
- desempenho de GPU: indisponível

## Limitações

- GPU não testada (sem driver carregado)
- ffmpeg não verificado dentro de cada container Docker

## Próximo passo

nenhum sem autorização explícita; instalar ffmpeg e popular .env com chave ElevenLabs foram identificados como ações fora do escopo e não executados

## Outros campos

- **caminho:** /tmp/claude-0/-root/689f7cca-0c88-4c3d-b340-9a7861cdc32d/scratchpad/video-use; inspeção via pct exec 100
- **checkout_reservado:** nenhum (somente leitura; clone isolado no scratchpad)
- **criterios_aceitacao:**   - pyproject/licença/deps/serviços pagos inventariados
  - modelo de execução comprovado por arquivo:linha
  - pré-requisitos no host e CT100 separados
  - exigência da chave ElevenLabs e fallback verificados na fonte
  - presença de faster-whisper confirmada
- **entrega_esperada:** formato do contrato; Alterações = nenhuma
- **fora_do_escopo:** instalar/remover pacotes, uv sync, pip install, apt install, alterar containers/serviços/rede, iniciar serviços, ler valores de secrets, escrever em /root/jaaz ou /root/opensuite
- **integrador:** coordenador
- **maquina:** host srv e CT100
- **skills_referencias:**   - team-operar-ambiente
  - verify-and-stop
- **versao_estado:** video-use HEAD 9575612f066aa517354790a645fd90f9f95a743b (clone 2026-09-17); uv 0.12.6; docker 29.7.2 no CT100
