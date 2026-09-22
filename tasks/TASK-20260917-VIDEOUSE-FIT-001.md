---
id: TASK-20260917-VIDEOUSE-FIT-001
tipo: task
estado: concluida
projeto: jaaz
responsavel: code-reviewer (subagente team-code-reviewer)
data: '2026-09-17'
dependencias: []
tags:
- video-studio
---

# TASK-20260917-VIDEOUSE-FIT-001

## Objetivo

Mapear na fonte real quais capacidades de edição de vídeo já existem e qual é o contrato de integração das tools do Jaaz

## Escopo

somente leitura: Read, Grep, Glob, git log/status/rev-parse, leituras do MCP code-review-graph

## Resultado

Os cinco critérios verificados. Tabela de sobreposição: JÁ EXISTE para legendas burn-in word-level e overlays Remotion/PIL; EXISTE PARCIALMENTE para remoção de silêncio, color grading e fades de áudio (presentes no OpenMontage mas não ligados ao screen-demo.yaml nem ao Jaaz); NÃO EXISTE para remoção de filler words; NÃO ENCONTRADO NA FONTE para autoverificação de qualidade de cortes. Contrato confirmado: provider=system registra sem gate de api_key e não exige serviço HTTP, mas o resultado precisa ser URL buscável por HTTP para entrar no canvas.

## Verificações

- 5/5 critérios: passou
- execução de pipeline/teste: não executada (fora do escopo)

## Limitações

- /root/opensuite não contém o OpenMontage; fonte real em /root/video-platform-audit/openmontage, sem git
- pipeline de dublagem não localizado no host
- achados refletem working tree não commitado do Jaaz
- grafo stale; build/update não executado

## Próximo passo

tarefa somente-leitura dedicada para decidir qual árvore é a de produção e localizar o pipeline de dublagem

## Outros campos

- **caminho:** /root/jaaz; /root/video-platform-audit/openmontage (caminho real, divergente do esperado /root/opensuite)
- **checkout_reservado:** nenhum (somente leitura)
- **criterios_aceitacao:**   - inventário do /video_studio com arquivo:linha
  - contrato de process_video_result e tratamento de provider=system
  - pipelines OpenMontage e primitivas do screen-demo.yaml
  - transcrição word-level e corte por silêncio em MoneyPrinter/OpenShorts/dublagem
  - tabela de sobreposição das sete capacidades do video-use
- **entrega_esperada:** formato do contrato; tabela de sobreposição como entregável central; Alterações = nenhuma
- **fora_do_escopo:** qualquer escrita, commit, stage, instalação, execução da aplicação ou de pipeline, chamada de API externa, leitura de valores de secrets
- **integrador:** coordenador
- **maquina:** host srv
- **skills_referencias:**   - team-revisar-alteracao
  - verify-and-stop
- **versao_estado:** jaaz remote 11cafe/jaaz branch main HEAD e07e5e98c63f8648d1947f09230773533e388e88, 17 entradas não commitadas; openmontage/moneyprinter/openshorts/facefusion não são repositórios git
