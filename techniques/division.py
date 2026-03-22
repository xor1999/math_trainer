from random import randint
from models.technique import Technique, register


@register
class DivBy1Digit(Technique):
    name = "Divide by 1-digit"
    category = "division"
    description = "Divide a 2-3 digit number by a 1-digit divisor (exact)"

    def generate(self) -> tuple[str, int]:
        divisor = randint(2, 9)
        quotient = randint(10, 150)
        dividend = divisor * quotient
        return f"{dividend} ÷ {divisor}", quotient


@register
class DivBy1DigitRemainder(Technique):
    name = "Divide by 1-digit (with remainder)"
    category = "division"
    description = "Divide and give quotient with remainder"

    def generate(self) -> tuple[str, int]:
        divisor = randint(2, 9)
        dividend = randint(20, 999)
        # Answer is just the integer quotient
        return f"{dividend} ÷ {divisor} (integer part)", dividend // divisor
