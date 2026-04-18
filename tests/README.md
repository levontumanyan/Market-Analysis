# Test Suite

This directory contains the automated tests for the Market Analysis project. We use `pytest` for testing and `unittest.mock` to ensure tests are fast and reliable.

## Directory Structure

*   **`conftest.py`**: Shared test configuration. It automatically adds the project root to the Python path so that tests can import `analyze.py` without environment hacks.
*   **`test_analysis.py`**: Unit tests for the core logic.
    *   `test_evaluate_metric_pass/fail`: Verifies that stock metrics are correctly scored against thresholds.
    *   `test_evaluate_metric_na`: Ensures missing data from Yahoo Finance doesn't crash the script.
    *   `test_evaluate_metric_percentage`: Verifies that percentage-based metrics are formatted correctly.
    *   `test_load_benchmarks`: Verifies that the JSON configuration is loaded and parsed correctly.

## Best Practices

1.  **Mocking**: Never call real APIs in unit tests. Use `mocker` (from `pytest-mock`) to simulate data from `yfinance`.
2.  **Tabs**: All test files must follow the project rule of using **Tabs** for indentation.
3.  **Isolation**: Each test should be independent and not rely on the state of other tests.

## Running Tests

To run all tests:
```bash
make test
```

To run with coverage (if installed):
```bash
uv run pytest --cov=.
```
