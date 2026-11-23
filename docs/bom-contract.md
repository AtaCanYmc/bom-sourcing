[← Back to Documentation](README.md)

# BOM Item Contract

Every component extracted by `bom-sourcing` must populate all ten contract fields in both offline and live outputs.

## Field Specification

| Field | Type | Required | Rules |
| :--- | :--- | :---: | :--- |
| `raw_name` | String | Yes | Exact wording found in the project. For inferred items, use a labeled description of the missing function. |
| `canonical_name` | String | Yes | Searchable standard component name. Must preserve `raw_name` and hard constraints. |
| `quantity` | Integer or `null` | Yes | Positive integer when confirmed, or `null` when unknown. Explain any estimate in `notes`. |
| `status` | Enum | Yes | `confirmed`, `inferred_required`, or `optional_or_assumed`. |
| `source_files` | Array of Strings | Yes | Project-relative `path:line` or line ranges. Use path plus sheet, component, or feature for binary files. |
| `constraints` | Object | Yes | Known electrical, protocol, power, dimensional, connector, and form-factor requirements. |
| `search_queries` | Array of Strings | Yes | Alternate catalog search terms, part codes, module variants, and Turkish or English names. |
| `match_confidence` | Enum | Yes | `exact`, `partial`, `ambiguous`, or `unmatched`. Use `unmatched` in offline mode or without a selected candidate. |
| `stock_status` | Enum | Yes | `in_stock`, `low_stock`, `out_of_stock`, or `unknown`. Use `unknown` in offline mode. |
| `notes` | String | Yes | Assumptions, conflicts, verification needs, compatibility warnings, and stock warnings. |

## Classification Semantics

### Status Values

| Value | Definition |
| :--- | :--- |
| `confirmed` | Project explicitly identifies the component. Specifications or quantity may still be incomplete. |
| `inferred_required` | Indispensable complementary function supported by project evidence, such as a regulator, charger, or connector. |
| `optional_or_assumed` | Conditional or speculative accessory such as an enclosure, mounting hardware, or optional indicator. |

### Match Confidence Values

| Value | Definition |
| :--- | :--- |
| `exact` | Candidate identity and all known critical constraints are verified. |
| `partial` | Relevant properties match, but at least one critical property remains unverified. |
| `ambiguous` | Multiple plausible identities or unresolved conflicting specifications exist. |
| `unmatched` | No acceptable candidate identified, or running in offline mode. |

### Stock Status Values

| Value | Definition |
| :--- | :--- |
| `in_stock` | Observed store evidence confirms availability. |
| `low_stock` | Store explicitly indicates low remaining stock. |
| `out_of_stock` | Confirmed out of stock. Retain the item with an out-of-stock note in the user's language (for example, `stok yok / alternatif aranmalı` or `out of stock / find alternative`) in `notes`. |
| `unknown` | Offline mode, missing stock count, or unreliable availability signal. |

## Evidence and Unknowns

- Distinguish runtime hardware from software-only dependencies, examples, tests, commented-out code, and alternative designs.
- Reconcile duplicate references without merging electrically distinct variants. Cite all supporting files.
- Report conflicting counts or specifications and request clarification instead of choosing silently.
- Mark unverified critical specifications in the user's language (for example, `belirsiz / projeden doğrulanmalı` or `uncertain / verify from project`). Do not invent voltage ratings, battery chemistries, resistor values, connectors, or quantities.

## JSON Output Example

When structured JSON is requested in Section 4 of [bom-sourcing/SKILL.md](../bom-sourcing/SKILL.md), emit an array of objects with exact contract keys:

```json
[
  {
    "raw_name": "ESP32 dev board",
    "canonical_name": "ESP32-WROOM-32 Development Board",
    "quantity": 1,
    "status": "confirmed",
    "source_files": ["README.md:14", "firmware/platformio.ini:6"],
    "constraints": {
      "supply_voltage": "5V USB / 3.3V logic",
      "interfaces": ["I2C", "UART"]
    },
    "search_queries": [
      "ESP32-WROOM-32",
      "ESP32 geliştirme kartı"
    ],
    "match_confidence": "unmatched",
    "stock_status": "unknown",
    "notes": "Offline BOM extraction. Pin count and USB connector type: belirsiz / projeden doğrulanmalı."
  }
]
```
