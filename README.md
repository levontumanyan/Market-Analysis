# Market-Analysis

Personal stock market analysis tool. A programmatic financial analysis pipeline integrating quantitative benchmarks with LLM-based qualitative synthesis.

# Quick Start

Run analysis for one or more tickers:
```bash
make run TICKER="AAPL MSFT GOOGL"
```

# Development & Automation

`make run TICKER="XXX YYY"` - Run the analysis script for one or more stocks.
`make run TICKER="AAPL MSFT GOOGL" PROFILE="growth"` - Run and specify a profile.
`make check` - Run formatting, linting, and all tests in sequence.
`make test` - Run the test suite (`pytest`).
`make format` - Automatically fix code formatting.
`make lint` - Check for code style and logical errors.
`make setup` - Install git pre-commit hooks to ensure code quality before every commit.

# Configuration

Benchmarks are defined in `benchmarks.json`.

## Weight Merging Logic

The system uses a hierarchical approach to determine the weight of each metric during evaluation:

1.  **Profile Overrides**: When a profile is selected (e.g., `growth`), the system first looks for the metric's weight in `profiles.json`. If the metric exists in the profile's `weights` dictionary, that value is used.
2.  **Benchmark Defaults**: If the metric is not defined in the selected profile, the system falls back to the `weight` defined in `benchmarks.json` for that specific benchmark.
3.  **Global Default**: If no weight is found in either file, it defaults to `1.0`.

This allows for easy customization: you can define a standard weight for a metric in `benchmarks.json` and only override it in specific profiles where that metric is more or less important.

**Sigmoid (S-Curve) Scoring Model**:

*   **`best`**: The value that awards ~95% of the weight (points).
*   **`worst`**: The value that awards ~5% of the weight (points).
*   **Midpoint**: The value exactly between `best` and `worst` awards exactly 50% of the weight.
*   This model is non-linear: it is highly sensitive near the center of your range but tapers off at the extremes, allowing for wide ranges without washing out meaningful differences.

# Scoring Methodologies

## Sigmoid Score (`calculate_sigmoid_score`)

Maps a metric to an S-curve, providing a non-linear transition between the `best` and `worst` benchmarks. It is designed to reward values approaching the "best" target while aggressively penalizing values as they move toward the "worst" threshold.

**Logic:** Uses a logistic function $f(x) = \frac{1}{1 + e^{k(x - x_0)}}$.
**Midpoint ($x_0$):** Calculated as the arithmetic mean of `best` and `worst`.
**Growth Rate ($k$):** Derived using $\ln(1/19)$ to ensure a 95% score at the `best` value and a 5% score at the `worst` value.
**Use Case:** Metrics where there is a diminishing return on "good" values (e.g., P/E ratios or Revenue Growth).

## Linear Score (`calculate_linear_score`)

Calculates a proportional score based on the value's position between two bounds.

**Logic:**
    * **Higher is Better:** $score = \frac{val - worst}{best - worst}$
    * **Lower is Better:** $score = 1.0 - \frac{val - best}{worst - best}$
**Clamping:** The result is strictly constrained to the $[0.0, 1.0]$ range using `min()` and `max()`.
**Use Case:** Profit margins or simple percentage-based comparisons.

### 3. Bell Curve Score (`calculate_bell_score`)

Utilizes a Gaussian distribution to reward values that cluster around a specific ideal target.

**Logic:** $f(x) = e^{-0.5 \cdot (\frac{val - target}{width})^2}$
**Target:** The peak of the curve (Score = 1.0).
**Width:** Controls the standard deviation (spread) of the curve.
**Use Case:** Debt-to-Equity ratios, where both extreme low leverage and extreme high leverage may indicate inefficiency or risk.

## Threshold Score (`calculate_threshold_score`)

A binary pass/fail mechanism.

* **Logic:** Returns `1.0` if $val \ge threshold$, otherwise `0.0`.
* **Use Case:** Dividend yields or minimum liquidity requirements.

