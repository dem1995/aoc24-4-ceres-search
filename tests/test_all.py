import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ceres_search import (  # noqa: E402
    Direction,
    read_input,
    find_string_locations_in_grid,
    find_string_crossings_in_grid,
    is_string_at_location,
    is_string_crossing_at_location,
)


def test_read_input():
    sample_path = Path(__file__).parent / "test_input.txt"
    grid = read_input(sample_path)
    assert len(grid) == 4
    assert len(grid[0]) == 7
    assert grid[0] == "FISHFIS"


@pytest.fixture
def example_grid():
    return [
        "COD....",
        ".COD...",
        "C.COD.D",
        ".O...O.",
        "D.D.C.C",
    ]


def test_is_string_at_location(example_grid):
    assert is_string_at_location("COD", example_grid, 0, 0, Direction.EAST)
    assert not is_string_at_location("COD", example_grid, 0, 0, Direction.SOUTH)
    assert is_string_at_location("COD", example_grid, 2, 2, Direction.NORTH)
    assert is_string_at_location("COD", example_grid, 2, 2, Direction.EAST)
    assert is_string_at_location("COD", example_grid, 2, 2, Direction.SOUTHWEST)
    assert not is_string_at_location("COD", example_grid, 2, 2, Direction.SOUTHEAST)
    assert not is_string_at_location("COD", example_grid, 0, 0, Direction.NORTH)


def test_is_string_crossing_at_location(example_grid):
    assert not is_string_crossing_at_location("COD", example_grid, 2, 2)
    assert is_string_crossing_at_location("COD", example_grid, 3, 1)
    assert is_string_crossing_at_location("COD", example_grid, 3, 5)


def test_find_string_locations_in_grid(example_grid):
    assert len(list(find_string_locations_in_grid("COD", example_grid))) == 8


def test_find_string_crossings_in_grid(example_grid):
    assert len(list(find_string_crossings_in_grid("COD", example_grid))) == 2
