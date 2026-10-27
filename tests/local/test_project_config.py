from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.local
def test_pytest_registers_local_and_integration_markers(
    pytestconfig: pytest.Config,
) -> None:
    markers = pytestconfig.getini("markers")

    assert any(marker.startswith("local:") for marker in markers)
    assert any(marker.startswith("integration:") for marker in markers)


@pytest.mark.local
def test_project_has_expected_setup_and_ci_files() -> None:
    expected_files = (
        "pytest.ini",
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "README.md",
        ".github/workflows/ui-tests.yml",
    )

    for relative_path in expected_files:
        assert (PROJECT_ROOT / relative_path).is_file(), (
            f"Missing project file: {relative_path}"
        )
