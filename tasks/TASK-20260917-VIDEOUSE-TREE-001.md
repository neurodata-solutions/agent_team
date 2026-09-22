---
id: TASK-20260917-VIDEOUSE-TREE-001
tipo: task
estado: concluida
projeto: opensuite
responsavel: ambiente-linux-devops (subagente team-ambiente-linux-devops)
data: '2026-09-17'
dependencias:
- TASK-20260917-VIDEOUSE-FIT-001
tags:
- video-studio
---

# TASK-20260917-VIDEOUSE-TREE-001

## Objetivo

Decidir qual árvore OpenMontage/MoneyPrinter é a de produção (host vs CT100 vs /root/video-platform-audit) e localizar o pipeline de dublagem

## Escopo

somente leitura; comparação de hashes/tamanhos/mtimes; inspeção de containers em modo leitura

## Resultado

Os dois critérios verificados com evidência. (1) Árvore de produção do OpenMontage = CT100 /root/opensuite/services/openmontage, rastreada no git local do CT100 (4232 arquivos sob services/openmontage) e confirmada pelos labels do compose (project=opensuite, config=/root/opensuite/docker-compose.yml). Comparação recursiva md5+path: os 453 arquivos de /root/video-platform-audit/openmontage batem exatamente com a árvore do CT100 (2117 arquivos), zero divergência e zero arquivo exclusivo — a cópia do host é subconjunto byte-idêntico (21,4%), sem git, portanto snapshot de auditoria e não checkout de produção. O /app do container opensuite-openmontage é idêntico à árvore do CT100 (única divergência: 6 .pyc gerados em runtime e .dockerignore excluído da imagem). O host /root/opensuite existe mas é pasta solta de 12 arquivos .tsx/.py sem git e sem services/ — a conclusão anterior de que 'não contém OpenMontage' valia só para o host. (2) Pipeline de dublagem LOCALIZADO, em duas variantes que correspondem à memória do usuário: Bloco 1 literal = CT100 /root/opensuite/dub_pipeline.py (11955 B, md5 0b1558e1f6a5, faster-whisper -> Argos Translate -> edge-tts pt-BR-AntonioNeural -> ajuste de tempo -> .srt -> ffmpeg) e Bloco 2 adaptação criativa via LLM = CT100 /root/opensuite/recreate_pipeline.py (19480 B, md5 b913595426b9, LLM_PROVIDER openrouter/openai/anthropic, prompt exige PT-BR explícito, linha 3 'adaptação criativa (não é tradução literal)'). Ambos estão presentes e executáveis dentro do container opensuite-moneyprinter em /MoneyPrinterTurbo/ com md5 idêntico ao do disco do CT100, e as dependências estão instaladas (argostranslate 1.11.0, faster-whisper 1.1.0, edge-tts 7.2.7, openai 2.24.0, ffmpeg/ffprobe em /usr/bin). Insumos do teste NASA presentes: nasa_epps_full.mp4 (19,2 MB), video_teste_pt.mp4 + .srt. Achado de risco: docker diff mostra os dois pipelines como 'A' (adicionados na camada mutável do container), não na imagem nem em bind mount, e ambos são UNTRACKED no git do CT100 — sobrevivem só enquanto o container não for recriado. Achado adicional: existem DUAS stacks MoneyPrinter vivas no CT100 com bases de código diferentes — a de produção opensuite-moneyprinter/-worker/-webui (código na imagem, fonte em /root/opensuite/services/moneyprinter, cli.py 54832 B) e uma paralela legada moneyprinterturbo-api/-webui que bind-monta /root/pessoal/ai-lab/MoneyPrinterTurbo (cli.py 29058 B, compose próprio); /root/apps/estudio-visual/MoneyPrinterTurbo é terceira cópia inerte (mtimes achatados em Aug 26, sem config.toml nem storage). CT102 não contém nenhuma dessas árvores nem os pipelines.

## Verificações

- 2/2 critérios: passou
- comparação recursiva md5+path openmontage (audit vs CT100): executada, passou (453/453 idênticos, 0 divergentes)
- comparação /app do container vs árvore CT100: executada, passou (só .pyc de runtime divergem)
- rastreio git de services/openmontage no CT100: executada, passou
- presença e md5 dos dois pipelines no container opensuite-moneyprinter: executada, passou
- dependências argostranslate/faster-whisper/edge-tts/openai/ffmpeg no container: executada, passou
- busca de árvores e pipelines no CT102: executada, resultado vazio
- execução dos pipelines de dublagem: não executada (fora do escopo)
- conteúdo de secrets (.env, config.toml): não lido (proibido pelo contrato)

## Limitações

- repo git do CT100 não tem remote: não há origem remota para confirmar linhagem além do histórico local
- os dois pipelines de dublagem são untracked no git e vivem na camada mutável do container: não há artefato versionado da versão em execução
- diferença entre as duas stacks MoneyPrinter não foi diffada arquivo a arquivo (só metadados e amostras)

## Próximo passo

propor ao usuário uma ação reversível e autorizável para persistir os dois pipelines de dublagem (git add + commit em CT100 /root/opensuite, ou COPY no Dockerfile do moneyprinter) antes de qualquer recreate do container; e decidir qual das duas stacks MoneyPrinter é a alvo de integração. Nenhuma dessas ações foi executada.
