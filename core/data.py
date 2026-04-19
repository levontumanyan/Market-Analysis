import json
import random
import time
from functools import lru_cache
from typing import Any, Dict, List

import pandas as pd
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
		return {"profiles": {}, "benchmarks": []}


@lru_cache(maxsize=100)
def get_stock_data(ticker_symbol: str) -> Dict[str, Any]:
	"""Fetch stock data with caching (3 hour)."""
	cache_file = CACHE_DIR / f"{ticker_symbol.upper()}.json"

	# Return cache if fresh (< 3 hour)
	if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < 10800:
		try:
			return json.loads(cache_file.read_text())
		except Exception:
			pass

	ticker = yf.Ticker(ticker_symbol)
	info = ticker.info

	# Add shares outstanding change data
	try:
		latest_shares = info.get("sharesOutstanding")
		
		# Try to get 1 year change
		shares_full = ticker.get_shares_full()
		if shares_full is not None and not shares_full.empty:
			if latest_shares is None:
				latest_shares = shares_full.iloc[-1]
			
			one_year_ago = shares_full.index[-1] - pd.DateOffset(years=1)
			shares_1y = shares_full.asof(one_year_ago)
			if not pd.isna(shares_1y) and shares_1y > 0:
				info["sharesChange1Year"] = float((latest_shares - shares_1y) / shares_1y)

		# Try to get 3 year change (fallback to balance sheet for longer history)
		bs = ticker.balance_sheet
		if "Ordinary Shares Number" in bs.index:
			shares_series = bs.loc["Ordinary Shares Number"].dropna()
			if not shares_series.empty:
				# shares_series is usually sorted newest to oldest
				current_bs_shares = shares_series.iloc[0]
				print(f"[DEBUG] BS shares series length: {len(shares_series)}")
				
				# If we don't have 1y change yet, try from BS
				if "sharesChange1Year" not in info and len(shares_series) > 1:
					prev_1y = shares_series.iloc[1]
					if prev_1y > 0:
						info["sharesChange1Year"] = float((current_bs_shares - prev_1y) / prev_1y)
				
				# 3 year change from BS
				if len(shares_series) > 3:
					prev_3y = shares_series.iloc[3]
					print(f"[DEBUG] prev_3y: {prev_3y}")
					if prev_3y > 0:
						info["sharesChange3Year"] = float((current_bs_shares - prev_3y) / prev_3y)
						print(f"[DEBUG] sharesChange3Year: {info['sharesChange3Year']}")
				elif len(shares_series) > 1:
					# Fallback to whatever oldest we have if less than 3 years but more than 1
					oldest = shares_series.iloc[-1]
					if oldest > 0 and current_bs_shares != oldest:
						info["sharesChange3Year"] = float((current_bs_shares - oldest) / oldest)
		else:
			print("[DEBUG] 'Ordinary Shares Number' not in BS index")

	except Exception as e:
		print(f"[DEBUG] Share calculation error: {e}")

	# Save to cache
	try:
		cache_file.parent.mkdir(parents=True, exist_ok=True)
		cache_file.write_text(json.dumps(info, default=str, indent=2))
	except Exception:
		pass

	# Light rate limiting
	time.sleep(random.uniform(0.6, 1.1))

	return info
