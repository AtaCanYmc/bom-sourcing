---
name: bom-sourcing
description: Use when a hardware, IoT, maker, or software project needs a bill of materials (BOM), component name normalization, missing parts identification, or price, stock, cart, and shipping comparison using robo-market-search.
---

# BOM sourcing

Produce a traceable parts list first. Treat catalog matches and calculated purchase plans as evidence to check, not proof of electrical compatibility or the global cheapest price.

## 1. Choose the scope

- If the user asks for an offline BOM, do not access the network, invoke catalog tools, or use cached prices as current prices.
- If the user requests prices, availability, stores, a cart, or shipping optimization, extract the BOM first and then perform live sourcing.
- If the mode is unclear, ask whether live sourcing is wanted before any network access. Ask for the project path if it cannot be identified.
- For live sourcing, establish the delivery destination, currency, quantities, and shipping assumptions needed for a comparable total. If unavailable, report the unknowns and offer only conditional estimates; do not invent them. Do not send project files, credentials, or unrelated project content to catalog services: submit component search terms only.

## 2. Discover project evidence

Read relevant README and requirements, source code and dependency manifests, configuration and pinout files, circuit/schematic notes and BOMs, plus power, battery, 3D-printing, mechanical, and enclosure notes when present. Follow references to other relevant files. Distinguish runtime hardware from software-only dependencies, examples, tests, commented-out code, and alternative designs; do not automatically count those as required hardware.

For each component, retain evidence as project-relative `path:line` or line range. For a binary schematic or model, use its path and identifiable sheet, component, or feature instead of inventing line numbers. Reconcile duplicates without merging electrically distinct variants; cite all supporting evidence. If counts or specifications conflict, report the conflict and request clarification instead of choosing silently.

Create one item per distinct component with all fields below, including in offline output:

| Field | Contract |
|---|---|
| `raw_name` | Exact project wording; for an inferred item, use a clearly labeled description of the missing function. |
| `canonical_name` | Searchable standard component name; preserve `raw_name`. |
| `quantity` | Positive integer or `null` if unknown. Explain an estimate in `notes`; do not present it as confirmed. |
| `status` | `confirmed`, `inferred_required`, or `optional_or_assumed`. |
| `source_files` | Array of evidence references; for inference, cite the evidence supporting the need. |
| `constraints` | Object of known electrical, protocol, power, dimensional, connector, and form-factor requirements; mark unknown critical properties in `notes`. |
| `search_queries` | Array of alternate catalog terms, including relevant part codes, module variants and Turkish/English names. |
| `match_confidence` | `exact`, `partial`, `ambiguous`, or `unmatched`; offline or without a selected candidate use `unmatched`. |
| `stock_status` | `in_stock`, `low_stock`, `out_of_stock`, or `unknown`; offline use `unknown`. |
| `notes` | Assumptions, conflicts, verification needs, compatibility and stock warnings. |

`confirmed` means the project explicitly identifies the component, not that every specification or its quantity is known. Mark an indispensable complementary function `inferred_required` only when the evidence supports its necessity; mark conditional or speculative accessories `optional_or_assumed`. Inspect power supply, regulator/buck converter, battery/charging/protection, wiring/jumpers/connectors/headers, buttons/resistors, enclosure and mounting needs. Do not add a particular rating, connector, battery chemistry, resistor value, or quantity without evidence. Mark unknowns clearly in the user's language (for example, "belirsiz / projeden doğrulanmalı" in Turkish or "uncertain / verify from project" in English).

Normalize part names while preserving protocol, supply voltage, current, power, pinout, dimensions, and other hard constraints. Flag a candidate that violates a known constraint as incompatible, never as an acceptable cheap substitute. Missing candidate specifications mean unverified compatibility, not compatibility. For example, an SPI-only module is incompatible with a required I2C interface; a board mentioning a sensor alone does not establish its interface or voltage.

## 3. Source and compare, only in live mode

Discover the available installed interface and its actual version/help or MCP tool definitions before invocation. `robo-search` is the documented CLI executable, `robo_market_search` is the Python package, and `robo-mcp` is the MCP server. See [references/interfaces.md](references/interfaces.md) for documented CLI, Python SDK, MCP, and REST API entry points and optimizer caveats. Capabilities and tool names vary by version: for example, documentation may mention MCP `search_products`/`optimize_cart` while the server may expose `search_electronic_components` only. Do not fabricate an interface or install software without user authorization.

Query each required item with its alternate terms, preserving distinct candidates and their store, URL, price, currency, observed stock, and query time. Check candidate identity and specifications against constraints, and classify the match:

- `exact`: identity and all known critical constraints are verified.
- `partial`: some relevant properties match but at least one critical property remains unverified.
- `ambiguous`: several plausible identities or unresolved conflicting specifications.
- `unmatched`: no acceptable candidate identified.

Map actual stock evidence to the stock enum; `low_stock` requires an explicit indication, and missing or unreliable evidence is `unknown`. A default boolean or missing stock count is not evidence that the required quantity is available. Retain out-of-stock items with an explicit out-of-stock note in the user's language (for example, "stok yok / alternatif aranmalı" in Turkish or "out of stock / find alternative" in English); distinguish no results, unavailable store, tool error, and confirmed out-of-stock. Report failed stores and partial coverage.

Compare feasible single-store and multi-store plans using the same required items and quantities. Include per-store item subtotals, shipping charges, free-shipping thresholds and their source, grand total, currency, delivery assumptions, coverage, and missing items. Include optional items only in a separately labeled scenario. A partial cart is not comparable as a complete cart. Ask for user approval before selecting `partial` or `ambiguous` matches for a definitive purchase plan; show provisional scenarios separately.

The catalog optimizer's candidate choice may be based on search results rather than verified compatibility, and its shipping defaults may be stale estimates. Inspect every chosen product and independently verify price, stock, quantity, and shipping assumptions before recommending it. The upstream split optimizer can be heuristic and its query-keyed interface may not represent repeated items or quantities correctly. Verify quantity support and the returned assignment; do not assume repeated query strings encode quantity. If needed, calculate subtotals and compare feasible assignments separately using verified candidates and shipping rules. Label the result as "lowest among evaluated candidates" in the user's language unless exhaustive optimality is established. If quantity, compatibility, price, stock, shipping, currency conversion, or store coverage is unknown, mark the affected total or recommendation as incomplete or conditional rather than claiming a definitive cheapest plan.

If no usable interface, permission, network, or shipping data is available, state the blocker and provide the offline BOM and any verifiable partial results. Never silently substitute fabricated prices or shipping. State that prices and stock are observations at the query time and require a final check before ordering.

## 4. Deliver

Respond in the user's language, in this order:

1. **Summary:** project scope, confirmed versus inferred items, major unknowns, and whether sourcing was offline, complete, or partial.
2. **Sourcing and cart comparison:** for live mode, present the comparable single-store and split-store scenarios with product subtotal, shipping, total, coverage, assumptions, and timestamp. Explicitly identify excluded, unavailable, unverified, or incomplete scenarios. For offline mode say live comparison was not requested.
3. **Readable BOM table:** show all contract fields, using concise cells and evidence references. Keep missing and out-of-stock items visible.
4. **Optional JSON:** when requested, output an array of item objects with exactly the field names and enum values above. Use JSON `null` for unknown quantity, arrays for `source_files` and `search_queries`, an object for `constraints`, and strings for the remaining fields.

Separate verified facts from inferences and recommendations throughout. Do not report a shopping plan as an order or claim a purchase was made.
