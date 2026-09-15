#!/usr/bin/env python3
"""Lint the public API docs. Exits 1 on any hit.

1. Every property and parameter name in api-reference/openapi.json is snake_case.
2. Every JSON key in ```json fences of the top-level *.mdx is snake_case.
3. No em dash in the top-level *.mdx.

Keys only, never values: SPEAKER_00, ISO timestamps and event names are values.
No allowlist. A camelCase hit in the spec is a backend bug; re-sync, never patch.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "api-reference" / "openapi.json"
CAMEL = re.compile(r"[a-z][A-Z]")
FENCE = re.compile(r"^```json[^\n]*\n(.*?)^```", re.MULTILINE | re.DOTALL)
KEY = re.compile(r'"([^"\\]+)"\s*:')
EM_DASH = "\u2014"


def walk_schema_names(node, path, hits):
    """Collect camelCase property and parameter names anywhere in the spec."""
    if isinstance(node, dict):
        for name in node.get("properties") or {}:
            if CAMEL.search(name):
                hits.append(f"{path}.properties.{name}")
        # Header names (X-Vook-Signature) follow HTTP convention, not the casing rule.
        if node.get("in") in {"query", "path", "cookie"} and CAMEL.search(node.get("name", "")):
            hits.append(f"{path}.name={node['name']}")
        for key, value in node.items():
            walk_schema_names(value, f"{path}.{key}", hits)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            walk_schema_names(value, f"{path}[{i}]", hits)


def json_keys(node):
    if isinstance(node, dict):
        for key, value in node.items():
            yield key
            yield from json_keys(value)
    elif isinstance(node, list):
        for value in node:
            yield from json_keys(value)


def lint_spec():
    hits = []
    walk_schema_names(json.loads(SPEC.read_text()), "openapi", hits)
    return [f"{SPEC.relative_to(ROOT)}: camelCase name {hit}" for hit in hits]


def lint_mdx(page):
    errors = []
    text = page.read_text()
    rel = page.relative_to(ROOT)

    for lineno, line in enumerate(text.splitlines(), 1):
        if EM_DASH in line:
            errors.append(f"{rel}:{lineno}: em dash")

    for match in FENCE.finditer(text):
        block = match.group(1)
        lineno = text.count("\n", 0, match.start()) + 1
        try:
            keys = set(json_keys(json.loads(block)))
        except json.JSONDecodeError:
            # Examples with placeholders are not valid JSON; fall back to key positions.
            keys = set(KEY.findall(block))
        for key in sorted(keys):
            if CAMEL.search(key):
                errors.append(f"{rel}:{lineno}: camelCase JSON key {key!r}")
    return errors


def main():
    errors = lint_spec()
    for page in sorted(ROOT.glob("*.mdx")):
        errors.extend(lint_mdx(page))
    for error in errors:
        print(error)
    if errors:
        print(f"\n{len(errors)} problem(s).")
        return 1
    print("Docs lint passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
