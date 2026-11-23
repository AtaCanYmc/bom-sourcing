# `robo-market-search` Interface Discovery Reference

Upstream documentation: https://github.com/AtaCanYmc/robo-market-search

Always inspect the locally installed version, CLI `--help` output, MCP tool definitions, or OpenAPI schema before invocation. Capabilities and tool names vary across versions. Do not fabricate an interface or install software without user authorization.

## Known Entry Points (Subject to Local Verification)

### CLI (`robo-search`)

```bash
robo-search --help
robo-search search --help
robo-search cart --help

# Search a single component
robo-search search "ESP32-WROOM"

# Compare multi-item cart
robo-search cart "ESP32" "0.96 OLED Display"
```

### Python SDK (`robo_market_search`)

```python
from robo_market_search import Client

client = Client()
results = client.search(query, limit_per_store=5)
cart = client.cart_search(queries=queries, limit_per_store=5)
```

### MCP Server (`robo-mcp`)

Inspect registered tool schemas at runtime before calling tools. Documentation may reference `search_products` or `optimize_cart`, while a given server build may expose `search_electronic_components` only.

### REST API

Inspect the running server's `/docs` or OpenAPI schema before sending requests. Documented endpoints include:

- `GET /api/v1/search` with query parameter `q`
- `POST /api/v1/cart/optimize` with an `items` array

## Optimizer Verification Notes

- Catalog optimizer choices may be based on raw search rankings rather than verified electrical compatibility.
- Default shipping charges and free-shipping thresholds may be stale estimates.
- Heuristic split optimizers and query-keyed interfaces may not represent repeated items or quantities accurately. Do not assume repeated query strings encode quantity.
- Inspect every chosen candidate and verify price, stock, quantity, compatibility, and shipping rules independently before recommending a plan.
