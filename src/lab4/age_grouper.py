"""Модуль разбивки респондентов социологического опроса по возрастным группам."""

from __future__ import annotations

import sys
from typing import List, Optional


class Respondent:
    """Респондент опроса."""

    def __init__(self, full_name: str, age: int) -> None:
        self.full_name = full_name.strip()
        self.age = age

    def __str__(self) -> str:
        return f"{self.full_name} ({self.age})"

    def __lt__(self, other: Respondent) -> bool:
        if self.age != other.age:
            return self.age > other.age
        return self.full_name < other.full_name


class AgeGroup:
    """Возрастная группа."""

    def __init__(self, min_age: int, max_age: Optional[int] = None) -> None:
        self.min_age = min_age
        self.max_age = max_age
        self.respondents: List[Respondent] = []

    def add(self, respondent: Respondent) -> None:
        """Добавляет респондента в группу."""
        self.respondents.append(respondent)

    def label(self) -> str:
        """Возвращает текстовое представление границ группы."""
        if self.max_age is None:
            return f"{self.min_age}+"
        if self.min_age == 0:
            return f"0-{self.max_age}"
        return f"{self.min_age}-{self.max_age}"

    def is_empty(self) -> bool:
        """Проверяет, есть ли в группе респонденты."""
        return not self.respondents

    def sorted_list(self) -> List[Respondent]:
        """Возвращает отсортированный список респондентов группы."""
        return sorted(self.respondents)


class AgeGrouper:
    """Разбивает респондентов по возрастным группам."""

    def __init__(self, boundaries: List[int]) -> None:
        self.boundaries = sorted(set(boundaries))
        self.groups: List[AgeGroup] = self._build_groups()

    def _build_groups(self) -> List[AgeGroup]:
        """Создаёт список возрастных групп по границам."""
        groups: List[AgeGroup] = []
        if not self.boundaries:
            return [AgeGroup(0, None)]

        groups.append(AgeGroup(0, self.boundaries[0]))
        for index in range(len(self.boundaries) - 1):
            groups.append(
                AgeGroup(
                    self.boundaries[index] + 1,
                    self.boundaries[index + 1],
                ),
            )
        groups.append(AgeGroup(self.boundaries[-1] + 1, None))
        return groups

    def add_respondent(self, respondent: Respondent) -> None:
        """Распределяет респондента в подходящую группу."""
        for group in self.groups:
            if group.max_age is None:
                if respondent.age >= group.min_age:
                    group.add(respondent)
                    return
            elif group.min_age <= respondent.age <= group.max_age:
                group.add(respondent)
                return

    def format_output(self) -> str:
        """Формирует итоговый вывод по группам."""
        lines: List[str] = []
        for group in reversed(self.groups):
            if group.is_empty():
                continue
            people = ", ".join(
                str(respondent) for respondent in group.sorted_list()
            )
            lines.append(f"{group.label()}: {people}")
        return "\n".join(lines)


def main() -> None:
    """Точка входа приложения."""
    if len(sys.argv) < 2:
        print(
            "Usage: python age_grouper.py <границы...>",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        boundaries = [int(arg) for arg in sys.argv[1:]]
    except ValueError:
        print("Границы должны быть числами", file=sys.stderr)
        sys.exit(1)

    grouper = AgeGrouper(boundaries)

    for line in sys.stdin:
        line = line.strip()
        if line == "END":
            break
        if "," not in line:
            continue
        name, age_str = line.rsplit(",", 1)
        try:
            age = int(age_str.strip())
            if 0 <= age <= 123:
                grouper.add_respondent(Respondent(name, age))
        except ValueError:
            continue

    print(grouper.format_output())


if __name__ == "__main__":
    main()