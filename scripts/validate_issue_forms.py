#!/usr/bin/env python3
"""Validate this repository's community-health assets.

Checks:
  * every GitHub Issue Form under .github/ISSUE_TEMPLATE/*.yml parses as YAML
    and conforms to the GitHub Issue Forms structure;
  * the pull request template and the top-level docs exist and are non-empty.

Exit code is 0 when everything is valid, 1 otherwise. Intended to be run
locally or in CI:  python3 scripts/validate_issue_forms.py
"""
from __future__ import annotations

import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
ISSUE_DIR = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"

VALID_BODY_TYPES = {"markdown", "textarea", "input", "dropdown", "checkboxes"}
TOP_LEVEL_ALLOWED = {
    "name", "description", "title", "labels", "assignees", "projects", "body",
}

checks: list[tuple[bool, str]] = []


def record(passed: bool, msg: str) -> None:
    checks.append((passed, msg))


def validate_issue_form(path: pathlib.Path) -> None:
    rel = path.relative_to(REPO_ROOT)
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        first_line = str(exc).splitlines()[0]
        record(False, f"{rel}: YAML parse error: {first_line}")
        return

    if not isinstance(data, dict):
        record(False, f"{rel}: top-level document must be a mapping")
        return

    problems: list[str] = []

    for key in ("name", "description", "body"):
        if key not in data:
            problems.append(f"missing required key '{key}'")

    unknown = sorted(set(data) - TOP_LEVEL_ALLOWED)
    if unknown:
        problems.append(f"unknown top-level key(s): {unknown}")

    body = data.get("body")
    input_fields = 0
    if not isinstance(body, list) or not body:
        problems.append("'body' must be a non-empty list")
    else:
        ids: list[str] = []
        for i, item in enumerate(body):
            if not isinstance(item, dict):
                problems.append(f"body[{i}] must be a mapping")
                continue
            block_type = item.get("type")
            if block_type not in VALID_BODY_TYPES:
                problems.append(
                    f"body[{i}] invalid/missing type {block_type!r}"
                )
                continue
            attrs = item.get("attributes")
            if not isinstance(attrs, dict):
                problems.append(f"body[{i}] '{block_type}' needs attributes")
            elif block_type == "markdown":
                if "value" not in attrs:
                    problems.append(f"body[{i}] markdown needs attributes.value")
            elif "label" not in attrs:
                problems.append(f"body[{i}] '{block_type}' needs attributes.label")

            if block_type != "markdown":
                input_fields += 1
                if "id" in item:
                    ids.append(item["id"])
            validations = item.get("validations")
            if validations is not None and not isinstance(validations, dict):
                problems.append(f"body[{i}] 'validations' must be a mapping")
        if len(ids) != len(set(ids)):
            problems.append(f"duplicate field ids: {ids}")

    if problems:
        for problem in problems:
            record(False, f"{rel}: {problem}")
    else:
        record(
            True,
            f"{rel}: valid issue form "
            f"(name={data.get('name')!r}, {input_fields} input field(s))",
        )


def check_nonempty(path: pathlib.Path) -> None:
    rel = path.relative_to(REPO_ROOT)
    if not path.exists():
        record(False, f"{rel}: expected file is missing")
    elif path.stat().st_size == 0:
        record(False, f"{rel}: file is empty")
    else:
        record(True, f"{rel}: present ({path.stat().st_size} bytes)")


def main() -> int:
    yml_files = sorted(ISSUE_DIR.glob("*.yml")) + sorted(ISSUE_DIR.glob("*.yaml"))
    if not yml_files:
        record(False, "no issue-form YAML files found under .github/ISSUE_TEMPLATE")
    for path in yml_files:
        validate_issue_form(path)

    check_nonempty(REPO_ROOT / ".github" / "pull_request_template.md")
    for name in ("README.md", "SECURITY.md", "GOVERNANCE.md", "CODE_OF_CONDUCT.md", "LICENSE"):
        check_nonempty(REPO_ROOT / name)

    for passed, msg in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {msg}")

    passed = sum(1 for ok, _ in checks if ok)
    print("=" * 60)
    print(f"Result: {passed}/{len(checks)} checks passed")
    if passed != len(checks):
        return 1
    print("All community-health assets are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
