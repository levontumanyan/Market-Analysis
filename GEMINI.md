# Project-Specific Instructions (GEMINI.md)

## Code Standards
- **Indentation**: Use **Tabs** exclusively for all code. 
- **Exception**: Use **Spaces (2 or 4)** only for YAML if required by the specification.
- **Formatting**: Always run `make format` and `make lint` before finishing any task to ensure compliance with the project's Ruff configuration.

## Environment & Execution
- **Environment**: Use `uv` for dependency management and execution.
- **Python Commands**: Always run python scripts using `uv run python3 <script_name>.py`.

## Data & Architecture
- **Data Fetching Hierarchy**: 
	1. **Financial Modeling Prep (FMP)**: Primary source for all fundamental metrics (P/E, PEG, Financials).
	2. **Yahoo Finance (yfinance)**: Secondary source for real-time pricing and fallback for missing FMP metrics.
- **Evaluation Logic**: `benchmarks.json` defines the scoring parameters (type, target, width, best, worst). Always update this file when adjusting how a metric is interpreted.
- **Investment Profiles**: `profiles.json` defines the relative importance (weights) of metrics for different investor types.

## Testing & Validation
- **Test Suite**: `make test` to validate changes. 
- **Validation**: When adding or modifying scoring functions in `core/scorers.py`, always verify the output against the expected curve documented in `benchmarks.md`.
