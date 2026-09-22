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
    `id` key nenhuma é mesclado na task atualmente aberta (é assim que os
    pares Entrada/Retorno do template se juntam).

    Blocos com um `id` key:
    - Se matches TASK-YYYYMMDD-... : abre/reabre (ou erro se duplicado)
    - Se é exatamente o template placeholder TASK-YYYYMMDD-### : pulado
    - Se é outro string não-vazio que falha o regex : ValueError (malformado)

    Blocos SEM um `id` key, antes de qualquer task válida, são órfãos -> ignorado.
    Blocos SEM um `id` key, depois que uma task foi aberta : merged.
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
            # Valid task ID format
            if block_id in tasks:
                raise ValueError(f"id duplicado em TASK_REGISTER.md: {block_id}")
            tasks[block_id] = dict(data)
            order.append(block_id)
            current_id = block_id
        elif "id" in data:
            # Has an id key, but it doesn't match the regex
            if block_id == "TASK-YYYYMMDD-###":
                # Known template placeholder - skip silently
                continue
            # Malformed id - raise error
            raise ValueError(
                f"id malformado em bloco YAML: '{block_id}' "
                f"não corresponde ao padrão TASK-YYYYMMDD-..."
            )
        elif current_id is not None:
            # No id key at all - this is a continuation block (Retorno)
            # Merge it, but protect id field from being overwritten
            merged = dict(data)
            merged.pop("id", None)
            tasks[current_id].update(merged)
        # else: orphaned block (no id key, before any valid task) -> ignored
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
