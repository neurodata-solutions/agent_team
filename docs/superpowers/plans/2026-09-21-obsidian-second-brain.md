# Segundo Cérebro Obsidian (agent-team → vault git) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar `/root/agent-team` num repositório git que serve como vault Obsidian ("segundo cérebro"), migrando as tasks de `TASK_REGISTER.md` para notas individuais e adicionando notas de entrada para `jaaz`, `opensuite` e `neuro-studio-mvp`, sem duplicar nenhuma fonte de verdade existente.

**Architecture:** Script Python testado (`scripts/migrate_task_register.py`) faz a migração de `TASK_REGISTER.md` (blocos YAML fenced) para `tasks/<id>.md` (frontmatter + markdown). `TASK_REGISTER.md` vira um stub de redirecionamento. Referências no contrato/README/adapters trocam de `TASK_REGISTER.md` para `tasks/`. O repo é inicializado, verificado contra segredos manualmente (agent-guard está degradado nesta máquina) e empurrado para um novo repositório GitHub privado em `neurodata-solutions`.

**Tech Stack:** Python 3 + PyYAML + pytest (já usados no repo, ver `improvement-loop/scripts/validate_record.py`), git, GitHub via SSH (autenticação já confirmada como `neurodata-solutions`).

**Spec:** `/root/agent-team/docs/superpowers/specs/2026-09-21-obsidian-second-brain-design.md`

## Global Constraints

- `agent-team` vira o próprio vault — nenhum conteúdo é copiado para um repositório separado.
- Nenhum código-fonte ou README de `jaaz`/`opensuite`/`neuro-studio-mvp` é copiado para dentro do vault — só notas de entrada com metadados e links.
- `TASK_REGISTER.md` não é apagado sem deixar rastro — vira stub curto apontando para `tasks/`.
- Cada task migrada precisa preservar `id`, `estado`, `objetivo`/`resultado`, evidências — nenhuma perda de campo.
- `id` de task ausente ou duplicado faz o script de migração falhar alto (nunca sobrescrever/pular em silêncio, exceto reexecução idempotente do mesmo arquivo já escrito).
- Nenhum push para o remote acontece sem o repositório GitHub já existir (não há `gh` CLI nem token de API neste ambiente — confirmado por checagem prévia).
- Antes do primeiro push: varredura manual por segredos no diff (agent-guard/gitleaks indisponíveis nesta máquina).

## Desvios conhecidos deste plano

- O repositório foi criado como `neurodata-solutions/agent_team` (underscore),
  não `agent-team` (hífen) como planejado originalmente.
- `git remote add` / `git push` tiveram que ser executados pelo usuário
  diretamente, não pela sessão do controlador — o classificador de auto-mode
  do Claude Code bloqueou esses comandos especificamente para o controlador
  (motivos: "Data Exfiltration" e depois "Out-of-Place Publication").

---

### Task 1: Inicializar o repositório git e criar o commit-base (pré-migração)

**Files:**
- Create: `.gitignore` (em `/root/agent-team/.gitignore`)
- Nenhum outro arquivo de conteúdo é criado nesta task — é só a baseline em git do que já existe.

**Interfaces:**
- Consumes: nada.
- Produces: repositório git local em `/root/agent-team` com um commit `baseline`, referência que a Task 6 usa para adicionar o remote e dar push.

- [ ] **Step 1: Verificar que não há git já iniciado por engano**

Run: `git -C /root/agent-team status` (esperar erro "not a git repository")

- [ ] **Step 2: Criar `.gitignore`**

