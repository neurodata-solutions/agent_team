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
