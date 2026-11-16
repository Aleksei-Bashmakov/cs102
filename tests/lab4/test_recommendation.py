"""Модульные тесты системы рекомендаций фильмов."""

import sys
import unittest
from pathlib import Path

# Добавляем src/lab4 в путь
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "lab4"))

from recommendation import RecommendationSystem


class TestRecommendation(unittest.TestCase):
    """Модульные тесты системы рекомендаций."""

    @classmethod
    def setUpClass(cls) -> None:
        with open("movies_test.txt", "w", encoding="utf-8") as file:
            file.write("1,Мстители: Финал\n")
            file.write("2,Хатико\n")
            file.write("3,Дюна\n")
            file.write("4,Унесенные призраками\n")
            file.write("5,Интерстеллар\n")
            file.write("6,Начало\n")

        with open("history_test.txt", "w", encoding="utf-8") as file:
            file.write("2,1,3\n")
            file.write("1,4,3\n")
            file.write("2,2,2,2,2,3\n")
            file.write("1,5,6\n")
            file.write("4,5,3\n")
            file.write("2,4,5\n")

        cls.system = RecommendationSystem(
            "movies_test.txt",
            "history_test.txt",
        )

    def test_example_from_task(self) -> None:
        """Пример из условия: 2,4 → Дюна."""
        self.assertEqual(self.system.recommend([2, 4]), "Дюна")

    def test_empty_list(self) -> None:
        """Пустой список просмотров."""
        self.assertEqual(self.system.recommend([]), "Нет рекомендации")

    def test_single_movie(self) -> None:
        """Один фильм — рекомендация по схожим."""
        result = self.system.recommend([2])
        self.assertIn(result, self.system.movies.values())

    def test_all_movies_watched(self) -> None:
        """Пользователь посмотрел все фильмы из базы."""
        result = self.system.recommend([1, 2, 3, 4, 5, 6])
        self.assertEqual(result, "Нет рекомендации")

    def test_no_similar_users(self) -> None:
        """Нет пользователей с достаточным пересечением."""
        result = self.system.recommend([999, 1000])
        self.assertEqual(result, "Нет рекомендации")

    def test_high_overlap(self) -> None:
        """Высокое пересечение (вес ближе к 1)."""
        result = self.system.recommend([2, 4, 5])
        self.assertIn(result, self.system.movies.values())


if __name__ == "__main__":
    unittest.main()