```gitignore
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 3: `git init`**

Run: `git -C /root/agent-team init`
Expected: "Initialized empty Git repository in /root/agent-team/.git/"

- [ ] **Step 4: Adicionar tudo e revisar a lista antes de commitar**

Run: `git -C /root/agent-team add -A && git -C /root/agent-team status --short`
Ler a lista inteira — nenhum arquivo com nome que sugira segredo/credencial
(`.env`, `*key*`, `*token*`, `*credential*`). Se aparecer algo assim, `git
reset` esse arquivo específico e investigar antes de continuar.

- [ ] **Step 5: Varredura manual por segredo no conteúdo staged (agent-guard degradado nesta máquina)**

Run:
```bash
git -C /root/agent-team diff --cached | grep -iE "api[_-]?key|secret[_-]?key|password|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|ghp_[a-zA-Z0-9]{20,}|sk-[a-zA-Z0-9]{20,}"
```
Expected: nenhuma saída. Se algo aparecer, remover o arquivo do stage e do
disco (se for lixo) ou investigar antes de prosseguir — nunca commitar.

- [ ] **Step 6: Commit baseline**

```bash
git -C /root/agent-team commit -m "baseline: conteúdo existente de agent-team antes da migração pro vault Obsidian"
```

---

### Task 2: Escrever e testar o script de migração `scripts/migrate_task_register.py`

**Files:**
- Create: `/root/agent-team/scripts/migrate_task_register.py`
- Test: `/root/agent-team/scripts/test_migrate_task_register.py`

**Interfaces:**
- Consumes: nada de tasks anteriores (função pura sobre texto).
- Produces (usado pela Task 3):
  - `parse_task_register(text: str) -> list[dict]`
  - `render_task_note(task: dict) -> str`
  - `migrate(task_register_path: Path, tasks_dir: Path) -> MigrationReport` com
    atributos `.written: list[str]` e `.skipped: list[str]`.

- [ ] **Step 1: Escrever os testes (falhando, módulo ainda não existe)**

`scripts/test_migrate_task_register.py`:

```python
import textwrap
import pytest
from migrate_task_register import (
    parse_task_register,
    render_task_note,
    normalize_project,
    classify_tipo,
    extract_date,
)

SAMPLE = textwrap.dedent('''
    ## Entrada

    ```yaml
    id: TASK-YYYYMMDD-###
    objetivo: ""
    responsavel: ""
    ```

    ## Retorno

    ```yaml
    estado: concluida
    resultado: ""
    ```

    ---

    ## Exemplo real

    ```yaml
    id: TASK-20260101-001
    objetivo: "Corrigir bug X no jaaz"
    responsavel: "debug"
    projeto: "jaaz"
    estado: planejada
    ```

    ```yaml
    estado: concluida
    resultado: "Corrigido"
    evidencias: ["log X"]
    ```
    ''')

DUPLICATE_SAMPLE = SAMPLE + textwrap.dedent('''

    ## Duplicata

    ```yaml
    id: TASK-20260101-001
    objetivo: "duplicado de propósito"
    ```
    ''')


def test_template_block_is_ignored_and_only_real_task_parsed():
    tasks = parse_task_register(SAMPLE)
    assert len(tasks) == 1
    assert tasks[0]["id"] == "TASK-20260101-001"


def test_retorno_block_merges_and_overrides_entrada_fields():
    tasks = parse_task_register(SAMPLE)
    task = tasks[0]
    # Retorno tinha estado: concluida: deve vencer o planejada da Entrada
    assert task["estado"] == "concluida"
    assert task["resultado"] == "Corrigido"
    assert task["evidencias"] == ["log X"]
    # campo só presente na Entrada continua disponível
    assert task["objetivo"] == "Corrigir bug X no jaaz"


def test_duplicate_id_raises():
    with pytest.raises(ValueError, match="duplicado"):
        parse_task_register(DUPLICATE_SAMPLE)


@pytest.mark.parametrize("projeto,caminho,expected", [
    ("jaaz", "", "jaaz"),
    ("estudio-visual / Jaaz", "", "jaaz"),
    ("", "/root/opensuite/services/openshorts", "opensuite"),
    ("neuro-studio hub", "", "neuro-studio-mvp"),
    ("", "", "agent-team-meta"),
])
def test_normalize_project(projeto, caminho, expected):
    task = {"projeto": projeto, "caminho": caminho}
    assert normalize_project(task) == expected


def test_classify_tipo_detects_debug_by_keyword():
    assert classify_tipo({"id": "TASK-20260101-001", "objetivo": "Investigar causa raiz do crash"}) == "debug"
    assert classify_tipo({"id": "TASK-20260101-002", "objetivo": "Adicionar botão de logout"}) == "task"


def test_extract_date_from_id():
    assert extract_date("TASK-20260921-GOVERNANCE-001") == "2026-09-21"
    assert extract_date("id-invalido") == "desconhecida"


