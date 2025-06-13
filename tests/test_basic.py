import importlib
import sys
from pathlib import Path

# allow import of src package
sys.path.append(str(Path(__file__).resolve().parents[1]))

def test_bot_import():
    assert importlib.import_module('src.bot') is not None
