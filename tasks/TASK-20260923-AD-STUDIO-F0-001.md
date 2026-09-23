---
id: TASK-20260923-AD-STUDIO-F0-001
tipo: coordenacao
estado: parcial
projeto: jaaz
responsavel: coordenador
data: '2026-09-23'
dependencias: []
tags:
- ad-studio
- f0
modo_escolhido: padrão
justificativa_modo: A SPEC envolve Jaaz, canvas, MPT, volumes, SQLite e QA; exige baseline e verificação independente antes de implementação.
checkout_reservado: /root/jaaz (documental; árvore já contém alterações não commitadas pré-existentes)
---

# Tarefa F0 — baseline e contrato de render local

## Objetivo

Iniciar a implementação do Ad Studio pela confirmação do ambiente real, do
container que processa as tarefas do MPT e da possibilidade de renderizar três
clipes locais em ordem determinística.

## Escopo

- Jaaz `/root/jaaz`, branch `jaaz`, HEAD `b4b863d017715577de22b9131c43559f567416b9`.
- CT100 `192.168.0.200` e containers `opensuite-jaaz`, `opensuite-moneyprinter` e `opensuite-moneyprinter-worker`.
- Leitura de mounts, compose, código MPT e teste de render autorizado pela decisão D-01 da SPEC.

## Fora do escopo

- Alterar código do MPT.
- Migrar segredos ou alterar `config.toml`.
- Rebuild/recreate/deploy de containers.
- Implementar busca de provedores, canvas ou migrations v5 nesta tarefa.

## Critérios de aceitação

1. Identificar qual processo/container consome a fila/API do MPT.
2. Identificar mounts comuns disponíveis para Jaaz, API e worker.
3. Executar o teste D-01 com três clipes locais existentes, sem busca externa, e registrar ordem, ffprobe e logs.
4. Se o teste falhar, registrar causa confirmada e decisão sobre `local_ffmpeg`.

## Resultado

T0.1 passou parcialmente: `opensuite-moneyprinter` executa a API com
`python3 main.py`; `opensuite-moneyprinter-worker` executa
`python -m app.services.worker`; ambos compartilham o volume
`opensuite_moneyprinter_outputs` em `/MoneyPrinterTurbo/storage`. O Jaaz não
compartilha ainda um diretório de materiais com esses containers.

O teste D-01 foi executado com três clipes locais e concluiu a tarefa
`e782a48a-a5fb-4e22-a130-f78292b1730b`. O manifesto do MPT registrou os três
arquivos na ordem 0, 1, 2; os logs mostraram `preprocess local materials` e
não mostraram busca Pexels/Pixabay/Coverr. O resultado foi 1080x1920, com
áudio silencioso e duração final de aproximadamente 3,03 s.

O primeiro envio com caminhos absolutos em `cache_videos` foi rejeitado. A
implementação de `preprocess_video` resolve `MaterialInfo.url` dentro de
`storage/local_videos` e rejeita caminhos que escapem desse diretório. Após
copiar os três arquivos para esse diretório e enviar apenas os nomes de
arquivo, o teste passou. A SPEC precisa refletir essa restrição, e o volume
compartilhado deve alimentar `storage/local_videos` sem aceitar caminhos
arbitrários.

## Estado inicial / evidências

- Jaaz está ativo na imagem `opensuite-jaaz:no-voice-fix-20260923`.
- MPT principal e worker montam o volume `opensuite_moneyprinter_outputs` em `/MoneyPrinterTurbo/storage`.
- Jaaz não possui atualmente o volume de materiais compartilhado com o MPT.
- `/root/opensuite/services/moneyprinter/docker-compose.yml` declara apenas `webui` e `api`; a origem do worker customizado ainda precisa ser confirmada.
- O grafo do code-review-graph está atualizado no HEAD, mas não encontrou símbolos do adaptador por busca semântica; a fonte direta prevalece.

## Limitação confirmada

O teste não atende ainda a duração esperada de três segmentos de 2 s: o
`combined-1.mp4` e o `final-1.mp4` ficaram em aproximadamente 3,03 s. A causa
exata entre duração de áudio silencioso, concatenação e parâmetros de tarefa
precisa ser isolada antes de declarar o contrato de render determinístico como
aprovado. O teste também mostrou que `voice_name=no-voice` no MPT cria um
stream de áudio silencioso; a remoção física da faixa continua sendo
responsabilidade do adaptador Jaaz conforme a SPEC.

Os artefatos temporários do teste foram removidos após a validação. Nenhum
container foi reiniciado e nenhuma configuração foi alterada.

## Próximo passo

Investigar a causa da duração de 3,03 s e testar o mapeamento do adaptador v2
com um contrato de duração explícito; depois repetir a validação com QA
independente antes de implementar o pipeline completo.
