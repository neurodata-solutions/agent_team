---
id: TASK-20260917-VIDEOUSE-EVAL-001
tipo: task
estado: concluida
projeto: jaaz
responsavel: coordenador
data: '2026-09-17'
dependencias: []
tags:
- video-studio
---

# TASK-20260917-VIDEOUSE-EVAL-001

## Objetivo

Determinar onde, se em algum lugar, o repositório browser-use/video-use se encaixa como capacidade do nosso app de criação/edição/postagem de vídeo

## Escopo

diagnóstico somente leitura; clone somente-leitura no scratchpad; inspeção read-only de host e CT100; TASK_REGISTER.md

## Resultado

Veredito: ENCAIXA PARCIALMENTE, e apenas como fonte de duas primitivas e de decisões de design — NÃO como componente instalado ou dependência de runtime. Cinco das sete capacidades anunciadas já existem na nossa fonte (legendas burn-in word-level e overlays Remotion/PIL no Jaaz; silence_cutter, color_grade e fades de áudio no OpenMontage). Apenas duas são genuinamente novas: remoção de filler words (inexistente em toda a nossa fonte) e autoverificação de qualidade de cortes. O bloqueio decisivo é o modelo de execução: o video-use não tem entrypoint headless que orquestre o fluxo completo — o valor editorial mora no SKILL.md lido por um agente, com dependência explícita da ferramenta Agent do Claude Code (Hard Rule 10). Os helpers individuais são chamáveis via CLI, mas a decisão/orquestração não é código. Somado à exigência de chave paga ElevenLabs Scribe sem fallback (com whisper local declarado anti-pattern pelo próprio projeto), enquanto já rodamos faster-whisper com word_timestamps=True de graça em produção, a adoção como dependência é rejeitada.

## Evidências

- video-use: MIT, requires-python >=3.10, deps diretas requests/librosa/matplotlib/pillow/numpy, extra opcional manim; sem [project.scripts]
- video-use SKILL.md:1-4 declara-se skill para Claude Code; SKILL.md:31 (Hard Rule 10) exige a ferramenta Agent para sub-agentes paralelos; README.md:25-40 exige agente com shell access
- video-use helpers são CLI standalone (argparse + __main__): helpers/transcribe.py:240, helpers/render.py:770, helpers/pack_transcripts.py:205, helpers/grade.py:374, helpers/transcribe_batch.py:125, helpers/timeline_view.py:391
- video-use helpers/transcribe.py:33 SCRIBE_URL ElevenLabs; :36-49 load_api_key; :48 sys.exit sem fallback; SKILL.md:312-313 declara whisper local anti-pattern
- jaaz server/tools/local_video_worker.py:264-289 faster_whisper word_timestamps=True; :68-233 write_caption_files burn-in ASS por palavra; :393,398 filtro ass=; :394-399 corte vertical por scale/crop/gblur
- jaaz local_video_worker.py: ausência verificada de remoção de silêncio, filler words, color grading e fade de áudio; o único \fad (:190-203) é fade visual de texto
- jaaz server/tools/video_generation/video_canvas_utils.py:158-200 process_video_result(video_url,...); :207-219 exige URL buscável por HTTP GET, sem fallback para path local; video_router.py:549-563 constrói URL local antes de registrar no canvas
- jaaz server/services/tool_service.py:201-209 registra provider=system incondicionalmente, fora do gate de api_key de :220-233 — capacidade local não precisa ser serviço HTTP
- openmontage tools/video/silence_cutter.py:1-51 (modos remove/speed_up/mark, silencedetect, stability EXPERIMENTAL) ligado a pipeline_defs/talking-head.yaml:94,98,146,149,182,197
- openmontage tools/enhancement/color_grade.py:1-60+ (5 perfis + LUT .cube) ligado a cinematic.yaml:109,245,253, clip-factory.yaml:171,177, documentary-montage.yaml:153,159,167, hybrid.yaml:186,194, talking-head.yaml:178,193
- openmontage tools/audio/audio_mixer.py:43,86-87,235-251,672-771 fades de áudio, com tests/tools/test_audio_mixer_track_fades.py
- openmontage pipeline_defs/screen-demo.yaml: zero ocorrências de silêncio/filler/color-grade/fade; :226 valida apenas ffprobe; :84-247 depende de checkpoint/human_approval
- filler words: busca ampla (filler.?word|\bumm\b|disfluenc) em jaaz/, openmontage/, moneyprinter/, openshorts/ sem nenhuma ocorrência
- moneyprinter/app/services/subtitle.py:58-60 e openshorts/subtitles.py:31-33 têm word_timestamps=True + VAD, mas VAD serve à transcrição, não a corte de vídeo
- ambiente: ffmpeg ausente do PATH no host e na base do CT100 (só binário estático bundlado em /root/youtube-automation-agent/node_modules/ffmpeg-static/ffmpeg 7.0.2 no CT100); python3 3.9.2 em ambos; uv 0.12.6 só no host com toolchains 3.10/3.11/3.13/3.14 já baixados; CT100 sem uv
- ambiente: host 60G livres (34% uso); CT100 23G livres (86% uso); GPU GT 610 sem driver carregado no host, sem passthrough para o CT100
- faster-whisper já em produção dentro dos containers opensuite-jaaz (1.2.1) e opensuite-moneyprinter/-worker (1.1.0); ausente do host e da base do CT100

