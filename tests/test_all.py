import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ceres_search import read_input  # noqa: E402


def test_read_input():
    sample_path = Path(__file__).parent / "test_input.txt"
    grid = read_input(sample_path)
    assert len(grid) == 4
    assert len(grid[0]) == 7
    assert grid[0] == "FISHFIS"
