from pathlib import Path

import pytest

@pytest.fixture
def model_paths_abc_steps() -> tuple[Path, Path]:
    """Fixture for a model file."""
    return (Path(__file__).parent / "data" / "abc_steps.pblang",
            Path(__file__).parent / "data" / "abc_steps.pblang.json")


@pytest.fixture
def model_paths_abc_processes() -> tuple[Path, Path]:
    """Fixture for a model file."""
    return (Path(__file__).parent / "data" / "abc_processes.pblang",
            Path(__file__).parent / "data" / "abc_processes.pblang.json")

