# Segundo cérebro em Obsidian para agent-team / Video Studio

Data: 2026-09-21
Status: aprovado para plano de implementação

## Contexto e motivação

O usuário quer levar o estado do time de agentes (`/root/agent-team`) e do
produto Video Studio (`estudio-visual`/Jaaz + backend `opensuite` +
`neuro-studio-mvp`) para um vault Obsidian, como "segundo cérebro" —
tasks, debug, decisões, tudo consultável e navegável fora do terminal.

Restrição descoberta durante o brainstorming: este servidor (`root@srv`) é
um host Proxmox VE headless (Debian 11.6, sem ambiente gráfico, sem
Obsidian instalável aqui). O vault precisa existir como pasta de arquivos
neste servidor e ser sincronizado para o(s) dispositivo(s) do usuário, que
roda o Obsidian de verdade.

Decisões já fechadas com o usuário (via `AskUserQuestion` durante o
brainstorming):

1. **Acesso**: git. O vault é um repositório git hospedado (GitHub, org
   `neurodata-solutions`, privado). O usuário clona localmente e usa o
   plugin `obsidian-git` para sincronizar. Sem isso não dá para vincular a
   conta de um Obsidian Sync pago 100% a partir deste servidor headless.
2. **Escopo**: `jaaz` (repo `estudio-visual`) + `opensuite` (backend/
   renderer que o worker do jaaz usa) + `neuro-studio-mvp`.
3. **Identidade do vault**: `/root/agent-team` **vira** o repositório git
   e o próprio vault — não um repositório novo e separado. Isso evita
   recriar o problema de duplicação/divergência que esta mesma sessão
   passou corrigindo entre Codex/Claude/Antigravity (ver
   `TASK-20260921-GOVERNANCE-001` em `tasks/` após a migração descrita
   abaixo, ou em `TASK_REGISTER.md` antes dela).
4. **Granularidade de tasks**: cada task vira uma nota individual (com
   frontmatter consultável), não um arquivo único (`TASK_REGISTER.md`
   deixa de ser a fonte viva).
5. **Conteúdo dos produtos**: cada produto (`jaaz`, `opensuite`,
   `neuro-studio-mvp`) ganha uma única nota de entrada no vault — caminho,
   remote, propósito, pontos de entrada — nunca cópia de código-fonte ou de
   README. Código e documentação de produto continuam a fonte de verdade
   nos próprios repositórios.

## Objetivos

- `agent-team` torna-se um repositório git versionado (hoje não é).
- Toda task hoje registrada em `TASK_REGISTER.md` (~34 entradas) migra
  para uma nota individual em `tasks/`, com frontmatter que o Dataview (ou
  busca simples do Obsidian) consegue filtrar por projeto/estado/tipo.
- `jaaz`, `opensuite` e `neuro-studio-mvp` ganham nota de entrada em
  `projects/`.
- Todas as referências a `TASK_REGISTER.md` escritas nesta mesma sessão
  (`TEAM_CONTRACT.md`, `README.md`, `agents/*.md`,
  `adapters/antigravity/subagents.json`) são atualizadas para apontar a
  `tasks/`, para não deixar a regra que acabamos de criar já nascer
  quebrada.
- Documentação de como o usuário conecta seu próprio Obsidian ao vault.

## Não-objetivos (fora de escopo desta spec)

- Rodar Obsidian neste servidor — impossível (headless).
- Dashboard com plugin Dataview — adiado. `STATUS.md` continua prosa
  mantida à mão, como hoje. Adicionar Dataview implica uma dependência de
  plugin que o usuário precisa instalar e decidir separadamente; não é
  bloqueador para o "segundo cérebro" funcionar.
- Copiar ou espelhar código-fonte/documentação de `jaaz`/`opensuite`/
  `neuro-studio-mvp` para dentro do vault.
- Migrar o pipeline de dublagem, pilotos (`pilots/hhmmss`) ou histórico de
  avaliação de MCP para uma estrutura diferente — eles já vivem dentro de
  `agent-team` e simplesmente acompanham a virada para git sem mudança de
  formato.
- Automatizar a sincronização Obsidian → servidor no sentido inverso
  (edição feita no Obsidian do usuário virando commit automático) — o
  plugin `obsidian-git` já resolve isso do lado do usuário; nada a
  construir aqui.

## Arquitetura

### 1. `agent-team` vira repositório git

