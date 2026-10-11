import unittest
import io
from unittest.mock import patch

from src.lab1.calculator import addiction, subtract, multiply, divide, power, calculator


class CalculatorTestCase(unittest.TestCase):

    def run_calculator(self, inputs):
        with patch("builtins.input", side_effect=inputs), \
                patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            calculator()
        return fake_out.getvalue()

    def test_addiction(self):
        self.assertEqual(addiction(2, 3), 5)
        self.assertEqual(addiction(-2, -3), -5)
        self.assertEqual(addiction(-2, 3), 1)
        self.assertEqual(addiction(5, 0), 5)
        self.assertAlmostEqual(addiction(0.1, 0.2), 0.3)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)
        self.assertEqual(subtract(-3, -5), 2)
        self.assertEqual(subtract(5, 0), 5)
        self.assertAlmostEqual(subtract(0.3, 0.1), 0.2)

    def test_multiply(self):
        self.assertEqual(multiply(4, 3), 12)
        self.assertEqual(multiply(-4, 3), -12)
        self.assertEqual(multiply(-4, -3), 12)
        self.assertEqual(multiply(5, 0), 0)
        self.assertEqual(multiply(5, 1), 5)
        self.assertAlmostEqual(multiply(0.5, 4), 2.0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(7, 2), 3.5)
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(-10, -2), 5)
        self.assertEqual(divide(0, 5), 0)

    def test_divide_by_zero(self):
        self.assertEqual(divide(5, 0), "Ошибка: на ноль делить нельзя")
        self.assertEqual(divide(0, 0), "Ошибка: на ноль делить нельзя")

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(5, 1), 5)
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(-2, 3), -8)
        self.assertEqual(power(-2, 2), 4)
        self.assertEqual(power(0, 5), 0)
        self.assertAlmostEqual(power(4, 0.5), 2.0)

    def test_power_zero_to_negative(self):
        self.assertEqual(power(0, -1), "Ошибка: ноль нельзя возводить в отрицательную степень!")

    def test_power_negative_base_fractional(self):
        self.assertEqual(power(-8, 0.5), "Ошибка: результат не является вещественным числом!")

    def test_power_overflow(self):
        self.assertEqual(power(10.0, 1000), "Ошибка: слишком большое число!")

    # ---------- интерактивная функция calculator() ----------
    def test_calculator_operations(self):
        cases = [
            ("+", "2", "3", "Результат: 5.0"),
            ("-", "5", "3", "Результат: 2.0"),
            ("*", "4", "3", "Результат: 12.0"),
            ("/", "10", "4", "Результат: 2.5"),
            ("**", "2", "3", "Результат: 8.0"),
        ]
        for op, a, b, expected in cases:
            with self.subTest(op=op):
                output = self.run_calculator([op, a, b, "q"])
                self.assertIn(expected, output)

    def test_calculator_division_by_zero(self):
        output = self.run_calculator(["/", "5", "0", "q"])
        self.assertIn("Ошибка: на ноль делить нельзя", output)

    def test_calculator_power_error(self):
        output = self.run_calculator(["**", "0", "-1", "q"])
        self.assertIn("Ошибка: ноль нельзя возводить в отрицательную степень!", output)

    def test_calculator_unknown_operation(self):
        output = self.run_calculator(["%", "q"])
        self.assertIn("Неизвестная операция", output)

    def test_calculator_invalid_second_number(self):
        output = self.run_calculator(["+", "2", "abc", "q"])
        self.assertIn("Нужно вводить числа!", output)

    def test_calculator_invalid_first_number(self):
        output = self.run_calculator(["+", "abc", "q"])
        self.assertIn("Нужно вводить числа!", output)

    def test_calculator_quit(self):
        output = self.run_calculator(["q"])
        self.assertIn("До свидания!", output)

    def test_calculator_several_calculations_in_a_row(self):
        output = self.run_calculator(["+", "1", "2", "*", "3", "4", "q"])
        self.assertIn("Результат: 3.0", output)
        self.assertIn("Результат: 12.0", output)

    def test_calculator_continues_after_errors(self):
        # сначала неизвестная операция, потом неверное число, потом нормальный расчёт
        output = self.run_calculator(["%", "+", "x", "+", "1", "2", "q"])
        self.assertIn("Неизвестная операция", output)
        self.assertIn("Нужно вводить числа!", output)
        self.assertIn("Результат: 3.0", output)


if __name__ == "__main__":
    unittest.main()