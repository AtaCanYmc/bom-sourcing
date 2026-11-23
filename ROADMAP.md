# Roadmap

Milestones track concrete improvements to the `bom-sourcing` skill specification, validation tooling, and upstream catalog alignment.

## v0.1.0 (Completed)

- Core agent skill specification in [bom-sourcing/SKILL.md](bom-sourcing/SKILL.md).
- Traceable BOM item contract with evidence references (`path:line`), electrical constraint preservation, and Turkish or English search query normalization.
- Live sourcing workflow aligned with [robo-market-search](https://github.com/AtaCanYmc/robo-market-search) CLI, Python SDK, MCP, and REST API entry points.
- Repository governance, CI link and frontmatter verification, and release automation.

## v0.2.0 (Current)

- JSON Schema definition in [schemas/bom-output.schema.json](schemas/bom-output.schema.json) for validating structured BOM output arrays emitted in Section 4 of the skill.
- Representative test fixtures in `tests/fixtures/` covering offline hardware projects, conflicting part counts, and incompatible voltage or bus variants.
- Automated zero-dependency schema validation via [scripts/validate_bom.py](scripts/validate_bom.py) in CI.

## v0.3.0 (Planned)

- Version-specific capability matrix tracking `robo-market-search` MCP tool names and cart optimization behavior.
- Guidance for multi-board assemblies and KiCad or EasyEDA BOM exports.
