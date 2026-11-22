# Security Policy

## Supported Versions

| Version | Supported |
| :--- | :---: |
| `main` (latest) | Yes |

## Data and Credential Handling Boundary

`bom-sourcing` operates on local project repositories that may contain `.env` files, API keys, Wi-Fi credentials, or proprietary schematics.

- Offline BOM mode must never invoke network tools or external catalog services.
- Live sourcing mode must submit sanitized component search queries only.
- Project source files, credentials, tokens, and unrelated repository content must never be transmitted to external services.

## Reporting a Vulnerability

Do not open a public GitHub issue for security vulnerabilities, prompt-injection bypasses that leak local credentials, or unsafe tool invocation flaws.

Report issues privately through one of the following channels:

1. GitHub Private Vulnerability Reporting under the repository's **Security** tab.
2. Direct email to `atacanymc@gmail.com` with the subject prefix `[SECURITY] bom-sourcing`.

Include a clear description of the issue, reproduction steps, and affected files.

## Response SLA

- **Initial acknowledgment**: Within 48 hours of receipt.
- **Triage and assessment**: Within 5 business days.
- **Resolution disclosure**: Coordinated with the reporter once a fix is merged on `main`.
