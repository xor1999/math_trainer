from random import randint
from models.technique import Technique, register


@register
class Add2Digit(Technique):
    name = "2-digit + 2-digit"
    category = "addition"
    description = "Add two 2-digit numbers left to right"

    def generate(self) -> tuple[str, int]:
        a, b = randint(10, 99), randint(10, 99)
        return f"{a} + {b}", a + b

    def hint(self, problem: str) -> str:
        a, b = (int(x) for x in problem.split(" + "))
        tens_b, ones_b = divmod(b, 10)
        step1 = a + tens_b * 10
        return (
            f"Left to right:\n"
            f"  {a} + {tens_b * 10} = {step1}\n"
            f"  {step1} + {ones_b} = {step1 + ones_b}"
        )


@register
class Add3Digit(Technique):
    name = "3-digit + 3-digit"
    category = "addition"
    description = "Add two 3-digit numbers left to right"

    def generate(self) -> tuple[str, int]:
        a, b = randint(100, 999), randint(100, 999)
        return f"{a} + {b}", a + b

    def hint(self, problem: str) -> str:
        a, b = (int(x) for x in problem.split(" + "))
        hundreds = (b // 100) * 100
        tens = ((b % 100) // 10) * 10
        ones = b % 10
        s1 = a + hundreds
        s2 = s1 + tens
        return (
            f"Left to right:\n"
            f"  {a} + {hundreds} = {s1}\n"
            f"  {s1} + {tens} = {s2}\n"
            f"  {s2} + {ones} = {s2 + ones}"
        )
