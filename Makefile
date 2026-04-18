.PHONY: run lint format test clean

# Run the analysis for a specific ticker
# Usage: make run TICKER=MSFT
run:
	uv run analyze.py $(TICKER)

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

# Setup git hooks
setup:
	cp scripts/setup_hooks.sh .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	echo "Git hooks installed successfully."

# Remove temporary files and the virtual environment
clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
