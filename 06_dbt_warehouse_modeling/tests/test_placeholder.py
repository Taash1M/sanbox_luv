import subprocess
import pathlib
import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt_project"


@pytest.mark.integration
def test_dbt_models_build_successfully():
    """
    Director-level sanity check:
    - Ensures the dbt project is structurally valid.
    - Validates that core models compile and run in the target environment.
    This test is intentionally high-level and would normally run in CI.
    """
    assert DBT_PROJECT_DIR.exists(), f"dbt_project directory not found at {DBT_PROJECT_DIR}"

    # In a real environment, the profile/target would be configured via env vars or CI secrets.
    result = subprocess.run(
        ["dbt", "build", "--project-dir", str(DBT_PROJECT_DIR)],
        capture_output=True,
        text=True,
    )

    # Log output to help diagnose failures in CI.
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    assert result.returncode == 0, "dbt build failed; see output above for details."
