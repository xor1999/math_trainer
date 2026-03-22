import time
from models.technique import Technique
from models.result import Result
from stats.tracker import save_result


def run_test(technique_classes: list[type[Technique]], num_problems: int = 20) -> None:
    """Timed test across one or more techniques. No hints."""
    import random

    print(f"\n--- Test Mode ---")
    techniques_desc = ", ".join(t.name for t in technique_classes)
    print(f"Techniques: {techniques_desc}")
    print(f"{num_problems} problems, timed, no hints. Type 'q' to quit.\n")

    instances = [cls() for cls in technique_classes]
    correct = 0
    total = 0
    total_time = 0.0

    for i in range(num_problems):
        technique = random.choice(instances)
        problem, answer = technique.generate()
        print(f"  [{i + 1}/{num_problems}] {problem} = ?")

        start = time.time()
        user_input = input("  > ").strip()
        elapsed = time.time() - start

        if user_input.lower() == "q":
            print("  Stopped early.")
            break

        total += 1
        total_time += elapsed

        try:
            user_answer: int | float | None = int(user_input)
        except ValueError:
            try:
                user_answer = float(user_input)
            except ValueError:
                user_answer = None

        if user_answer == answer:
            correct += 1
            print(f"  ✓ ({elapsed:.1f}s)")
        else:
            print(f"  ✗ {answer} ({elapsed:.1f}s)")

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
        print(f"\n  Results: {correct}/{total} ({correct / total * 100:.0f}%)")
        print(f"  Total time: {total_time:.1f}s")
        print(f"  Avg time per problem: {total_time / total:.1f}s")
