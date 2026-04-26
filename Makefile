.PHONY: run lint format test check setup clean

# Run the analysis for one or more tickers
# Usage: make run TICKER="AAPL MSFT GOOGL" [PROFILE="growth"]
PROFILE ?= balanced

run:
	uv run analyze.py $(TICKER) --profile $(PROFILE)

# Run code linting and formatting checks
lint:
	uv run ruff check .
	uv run ruff format --check .

# Automatically fix linting issues and format code
format:
	uv run ruff check --fix .
	uv run ruff format .

# Run tests
test:
	uv run pytest

# Comprehensive check: format, lint, and test
check: format lint test

# Compare data sources from cache
compare:
	uv run python3 scripts/compare_sources.py

# Debug FMP API permissions
debug-fmp:
	uv run python3 scripts/debug_fmp.py

# Setup git hooks
setup:
	cp scripts/setup_hooks.sh .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	echo "Git hooks installed successfully."

# Remove temporary files and the virtual environment
clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
