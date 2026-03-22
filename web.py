import sys
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Register all techniques
for module_file in (Path(__file__).resolve().parent / "techniques").glob("*.py"):
    if module_file.name != "__init__.py":
        importlib.import_module(f"techniques.{module_file.stem}")

from flask import Flask, render_template, jsonify, request
from models.technique import get_techniques_by_category, get_all_techniques, find_technique
from models.result import Result
from stats.tracker import save_result, get_stats_by_technique

app = Flask(__name__)

# Keep technique instances alive so generate() works
_instances: dict[str, object] = {}


def _get_instance(name: str):
    if name not in _instances:
        cls = find_technique(name)
        if cls is None:
            return None
        _instances[name] = cls()
    return _instances[name]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/techniques")
def api_techniques():
    by_cat = get_techniques_by_category()
    result = {}
    for cat, techniques in sorted(by_cat.items()):
        result[cat] = [
            {"name": t.name, "description": t.description}
            for t in techniques
        ]
    return jsonify(result)


@app.route("/api/problem", methods=["POST"])
def api_problem():
    data = request.get_json()
    name = data.get("technique")
    instance = _get_instance(name)
    if instance is None:
        return jsonify({"error": "Unknown technique"}), 400
    problem, answer = instance.generate()
    return jsonify({"problem": problem, "answer": answer})


@app.route("/api/hint", methods=["POST"])
def api_hint():
    data = request.get_json()
    name = data.get("technique")
    problem = data.get("problem")
    instance = _get_instance(name)
    if instance is None:
        return jsonify({"hint": None})
    hint = instance.hint(problem)
    return jsonify({"hint": hint})


@app.route("/api/submit", methods=["POST"])
def api_submit():
    data = request.get_json()
    result = Result.create(
        technique=data["technique"],
        category=data["category"],
        problem=data["problem"],
        correct_answer=data["correct_answer"],
        user_answer=data.get("user_answer"),
        time_seconds=data.get("time_seconds", 0),
    )
    save_result(result)
    return jsonify({"is_correct": result.is_correct})


@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats_by_technique())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
