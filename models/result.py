from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Result:
    technique: str
    category: str
    problem: str
    correct_answer: int | float
    user_answer: int | float | None
    is_correct: bool
    time_seconds: float
    timestamp: str

    @staticmethod
    def create(technique: str, category: str, problem: str,
               correct_answer: int | float, user_answer: int | float | None,
               time_seconds: float) -> "Result":
        return Result(
            technique=technique,
            category=category,
            problem=problem,
            correct_answer=correct_answer,
            user_answer=user_answer,
            is_correct=user_answer == correct_answer,
            time_seconds=time_seconds,
            timestamp=datetime.now().isoformat(),
        )

    def to_dict(self) -> dict:
        return asdict(self)
