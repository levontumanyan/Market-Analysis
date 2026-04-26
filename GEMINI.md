# Project-Specific Instructions

## Code Standards
- **Indentation**: Use **Tabs** exclusively for all code. 
- **Exception**: Use **Spaces (2 or 4)** only for YAML if required by the specification.
- **Formatting**: Always run `make format` and `make lint` before finishing any task to ensure compliance with the project's Ruff configuration.

## Environment & Execution
- **branch**: always make sure to create a new branch and work in that once the work is done and the user is satisfied, switch to main locally and merge. no prs for now.
- **Command Policy**: **ALWAYS** use `make` commands for all operations (running analysis, testing, linting).
- **Prohibited**: Do **NOT** run or suggest direct `uv` or `python3` command calls.

## Data & Architecture
- **Data Source**: **Yahoo Finance (yfinance)** is the primary source for all data.
- **Evaluation Logic**: `benchmarks.json` defines the scoring parameters (type, target, width, best, worst). Always update this file when adjusting how a metric is interpreted.
- **Investment Profiles**: `profiles.json` defines the relative importance (weights) of metrics for different investor types.

## Testing & Validation
- **Test Suite**: Use `make test` to validate changes. 
- **Requirement**: ALWAYS add comprehensive tests for new functionality and major refactorings.
- **Validation**: When adding or modifying scoring functions in `core/scorers.py`, always verify the output against the expected curve documented in `benchmarks.md`.
