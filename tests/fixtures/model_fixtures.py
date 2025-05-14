from pathlib import Path

import pytest

@pytest.fixture
def model_path_abc() -> Path:
    """Fixture for a model file."""
    return Path(__file__).parent / "data" / "abc.pblang"
