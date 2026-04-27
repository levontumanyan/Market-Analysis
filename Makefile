.PHONY: run lint format test check setup clean

# Run the analysis for one or more tickers
# Usage: make run TICKER="AAPL MSFT" PROFILE="growth" EXPORT="report.csv"
PROFILE ?= balanced
TICKER ?=
FILE ?=
EXPORT ?=
INDEX ?=

run:
	@uv run analyze.py $(TICKER) \
		$(if $(FILE),--file $(FILE)) \
		$(if $(EXPORT),--export $(EXPORT)) \
		$(if $(INDEX),--index $(INDEX)) \
		--profile $(PROFILE)

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

# Run tests with coverage report
coverage:
	uv run pytest --cov=core --cov-report=term-missing

# Comprehensive check: format, lint, and test
check: format lint test coverage

# Setup git hooks
setup:
	cp scripts/setup_hooks.sh .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Git hooks installed successfully."

# Remove temporary files and the virtual environment
clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
