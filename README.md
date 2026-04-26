# Market-Analysis

Personal stock market analysis tool. A programmatic financial analysis pipeline integrating quantitative benchmarks with extensible scoring methodologies.

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
2.  **Benchmark Defaults**: If the metric is not defined in the selected profile, the system falls back to the default weight in the corresponding benchmark JSON (`benchmarks_stock.json` or `benchmarks_etf.json`).
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

The project follows a modular, functional architecture designed for high testability and scalability.

### Project Structure

- `analyze.py`: CLI entry point.
- `core/`: The engine of the application.
	- `orchestrator.py`: Orchestration of the analysis pipeline, decoupling logic from the CLI.
	- `analysis/`: Specialized logic for index fetching and data preprocessing.
	- `reporting/`: Pluggable reporting system with support for CSV and TXT.
	- `io/`: Input parsers for ticker files.
	- `ui/`: Terminal display and formatting logic.
	- `providers/`: Data acquisition layer with mapping support for multi-source scalability.
	- `schema.py`: Unified data models (`AssetData`).
	- `scorers.py`: Pure mathematical functions for different scoring curves.
	- `evaluation.py`: Core logic for mapping raw data to benchmarked scores.
- `benchmarks_*.json`: Configurable threshold and target values for different asset classes.
- `profiles.json`: Weighting configurations for different investment strategies.

### How to Extend

- **Add a Data Source**: Inherit from `BaseProvider` in `core/providers/` and implement `get_data`. Update `core/data.py` to utilize the new provider.
- **Add a New Metric**: 
	1. Add the field to `AssetData` in `core/schema.py`.
	2. Update the provider to fetch this field.
	3. Add the metric definition to `benchmarks_stock.json` or `benchmarks_etf.json`.
- **Add a Scoring Methodology**: Add a new function to `core/scorers.py`, register it in the `SCORERS` map, and it becomes immediately available for use in the JSON benchmark files.
- **Add a Feature**: Create a new module in `core/` if it represents a new domain (e.g., `core/sentiment.py`). Ensure every new logic component is a standalone, testable function.

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
- [ ] Add an AI layer for LLM-based qualitative synthesis and sentiment analysis.
