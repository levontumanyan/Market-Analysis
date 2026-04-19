import json
import random
import time
from functools import lru_cache
from typing import Any, Dict, List

import pandas as pd
import yfinance as yf

from config import BENCHMARKS_PATH, CACHE_DIR

from .fmp_client import get_fmp_data


def load_benchmarks() -> List[Dict[str, Any]]:
	"""Load benchmarks from JSON file."""
	try:
		with open(BENCHMARKS_PATH, "r") as f:
			data = json.load(f)
			return data.get("benchmarks", [])
	except Exception as e:
		print(f"[ERROR] Failed to load benchmarks.json: {e}")
		return {"profiles": {}, "benchmarks": []}


@lru_cache(maxsize=100)
def get_stock_data(ticker_symbol: str) -> Dict[str, Any]:
	"""Fetch stock data with caching (3 hour for price, 24 hour for FMP)."""
	cache_file = CACHE_DIR / f"{ticker_symbol.upper()}.json"

	# Return cache if fresh (< 3 hour)
	if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < 10800:
		try:
			return json.loads(cache_file.read_text())
		except Exception:
			pass

	# 1. Fetch FMP Data (Primary for Fundamentals)
	fmp_raw = get_fmp_data(ticker_symbol)
	info = {}

	if fmp_raw:
		profile = fmp_raw.get("profile", {})
		metrics = fmp_raw.get("key_metrics", {})
		ratios = fmp_raw.get("ratios", {})
		growth = fmp_raw.get("growth", {})
		quote = fmp_raw.get("quote", {})

		# Map FMP to our internal keys
		info.update(
			{
				"symbol": ticker_symbol.upper(),
				"longName": profile.get("companyName"),
				"currentPrice": quote.get("price") or profile.get("price"),
				"marketCap": quote.get("marketCap") or profile.get("mktCap"),
				"trailingPE": quote.get("pe"),  # Quote often has trailing
				"forwardPE": metrics.get("forwardPeRatio"),
				"pegRatio": metrics.get("pegRatio"),
				"priceToBook": metrics.get("pbRatio"),
				"returnOnEquity": ratios.get("returnOnEquity"),
				"profitMargins": ratios.get("netProfitMargin"),
				"debtToEquity": ratios.get("debtEquityRatio") * 100
				if ratios.get("debtEquityRatio") is not None
				else None,
				"currentRatio": ratios.get("currentRatio"),
				"revenueGrowth": growth.get("revenueGrowth"),
				"dividendYield": quote.get("dividendYield"),
				"sharesChange1Year": growth.get("weightedAverageSharesGrowth"),
				# We'll need a bit more logic for 3Y shares if we want it from FMP,
				# but FMP's 1Y is a good start.
			}
		)

	# 2. Fetch yfinance (Fallback and Supplementary)
	try:
		ticker = yf.Ticker(ticker_symbol)
		yf_info = ticker.info

		# Fill missing values from yfinance
		for key, val in yf_info.items():
			if info.get(key) is None:
				info[key] = val

		# Specialized yfinance logic for shares (if FMP missing or for 3Y)
		if (
			info.get("sharesChange1Year") is None
			or info.get("sharesChange3Year") is None
		):
			latest_shares = info.get("sharesOutstanding")
			shares_full = ticker.get_shares_full()
			if shares_full is not None and not shares_full.empty:
				if latest_shares is None:
					latest_shares = shares_full.iloc[-1]

				# 1Y
				if info.get("sharesChange1Year") is None:
					one_year_ago = shares_full.index[-1] - pd.DateOffset(years=1)
					shares_1y = shares_full.asof(one_year_ago)
					if not pd.isna(shares_1y) and shares_1y > 0:
						info["sharesChange1Year"] = float(
							(latest_shares - shares_1y) / shares_1y
						)

				# 3Y
				if info.get("sharesChange3Year") is None:
					three_years_ago = shares_full.index[-1] - pd.DateOffset(years=3)
					shares_3y = shares_full.asof(three_years_ago)
					if not pd.isna(shares_3y) and shares_3y > 0:
						info["sharesChange3Year"] = float(
							(latest_shares - shares_3y) / shares_3y
						)

	except Exception as e:
		print(f"[DEBUG] yfinance fetch error for {ticker_symbol}: {e}")

	# Save to cache
	try:
		cache_file.parent.mkdir(parents=True, exist_ok=True)
		cache_file.write_text(json.dumps(info, default=str, indent=2))
	except Exception:
		pass

	# Light rate limiting
	time.sleep(random.uniform(0.6, 1.1))

	return info
