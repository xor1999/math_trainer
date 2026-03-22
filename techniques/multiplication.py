from random import randint, choice
from models.technique import Technique, register


@register
class Mult2x1(Technique):
    name = "2-digit × 1-digit"
    category = "multiplication"
    description = "Multiply a 2-digit number by a 1-digit number"

    def generate(self) -> tuple[str, int]:
        a, b = randint(10, 99), randint(2, 9)
        return f"{a} × {b}", a * b

    def hint(self, problem: str) -> str:
        a, b = (int(x) for x in problem.split(" × "))
        tens, ones = divmod(a, 10)
        p1 = tens * 10 * b
        p2 = ones * b
        return (
            f"Break apart:\n"
            f"  {tens * 10} × {b} = {p1}\n"
            f"  {ones} × {b} = {p2}\n"
            f"  {p1} + {p2} = {p1 + p2}"
        )


@register
class Mult3x1(Technique):
    name = "3-digit × 1-digit"
    category = "multiplication"
    description = "Multiply a 3-digit number by a 1-digit number"

    def generate(self) -> tuple[str, int]:
        a, b = randint(100, 999), randint(2, 9)
        return f"{a} × {b}", a * b


@register
class Mult2x2(Technique):
    name = "2-digit × 2-digit"
    category = "multiplication"
    description = "Multiply two 2-digit numbers (criss-cross / addition method)"

    def generate(self) -> tuple[str, int]:
        a, b = randint(10, 99), randint(10, 99)
        return f"{a} × {b}", a * b

    def hint(self, problem: str) -> str:
        a, b = (int(x) for x in problem.split(" × "))
        # Round-up/down method from Arthur Benjamin
        a_tens, a_ones = divmod(a, 10)
        return (
            f"Addition method:\n"
            f"  {a} × {b // 10 * 10} = {a * (b // 10 * 10)}\n"
            f"  {a} × {b % 10} = {a * (b % 10)}\n"
            f"  Total = {a * b}"
        )


@register
class MultBy11(Technique):
    name = "Multiply by 11"
    category = "multiplication"
    description = "Multiply any 2-digit number by 11"

    def generate(self) -> tuple[str, int]:
        a = randint(10, 99)
        return f"{a} × 11", a * 11

    def hint(self, problem: str) -> str:
        a = int(problem.split(" × ")[0])
        d1, d2 = divmod(a, 10)
        middle = d1 + d2
        if middle < 10:
            return f"Spread and add: {d1}[{d1}+{d2}]{d2} = {d1}{middle}{d2}"
        return (
            f"Spread and add: {d1}[{d1}+{d2}]{d2}\n"
            f"  Middle = {middle}, carry 1\n"
            f"  Result = {a * 11}"
        )


@register
class MultBy5(Technique):
    name = "Multiply by 5"
    category = "multiplication"
    description = "Multiply by 5 (divide by 2, multiply by 10)"

    def generate(self) -> tuple[str, int]:
        a = randint(10, 999)
        return f"{a} × 5", a * 5

    def hint(self, problem: str) -> str:
        a = int(problem.split(" × ")[0])
        if a % 2 == 0:
            return f"{a} ÷ 2 = {a // 2}, then × 10 = {a * 5}"
        return f"{a} ÷ 2 = {a / 2}, then × 10 = {a * 5}"


@register
class SquareEndingIn5(Technique):
    name = "Square numbers ending in 5"
    category = "multiplication"
    description = "Square a 2-digit number ending in 5 (e.g. 35² = 3×4|25 = 1225)"

    def generate(self) -> tuple[str, int]:
        a = choice([15, 25, 35, 45, 55, 65, 75, 85, 95])
        return f"{a}²", a * a

    def hint(self, problem: str) -> str:
        a = int(problem.replace("²", ""))
        first = a // 10
        product = first * (first + 1)
        return (
            f"First digit × next digit: {first} × {first + 1} = {product}\n"
            f"Append 25: {product}25\n"
            f"  {a}² = {a * a}"
        )


@register
class MultSameFirstDigitSumTo10(Technique):
    name = "Same first digit, units sum to 10"
    category = "multiplication"
    description = "Multiply 2-digit numbers sharing first digit whose units sum to 10 (e.g. 83×87)"

    def generate(self) -> tuple[str, int]:
        first = randint(1, 9)
        d1 = randint(1, 9)
        d2 = 10 - d1
        a = first * 10 + d1
        b = first * 10 + d2
        return f"{a} × {b}", a * b

    def hint(self, problem: str) -> str:
        a, b = (int(x) for x in problem.split(" × "))
        first = a // 10
        front = first * (first + 1)
        back = (a % 10) * (b % 10)
        return (
            f"First digit × next digit: {first} × {first + 1} = {front}\n"
            f"Units product: {a % 10} × {b % 10} = {back:02d}\n"
            f"  {a} × {b} = {a * b}"
        )


@register
class SquareNumbers(Technique):
    name = "Square 2-digit numbers"
    category = "multiplication"
    description = "Square a 2-digit number using rounding technique"

    def generate(self) -> tuple[str, int]:
        a = randint(10, 99)
        return f"{a}²", a * a

    def hint(self, problem: str) -> str:
        a = int(problem.replace("²", ""))
        # Round to nearest 10
        nearest = round(a / 10) * 10
        diff = a - nearest
        up = nearest
        down = a + diff  # a - diff would be nearest, a + diff is the other side
        # Actually: a = nearest + diff, so (a-diff)*(a+diff) + diff^2
        complement = a - diff  # = nearest
        other = a + diff
        return (
            f"Round to {nearest}:\n"
            f"  {a - abs(diff)} × {a + abs(diff)} = {(a - abs(diff)) * (a + abs(diff))}\n"
            f"  + {abs(diff)}² = {diff * diff}\n"
            f"  = {a * a}"
        )
