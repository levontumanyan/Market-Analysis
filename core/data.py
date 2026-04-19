import json
import random
import time
from functools import lru_cache
from typing import Any, Dict, List

import yfinance as yf

from config import BENCHMARKS_PATH, CACHE_DIR


def load_benchmarks() -> List[Dict[str, Any]]:
	"""Load benchmarks from JSON file."""
	try:
		with open(BENCHMARKS_PATH, "r") as f:
			data = json.load(f)
			return data.get("benchmarks", [])
	except Exception as e:
		print(f"[ERROR] Failed to load benchmarks.json: {e}")
		return []


@lru_cache(maxsize=100)
def get_stock_data(ticker_symbol: str) -> Dict[str, Any]:
	"""Fetch stock data with caching (1 hour)."""
	cache_file = CACHE_DIR / f"{ticker_symbol.upper()}.json"

	# Return cache if fresh (< 1 hour)
	if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < 3600:
		try:
			return json.loads(cache_file.read_text())
		except Exception:
			pass  # Fall through to refetch

	ticker = yf.Ticker(ticker_symbol)
	info = ticker.info

	# Optional: Add more reliable data sources later
	try:
		info["trailingEps"] = (
			ticker.earnings.get("trailingEps")
			if hasattr(ticker, "earnings")
			else info.get("trailingEps")
		)
	except Exception:
		pass

	# Save to cache
	try:
		cache_file.parent.mkdir(parents=True, exist_ok=True)
		cache_file.write_text(json.dumps(info, default=str, indent=2))
	except Exception:
		pass

	# Light rate limiting
	time.sleep(random.uniform(0.6, 1.1))

	return info
