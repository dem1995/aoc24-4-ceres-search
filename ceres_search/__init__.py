from pathlib import Path


def read_input(file_input_path: Path) -> list[str]:
    """
    Reads the puzzle input from the provided file.

    Args:
        file_input_path (Path): The path to the file containing the puzzle input.

    Returns:
        list[str]: The puzzle input as a list of strings.
    """
    try:
        puzzle_input = (
            file_input_path.read_text(encoding="utf-8-sig").strip().splitlines()
        )
        return puzzle_input
    except FileNotFoundError as e:
        raise SystemExit(
            "Make sure to launch this script from the directory containing it."
        ) from e


def main():
    puzzle_input = read_input(Path("put_puzzle_input_here.txt"))
    print(puzzle_input)
