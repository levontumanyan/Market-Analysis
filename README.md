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

Benchmarks are defined in `benchmarks.json`. The system uses a **Sigmoid (S-Curve) Scoring Model**:
*   **`best`**: The value that awards ~95% of the weight (points).
*   **`worst`**: The value that awards ~5% of the weight (points).
*   **Midpoint**: The value exactly between `best` and `worst` awards exactly 50% of the weight.
*   This model is non-linear: it is highly sensitive near the center of your range but tapers off at the extremes, allowing for wide ranges without washing out meaningful differences.
## Architecture

**Data Layer**: Python-based ingestion using `yfinance`.
**Logic Layer**: Functional scoring engine against user-defined benchmarks.
**Indentation**: Strictly uses **Tabs** for all files.

## TODO

- [x] Add tests and automated quality checks.
- [x] Support passing multiple tickers to `analyze.py`.
- [x] Implement continuous linear/sigmoid scoring instead of binary pass/fail.
- [x] Add an inside ownership benchmark.
- [x] Add institutional ownership metrics.
- [ ] add dividend in the benchmarks
- [ ] per benchmark function usage
- [ ] Implement scoring profiles (Risky, Conservative, Graham, Buffett, dividend).
- [ ] Add an ETF/mutual fund scanning script.
- [ ] Change in institutional ownerships. [something like this](https://www.nasdaq.com/market-activity/stocks/aapl/institutional-holdings)
- [ ] change in insider ownership
- [ ] add analyst recommendations(buy/sell/hold)
- [ ] add an AI layer, that will analyze news. sentiments.
