[← Back to Documentation](README.md)

# Live Sourcing Protocol

Live sourcing runs only when explicitly requested by the user. Offline BOM extraction must never access the network or invoke catalog tools.

## Pre-Flight Requirements

Before running any catalog query, establish:

1. Delivery destination.
2. Target currency.
3. Required quantities per component.
4. Shipping assumptions and free-shipping thresholds.

If any of these inputs are unavailable, report the unknowns and present conditional estimates only. Never fabricate prices, stock counts, or shipping charges.

## Privacy Boundary

- Submit sanitized component search terms only.
- Never send project source files, schematics, `.env` values, credentials, or unrelated repository content to external catalog services.
- Do not install software or invoke undocumented interfaces without user authorization.

## Interface Discovery

Inspect the locally installed version of [robo-market-search](https://github.com/AtaCanYmc/robo-market-search) before calling tools. Tool names and capabilities vary across releases.

| Interface | Discovery Check | Search Operation | Cart Comparison Operation |
| :--- | :--- | :--- | :--- |
| CLI | `robo-search --help` | `robo-search search "ESP32-WROOM"` | `robo-search cart "ESP32" "0.96 OLED Display"` |
| Python SDK | `from robo_market_search import Client` | `Client().search(query, limit_per_store=5)` | `Client().cart_search(queries=queries, limit_per_store=5)` |
| MCP Server (`robo-mcp`) | Inspect active tool schema list | Active search tool (for example `search_products` or `search_electronic_components`) | Active cart tool if exposed by the server |
| REST API | Inspect running server `/docs` or OpenAPI spec | `GET /api/v1/search?q=...` | `POST /api/v1/cart/optimize` with `items` array |

## Candidate Verification Rules

- Preserve store name, product URL, unit price, currency, observed stock, and query timestamp for each candidate.
- Flag any candidate that violates a known electrical, protocol, voltage, or mechanical constraint as incompatible. Never recommend an incompatible part as a cheaper substitute.
- Treat missing specifications on a product listing as unverified (`partial`), not compatible.
- Distinguish clearly between no search results, unavailable store, tool error, and confirmed out-of-stock.

## Cart Comparison and Optimizer Caveats

Compare feasible single-store and split-store plans across the exact same required items and quantities.

1. Include per-store subtotals, shipping fees, free-shipping threshold sources, grand total, currency, delivery assumptions, coverage, and missing items.
2. Keep optional items in a separately labeled scenario.
3. Do not compare a partial cart as equivalent to a complete cart.
4. Request user approval before locking `partial` or `ambiguous` matches into a definitive purchase plan.
5. Verify upstream optimizer selections independently. Heuristic split optimizers and query-keyed interfaces can use stale shipping defaults or mishandle repeated quantities.
6. Label the winning plan as `lowest among evaluated candidates` unless exhaustive optimality is proven.
7. State that observed prices and stock reflect query time only and require a final check before ordering.
