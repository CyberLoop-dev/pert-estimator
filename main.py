#!/usr/bin/env python3
"""Dependency-aware PERT estimator."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_tasks(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {path}: {exc}") from exc
    tasks = data.get("tasks") if isinstance(data, dict) else data
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Input must be a non-empty task array or an object with a tasks array.")
    return tasks


def analyze(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    by_id: dict[str, dict[str, Any]] = {}
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str):
            raise ValueError("Every task must be an object with a string id.")
        task_id = task["id"]
        if task_id in by_id:
            raise ValueError(f"Duplicate task id: {task_id}")
        values = [task.get("optimistic"), task.get("most_likely"), task.get("pessimistic")]
        if any(not isinstance(value, (int, float)) or value < 0 for value in values):
            raise ValueError(f"Task {task_id}: durations must be non-negative numbers.")
        optimistic, likely, pessimistic = values
        if not optimistic <= likely <= pessimistic:
            raise ValueError(f"Task {task_id}: expected optimistic <= most_likely <= pessimistic.")
        dependencies = task.get("depends_on", [])
        if not isinstance(dependencies, list) or any(not isinstance(dep, str) for dep in dependencies):
            raise ValueError(f"Task {task_id}: depends_on must be an array of task ids.")
        by_id[task_id] = {**task, "depends_on": dependencies}

    for task_id, task in by_id.items():
        for dep in task["depends_on"]:
            if dep not in by_id:
                raise ValueError(f"Task {task_id} depends on unknown task {dep}.")

    order: list[str] = []
    temporary: set[str] = set()
    permanent: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in permanent:
            return
        if task_id in temporary:
            raise ValueError(f"Dependency cycle detected at task {task_id}.")
        temporary.add(task_id)
        for dep in by_id[task_id]["depends_on"]:
            visit(dep)
        temporary.remove(task_id)
        permanent.add(task_id)
        order.append(task_id)

    for task_id in by_id:
        visit(task_id)

    results: dict[str, dict[str, Any]] = {}
    predecessor: dict[str, str | None] = {}
    for task_id in order:
        task = by_id[task_id]
        optimistic, likely, pessimistic = task["optimistic"], task["most_likely"], task["pessimistic"]
        expected = (optimistic + 4 * likely + pessimistic) / 6
        variance = ((pessimistic - optimistic) / 6) ** 2
        deps = task["depends_on"]
        parent = max(deps, key=lambda dep: results[dep]["finish"]) if deps else None
        start = max((results[dep]["finish"] for dep in deps), default=0.0)
        results[task_id] = {
            "id": task_id,
            "name": task.get("name", task_id),
            "expected": expected,
            "variance": variance,
            "start": start,
            "finish": start + expected,
            "depends_on": deps,
        }
        predecessor[task_id] = parent

    end_id = max(results, key=lambda task_id: results[task_id]["finish"])
    critical_path: list[str] = []
    cursor: str | None = end_id
    while cursor is not None:
        critical_path.append(cursor)
        cursor = predecessor[cursor]
    critical_path.reverse()
    critical_set = set(critical_path)
    for task_id, result in results.items():
        result["critical"] = task_id in critical_set

    return {
        "project_duration": results[end_id]["finish"],
        "critical_path": critical_path,
        "critical_path_variance": sum(results[item]["variance"] for item in critical_path),
        "tasks": [results[item] for item in order],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate a dependency graph with PERT.")
    parser.add_argument("file", nargs="?", default="sample/tasks.json", type=Path)
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()
    result = analyze(load_tasks(args.file))
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"Estimated project duration: {result['project_duration']:.2f} time units")
    print("Critical path: " + " -> ".join(result["critical_path"]))
    print(f"Critical-path variance: {result['critical_path_variance']:.3f}")
    print("\nID       EXPECTED   START   FINISH   CRITICAL")
    print("-" * 52)
    for task in result["tasks"]:
        flag = "yes" if task["critical"] else "no"
        print(f"{task['id']:<8} {task['expected']:>8.2f} {task['start']:>7.2f} {task['finish']:>8.2f}   {flag}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(2)
