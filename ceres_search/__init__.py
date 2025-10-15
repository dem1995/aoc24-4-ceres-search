"""
This module provides methods for reading in a grid of letters
    and finding substrings (and crossings of substrings)
    within it.

`main` reads the puzzle input from a file
    and prints the number of substrings and crossings found.

Methods:
    `main() -> None`
    `read_input(file_input_path: Path) -> list[str]`
    `is_string_at_location(substring: str, grid: list[str], row: int, col: int, direction: Direction) -> bool`
    `is_string_crossing_at_location(substring: str, grid: list[str], row: int, col: int) -> bool`
    `find_string_locations_in_grid(substring: str, grid: list[str]) -> Iterable[tuple[int, int, Enum]]`
    `find_string_crossings_in_grid(substring: str, grid: list[str]) -> Iterable[tuple[int, int]]`

Classes:
    `Direction(Enum)`
"""

from enum import Enum
from pathlib import Path
from typing import Iterable


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


class Direction(Enum):
    EAST = (0, 1)
    SOUTHEAST = (1, 1)
    SOUTH = (1, 0)
    SOUTHWEST = (1, -1)
    WEST = (0, -1)
    NORTHWEST = (-1, -1)
    NORTH = (-1, 0)
    NORTHEAST = (-1, 1)


def is_string_at_location(
    substring: str, grid: list[str], row: int, col: int, direction: Direction
) -> bool:
    """
    Returns True if the string formed from walking the grid from the starting position along the provided direction
        matches the provided string.
    """
    if grid[row][col] != substring[0]:
        return False

    for i in range(1, len(substring)):
        row, col = row + direction.value[0], col + direction.value[1]
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[row]):
            return False
        if grid[row][col] != substring[i]:
            return False
    return True


def is_string_crossing_at_location(
    substring: str, grid: list[str], row: int, col: int
) -> bool:
    """
    Returns True if the string twice diagonally crosses the provided location
        such that the center of the string is that location each time.
    """

    # If the string is a palindrome, it will be counted in both directions.
    #   We assume it's not one for convenience when checking for two crossings.
    is_palindrome = substring == substring[::-1]
    if is_palindrome:
        raise ValueError("Sought-after string must not be a palindrome.")

    necessary_offset = len(substring) // 2
    center_letter = substring[necessary_offset]

    if grid[row][col] != center_letter:
        return False

    # Check if there's enough room around the center letter to form the
    #   sought-for string.
    if (
        row < necessary_offset
        or col < necessary_offset
        or row >= len(grid) - necessary_offset
        or col >= len(grid[row]) - necessary_offset
    ):
        return False

    # Determine the paths that need to be checked to find the sought-for string.
    upper_left_starting_check = (row - necessary_offset, col - necessary_offset)
    upper_right_starting_check = (row - necessary_offset, col + necessary_offset)
    lower_left_starting_check = (row + necessary_offset, col - necessary_offset)
    lower_right_starting_check = (row + necessary_offset, col + necessary_offset)
    starting_check_map = {
        Direction.SOUTHEAST: upper_left_starting_check,
        Direction.SOUTHWEST: upper_right_starting_check,
        Direction.NORTHEAST: lower_left_starting_check,
        Direction.NORTHWEST: lower_right_starting_check,
    }

    # See in how many directions the sought-for string can be found.
    x_matches = 0
    for direction in starting_check_map:
        starting_check = starting_check_map[direction]
        if is_string_at_location(
            substring, grid, starting_check[0], starting_check[1], direction
        ):
            x_matches += 1

            # If the sought-for string can be found in two diagonal directions
            #   then it forms an x at that location
            if x_matches == 2:
                return True

    return False


def find_string_locations_in_grid(
    substring: str, grid: list[str]
) -> Iterable[tuple[int, int, Enum]]:
    """
    Given a grid of letters represented as a list of strings, find all occurrences of a given substring.

    The substring must not have duplicate letters and must not be a palindrome.

    Args:
        grid (list[str]): The grid of letters.
        substring (str): The substring to find.

    Returns:
        list[tuple[int, int, Enum]]: The locations of the substring in the grid.
    """

    # If the string has duplicate letters or is a palindrome, it is undefined
    #   whether it should be counted twice (or more) or not.
    has_duplicate_letters = len(set(substring)) < len(substring)
    is_palindrome = substring == substring[::-1]
    if has_duplicate_letters or is_palindrome:
        raise ValueError(
            "Sought-after string must not have duplicate letters and must not be a palindrome."
        )

    # For each location in the grid, check to see if, following that
    #   location in each direction, the string can be found in one of them.
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == substring[0]:
                for direction in Direction:
                    if is_string_at_location(substring, grid, row, col, direction):
                        yield (row, col, direction)


def find_string_crossings_in_grid(
    substring: str, grid: list[str]
) -> Iterable[tuple[int, int]]:
    """
    Given a grid of letters represented as a list of strings,
      find all intersecting substrings on the center letter.

    The substring must have an odd number of letters
       and must not be a palindrome
       and must not have duplicate letters.

    Args:
        grid (list[str]): The grid of letters.
        substring (str): The substring to find.

    Returns:
        list[tuple[int, int]]: The locations of the substring in the grid.
    """
    has_duplicate_letters = len(set(substring)) < len(substring)
    is_palindrome = substring == substring[::-1]
    if has_duplicate_letters or is_palindrome:
        raise ValueError(
            "Sought-after string must not have duplicate letters and must not be a palindrome."
        )

    if len(substring) % 2 == 0:
        raise ValueError("Sought-after string must have an odd number of letters.")

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if is_string_crossing_at_location(substring, grid, row, col):
                yield (row, col)


def main():
    puzzle_input = read_input(Path("put_puzzle_input_here.txt"))
    substring_matches = list(find_string_locations_in_grid("XMAS", puzzle_input))
    print(len(substring_matches))

    xcrossing_substring_matches = list(
        find_string_crossings_in_grid("MAS", puzzle_input)
    )
    print(len(xcrossing_substring_matches))


__all__ = [
    "main",
    "read_input",
    "is_string_at_location",
    "is_string_crossing_at_location",
    "find_string_locations_in_grid",
    "find_string_crossings_in_grid",
]
