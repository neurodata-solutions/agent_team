#!/usr/bin/env python3
"""Validate the minimal shape of local agent-improvement records."""

import json
import sys
from pathlib import Path


REQUIRED = {
    "trace": {
        "run_id", "task_id", "started_at", "agent", "repo", "branch",
        "commit", "outcome", "evidence",
    },
    "feedback": {
        "feedback_id", "run_id", "source", "severity", "finding",
        "expected", "observed", "recurrence_check", "recommended_action",
    },
    "eval": {
        "case_id", "task", "prompt", "assertions", "checks", "score",
        "threshold", "trace_ref", "status",
    },
}


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in REQUIRED:
        print("usage: validate_record.py {trace|feedback|eval} FILE", file=sys.stderr)
        return 2

    kind, filename = sys.argv[1], Path(sys.argv[2])
    try:
        record = json.loads(filename.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {filename}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}", file=sys.stderr)
        return 1

    if not isinstance(record, dict):
        print("ERROR: top-level JSON value must be an object", file=sys.stderr)
        return 1

    missing = sorted(REQUIRED[kind] - record.keys())
    if missing:
        print(f"ERROR: missing fields: {', '.join(missing)}", file=sys.stderr)
        return 1

    list_fields = {
        "trace": ("evidence",),
        "feedback": ("evidence",),
        "eval": ("assertions", "checks"),
    }[kind]
    for field in list_fields:
        if field in record and not isinstance(record[field], list):
            print(f"ERROR: {field} must be an array", file=sys.stderr)
            return 1

    if kind == "feedback" and not isinstance(record["recurrence_check"], dict):
        print("ERROR: recurrence_check must be an object", file=sys.stderr)
        return 1
    if kind == "eval":
        if record["score"] is not None and not isinstance(record["score"], (int, float)):
            print("ERROR: score must be a number or null", file=sys.stderr)
            return 1
        if not isinstance(record["threshold"], (int, float)):
            print("ERROR: threshold must be a number", file=sys.stderr)
            return 1

    print(f"VALID: {kind} record {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
