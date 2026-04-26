# Project-Specific Instructions (GEMINI.md)

## Code Standards
- **Indentation**: Use **Tabs** exclusively for all code. 
- **Exception**: Use **Spaces (2 or 4)** only for YAML if required by the specification.
- **Formatting**: Always run `make format` and `make lint` before finishing any task to ensure compliance with the project's Ruff configuration.

## Environment & Execution
- **Command Policy**: **ALWAYS** use `make` commands for all operations (running analysis, testing, linting).
- **Prohibited**: Do **NOT** run or suggest direct `uv` or `python3` command calls.
- **API Limits**: The FMP account has a **limited daily call budget**. 
	- **Caching**: 24-hour caching is strictly enforced in `core/fmp_client.py`.
	- **Development**: Do NOT delete `cache/fmp/` unless necessary, as it triggers expensive fresh API calls.

## Data & Architecture
- **Data Fetching Hierarchy**: 
	1. **Financial Modeling Prep (FMP)**: Primary source for all fundamental metrics (P/E, PEG, Financials).
	2. **Yahoo Finance (yfinance)**: Secondary source for real-time pricing and fallback for missing FMP metrics.
- **Evaluation Logic**: `benchmarks.json` defines the scoring parameters (type, target, width, best, worst). Always update this file when adjusting how a metric is interpreted.
- **Investment Profiles**: `profiles.json` defines the relative importance (weights) of metrics for different investor types.

## Testing & Validation
- **Test Suite**: Use `make test` to validate changes. 
- **Data Comparison**: Use `make compare` to manually compare cached data between FMP and Yahoo Finance. This will flag significant discrepancies in valuation and growth metrics.
- **Validation**: When adding or modifying scoring functions in `core/scorers.py`, always verify the output against the expected curve documented in `benchmarks.md`.

