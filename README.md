# math_trainer

A web app to practice mental math for quant trading interviews. Train and test yourself on addition, subtraction, multiplication, and division techniques with timed problems, hints, and performance tracking.

## How to run

```bash
pip install -r requirements.txt
python web.py
```

Then open http://localhost:5000.

## Features

- **Practice mode** — pick a specific technique, solve problems at your own pace with step-by-step hints
- **Test mode** — timed sessions with no hints to simulate interview pressure
- **Stats** — track accuracy and average response time per technique

## Techniques

- **Addition** — 2-digit and 3-digit left-to-right addition
- **Subtraction** — 2-digit and 3-digit left-to-right subtraction
- **Multiplication** — 2×1, 3×1, 2×2, multiply by 11, multiply by 5, squaring
- **Division** — single-digit divisor (exact and with remainder)

Techniques inspired by Arthur Benjamin's *Secrets of Mental Math*.
