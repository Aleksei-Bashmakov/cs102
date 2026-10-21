import pathlib
import unittest

from src.lab3 import sudoku

PUZZLES_DIR = pathlib.Path(__file__).resolve().parents[2] / "src" / "lab3"


class SudokuTestCase(unittest.TestCase):
    def setUp(self):
        self.grid = sudoku.read_sudoku(PUZZLES_DIR / "puzzle1.txt")
        self.solution = [
            ['5', '3', '4', '6', '7', '8', '9', '1', '2'],
            ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
            ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
            ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
            ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
            ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
            ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
            ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
            ['3', '4', '5', '2', '8', '6', '1', '7', '9'],
        ]

    def test_group(self):
        self.assertEqual(sudoku.group([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(
            sudoku.group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3),
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        )
        self.assertEqual(sudoku.group([], 3), [])

    def test_get_row(self):
        self.assertEqual(
            sudoku.get_row(self.grid, (0, 0)),
            ['5', '3', '.', '.', '7', '.', '.', '.', '.'],
        )
        self.assertEqual(
            sudoku.get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0)),
            ['4', '.', '6'],
        )
        self.assertEqual(
            sudoku.get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0)),
            ['.', '8', '9'],
        )

    def test_get_col(self):
        self.assertEqual(
            sudoku.get_col(self.grid, (0, 0)),
            ['5', '6', '.', '8', '4', '7', '.', '.', '.'],
        )
        self.assertEqual(
            sudoku.get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1)),
            ['2', '.', '8'],
        )
        self.assertEqual(
            sudoku.get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2)),
            ['3', '6', '9'],
        )

    def test_get_block(self):
        self.assertEqual(
            sudoku.get_block(self.grid, (0, 1)),
            ['5', '3', '.', '6', '.', '.', '.', '9', '8'],
        )
        self.assertEqual(
            sudoku.get_block(self.grid, (4, 7)),
            ['.', '.', '3', '.', '.', '1', '.', '.', '6'],
        )
        self.assertEqual(
            sudoku.get_block(self.grid, (8, 8)),
            ['2', '8', '.', '.', '.', '5', '.', '7', '9'],
        )

    def test_find_empty_positions(self):
        self.assertEqual(
            sudoku.find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]),
            (0, 2),
        )
        self.assertEqual(
            sudoku.find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]),
            (1, 1),
        )
        self.assertEqual(
            sudoku.find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]),
            (2, 0),
        )
        self.assertIsNone(sudoku.find_empty_positions(self.solution))

    def test_find_possible_values(self):
        self.assertEqual(sudoku.find_possible_values(self.grid, (0, 2)), {'1', '2', '4'})
        self.assertEqual(sudoku.find_possible_values(self.grid, (4, 7)), {'2', '5', '9'})

    def test_solve(self):
        self.assertEqual(sudoku.solve(self.grid), self.solution)

    def test_solve_already_solved(self):
        self.assertEqual(sudoku.solve(self.solution), self.solution)

    def test_solve_impossible(self):
        grid = [["."] * 9 for _ in range(9)]
        grid[0] = list("12345678.")
        grid[1][8] = '9'  # в клетку (0, 8) нельзя поставить ни одну цифру
        self.assertIsNone(sudoku.solve(grid))

    def test_check_solution(self):
        self.assertTrue(sudoku.check_solution(self.solution))

    def test_check_solution_bad(self):
        # строка корректна, но нарушены столбцы
        bad = [row[:] for row in self.solution]
        bad[0][0], bad[0][1] = bad[0][1], bad[0][0]
        self.assertFalse(sudoku.check_solution(bad))
        # есть незаполненная клетка
        unfinished = [row[:] for row in self.solution]
        unfinished[4][4] = '.'
        self.assertFalse(sudoku.check_solution(unfinished))
        # решения нет
        self.assertFalse(sudoku.check_solution(None))

    def test_generate_sudoku(self):
        for n, empty in [(40, 41), (1000, 0), (0, 81), (81, 0)]:
            with self.subTest(n=n):
                grid = sudoku.generate_sudoku(n)
                self.assertEqual(sum(1 for row in grid for e in row if e == '.'), empty)
                self.assertTrue(sudoku.check_solution(sudoku.solve(grid)))


if __name__ == "__main__":
    unittest.main()