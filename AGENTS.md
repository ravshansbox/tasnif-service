# AGENTS.md

## Developer Background
- Experienced JS/TS/Node developer
- New to Python — explain Python concepts in JS/Node terms when relevant

## Project Setup

This project uses **uv** (not poetry) for dependency management.

### JS/Node → Python equivalents
| JS/Node | Python | Purpose |
|---------|--------|---------|
| `package.json` | `pyproject.toml` | Project metadata & config |
| `npm install` | `uv pip install -r requirements.txt` | Install dependencies |
| `node_modules/` | `.venv/` | Installed packages |
| `npx` | `uv run` | Run commands in project context |
| `nodemon` | `uvicorn --reload` | Dev server with hot reload |
| `jest` | `pytest` | Testing |
| `eslint` | `ruff` | Linting |

### Commands
```bash
# Activate venv (like being "in" the project)
source .venv/bin/activate

# Install deps
uv pip install -r requirements.txt        # production
uv pip install -r requirements-dev.txt    # development

# Run tasks (via poe, like npm scripts)
poe dev      # start dev server
poe test     # run tests
poe lint     # lint code
```

### Key Files
- `requirements.txt` — production dependencies (like `dependencies` in package.json)
- `requirements-dev.txt` — dev dependencies (like `devDependencies`)
- `pyproject.toml` — project config, build settings, tool configs
- `.venv/` — virtual environment (gitignored, like node_modules)

### Virtual Environment
Think of `.venv/` like `node_modules/` but with its own Python interpreter. Each project gets its own isolated environment so dependencies don't conflict between projects.
