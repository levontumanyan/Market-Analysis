# Market-Analysis

Personal stock market analysis tool. A programmatic financial analysis pipeline integrating quantitative benchmarks with LLM-based qualitative synthesis.

## Quick Start

Run analysis for a specific ticker:
```bash
make run TICKER=AAPL
```

## Development & Automation

`make run TICKER=XXX` - Run the analysis script for a specific stock.
`make check` - Run formatting, linting, and all tests in sequence.
`make test` - Run the test suite (`pytest`).
`make format` - Automatically fix code formatting.
`make lint` - Check for code style and logical errors.
`make setup` - Install git pre-commit hooks to ensure code quality before every commit.

## Configuration

Benchmarks are defined in `benchmarks.json`. You can modify thresholds (min/max), weights, and metrics without changing the code.

## Architecture

**Data Layer**: Python-based ingestion using `yfinance`.
**Logic Layer**: Functional scoring engine against user-defined benchmarks.

## TODO

- [x] Add tests and automated quality checks.
- [ ] Add a script to parse multiple stocks and filter by pass percentage.
- [ ] Implement scoring profiles (Risky, Conservative, Graham, Buffett).
- [ ] Support passing multiple tickers to `analyze.py`.
