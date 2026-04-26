# Project-Specific Instructions

## Code Standards
- **Indentation**: Use **Tabs** exclusively for all code. 
- **Exception**: Use **Spaces (2 or 4)** only for YAML if required by the specification.
- **Formatting**: Always run `make format` and `make lint` before finishing any task to ensure compliance with the project's Ruff configuration.

## Architecture & Scalability
- **Modularity**: Logic must be decoupled from the CLI. `analyze.py` is for orchestration; all heavy lifting belongs in `core/`.
- **Functional Style**: Prefer pure functions. Each new feature or logic component should be its own function to ensure maximum testability.
- **Data Scalability**: To add a new data source, create a new class in `core/providers/` inheriting from `BaseProvider`.
- **Feature Scalability**: 
	- **New Scoring Math**: Add a pure function to `core/scorers.py` and register it in the `SCORERS` dictionary.
	- **New Asset Metrics**: Update the `AssetData` dataclass in `core/schema.py` and add the metric to the relevant `benchmarks_*.json`.
- **Separation of Concerns**: If a module grows too large, move it into its own logical directory within `core/` (e.g., `core/analysis/`).

## Environment & Execution
- **Branching Strategy**: Always create a new branch for features or fixes. Once the work is verified and complete, switch to `main` locally and merge. Do not create PRs for now.
- **Command Policy**: **ALWAYS** use `make` commands for all operations (running analysis, testing, linting).
- **Prohibited**: Do **NOT** run or suggest direct `uv` or `python3` command calls.

## Data & Architecture
- **Data Source**: **Yahoo Finance (yfinance)** is the primary source for all data (Price, Fundamentals, ETF metrics).
- **Evaluation Logic**: `benchmarks_stock.json` and `benchmarks_etf.json` define the scoring parameters. Always update these files when adjusting how a metric is interpreted.
- **Investment Profiles**: `profiles.json` defines the relative importance (weights) of metrics for different investor types.

## Testing & Validation
- **Test Suite**: Use `make test` to validate changes. 
- **Requirement**: ALWAYS add comprehensive tests for new functionality and major refactorings. Every new function should have a corresponding test case.
- **Coverage Target**: Maintain a minimum overall test coverage of **80%**. Use `uv run pytest --cov=core` to verify.
- **Validation**: When adding or modifying scoring functions in `core/scorers.py`, always verify the output against the expected curve documented in `benchmarks.md`.