```
cd /root/agent-team
git init
git remote add origin git@github.com:neurodata-solutions/agent-team.git
```

Repositório novo, privado, mesma org dos demais (`estudio-visual` já está
lá). Primeiro commit inclui tudo que já existe hoje (contrato, papéis,
skills, `third_party/`, pilotos) mais as mudanças desta spec.

`.gitignore`: nada de específico identificado ainda — nenhum segredo ou
artefato binário grande foi encontrado em `agent-team` durante a sessão de
governança anterior. O plano de implementação deve rodar uma checagem
(`agent-guard`/`gitleaks`, hoje degradado por dependência ausente — ver
risco abaixo) antes do primeiro push.

### 2. Estrutura do vault

```
agent-team/
  tasks/                       ← NOVO — uma nota por task, substitui TASK_REGISTER.md
    TASK-20260915-003.md
    TASK-20260919-AVATAR-001.md
    TASK-20260921-GOVERNANCE-001.md
    ...
  projects/                    ← NOVO — nota de entrada por produto
    jaaz.md
    opensuite.md
    neuro-studio-mvp.md
  scripts/
    migrate_task_register.py   ← NOVO — script de migração (roda uma vez, fica no repo como registro)
  TASK_REGISTER.md             ← vira um stub curto de redirecionamento (ver abaixo), não é apagado sem rastro
  TEAM_CONTRACT.md, README.md, STATUS.md, agents/, .codex/, adapters/,
  third_party/, improvement-loop/, pilots/, VCS_PLAYBOOK.md, MCP_CATALOG.md
                                ← já existem, sem mudança estrutural
```

`debug` não vira pasta própria: uma investigação de bug já é registrada
como task em `TASK_REGISTER.md` hoje (tem `id`, `estado`, evidências). Ela
migra para `tasks/` como qualquer outra, diferenciada por
`tipo: debug` no frontmatter. Criar uma segunda pasta pra debug recriaria
"dois lugares pra mesma coisa" — exatamente o padrão que a sessão de
governança anterior identificou e corrigiu.

### 3. Esquema de frontmatter das notas de task

```yaml
---
id: TASK-20260920-001
tipo: task            # task | debug
estado: concluida     # planejada | em_execucao | concluida | parcial | bloqueada
projeto: jaaz          # jaaz | opensuite | neuro-studio-mvp | agent-team-meta
responsavel: "coordenador (sessão Claude Code)"
data: 2026-09-20
dependencias: []
tags: [video-studio]
---
```

Corpo da nota: markdown legível (não YAML aninhado) com seções fixas —
`## Objetivo`, `## Escopo`, `## Resultado`, `## Evidências`, `## Arquivos
alterados`, `## Verificações`, `## Limitações`, `## Próximo passo` —
extraídas dos campos correspondentes do bloco YAML original de
`TASK_REGISTER.md`. Frontmatter carrega só os campos que servem para
filtrar/buscar; o resto vira prosa normal, mais agradável de ler no
Obsidian do que YAML dentro de YAML.

`projeto: agent-team-meta` é o valor para tasks que não são sobre nenhum
produto específico (ex.: `TASK-20260917-SKILLS-LOAD-001`,
`TASK-20260921-GOVERNANCE-001`) — continuam no mesmo `tasks/`, só não
aparecem nas consultas por produto.

### 4. Migração (`scripts/migrate_task_register.py`)

Lido `TASK_REGISTER.md` uma vez, algoritmo:

1. Dividir o arquivo por cabeçalhos `## ` (um por task).
2. Em cada seção, extrair os dois blocos fenced ` ```yaml ... ``` ` (Entrada
   e Retorno, conforme o template já documentado no topo do arquivo) e
   fazer merge dos campos num dicionário único por `id`.
3. Gerar `tasks/<id>.md` com o frontmatter da seção 3 e o corpo markdown
   correspondente.
4. Falhar alto (parar e listar) se algum bloco não tiver `id:` reconhecível
   ou se dois blocos gerarem o mesmo `id` — nunca sobrescrever
   silenciosamente.
5. Ao final, relatório: quantas tasks migradas, quantas ignoradas/erro.

Script fica versionado em `scripts/` depois de rodar — não é apagado —
como registro de como a migração aconteceu (mesmo padrão de
`improvement-loop/scripts/validate_record.py`, que já existe no repo).

