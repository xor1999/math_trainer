from math import ceil
from random import randint
from models.technique import Technique, register


@register
class Sub2Digit(Technique):
    name = "2-digit - 2-digit"
    category = "subtraction"
    description = "Subtract two 2-digit numbers left to right"

    def generate(self) -> tuple[str, int]:
        a, b = randint(10, 99), randint(10, 99)
        if a < b:
            a, b = b, a
        return f"{a} - {b}", a - b

    def hint(self, problem: str) -> str:
        a, b = (int(x) for x in problem.split(" - "))
        tens_b, ones_b = divmod(b, 10)
        step1 = a - tens_b * 10
        return (
            f"Left to right:\n"
            f"  {a} - {tens_b * 10} = {step1}\n"
            f"  {step1} - {ones_b} = {step1 - ones_b}"
        )


@register
class Sub3Digit(Technique):
    name = "3-digit - 3-digit"
    category = "subtraction"
    description = "Subtract two 3-digit numbers left to right"

    def generate(self) -> tuple[str, int]:
        a, b = randint(100, 999), randint(100, 999)
        if a < b:
            a, b = b, a
        return f"{a} - {b}", a - b


@register
class SubComplements(Technique):
    name = "Subtraction by complements"
    category = "subtraction"
    description = "Subtract by rounding up, then adding back the complement"

    def generate(self) -> tuple[str, int]:
        a = randint(200, 999)
        b = randint(100, a - 1)
        # Ensure b doesn't end in 0 (complement would be trivial)
        while b % 100 == 0:
            b = randint(100, a - 1)
        return f"{a} - {b}", a - b

    def hint(self, problem: str) -> str:
        a, b = (int(x) for x in problem.split(" - "))
        # Round b up to next hundred
        round_up = ceil(b / 100) * 100
        complement = round_up - b
        step1 = a - round_up
        return (
            f"Round {b} up to {round_up}, complement is {complement}:\n"
            f"  {a} - {round_up} = {step1}\n"
            f"  {step1} + {complement} = {step1 + complement}"
        )
