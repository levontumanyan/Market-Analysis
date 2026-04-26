import json
import random
import time
from typing import Any, Dict

import pandas as pd
import yfinance as yf

from config import CACHE_DIR


def get_yf_data(ticker_symbol: str) -> Dict[str, Any]:
	"""
	Fetch raw yfinance info and handle its own 3-hour caching.
	This ensures we always have a 'pure' yfinance dump.
	"""
	ticker_symbol = ticker_symbol.upper()
	cache_file = CACHE_DIR / f"{ticker_symbol}.json"

	# 1. Return cache if fresh (< 3 hour)
	if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < 10800:
		try:
			return json.loads(cache_file.read_text())
		except Exception:
			pass

	# 2. Fetch fresh data
	try:
		ticker = yf.Ticker(ticker_symbol)
		info = ticker.info

		# Add specialized share logic
		latest_shares = info.get("sharesOutstanding")
		shares_full = ticker.get_shares_full()
		if shares_full is not None and not shares_full.empty:
			if latest_shares is None:
				latest_shares = shares_full.iloc[-1]

			# 1Y Change
			one_year_ago = shares_full.index[-1] - pd.DateOffset(years=1)
			shares_1y = shares_full.asof(one_year_ago)
			if not pd.isna(shares_1y) and shares_1y > 0:
				info["sharesChange1Year"] = float(
					(latest_shares - shares_1y) / shares_1y
				)

			# 3Y Change
			three_years_ago = shares_full.index[-1] - pd.DateOffset(years=3)
			shares_3y = shares_full.asof(three_years_ago)
			if not pd.isna(shares_3y) and shares_3y > 0:
				info["sharesChange3Year"] = float(
					(latest_shares - shares_3y) / shares_3y
				)

		# Save to pure yfinance cache
		CACHE_DIR.mkdir(parents=True, exist_ok=True)
		cache_file.write_text(json.dumps(info, default=str, indent=2))

		# Light rate limiting
		time.sleep(random.uniform(0.6, 1.1))
		return info
	except Exception as e:
		print(f"[DEBUG] yfinance error for {ticker_symbol}: {e}")
		return {}
