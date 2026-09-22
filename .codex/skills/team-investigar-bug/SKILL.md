---
name: team-investigar-bug
description: Investigue falhas ambíguas ou intermitentes antes de propor correções, mantendo hipótese separada de causa confirmada. Suporta modo comum econômico e modo aprofundado de contestação independente.
---

# Team — investigar bug

## Objetivo e entradas

Explicar um sintoma por mecanismo comprovável. Receba relato, versão, caminho,
condição de ocorrência, logs seguros e limite de reprodução.

## Modo padrão: investigação econômica direta

O fluxo padrão da equipe para problemas simples e diagnóstico inicial:

0. **Leia o log real do serviço/processo afetado antes de formar qualquer
   hipótese.** `journalctl -u <serviço> -n 200`, `docker logs --tail 200
   <container>` (ou `pct exec 100 -- docker logs ...` para stacks em CT),
   ou o arquivo de log da aplicação. Registre timestamp do evento e a linha
   de erro literal como evidência primária. Ausência de log correspondente
   ao sintoma é achado a registrar, não algo a pular em silêncio. Na
   superfície Claude, a skill `systematic-debugging` (pacote `superpowers`,
   já instalado) reforça essa disciplina antes de propor causa.
1. Registre sintoma observável e expectativa, sem assumir causa.
2. Confirme versão/ambiente e reproduza com o menor caso; preserve um baseline.
3. Trace entradas, estados, fronteiras de ownership e saída de erro.
4. Liste hipóteses ranqueadas por evidência e falsificação barata; use
   `investigate-first` e descarte hipóteses com observações reproduzíveis.
   Quando a causa exigir evidência de runtime que o log não tem (variável
   em memória, ordem de eventos), use a instrumentação hipótese-orientada
   de `debug-mode` (`third_party/debug-mode/`) — grava em `.agents/debug.log`,
   nunca em stdout/stderr, e exige limpeza da instrumentação antes de
   `concluída`. Quando o sintoma for de UI/frontend, use
   `browser-testing-with-devtools` (`third_party/agent-skills/`, requer MCP
   `chrome-devtools` em modo `--isolated`) para inspecionar DOM, console e
   rede reais em vez de supor comportamento do navegador.
5. Nomeie causa confirmada somente quando uma mudança/condição explicar o
   sintoma e houver prova independente; caso contrário, mantenha hipóteses.

## Modo de contestação independente (Bug Hunt)

Modo aprofundado com contestação adversária entre papéis isolados, baseado no
insumo de `third_party/bug-hunt/` (Hunter/Skeptic/Referee original) e, como
insumo metodológico adicional para achados de segurança/concorrência, os
prompts de `third_party/bug-hunter/` (recon + threat-model) — nunca o CLI
nem o modo `--autonomous` da origem. Detalhado em `./modo-contestacao.md`.

### Critérios de acionamento

Use este modo exclusivamente quando:
1. A investigação inicial comum não resolver uma falha relevante.
2. Houver achados controversos entre agentes ou com o usuário.
3. O usuário solicitar expressamente busca aprofundada ou adversária por bugs.

Problemas simples mantêm a investigação comum direta como padrão econômico.

### Delimitação obrigatória de escopo

Antes de iniciar, delimite formalmente projeto, revisão/commit, arquivos ou
fluxo crítico específico, além de teto de esforço (número de arquivos inspecionados).
É expressamente vedada a varredura aberta de todo o repositório por omissão.

### Papéis e orquestração

Não cria novos agentes permanentes na equipe. O Coordenador ou agente principal
conduz a sequência linear utilizando execuções separadas e com contexto isolado
dos papéis existentes:

1. **Hunter (Papel Debug)**: Coleta candidatos a bug com evidência literal de código
   nos arquivos delimitados (`./prompts/hunter.md`).
   - *Poda econômica*: Se o Hunter reportar 0 candidatos, encerre o ciclo
     imediatamente sem acionar as fases seguintes.
2. **Skeptic (Papel Code Reviewer)**: Recebe apenas a lista estruturada de achados
   do Hunter e examina o código na fonte para contestar com explicações alternativas,
   comportamentos pretendidos ou falsos positivos (`./prompts/skeptic.md`).
3. **Referee (Papel QA)**: Recebe os achados estruturados e contestações, realiza
   leitura independente da fonte e profere os vereditos técnicos (`./prompts/referee.md`).

Subagentes não delegam entre si; o agente principal gerencia a passagem de dados
estruturados entre as etapas. Não são permitidas rodadas indefinidas de debate (máximo 1 ciclo).

### Qualidade e classificação de achados

- Pontuações dos prompts não determinam sozinhas severidade ou confirmação.
- Diferencie explicitamente:
  - `Bug reproduzido`: falha observada com comando ou teste reproduzível.
  - `Defeito demonstrado por análise`: inconsistência lógica ou falha provada por inspeção estática da fonte.
  - `Hipótese não confirmada`: comportamento suspeito sem prova conclusiva na fonte.
- Ausência de achados no escopo não prova ausência de bugs no software.
- A investigação não autoriza correções de código. Achados sustentados são
  encaminhados ao Desenvolvedor conforme autorização da tarefa.

## Limites e dependências

Diagnóstico não autoriza correção. Não exponha secrets, faça deploy ou altere
serviços. Pode usar `verify-and-stop` para encerrar quando a evidência bastar.

## Entrega e evidências

Entregue reprodução, comando, versão, logs redigidos, causa confirmada ou
hipóteses ranqueadas, correção proposta e prova necessária, no formato do
contrato.

## Impedimentos

Registre ambiente não reproduzível, logs insuficientes ou ausência de versão
como bloqueio específico; não converta silêncio em causa.