# Architecture

**Data Layer**: Python-based ingestion using `yfinance`.
**Logic Layer**: Functional scoring engine against user-defined benchmarks.
**Indentation**: Strictly uses **Tabs** for all files.

## Profiles

Investment profiles allow you to tailor the analysis to different investment strategies. Each profile assigns different weights to various financial metrics, influencing the scoring.

*   **Balanced**: (Default) A general-purpose profile aiming for a mix of growth and stability.
*   **Growth**: Prioritizes metrics associated with rapid company expansion and future potential.
*   **Dividend**: Focuses on metrics related to dividend payouts, yield, and financial stability for income generation.

You can specify a profile when running the analysis:
```bash
make run TICKER="AAPL MSFT GOOGL" PROFILE="growth"
```

# TODO

- [x] Add tests and automated quality checks.
- [x] Support passing multiple tickers to `analyze.py`.
- [x] Implement continuous linear/sigmoid scoring instead of binary pass/fail.
- [x] Add an inside ownership benchmark.
- [x] Add institutional ownership metrics.
- [x] add dividend in the benchmarks
- [x] per benchmark function usage
- [x] better folder structure and separation.
- [x] make sure if dividend yield is 0 it doesn't show N/A.
- [x] Implement scoring profiles (Risky, Conservative, Graham, Buffett, dividend).
- [ ] shares short numbers
- [ ] add different sectors so that we can potentially have p/e be compared to industry.
- [ ] data about shares outstanding. how many have been created. dilution.
  - [ ] share buyback
- [ ] implement functionality to pass it an etf/index and it checks the stocks inside it and runs scores.
- [ ] Add an ETF/mutual fund scanning script.
- [ ] Change in institutional ownerships. [something like this](https://www.nasdaq.com/market-activity/stocks/aapl/institutional-holdings)
- [ ] change in insider ownership
- [ ] add analyst recommendations(buy/sell/hold)
- [ ] add an AI layer, that will analyze news. sentiments.
- [ ] create a report on a stock. maybe a separate function. the report will show metrics. important ones.
- [ ] Add try/except around individual metric evaluation so one bad metric doesn't kill the whole report.
- [ ] [whalewisdom api](https://whalewisdom.com/stock/nvda)

# Issues

# Technical Observations & Improvements

## ZeroDivisionError in `calculate_linear_score`
If a benchmark is misconfigured such that `best == worst`, the function will trigger a `ZeroDivisionError`.
* **Fix:** Add a check: `if best == worst: return 1.0 if val == best else 0.0`.

## Directionality in `calculate_sigmoid_score`
The current calculation of $k$ assumes $best < worst$ (e.g., P/E ratio). However, your JSON defines **Return on Equity** with `best: 0.25` and `worst: 0.05`.
* **Issue:** The current $k$ derivation may invert the curve or produce unexpected results when `best > worst`.
* **Fix:** Use the absolute difference for the denominator when calculating $k$ and ensure the sign of the exponent correctly reflects whether "best" is the maximum or minimum value.

## Data Cleaning for `yfinance`
The `ticker.info` object often returns `0.0` or `None` for missing fundamental data (especially for P/E ratios in companies with negative earnings). 
* **Issue:** A P/E of `0` might be interpreted by the sigmoid function as "extremely good" (since $0 < 8.0$), whereas it actually represents a lack of earnings.
* **Improvement:** Explicitly check for `val <= 0` on metrics like `trailingPE` or `forwardPE` before scoring.

## Floating Point Precision in JSON
In `calculate_sigmoid_score`, the line `math.log(1 / 19)` is a constant. Calculating this on every function call is inefficient. 
* **Improvement:** Define $k$ as a pre-calculated constant or include it in the benchmark definition to allow for "steeper" or "flatter" S-curves per metric.

## How do you want to handle cases where a company has a "Negative P/E" due to losing money?
