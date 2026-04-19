import json
import time
from typing import Any, Dict

import requests

from config import FMP_API_KEY, FMP_CACHE_DIR

BASE_URL = "https://financialmodelingprep.com/api/v3"


def get_fmp_data(ticker: str) -> Dict[str, Any]:
	"""
	Fetch comprehensive data from FMP for a given ticker.
	Uses a 24-hour caching layer.
	"""
	ticker = ticker.upper()
	cache_file = FMP_CACHE_DIR / f"{ticker}.json"

	# 1. Check Cache (24 hours = 86400 seconds)
	if cache_file.exists():
		mtime = cache_file.stat().st_mtime
		if (time.time() - mtime) < 86400:
			try:
				return json.loads(cache_file.read_text())
			except Exception:
				pass

	# 2. Fetch fresh data if cache is expired or missing
	if not FMP_API_KEY:
		print("[WARNING] FMP_API_KEY not found in environment. Skipping FMP data.")
		return {}

	data = {}

	# Endpoints we need for fundamentals
	endpoints = {
		"profile": f"{BASE_URL}/profile/{ticker}",
		"key_metrics": f"{BASE_URL}/key-metrics/{ticker}?period=annual&limit=1",
		"ratios": f"{BASE_URL}/ratios/{ticker}?period=annual&limit=1",
		"growth": f"{BASE_URL}/financial-growth/{ticker}?period=annual&limit=1",
		"quote": f"{BASE_URL}/quote/{ticker}",
	}

	try:
		for key, url in endpoints.items():
			response = requests.get(
				f"{url}&apikey={FMP_API_KEY}"
				if "?" in url
				else f"{url}?apikey={FMP_API_KEY}"
			)
			if response.status_code == 200:
				res_json = response.json()
				if res_json and isinstance(res_json, list):
					data[key] = res_json[0]
				elif res_json:
					data[key] = res_json
			else:
				print(f"[ERROR] FMP API error for {key}: {response.status_code}")

		# 3. Save to Cache
		if data:
			FMP_CACHE_DIR.mkdir(parents=True, exist_ok=True)
			cache_file.write_text(json.dumps(data, indent=2))

	except Exception as e:
		print(f"[ERROR] Failed to fetch FMP data for {ticker}: {e}")

	return data
