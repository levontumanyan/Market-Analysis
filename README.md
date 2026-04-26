# Market-Analysis

Personal stock market analysis tool. A programmatic financial analysis pipeline integrating quantitative benchmarks with LLM-based qualitative synthesis.

# Quick Start

Run analysis for one or more tickers:
```bash
make run TICKER="AAPL MSFT GOOGL"
```

# Features

- **Multi-Source Data**: Scalable architecture supporting multiple data providers (currently Yahoo Finance).
- **Stock & ETF Support**: Automatically detects asset type and applies relevant benchmarks (e.g., Expense Ratio for ETFs).
- **Bulk Analysis**: Analyze dozens of tickers at once from CLI arguments or external files.
- **Reporting**: Generates condensed terminal summary tables and exports full results to CSV.
- **Investment Profiles**: Tailor scoring weights based on strategy (Balanced, Growth, Dividend).

# Development & Automation

- `make run TICKER="AAPL"`: Run analysis for a single stock.
- `make run TICKER="AAPL MSFT GOOGL"`: Run bulk analysis for multiple stocks (displays a summary table).
- `make run FILE="tickers.txt"`: Load tickers from a text or CSV file.
- `make run TICKER="AAPL MSFT" EXPORT="report.csv"`: Export bulk analysis results to `reports/report.csv` (Horizontal CSV).
- `make run TICKER="AAPL MSFT" EXPORT="report.txt"`: Export bulk analysis results to `reports/report.txt` (Human-readable text).
- `make run INDEX="SPY"`: Analyze components of an index or ETF.
- `make run PROFILE="growth" TICKER="AAPL"`: Run analysis with a specific investment profile.
- `make check`: Run formatting, linting, and all tests in sequence.
- `make test`: Run the test suite (`pytest`).
- `make format`: Automatically fix code formatting and linting issues.
- `make lint`: Check for code style and logical errors.
- `make setup`: Install git pre-commit hooks.

# Configuration

- **Stock Benchmarks**: Defined in `benchmarks_stock.json`.
- **ETF Benchmarks**: Defined in `benchmarks_etf.json`.
- **Investment Profiles**: Defined in `profiles.json`.
- **Reports**: All exported CSV files are saved in the `reports/` directory (ignored by Git).

## Weight Merging Logic

The system uses a hierarchical approach to determine the weight of each metric during evaluation:

1.  **Profile Overrides**: When a profile is selected (e.g., `growth`), the system first looks for the metric's weight in `profiles.json`.
2.  **Benchmark Defaults**: If the metric is not defined in the selected profile, the system falls back to the default weight in the benchmark JSON.
3.  **Global Default**: If no weight is found, it defaults to `1.0`.

# Scoring Methodologies

## Sigmoid Score (`calculate_sigmoid_score`)
Maps a metric to an S-curve, providing a non-linear transition between `best` and `worst`. Diminishing returns on "good" values.

## Linear Score (`calculate_linear_score`)
Calculates a proportional score based on position between two bounds.

## Bell Curve Score (`calculate_bell_score`)
Uses a Gaussian distribution to reward values that cluster around a specific ideal target (e.g., Debt-to-Equity).

## Threshold Score (`calculate_threshold_score`)
A binary pass/fail mechanism (e.g., Dividend Yield > 2%).

# Architecture

- **Core Logic**: Decoupled from data sources using a unified `AssetData` schema.
- **Providers**: Pluggable provider system (`BaseProvider`) for future data source integration (e.g., FMP).
- **Bulk Engine**: Parallel-ready processing logic for high-volume analysis.
- **Indentation**: Strictly uses **Tabs** for all files.

# TODO

- [ ] Add analyst recommendations (buy/sell/hold)
- [ ] Shares short numbers
- [ ] Human company speech to ticker
- [x] Add tests and automated quality checks.
- [x] Support passing multiple tickers to `analyze.py`.
- [x] Implement continuous linear/sigmoid scoring.
- [x] Support ETF/Index analysis.
- [x] Implement bulk reporting and CSV export.
- [ ] Add different sectors for industry comparisons.
- [ ] Add an AI layer for sentiment analysis.
