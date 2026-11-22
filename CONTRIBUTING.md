# Contributing to bom-sourcing

Contributions that improve BOM extraction precision, schema clarity, electrical constraint checks, or `robo-market-search` interface alignment are welcome.

## Workflow

1. Fork the repository and create a branch from `main`.
2. Use descriptive branch names prefixed by change type: `feat/`, `fix/`, `docs/`, or `chore/`.
3. Keep pull requests focused on a single behavioral or documentation change.
4. Run the local verification checks before opening a pull request.

## Commit Convention

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Usage |
| :--- | :--- |
| `feat:` | New skill capability, contract field, or sourcing rule |
| `fix:` | Correction to schema semantics, evidence rules, or broken references |
| `docs:` | Updates to `README.md`, `ROADMAP.md`, or supporting documentation |
| `chore:` | CI workflows, templates, linters, or repository maintenance |

Example:

```text
fix(skill): clarify quantity handling for repeated cart queries
```

## Skill Editing Rules

When editing [bom-sourcing/SKILL.md](bom-sourcing/SKILL.md):

- Preserve the offline privacy guarantee: no network access when offline mode is requested, and no project files or secrets sent to catalog services.
- Keep all BOM contract field names and enum values backward compatible unless proposing a versioned breaking change.
- Update [README.md](README.md) and [bom-sourcing/README.md](bom-sourcing/README.md) whenever contract fields, enums, or supported interfaces change.
- Avoid marketing adjectives, em-dashes, and unverified claims in documentation.

## Local Verification

Run the governance and link validation check from the repository root:

```bash
python3 -c '
import glob, os, re, sys

for f in ["README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "ROADMAP.md", "bom-sourcing/SKILL.md"]:
    assert os.path.isfile(f), f"Missing {f}"

text = open("bom-sourcing/SKILL.md", encoding="utf-8").read()
assert text.startswith("---\n") and "name: bom-sourcing" in text.split("---\n", 2)[1]

for f in glob.glob("**/*.md", recursive=True):
    content = re.sub(r"```[\s\S]*?```", "", open(f, encoding="utf-8").read())
    content = re.sub(r"`[^`]*`", "", content)
    for link in re.findall(r"\[.*?\]\((?!https?://|mailto:)(.*?)(?:#.*)?\)", content):
        link = link.strip().split("?")[0]
        if link and not link.startswith("#"):
            target = os.path.normpath(os.path.join(os.path.dirname(f), link))
            assert os.path.exists(target), f"Broken link: {f} -> {link}"
print("All local checks passed.")
'
```

## Pull Request Checklist

- Commits adhere to Conventional Commits.
- All modified Markdown files pass internal link checks.
- No secrets, local environment files, or IDE metadata are committed.
- Documentation stays aligned with [bom-sourcing/SKILL.md](bom-sourcing/SKILL.md).