## Arquivos alterados

- TASK_REGISTER.md

## Verificações

- inspeção do pyproject/licença/deps do video-use: passou
- modelo de execução comprovado por arquivo:linha: passou
- matriz de sobreposição com arquivo:linha por célula: passou
- contrato de integração do Jaaz (process_video_result e TOOL_MAPPING): passou
- inventário de pré-requisitos no host e CT100: passou
- execução de pipeline, render ou instalação: não executada (fora do escopo)

## Limitações

- /root/opensuite NÃO contém o OpenMontage; a fonte real inspecionada foi /root/video-platform-audit/openmontage, que não é repositório git — pode ser cópia de auditoria e não o checkout de produção
- nenhum caminho *dubbing* ou opensuite-moneyprinter existe neste host; o pipeline de dublagem da memória não foi localizado na fonte (não confirmado nem negado)
- os achados do Jaaz refletem o working tree com 17 alterações não commitadas, incluindo os três arquivos centrais da análise (video_router.py, enhance_canvas_video.py, local_video_worker.py), não o HEAD
- grafo code-review-graph de /root/jaaz está stale (build a6e465b5 vs HEAD e07e5e98); build/update não executado; todas as conclusões vêm de leitura direta da fonte
- ffmpeg foi verificado no host e na base do CT100, não dentro de cada container Docker; o Jaaz claramente usa ffmpeg, logo ele existe em nível de container — a verificação por container não foi feita
- desempenho/compatibilidade real da GPU GT 610 não testado (sem driver carregado; testar exigiria instalação)

## Próximo passo

Escrever uma spec somente-documental de um tool `filler_cutter` para o OpenMontage, portando apenas a lógica de detecção de disfluência do video-use (MIT, compatível com AGPL-3.0) adaptada ao output word-level do faster-whisper que já produzimos, mais a decisão de ligar os silence_cutter/color_grade/audio_mixer existentes ao screen-demo.yaml. Nenhuma instalação do video-use, nenhuma chave ElevenLabs. Antes disso, resolver a lacuna de árvore de produção (TASK-20260917-VIDEOUSE-TREE-001, proposta e não disparada).

## Outros campos

- **agentes:** 2
- **caminho:** /root/jaaz, /root/opensuite, /root/video-platform-audit/openmontage, clone em /tmp/claude-0/-root/689f7cca-0c88-4c3d-b340-9a7861cdc32d/scratchpad/video-use
- **checkout_reservado:** nenhum (diagnóstico somente leitura); apenas TASK_REGISTER.md foi escrito
- **criterios_aceitacao:**   - veredito claro: encaixa / não encaixa / encaixa parcialmente
  - justificativa técnica com evidência de fonte
  - localização proposta na arquitetura atual ou motivo da recusa
  - lista de riscos e custos
- **custo:** não disponível; nenhum preço consultado
- **entrega_esperada:** veredito, matriz de sobreposição, análise do modelo de integração, riscos/custos e próximo passo reversível
- **ferramenta:** Claude Code (Agent tool) + code-review-graph MCP (leitura) + git/pct/docker em modo leitura
- **fora_do_escopo:** alteração de código do produto, instalação de pacotes, uv sync, apt install, criação/alteração de containers ou serviços, leitura de valores de secrets, deploy, commit/push em jaaz ou opensuite
- **integrador:** coordenador
- **justificativa_modo:** Decisão de roadmap com impacto relevante e dois eixos de investigação genuinamente independentes (repositório+ambiente vs. capacidades já existentes na nossa fonte); paralelizados sem sobreposição de arquivos, com síntese pelo coordenador.
- **maquina:** host srv (Debian 11.6, pve-manager/7.4-3); CT100 (LXC docker, Debian 11.7); CT102 fora do escopo
- **modelo:** coordenador em Opus 5; dois subagentes em Sonnet
- **modo_escolhido:** ampliado
- **provedor:** não disponível
- **resultado_retrabalho:** sem retrabalho; dois eixos independentes, nenhuma análise repetida
- **skills_referencias:**   - team-coordenar-entrega
  - team-operar-ambiente
  - team-revisar-alteracao
  - verify-and-stop
- **tentativas:** 1
- **tokens_cache:** não disponíveis
- **tokens_entrada:** não disponíveis
- **tokens_saida:** não disponíveis
- **versao_estado:** video-use HEAD 9575612f066aa517354790a645fd90f9f95a743b; jaaz remote 11cafe/jaaz branch main HEAD e07e5e98c63f8648d1947f09230773533e388e88 com 17 entradas não commitadas; agent-team master a36b7e2
