"""Модульные тесты разбивки респондентов по возрастным группам."""

import sys
import unittest
from pathlib import Path

# Добавляем src/lab4 в путь
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "lab4"))

from age_grouper import AgeGrouper, Respondent


class TestAgeGrouper(unittest.TestCase):
    """Модульные тесты разбивки по возрастным группам."""

    def setUp(self) -> None:
        self.grouper = AgeGrouper([18, 25, 35, 45, 60, 80, 100])

    def test_example_from_task(self) -> None:
        """Полный пример из условия."""
        data = [
            ("Кошельков Захар Брониславович", 105),
            ("Дьячков Нисон Иринеевич", 88),
            ("Иванов Варлам Якунович", 88),
            ("Старостин Ростислав Ермолаевич", 50),
            ("Ярилова Розалия Трофимовна", 29),
            ("Соколов Андрей Сергеевич", 15),
            ("Егоров Алан Петрович", 7),
        ]
        for name, age in data:
            self.grouper.add_respondent(Respondent(name, age))

        expected = (
            "101+: Кошельков Захар Брониславович (105)\n"
            "81-100: Дьячков Нисон Иринеевич (88), "
            "Иванов Варлам Якунович (88)\n"
            "46-60: Старостин Ростислав Ермолаевич (50)\n"
            "26-35: Ярилова Розалия Трофимовна (29)\n"
            "0-18: Соколов Андрей Сергеевич (15), "
            "Егоров Алан Петрович (7)"
        )
        self.assertEqual(self.grouper.format_output(), expected)

    def test_empty_groups_skipped(self) -> None:
        """Пустые группы не выводятся."""
        self.grouper.add_respondent(Respondent("Иванов Иван", 30))
        output = self.grouper.format_output()
        self.assertIn("26-35", output)
        self.assertNotIn("19-25", output)
        self.assertNotIn("36-45", output)

    def test_same_age_sorted_by_name(self) -> None:
        """При одинаковом возрасте сортировка по ФИО по возрастанию."""
        self.grouper.add_respondent(Respondent("Яковлев", 40))
        self.grouper.add_respondent(Respondent("Алексеев", 40))
        self.grouper.add_respondent(Respondent("Петров", 40))
        output = self.grouper.format_output()
        self.assertIn("Алексеев (40), Петров (40), Яковлев (40)", output)

    def test_age_descending_inside_group(self) -> None:
        """Внутри группы возраст убывает."""
        self.grouper.add_respondent(Respondent("Молодой", 20))
        self.grouper.add_respondent(Respondent("Старший", 25))
        output = self.grouper.format_output()
        self.assertTrue(output.index("Старший") < output.index("Молодой"))

    def test_open_end_group(self) -> None:
        """Последняя группа открытая (101+)."""
        self.grouper.add_respondent(Respondent("Долгожитель", 120))
        output = self.grouper.format_output()
        self.assertIn("101+: Долгожитель (120)", output)

    def test_no_respondents(self) -> None:
        """Нет ни одного респондента — пустой вывод."""
        self.assertEqual(self.grouper.format_output(), "")


if __name__ == "__main__":
    unittest.main()