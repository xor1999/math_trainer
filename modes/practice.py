import time
from models.technique import Technique
from models.result import Result
from stats.tracker import save_result


def run_practice(technique_cls: type[Technique], num_problems: int = 10) -> None:
    technique = technique_cls()
    print(f"\n--- Practice: {technique.name} ---")
    print(f"({technique.description})")
    print(f"{num_problems} problems. Type 'h' for hint, 'q' to quit.\n")

    correct = 0
    total = 0

    for i in range(num_problems):
        problem, answer = technique.generate()
        print(f"  [{i + 1}/{num_problems}] {problem} = ?")

        start = time.time()
        user_input = input("  > ").strip()

        if user_input.lower() == "q":
            print("  Stopped early.")
            break

        if user_input.lower() == "h":
            hint = technique.hint(problem)
            if hint:
                print(f"\n  Hint:\n  {hint}\n")
            else:
                print("  No hint available for this technique.\n")
            user_input = input("  > ").strip()
            if user_input.lower() == "q":
                break

        elapsed = time.time() - start
        total += 1

        try:
            user_answer: int | float | None = int(user_input)
        except ValueError:
            try:
                user_answer = float(user_input)
            except ValueError:
                user_answer = None

        if user_answer == answer:
            correct += 1
            print(f"  ✓ Correct! ({elapsed:.1f}s)\n")
        else:
            print(f"  ✗ Wrong. Answer: {answer} ({elapsed:.1f}s)\n")

        result = Result.create(
            technique=technique.name,
            category=technique.category,
            problem=problem,
            correct_answer=answer,
            user_answer=user_answer,
            time_seconds=elapsed,
        )
        save_result(result)

    if total > 0:
        print(f"  Score: {correct}/{total} ({correct / total * 100:.0f}%)")
