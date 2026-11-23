[← Back to Root Repository](../README.md)

# bom-sourcing Skill

Instruction package for AI coding agents that extracts traceable Bills of Materials from project repositories and optionally performs live component sourcing through [robo-market-search](https://github.com/AtaCanYmc/robo-market-search).

## Table of Contents

- [Contents](#contents)
- [Installation](#installation)
- [Execution Stages](#execution-stages)
- [Classification Enums](#classification-enums)
- [Local Verification](#local-verification)

## Contents

| File | Role |
| :--- | :--- |
| [SKILL.md](SKILL.md) | Canonical agent skill specification with YAML frontmatter, evidence rules, live sourcing protocol, and output format. |

## Installation

Install with the Skills CLI:

```bash
npx skills add AtaCanYmc/bom-sourcing
```

Or link this directory manually into your agent's skill search path:

```bash
ln -s "$(pwd)/bom-sourcing" ~/.agents/skills/bom-sourcing
```

## Execution Stages

1. **Choose the scope**: Determine offline BOM extraction versus live sourcing. Confirm delivery destination, currency, quantities, and shipping assumptions before any network access.
2. **Discover project evidence**: Scan README files, manifests, source code, pinout configs, schematics, and mechanical notes. Record project-relative `path:line` evidence for every component.
3. **Source and compare**: Run only in live mode. Detect the installed `robo-market-search` interface (`robo-search`, `robo_market_search`, `robo-mcp`, or REST API), validate electrical constraints, and compare single-store versus split-store plans.
4. **Deliver**: Emit Summary, Sourcing and Cart Comparison, Readable BOM Table, and optional JSON in the user's language.

## Classification Enums

| Field | Allowed Values | Offline Default |
| :--- | :--- | :--- |
| `status` | `confirmed`, `inferred_required`, `optional_or_assumed` | Determined from evidence |
| `match_confidence` | `exact`, `partial`, `ambiguous`, `unmatched` | `unmatched` |
| `stock_status` | `in_stock`, `low_stock`, `out_of_stock`, `unknown` | `unknown` |

## Local Verification

Verify that `SKILL.md` contains valid frontmatter keys (`name` and `description`):

```bash
python3 -c '
text = open("bom-sourcing/SKILL.md", encoding="utf-8").read()
assert text.startswith("---\n"), "Missing YAML frontmatter start"
frontmatter = text.split("---\n", 2)[1]
assert "name: bom-sourcing" in frontmatter, "Missing name key"
assert "description:" in frontmatter, "Missing description key"
print("SKILL.md frontmatter verified.")
'
```
