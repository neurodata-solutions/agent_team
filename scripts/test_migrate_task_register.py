import textwrap
import pytest
from pathlib import Path
from migrate_task_register import (
    parse_task_register,
    render_task_note,
    normalize_project,
    classify_tipo,
    extract_date,
    migrate,
    MigrationReport,
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


def test_normalize_project_checks_checkout_reservado():
    """Important: checkout_reservado is a stronger signal than projeto/caminho/
    maquina (present in 32/34 source entries) and must be inspected too."""
    task = {
        "projeto": "",
        "caminho": "",
        "maquina": "",
        "checkout_reservado": "liberado (/root/jaaz)",
    }
    assert normalize_project(task) == "jaaz"


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


def test_malformed_id_raises_error():
    """Critical: blocks with non-matching id strings must raise, not silently merge."""
    malformed_sample = textwrap.dedent('''
        ```yaml
        id: TASK-20260101-001
        objetivo: "Task válida"
        ```

        ```yaml
        id: MALFORMED-ID
        resultado: "Não deve ser mesclado"
        ```
    ''')
    with pytest.raises(ValueError, match="malformado"):
        parse_task_register(malformed_sample)


def test_migrate_fresh_run_writes_files(tmp_path):
    """Important: migrate() should write task files on fresh run."""
    task_register = tmp_path / "TASK_REGISTER.md"
    tasks_dir = tmp_path / "tasks"

    # Create a simple task register
    task_register.write_text(textwrap.dedent('''
        ```yaml
        id: TASK-20260101-001
        objetivo: "Test task"
        projeto: "jaaz"
        ```
    '''))

    # Run migration
    report = migrate(task_register, tasks_dir)

    # Verify files were written
    assert len(report.written) == 1
    assert "TASK-20260101-001" in report.written
    assert len(report.skipped) == 0

    # Verify the output file exists and has correct content
    out_file = tasks_dir / "TASK-20260101-001.md"
    assert out_file.exists()
    content = out_file.read_text()
    assert "id: TASK-20260101-001" in content
    assert "## Objetivo" in content


def test_migrate_idempotency_skips_existing_files(tmp_path):
    """Important: running migrate() twice should skip already-written files."""
    task_register = tmp_path / "TASK_REGISTER.md"
    tasks_dir = tmp_path / "tasks"

    # Create a simple task register
    task_register.write_text(textwrap.dedent('''
        ```yaml
        id: TASK-20260101-001
        objetivo: "Test task"
        projeto: "jaaz"
        ```
    '''))

    # Run migration first time
    report1 = migrate(task_register, tasks_dir)
    assert len(report1.written) == 1
    assert len(report1.skipped) == 0

    # Get the original content
    out_file = tasks_dir / "TASK-20260101-001.md"
    original_content = out_file.read_text()

    # Run migration second time
    report2 = migrate(task_register, tasks_dir)
    assert len(report2.written) == 0
    assert len(report2.skipped) == 1
    assert "TASK-20260101-001" in report2.skipped

    # Verify file was NOT overwritten
    final_content = out_file.read_text()
    assert final_content == original_content


def test_catch_all_renders_ad_hoc_fields():
    """Important: any unconsumed fields must be rendered in 'Outros campos' section."""
    task = {
        "id": "TASK-20260101-002",
        "objetivo": "Test with ad-hoc fields",
        "custo": "R$50",
        "tokens_entrada": 1000,
        "tokens_saida": 500,
        "modelo": "claude-3-sonnet",
    }
    note = render_task_note(task)

    # Should have "Outros campos" section
    assert "## Outros campos" in note

    # Ad-hoc fields should appear in the output
    assert "**custo:**" in note
    assert "R$50" in note
    assert "**tokens_entrada:**" in note
    assert "1000" in note
    assert "**tokens_saida:**" in note
    assert "500" in note
    assert "**modelo:**" in note
    assert "claude-3-sonnet" in note


def test_catch_all_renders_template_standard_fields():
    """Important: template-standard fields like maquina, caminho, etc. must be rendered if present."""
    task = {
        "id": "TASK-20260101-003",
        "objetivo": "Test with template standard fields",
        "maquina": "host /root/jaaz",
        "caminho": "/root/jaaz",
        "versao_estado": "branch main",
        "integrador": "coordenador",
    }
    note = render_task_note(task)

    # Should have "Outros campos" section
    assert "## Outros campos" in note

    # Fields should appear
    assert "**maquina:**" in note
    assert "host /root/jaaz" in note
    assert "**caminho:**" in note
    assert "/root/jaaz" in note


def test_catch_all_omitted_when_no_leftover_fields():
    """Important: 'Outros campos' section should NOT appear if all fields are consumed."""
    task = {
        "id": "TASK-20260101-004",
        "objetivo": "Standard task",
        "resultado": "Done",
        "estado": "concluida",
    }
    note = render_task_note(task)

    # Should NOT have "Outros campos" section
    assert "## Outros campos" not in note
