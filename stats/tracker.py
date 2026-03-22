import json
from pathlib import Path
from models.result import Result

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "history.json"


def _load() -> list[dict]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_result(result: Result) -> None:
    history = _load()
    history.append(result.to_dict())
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(history, indent=2))


def get_history() -> list[dict]:
    return _load()


def get_stats_by_technique() -> dict[str, dict]:
    history = _load()
    stats: dict[str, dict] = {}
    for r in history:
        name = r["technique"]
        if name not in stats:
            stats[name] = {"total": 0, "correct": 0, "total_time": 0.0}
        stats[name]["total"] += 1
        if r["is_correct"]:
            stats[name]["correct"] += 1
        stats[name]["total_time"] += r["time_seconds"]
    for name, s in stats.items():
        s["accuracy"] = s["correct"] / s["total"] if s["total"] else 0
        s["avg_time"] = s["total_time"] / s["total"] if s["total"] else 0
    return stats
