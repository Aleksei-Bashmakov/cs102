"""Utilities for reading, displaying, solving, and generating Sudoku puzzles."""

import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Read a Sudoku puzzle from the specified file."""
    file_path = pathlib.Path(path)
    with file_path.open(encoding="utf-8") as input_file:
        puzzle = input_file.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """Convert a string representation of Sudoku into a 9x9 grid."""
    digits = [char for char in puzzle if char in "123456789."]
    return group(digits, 9)


def display(grid: tp.List[tp.List[str]]) -> None:
    """Display a Sudoku grid in the console."""
    width = 2
    separator = "+".join(["-" * (width * 3)] * 3)

    for row_index in range(9):
        row = "".join(
            grid[row_index][col_index].center(width)
            + ("|" if col_index in (2, 5) else "")
            for col_index in range(9)
        )
        print(row)

        if row_index in (2, 5):
            print(separator)

    print()


def group(values: tp.List[T], group_size: int) -> tp.List[tp.List[T]]:
    """Group values into lists containing group_size elements.

    >>> group([1, 2, 3, 4], 2)
    [[1, 2], [3, 4]]
    >>> group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [
        values[index : index + group_size]
        for index in range(0, len(values), group_size)
    ]


def get_row(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Return all values in the row containing the specified position.

    >>> get_row(
    ...     [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']],
    ...     (0, 0)
    ... )
    ['1', '2', '.']
    >>> get_row(
    ...     [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']],
    ...     (1, 0)
    ... )
    ['4', '.', '6']
    >>> get_row(
    ...     [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']],
    ...     (2, 0)
    ... )
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Return all values in the column containing the specified position.

    >>> get_col(
    ...     [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']],
    ...     (0, 0)
    ... )
    ['1', '4', '7']
    >>> get_col(
    ...     [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']],
    ...     (0, 1)
    ... )
    ['2', '.', '8']
    >>> get_col(
    ...     [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']],
    ...     (0, 2)
    ... )
    ['3', '6', '9']
    """
    return [row[pos[1]] for row in grid]


def get_block(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Return all values in the 3x3 block containing the specified position.

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block_row = (pos[0] // 3) * 3
    block_col = (pos[1] // 3) * 3

    return [
        grid[row_index][col_index]
        for row_index in range(block_row, block_row + 3)
        for col_index in range(block_col, block_col + 3)
    ]


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Find the first empty position in a Sudoku grid.

    >>> find_empty_positions(
    ...     [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
    ... )
    (0, 2)
    >>> find_empty_positions(
    ...     [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]
    ... )
    (1, 1)
    >>> find_empty_positions(
    ...     [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]
    ... )
    (2, 0)
    """
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == ".":
                return row_index, col_index

    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """Return the possible values for the specified position.

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0, 2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4, 7))
    >>> values == {'2', '5', '9'}
    True
    """
    used_values = (
        set(get_row(grid, pos))
        | set(get_col(grid, pos))
        | set(get_block(grid, pos))
    )
    return set("123456789") - used_values


def solve(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.List[tp.List[str]]]:
    """Solve a Sudoku puzzle using recursive backtracking.

    Find an empty position, try every possible value, and recursively
    solve the remaining puzzle. If a value leads to a dead end, undo
    the assignment and try another value.

    >>> grid = read_sudoku('puzzle1.txt')
    >>> check_solution(solve(grid))
    True
    """
    pos = find_empty_positions(grid)

    if pos is None:
        return grid

    row_index, col_index = pos

    for value in find_possible_values(grid, pos):
        grid[row_index][col_index] = value
        result = solve(grid)

        if result is not None:
            return result

    grid[row_index][col_index] = "."
    return None


def check_solution(
    solution: tp.Optional[tp.List[tp.List[str]]],
) -> bool:
    """Return True if the completed Sudoku grid is valid."""
    if solution is None:
        return False

    if len(solution) != 9 or any(len(row) != 9 for row in solution):
        return False

    digits = set("123456789")

    for index in range(9):
        if set(get_row(solution, (index, 0))) != digits:
            return False

        if set(get_col(solution, (0, index))) != digits:
            return False

        block_row = (index // 3) * 3
        block_col = (index % 3) * 3

        if set(get_block(solution, (block_row, block_col))) != digits:
            return False

    return True


def generate_sudoku(filled_cells: int) -> tp.List[tp.List[str]]:
    """Generate a Sudoku grid with the specified number of filled cells.

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for cell in row if cell == '.')
    41
    >>> check_solution(solve(grid))
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for cell in row if cell == '.')
    0
    >>> check_solution(solve(grid))
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for cell in row if cell == '.')
    81
    >>> check_solution(solve(grid))
    True
    """
    grid = [["."] * 9 for _ in range(9)]

    first_row = list("123456789")
    random.shuffle(first_row)
    grid[0] = first_row

    solved_grid = solve(grid)

    if solved_grid is None:
        raise ValueError("The generated Sudoku grid has no solution")

    grid = solved_grid
    filled_cells = max(0, min(filled_cells, 81))

    cells = [(row, col) for row in range(9) for col in range(9)]

    for row_index, col_index in random.sample(
        cells, 81 - filled_cells
    ):
        grid[row_index][col_index] = "."

    return grid


if __name__ == "__main__":
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        puzzle_grid = read_sudoku(filename)
        display(puzzle_grid)

        puzzle_solution = solve(puzzle_grid)

        if puzzle_solution is None:
            print(f"Puzzle {filename} cannot be solved")
        else:
            display(puzzle_solution)

            if check_solution(puzzle_solution):
                print("Solution is correct")
            else:
                print("Solution is incorrect")