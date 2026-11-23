#!/usr/bin/env python3
"""Validate BOM JSON arrays against schemas/bom-output.schema.json (stdlib only)."""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas" / "bom-output.schema.json").read_text(encoding="utf-8"))
ITEM_SCHEMA = SCHEMA["items"]
PROPS = ITEM_SCHEMA["properties"]
REQUIRED = set(ITEM_SCHEMA["required"])


# ponytail: validates the Draft 2020-12 subset used by bom-output.schema.json; swap to jsonschema package if $ref/oneOf is added later
def validate_bom(data, label="<input>"):
    errors = []
    if not isinstance(data, list):
        return [f"{label}: root must be an array"]
    for i, item in enumerate(data):
        prefix = f"{label}[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: item must be an object")
            continue
        keys = set(item)
        if missing := sorted(REQUIRED - keys):
            errors.append(f"{prefix}: missing required keys {missing}")
        if extra := sorted(keys - set(PROPS)):
            errors.append(f"{prefix}: unexpected keys {extra}")
        for key, spec in PROPS.items():
            if key not in item:
                continue
            val = item[key]
            types = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
            ok_type = (
                ("null" in types and val is None)
                or ("string" in types and isinstance(val, str))
                or ("integer" in types and isinstance(val, int) and not isinstance(val, bool))
                or ("array" in types and isinstance(val, list))
                or ("object" in types and isinstance(val, dict))
            )
            if not ok_type:
                errors.append(f"{prefix}.{key}: expected {types}, got {type(val).__name__}")
                continue
            if "minLength" in spec and isinstance(val, str) and len(val) < spec["minLength"]:
                errors.append(f"{prefix}.{key}: string shorter than {spec['minLength']}")
            if "minimum" in spec and isinstance(val, int) and val < spec["minimum"]:
                errors.append(f"{prefix}.{key}: integer < {spec['minimum']}")
            if "enum" in spec and val not in spec["enum"]:
                errors.append(f"{prefix}.{key}: invalid enum value {val!r}")
            if "minItems" in spec and isinstance(val, list):
                if len(val) < spec["minItems"]:
                    errors.append(f"{prefix}.{key}: array shorter than {spec['minItems']}")
                for j, elem in enumerate(val):
                    if not isinstance(elem, str) or len(elem) < 1:
                        errors.append(f"{prefix}.{key}[{j}]: must be non-empty string")
    return errors


def self_check():
    valid = {
        "raw_name": "x", "canonical_name": "x", "quantity": 1, "status": "confirmed",
        "source_files": ["a:1"], "constraints": {}, "search_queries": ["x"],
        "match_confidence": "unmatched", "stock_status": "unknown", "notes": "",
    }
    assert validate_bom([valid]) == []
    assert validate_bom([{**valid, "quantity": None}]) == []
    assert validate_bom([{**valid, "quantity": 0}])
    assert validate_bom([{**valid, "quantity": True}])
    assert validate_bom([{**valid, "status": "bad"}])
    assert validate_bom([{**valid, "extra": 1}])
    assert validate_bom([{k: v for k, v in valid.items() if k != "notes"}])


if __name__ == "__main__":
    self_check()
    paths = [pathlib.Path(p) for p in sys.argv[1:]] or sorted((ROOT / "tests" / "fixtures").glob("*.json"))
    all_errors = []
    for path in paths:
        all_errors.extend(validate_bom(json.loads(path.read_text(encoding="utf-8")), str(path)))
    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        sys.exit(1)
    print(f"BOM schema validation passed ({len(paths)} fixtures + self-check).")
