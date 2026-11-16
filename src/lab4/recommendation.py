"""Модуль рекомендаций фильмов на основе истории просмотров.

Реализует алгоритм подбора следующего фильма по схожести с другими пользователями.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Set


class Movie:
    """Представление фильма."""

    def __init__(self, movie_id: int, name: str) -> None:
        self.movie_id = movie_id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.movie_id}: {self.name}"


class UserHistory:
    """История просмотров одного пользователя."""

    def __init__(self, movie_ids: List[int]) -> None:
        self.movies = movie_ids

    def unique_movies(self) -> Set[int]:
        """Возвращает множество уникальных идентификаторов фильмов."""
        return set(self.movies)


class RecommendationSystem:
    """Система рекомендаций фильмов."""

    def __init__(
        self,
        movies_file: str = "movies.txt",
        history_file: str = "history.txt",
    ) -> None:
        self.movies: Dict[int, str] = {}
        self.histories: List[UserHistory] = []
        self._load_movies(movies_file)
        self._load_histories(history_file)

    def _load_movies(self, path: str) -> None:
        """Загружает справочник фильмов из файла."""
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                movie_id_str, name = line.split(",", 1)
                self.movies[int(movie_id_str.strip())] = name.strip()

    def _load_histories(self, path: str) -> None:
        """Загружает истории просмотров пользователей."""
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                ids = [
                    int(part.strip())
                    for part in line.split(",")
                    if part.strip()
                ]
                self.histories.append(UserHistory(ids))

    def recommend(self, user_movies: List[int]) -> str:
        """Возвращает название рекомендуемого фильма.

        Args:
            user_movies: Список идентификаторов фильмов, просмотренных пользователем.

        Returns:
            Название фильма или сообщение об отсутствии рекомендации.
        """
        if not user_movies:
            return "Нет рекомендации"

        user_set = set(user_movies)
        user_size = len(user_set)
        if user_size == 0:
            return "Нет рекомендации"

        scores: Dict[int, float] = defaultdict(float)

        for history in self.histories:
            hist_set = history.unique_movies()
            common = len(hist_set & user_set)
            ratio = common / user_size

            if ratio >= 0.5:
                weight = ratio
                for movie_id in history.movies:
                    if movie_id not in user_set and movie_id in self.movies:
                        scores[movie_id] += weight

        if not scores:
            return "Нет рекомендации"

        best_id = max(scores, key=scores.get)
        return self.movies.get(best_id, "Неизвестный фильм")


if __name__ == "__main__":
    system = RecommendationSystem()
    raw = input("Введите id фильмов через запятую (например 2,4): ").strip()
    user_ids = [int(part.strip()) for part in raw.split(",") if part.strip()]
    print(system.recommend(user_ids))