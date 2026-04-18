# Market-Analysis

Personal stock market analysis tool. A programmatic financial analysis pipeline integrating quantitative benchmarks with LLM-based qualitative synthesis.

## Quick Start

Run analysis for one or more tickers:
```bash
make run TICKER="AAPL MSFT GOOGL"
```

## Development & Automation

`make run TICKER="XXX YYY"` - Run the analysis script for one or more stocks.
`make check` - Run formatting, linting, and all tests in sequence.
`make test` - Run the test suite (`pytest`).
`make format` - Automatically fix code formatting.
`make lint` - Check for code style and logical errors.
`make setup` - Install git pre-commit hooks to ensure code quality before every commit.

## Configuration

Benchmarks are defined in `benchmarks.json`. The system uses a **Linear Scoring Model**:
*   **`best`**: The value that awards 100% of the weight (points).
*   **`worst`**: The value that awards 0% of the weight (points).
*   Values in between receive a proportional score (e.g., halfway between best and worst awards 50% points).
*   The script automatically detects directionality:
		*   If `best < worst`, it assumes **Lower is Better** (e.g., P/E ratio).
		*   If `best > worst`, it assumes **Higher is Better** (e.g., Profit Margin).

## Architecture

**Data Layer**: Python-based ingestion using `yfinance`.
**Logic Layer**: Functional scoring engine against user-defined benchmarks.
**Indentation**: Strictly uses **Tabs** for all files.

## TODO

- [x] Add tests and automated quality checks.
- [x] Support passing multiple tickers to `analyze.py`.
- [ ] better benchmarking. more continuous instead of pass fail. so that if let's say p/e is 20 that is better than 55. instead of 55 just failing it adds a lower score than a stock with lower p/e.
- [ ] Implement scoring profiles (Risky, Conservative, Graham, Buffett).
- [ ] add an ETF/mutual fund scanning script.
