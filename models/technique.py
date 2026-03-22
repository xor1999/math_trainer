from abc import ABC, abstractmethod


_registry: dict[str, list[type["Technique"]]] = {}


def register(cls: type["Technique"]) -> type["Technique"]:
    category = cls.category
    _registry.setdefault(category, []).append(cls)
    return cls


def get_techniques_by_category() -> dict[str, list[type["Technique"]]]:
    return dict(_registry)


def get_all_techniques() -> list[type["Technique"]]:
    return [t for techniques in _registry.values() for t in techniques]


def find_technique(name: str) -> type["Technique"] | None:
    for t in get_all_techniques():
        if t.name.lower() == name.lower():
            return t
    return None


class Technique(ABC):
    name: str = ""
    category: str = ""
    description: str = ""

    @abstractmethod
    def generate(self) -> tuple[str, int | float]:
        """Return (problem_display_string, correct_answer)."""

    def hint(self, problem: str) -> str | None:
        """Optional step-by-step hint. Override in subclass."""
        return None
