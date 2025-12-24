# GEMINI.md - Agent Context

> [!IMPORTANT]
> This file is for **AI Agents** working on the project. It defines the rules, context, and preferred coding style.

## Project Identity

* **Name**: Preloto
* **Core Purpose**: A robust, deterministic CLI for generating lottery predictions.

## Architecture

See [docs/TECHNICAL.md](docs/TECHNICAL.md) for full details.

* **Core**: `src/loterias` (OO design).
* **CLI**: `src/cli.py` (Single entry point `preloto`).
* **Tests**: `tests/` (pytest).

## Development Rules

1. **Determinism is King**: All models generally must be seeded or sorted.
2. **Clean Output**: CLI must output parseable JSON/CSV to stdout. Logs go to stderr.
3. **Tests Required**: Any logic change requires a corresponding `pytest` test.
4. **No "Lucky" Numbers**: We build scientific tools, not magic eight balls.

## Documentation Map

* **User Guide**: `README.md`
* **Vision**: `docs/PRODUCT.md`
* **Roadmap**: `docs/PLANNING.md`