def test_render_task_note_has_valid_frontmatter_and_sections():
    task = {
        "id": "TASK-20260101-001",
        "objetivo": "Corrigir bug X no jaaz",
        "projeto": "jaaz",
        "estado": "concluida",
        "resultado": "Corrigido",
        "evidencias": ["log X"],
    }
    note = render_task_note(task)
    assert note.startswith("---\n")
    fm_end = note.index("---\n", 4)
    frontmatter_text = note[4:fm_end]
    import yaml
    fm = yaml.safe_load(frontmatter_text)
    assert fm["id"] == "TASK-20260101-001"
    assert fm["projeto"] == "jaaz"
    assert fm["tags"] == ["video-studio"]
    assert "## Objetivo" in note
    assert "## Evidências" in note
    assert "- log X" in note
    # seção sem dado correspondente não aparece
    assert "## Próximo passo" not in note
```

- [ ] **Step 2: Rodar os testes pra confirmar que falham (módulo não existe)**

Run: `cd /root/agent-team/scripts && python3 -m pytest test_migrate_task_register.py -v`
Expected: `ModuleNotFoundError: No module named 'migrate_task_register'`

- [ ] **Step 3: Implementar `migrate_task_register.py`**

```python
"""Migra TASK_REGISTER.md (blocos YAML fenced) para uma nota por task em tasks/.

Uso: python3 scripts/migrate_task_register.py
Roda a partir da raiz do repo (assume TASK_REGISTER.md e tasks/ como irmãos
de scripts/). Idempotente: reexecutar não sobrescreve notas já escritas.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

TASK_ID_RE = re.compile(r"^TASK-(\d{8})-")
FENCE_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)

PROJECT_KEYWORDS = [
    ("jaaz", "jaaz"),
    ("estudio-visual", "jaaz"),
    ("opensuite", "opensuite"),
    ("openshorts", "opensuite"),
    ("moneyprinter", "opensuite"),
    ("neuro-studio", "neuro-studio-mvp"),
]

DEBUG_KEYWORDS = ["bug", "debug", "causa raiz", "incidente", "investigar"]


def parse_task_register(text: str) -> list[dict]:
    """Extrai uma lista de dicts, um por task real, na ordem em que aparecem.

    Um bloco YAML fenced que tenha um `id` no formato TASK-YYYYMMDD-... abre
    (ou reabre, se repetido -> erro) uma task. Qualquer bloco seguinte sem
    `id` reconhecível é mesclado na task atualmente aberta (é assim que os
    pares Entrada/Retorno do template se juntam). O bloco de template
    (`id: TASK-YYYYMMDD-###`) não bate no regex de 8 dígitos e é ignorado,
    e o bloco "Retorno" do template (sem id nenhum) fica órfão -- também
    ignorado, porque nenhuma task válida foi aberta ainda nesse ponto.
    """
    tasks: dict[str, dict] = {}
    order: list[str] = []
    current_id: str | None = None
    for block_text in FENCE_RE.findall(text):
        data = yaml.safe_load(block_text)
        if not isinstance(data, dict):
            continue
        block_id = data.get("id")
        if isinstance(block_id, str) and TASK_ID_RE.match(block_id):
            if block_id in tasks:
                raise ValueError(f"id duplicado em TASK_REGISTER.md: {block_id}")
            tasks[block_id] = dict(data)
            order.append(block_id)
            current_id = block_id
        elif current_id is not None:
            tasks[current_id].update(data)
        # bloco órfão (sem id, antes de qualquer task válida) -> ignorado
    return [tasks[i] for i in order]


def normalize_project(task: dict) -> str:
    haystack = " ".join(
        str(task.get(k, "")) for k in ("projeto", "caminho", "maquina")
    ).lower()
    for keyword, project in PROJECT_KEYWORDS:
        if keyword in haystack:
            return project
    return "agent-team-meta"


def classify_tipo(task: dict) -> str:
    haystack = f"{task.get('id', '')} {task.get('objetivo', '')}".lower()
    return "debug" if any(k in haystack for k in DEBUG_KEYWORDS) else "task"


def extract_date(task_id: str) -> str:
    m = TASK_ID_RE.match(task_id)
    if not m:
        return "desconhecida"
    d = m.group(1)
    return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"


def render_task_note(task: dict) -> str:
    task_id = task["id"]
    projeto = normalize_project(task)
    frontmatter = {
        "id": task_id,
        "tipo": classify_tipo(task),
        "estado": task.get("estado", "desconhecido"),
        "projeto": projeto,
        "responsavel": task.get("responsavel", ""),
        "data": extract_date(task_id),
        "dependencias": task.get("dependencias") or [],
        "tags": ["video-studio"] if projeto in {"jaaz", "opensuite", "neuro-studio-mvp"} else [],
    }
    fm_yaml = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()

    sections: list[str] = []

    def add_section(title: str, key: str, is_list: bool = False) -> None:
        val = task.get(key)
        if not val:
            return
        if is_list:
            items = val if isinstance(val, list) else [val]
            body = "\n".join(f"- {item}" for item in items)
        else:
            body = str(val).strip()
        sections.append(f"## {title}\n\n{body}\n")

    add_section("Objetivo", "objetivo")
    add_section("Escopo", "escopo_permitido")
    add_section("Resultado", "resultado")
    add_section("Evidências", "evidencias", is_list=True)
    add_section("Arquivos alterados", "arquivos_alterados", is_list=True)
    add_section("Verificações", "verificacoes", is_list=True)
    add_section("Limitações", "limitacoes", is_list=True)
    add_section("Próximo passo", "proximo_passo")

    body = "\n".join(sections)
    return f"---\n{fm_yaml}\n---\n\n# {task_id}\n\n{body}"


@dataclass
class MigrationReport:
    written: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def migrate(task_register_path: Path, tasks_dir: Path) -> MigrationReport:
    text = task_register_path.read_text(encoding="utf-8")
    tasks = parse_task_register(text)
    tasks_dir.mkdir(parents=True, exist_ok=True)
    report = MigrationReport()
    for task in tasks:
        task_id = task["id"]
        out_path = tasks_dir / f"{task_id}.md"
        if out_path.exists():
            report.skipped.append(task_id)
            continue
        out_path.write_text(render_task_note(task), encoding="utf-8")
        report.written.append(task_id)
    return report


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    report = migrate(root / "TASK_REGISTER.md", root / "tasks")
    print(f"Migradas: {len(report.written)}")
    if report.skipped:
        print(f"Já existiam (puladas): {len(report.skipped)} -> {report.skipped}")
    sys.exit(0)
```

- [ ] **Step 4: Rodar os testes de novo, confirmar que passam**

Run: `cd /root/agent-team/scripts && python3 -m pytest test_migrate_task_register.py -v`
Expected: 8 testes, todos `PASSED`. Se `ModuleNotFoundError: yaml`, rodar
`pip install pyyaml pytest` antes (ou `apt install python3-yaml
python3-pytest` conforme o ambiente) e repetir.

- [ ] **Step 5: Commit**

```bash
git -C /root/agent-team add scripts/migrate_task_register.py scripts/test_migrate_task_register.py
git -C /root/agent-team commit -m "feat: script de migração TASK_REGISTER.md -> tasks/, com testes"
```

---

### Task 3: Rodar a migração real, substituir TASK_REGISTER.md por um stub

**Files:**
- Create: `/root/agent-team/tasks/*.md` (uma por task real — quantidade determinada pela migração, não fixa)
- Modify: `/root/agent-team/TASK_REGISTER.md` (substituído por stub curto)

**Interfaces:**
- Consumes: `migrate()` da Task 2.
- Produces: diretório `tasks/` populado, usado pelas Tasks 5 e 6 como a nova
  fonte que `TEAM_CONTRACT.md`/`README.md`/`subagents.json` passam a citar.

- [ ] **Step 1: Contar quantas tasks reais existem antes de migrar (checagem independente do script)**

Run: `grep -cE "^id: TASK-[0-9]{8}" /root/agent-team/TASK_REGISTER.md`
Anotar o número — é o valor esperado de `len(report.written)` no passo
seguinte.

- [ ] **Step 2: Rodar a migração**

Run: `cd /root/agent-team && python3 scripts/migrate_task_register.py`
Expected: `Migradas: <mesmo número do Step 1>`, sem linha "Já existiam".

- [ ] **Step 3: Spot-check de 2 notas migradas**

Run: `cat /root/agent-team/tasks/TASK-20260921-GOVERNANCE-001.md`
Conferir visualmente: frontmatter com `id`, `tipo: task`, `projeto:
agent-team-meta`, `estado: concluida`; seções `## Objetivo`, `## Resultado`,
`## Evidências` presentes e com o texto real (não vazio).

Run: `cat /root/agent-team/tasks/TASK-20260920-005.md` (ou outro id real
que exista na sua árvore)
Conferir: `projeto: jaaz` (a task fala de `server/main.py` do jaaz),
`tipo: task`.

- [ ] **Step 4: Substituir `TASK_REGISTER.md` pelo stub**

Escrever em `/root/agent-team/TASK_REGISTER.md` (sobrescrevendo o conteúdo
inteiro):

```markdown
# TASK_REGISTER.md — retirado de uso em 2026-09-21

Este arquivo não é mais a fonte viva de tasks. Foi migrado para notas
individuais em `tasks/` (uma por `id`), como parte do vault Obsidian —
ver `docs/superpowers/specs/2026-09-21-obsidian-second-brain-design.md`.

Migração feita por `scripts/migrate_task_register.py`. O histórico
original (todas as entradas em formato YAML, texto integral) continua
disponível no histórico git deste arquivo (`git log -p -- TASK_REGISTER.md`
até este commit).

**Se você é um agente com instrução antiga pra ler/escrever
`TASK_REGISTER.md`: leia e escreva em `tasks/` a partir de agora.**
```

- [ ] **Step 5: Commit**

```bash
git -C /root/agent-team add tasks/ TASK_REGISTER.md
git -C /root/agent-team commit -m "migra TASK_REGISTER.md para notas individuais em tasks/"
```

---

### Task 4: Notas de entrada dos projetos (`projects/jaaz.md`, `projects/opensuite.md`, `projects/neuro-studio-mvp.md`)

**Files:**
- Create: `/root/agent-team/projects/jaaz.md`
- Create: `/root/agent-team/projects/opensuite.md`
- Create: `/root/agent-team/projects/neuro-studio-mvp.md`

**Interfaces:**
- Consumes: nada de tasks anteriores.
- Produces: notas que a Task 5 referencia a partir de `README.md`.

- [ ] **Step 1: `projects/jaaz.md`**

```markdown
---
projeto: jaaz
caminho: /root/jaaz
remote: git@github.com:neurodata-solutions/estudio-visual.git
branch: jaaz
tags: [video-studio]
---

# Jaaz (Estúdio Visual / Video Studio)

Produto principal do Video Studio. Repositório real: `estudio-visual`
(nome do repo no GitHub), rodando no host como `/root/jaaz` e em produção
como container `opensuite-jaaz` dentro do CT100 (Proxmox).

## Pontos de entrada

- `package.json` — scripts do frontend/build
- `Dockerfile.local` — build local da imagem de produção
- `server/` — backend/worker Python
- `react/` — frontend
- `electron/` — empacotamento desktop
- `docs/` — documentação própria do repositório (não duplicada aqui)

## Depende de

- `opensuite` (ver `[[opensuite]]`) para renderização (Remotion) e
  pipelines de dublagem/geração — roda como stack separada no CT100.

## Tasks relacionadas

Ver `tasks/` filtrando `projeto: jaaz` no frontmatter (busca do Obsidian
ou `grep -l "projeto: jaaz" tasks/*.md`).
```

- [ ] **Step 2: `projects/opensuite.md`**

```markdown
---
projeto: opensuite
caminho: /root/opensuite
remote: nenhum (pasta solta, sem git — ver risco abaixo)
branch: n/a
tags: [video-studio]
---

# Opensuite (backend/renderer do Jaaz)

Pipelines de renderização e geração que o worker do `[[jaaz]]` consome:
Remotion (`MultiPanelScene.tsx`, `DynamicText.tsx`, `AnimatedSticker.tsx`),
integração FaceFusion (`api_wrapper_facefusion.py`), Postiz
(`postiz_client.py`), entre outros.

## Risco conhecido (herdado de `STATUS.md`)

`/root/opensuite` no host é uma pasta solta **sem git**. A árvore de
produção real roda dentro do CT100 (container), que pode divergir do host
mesmo parecendo igual — sempre confirmar com `md5sum` dos dois lados antes
de editar, conforme o checklist de deploy em `TEAM_CONTRACT.md`.

## Tasks relacionadas

Ver `tasks/` filtrando `projeto: opensuite` no frontmatter.
```

- [ ] **Step 3: `projects/neuro-studio-mvp.md`**

```markdown
---
projeto: neuro-studio-mvp
caminho: /root/neuro-studio-mvp
remote: nenhum (sem git inicializado)
branch: n/a
tags: [video-studio]
---

# Neuro Studio (hub)

Estrutura confirmada no disco: `docker-compose.yml`, `frontend/`, `hub/`.
Corresponde ao "neuro-studio product plan" registrado na memória do
projeto — hub sob demanda que embute UIs originais via iframe (fase 1 de
uso interno), open-core AGPL-3.0. Ainda sem repositório git nem README
próprio nesta máquina — a nota é mínima até que o repositório seja
inicializado (fora do escopo desta migração).

## Tasks relacionadas

Ver `tasks/` filtrando `projeto: neuro-studio-mvp` no frontmatter.
```

- [ ] **Step 4: Commit**

```bash
git -C /root/agent-team add projects/
git -C /root/agent-team commit -m "adiciona notas de entrada pra jaaz, opensuite e neuro-studio-mvp"
```

---

### Task 5: Atualizar referências de `TASK_REGISTER.md` para `tasks/` e documentar a conexão do Obsidian

**Files:**
- Modify: `/root/agent-team/TEAM_CONTRACT.md`
- Modify: `/root/agent-team/README.md`
- Modify: `/root/agent-team/adapters/antigravity/subagents.json`
- Create: `/root/agent-team/docs/obsidian-setup.md`

**Interfaces:**
- Consumes: `tasks/` (Task 3) e `projects/` (Task 4) já existentes.
- Produces: nada consumido por tasks futuras — é o fechamento do plano.

- [ ] **Step 1: `TEAM_CONTRACT.md` — trocar a exigência de leitura**

Localizar (adicionado na sessão de governança anterior, seção "Escopo e
autoridade"):

```
- Antes de iniciar, ler `STATUS.md` e as entradas pertinentes de
  `TASK_REGISTER.md` para o projeto/serviço da tarefa. `STATUS.md` e
  `TASK_REGISTER.md` são a memória oficial e compartilhável do time —
```

Substituir por:

```
- Antes de iniciar, ler `STATUS.md` e as notas pertinentes em `tasks/`
  (filtrando por `projeto:` no frontmatter) para o projeto/serviço da
  tarefa. `STATUS.md` e `tasks/` são a memória oficial e compartilhável do
  time —
```

(manter o restante do parágrafo como está, só a frase inicial muda).

Localizar também, na seção "Ciclo de melhoria de agentes":

```
**Obrigatório, não opcional:** toda tarefa que fechar como `bloqueada`, ou
cuja causa confirmada já apareça em outra entrada de `TASK_REGISTER.md`
```

Substituir `TASK_REGISTER.md` por `tasks/` nessa frase.

- [ ] **Step 2: `README.md` — trocar o passo 2 do onboarding**

Localizar:

```
2. Ler `STATUS.md` (orientação rápida) e as entradas relevantes do projeto/
   serviço em `TASK_REGISTER.md` — sem isso a tarefa é delimitada sem saber
```

Substituir `TASK_REGISTER.md` por `tasks/` (mantendo o resto do parágrafo).

- [ ] **Step 3: `adapters/antigravity/subagents.json` — trocar a menção no Coordenador**

Localizar (dentro do `system_prompt` de `team-coordenador`):

```
Leia também STATUS.md e as entradas pertinentes de TASK_REGISTER.md antes de delimitar a tarefa.
```

Substituir por:

```
Leia também STATUS.md e as notas pertinentes em tasks/ antes de delimitar a tarefa.
```

Validar o JSON depois de editar:
Run: `python3 -c "import json; json.load(open('/root/agent-team/adapters/antigravity/subagents.json'))" && echo OK`

- [ ] **Step 4: Criar `docs/obsidian-setup.md`**

```markdown
# Conectar seu Obsidian a este vault

Este repositório (`agent-team`) é o vault. O servidor onde ele vive é
headless — o Obsidian roda no seu dispositivo, não aqui.

## Passos

1. Clonar o repositório no seu computador/celular:
   ```
   git clone git@github.com:neurodata-solutions/agent-team.git
   ```
2. No Obsidian: "Open folder as vault" e escolher a pasta clonada.
3. Instalar o plugin comunitário `obsidian-git` (Configurações → Plugins
   comunitários → Procurar → "Git").
4. Configurar no `obsidian-git`: intervalo de auto-commit/pull (ex.: a
   cada 10 min) e "Pull on boot" ligado, pra sempre abrir com o estado
   mais recente.

## O que NÃO fazer

- Não editar `tasks/*.md` fora do padrão de frontmatter (`id`, `tipo`,
  `estado`, `projeto`, `responsavel`, `data`, `dependencias`, `tags`) —
  agentes e buscas dependem desses campos existirem.
- Não copiar código-fonte de `jaaz`/`opensuite`/`neuro-studio-mvp` pra
  dentro deste vault — as notas em `projects/` só linkam pra lá.
```

- [ ] **Step 5: Commit**

```bash
git -C /root/agent-team add TEAM_CONTRACT.md README.md adapters/antigravity/subagents.json docs/obsidian-setup.md
git -C /root/agent-team commit -m "atualiza referências de TASK_REGISTER.md pra tasks/ e documenta conexão do Obsidian"
```

---

### Task 6: Criar o repositório remoto no GitHub e dar push

**Files:** nenhum arquivo novo — só operação de rede/git.

**Interfaces:**
- Consumes: todos os commits das Tasks 1–5.
- Produces: repositório remoto acessível para o usuário clonar (ver Task 5,
  Step 4).

- [ ] **Step 1: Confirmar que não há credencial automatizada de criação de repo (checado previamente: sem `gh`, sem `GITHUB_TOKEN`/`GH_TOKEN`)**

Run: `which gh; env | grep -iE "GITHUB_TOKEN|GH_TOKEN"`
Expected: nenhuma saída (confirma que a criação do repo precisa ser manual
— ver Step 2).

- [ ] **Step 2: PARAR aqui e pedir para o usuário criar o repositório vazio**

Isto não é executável a partir deste servidor sem token/`gh`. Mensagem
para o usuário:

> Crie um repositório vazio (sem README, sem .gitignore, sem license —
> vamos empurrar o conteúdo já pronto) em
> https://github.com/organizations/neurodata-solutions/repositories/new
> com o nome `agent-team`, visibilidade **privada**. Me avise quando
> estiver criado.

- [ ] **Step 3: Adicionar o remote e dar push (só depois da confirmação do usuário)**

```bash
git -C /root/agent-team remote add origin git@github.com:neurodata-solutions/agent-team.git
git -C /root/agent-team push -u origin master
```

(ou `main`, conforme o nome do branch padrão local — checar com `git -C
/root/agent-team branch --show-current` antes do push).

- [ ] **Step 4: Verificar**

Run: `git -C /root/agent-team log --oneline -5` e confirmar visualmente
com o usuário que o repositório aparece em
`https://github.com/neurodata-solutions/agent-team`.

---

## Self-Review (preenchido antes de entregar o plano)

**Cobertura da spec:** git init+push (Task 1+6), migração de tasks (Task
2+3), notas de projeto (Task 4), atualização de referências + doc de
conexão (Task 5). Todos os critérios de aceitação da spec têm task
correspondente.

**Placeholders:** nenhum "TBD"/"implementar depois" — todo código e
conteúdo de nota está escrito por extenso nas steps.

**Consistência de tipos:** `MigrationReport.written`/`.skipped` usados
identicamente na Task 2 (definição) e Task 3 (uso). Nomes de função
(`parse_task_register`, `render_task_note`, `normalize_project`,
`classify_tipo`, `extract_date`, `migrate`) iguais em toda parte onde
aparecem.
