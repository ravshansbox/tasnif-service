# AGENTS.md

## User Instructions
- When the user says "note" or "remember", update this AGENTS.md file with the information

## Important File Notes
- `products.json` and `groups.json` are potentially huge and may lack newlines — use `jq` for reading/querying instead of the Read tool

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

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