`TASK_REGISTER.md` não é apagado sem deixar rastro: vira um arquivo curto
(~10 linhas) dizendo que foi retirado de uso em 2026-09-21, migrado para
`tasks/` por `scripts/migrate_task_register.py`, e apontando pra lá — para
qualquer contexto de agente que ainda tenha instrução antiga gravada
(memória, prompt cacheado) não bater num 404 conceitual.

### 5. Notas de projeto (`projects/*.md`)

Cada uma com: caminho absoluto no host, remote git (quando houver),
branch/estado no momento da criação da nota, propósito em 2-3 frases,
pontos de entrada (arquivo principal, como rodar/buildar), e uma lista
manual (não Dataview, já que isso é não-objetivo) dos `id`s de task mais
relevantes daquele projeto — o Obsidian já mostra backlinks automáticos
para quem linkar `[[jaaz]]` no corpo de uma nota de task.

### 6. Atualização de referências (evitar contrato nascendo quebrado)

Arquivos editados na sessão de governança anterior que citam
`TASK_REGISTER.md` e precisam trocar para `tasks/`:

- `TEAM_CONTRACT.md` (seção "Escopo e autoridade": leitura obrigatória;
  seção "Ciclo de melhoria": registro de causa recorrente)
- `README.md` (passo 2 do onboarding)
- `adapters/antigravity/subagents.json` (linha adicionada ao
  `system_prompt` do Coordenador: "Leia também STATUS.md e as entradas
  pertinentes de TASK_REGISTER.md")

Formato de entrega do contrato (`Entrega obrigatória`) não muda de forma —
continua os mesmos campos (`Tarefa`, `Estado`, `Escopo verificado` etc.);
o que muda é onde esse relato termina registrado (uma nota nova em
`tasks/` em vez de um bloco anexado a `TASK_REGISTER.md`).

### 7. Conexão do lado do usuário (documentado, não executável daqui)

Nota curta em `README.md` (ou um `docs/obsidian-setup.md` novo):

1. `git clone git@github.com:neurodata-solutions/agent-team.git` no
   dispositivo do usuário.
2. Abrir essa pasta como vault no Obsidian ("Open folder as vault").
3. Instalar o plugin comunitário `obsidian-git` e configurar auto-commit/
   pull no intervalo desejado.
4. Qualquer edição feita no Obsidian sincroniza como commit git comum —
   nenhuma infraestrutura nova no servidor além do repositório remoto.

## Riscos e limitações conhecidas

- **`agent-guard` está degradado** nesta máquina (jq/gitleaks ausentes,
  reportado em todo hook desta sessão) — o primeiro push de um repositório
  novo é exatamente o tipo de operação que essa proteção existe para
  cobrir. O plano de implementação deve verificar/instalar as dependências
  do `agent-guard` (ou rodar uma varredura equivalente manual) antes do
  primeiro `git push`, não depois.
- **34 tasks para migrar por script, não à mão** — risco de o parser errar
  em alguma entrada com formatação levemente diferente (foram escritas ao
  longo de várias sessões). O script precisa falhar alto e listar, não
  gerar nota malformada em silêncio.
- **Conexão final do Obsidian é do lado do usuário** — esta spec e o plano
  decorrente terminam no repositório pronto para clonar; não há como
  validar aqui que o `obsidian-git` está sincronizando de verdade.
- **`neuro-studio-mvp` não tem remote git nem README** — a nota de entrada
  desse projeto será mais enxuta (sem link de remote) até que o próprio
  repositório seja inicializado, o que está fora do escopo desta spec.

## Critérios de aceitação

- `agent-team` é um repositório git com pelo menos um commit e um remote
  configurado.
- `tasks/` contém uma nota por `id` presente em `TASK_REGISTER.md` hoje,
  sem perda de campo (objetivo/resultado/evidências/etc. presentes na
  nota correspondente).
- `TASK_REGISTER.md` existe apenas como stub de redirecionamento.
- `projects/jaaz.md`, `projects/opensuite.md`, `projects/neuro-studio-mvp.md`
  existem com os campos mínimos descritos na seção 5.
- `TEAM_CONTRACT.md`, `README.md` e `adapters/antigravity/subagents.json`
  não citam mais `TASK_REGISTER.md` como leitura/escrita obrigatória —
  citam `tasks/`.
- Documentação de conexão do usuário existe e é seguível sem acesso a este
  servidor além do `git clone`.
