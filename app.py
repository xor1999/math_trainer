import sys
import importlib
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import all technique modules so they register themselves
for module_file in (Path(__file__).resolve().parent / "techniques").glob("*.py"):
    if module_file.name != "__init__.py":
        importlib.import_module(f"techniques.{module_file.stem}")

from models.technique import get_techniques_by_category, get_all_techniques
from modes.practice import run_practice
from modes.test import run_test
from stats.tracker import get_stats_by_technique


def print_menu() -> None:
    print("\n=== Mental Math Trainer ===")
    print("  1. Practice (pick a technique)")
    print("  2. Test (pick techniques, timed)")
    print("  3. View stats")
    print("  4. List all techniques")
    print("  q. Quit")


def pick_techniques(allow_multiple: bool = False) -> list:
    by_category = get_techniques_by_category()
    categories = sorted(by_category.keys())

    print("\nCategories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    print(f"  {'a. All' if allow_multiple else ''}")

    choice = input("\nCategory> ").strip().lower()
    if choice == "a" and allow_multiple:
        return get_all_techniques()

    try:
        cat_idx = int(choice) - 1
        category = categories[cat_idx]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return []

    techniques = by_category[category]
    print(f"\n{category.title()} techniques:")
    for i, t in enumerate(techniques, 1):
        print(f"  {i}. {t.name} — {t.description}")
    if allow_multiple:
        print(f"  a. All {category}")

    choice = input("\nTechnique> ").strip().lower()
    if choice == "a" and allow_multiple:
        return techniques

    try:
        t_idx = int(choice) - 1
        return [techniques[t_idx]]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return []


def show_stats() -> None:
    stats = get_stats_by_technique()
    if not stats:
        print("\nNo history yet. Go practice!")
        return
    print(f"\n{'Technique':<30} {'Done':>5} {'Acc':>6} {'Avg Time':>9}")
    print("-" * 55)
    for name, s in sorted(stats.items()):
        print(
            f"  {name:<28} {s['total']:>5} "
            f"{s['accuracy'] * 100:>5.0f}% {s['avg_time']:>7.1f}s"
        )


def list_techniques() -> None:
    by_category = get_techniques_by_category()
    for cat in sorted(by_category.keys()):
        print(f"\n  {cat.upper()}")
        for t in by_category[cat]:
            print(f"    • {t.name} — {t.description}")


def main() -> None:
    while True:
        print_menu()
        choice = input("\n> ").strip()

        if choice == "1":
            selected = pick_techniques(allow_multiple=False)
            if selected:
                num = input("How many problems? [10] ").strip()
                num = int(num) if num.isdigit() else 10
                run_practice(selected[0], num_problems=num)

        elif choice == "2":
            selected = pick_techniques(allow_multiple=True)
            if selected:
                num = input("How many problems? [20] ").strip()
                num = int(num) if num.isdigit() else 20
                run_test(selected, num_problems=num)

        elif choice == "3":
            show_stats()

        elif choice == "4":
            list_techniques()

        elif choice in ("q", "Q"):
            print("Bye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
