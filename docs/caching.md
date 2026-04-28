# Intelligent Caching Logic

To optimize API usage and ensure data consistency, this project implements a market-aware caching strategy.

## How it Works

The caching logic is located in `core/openbb_client.py` and uses utility functions from `core/utils/market.py`.

### 1. Freshness Check (Market Open)
During active market hours, the cache is considered fresh if it is less than **3 hours old**. This allows for periodic updates during the trading day while minimizing redundant API calls.

### 2. Post-Close Persistence (Market Closed)
When the market is closed, the script optimizes for persistence. If a cache file exists and its modification time is **after the most recent market close**, it is considered valid until the next market open, regardless of the 3-hour limit.

**Example:**
*   Market closes at 4:00 PM ET.
*   You run an analysis at 5:00 PM ET (API call made, cache saved).
*   You run the same analysis at 11:00 PM ET. Even though the cache is 6 hours old, the script identifies that the market has been closed since the data was last fetched and will reuse the cache.

## Timezone & Machine Agnosticism
*   **Timezone:** All internal calculations use **UTC**.
*   **Market Hours:** Hardcoded to **NYSE/NASDAQ** (9:30 AM - 4:00 PM Eastern Time).
*   **DST:** Automatically handled via Python's `zoneinfo` module (`America/New_York`).

## Logging
The script logs its caching decisions:
*   `Cache hit for [TICKER]`: Standard 3-hour cache hit.
*   `Market closed; using post-close cache for [TICKER]`: Intelligent post-close hit.
