import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "001_pen_cup"


@pytest.fixture
def models_dir(tmp_path):
    """A models/ directory holding one complete, consistent model (001_pen_cup)."""
    d = tmp_path / "models"
    shutil.copytree(FIXTURE, d / "001_pen_cup")
    return d
