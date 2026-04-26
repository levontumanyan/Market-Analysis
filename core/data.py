import json
from functools import lru_cache
from typing import Any, Dict, List

from config import BENCHMARKS_PATH

from .fmp_client import get_fmp_data
from .yf_client import get_yf_data


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
	"""
	Master function:
	1. Loads/Fetches FMP (cached 24h)
	2. Loads/Fetches Yahoo Finance (cached 3h)
	3. Merges them with FMP as primary.
	"""
	ticker_symbol = ticker_symbol.upper()

	# 1. Get raw sources from their respective clients
	fmp_raw = get_fmp_data(ticker_symbol)
	yf_raw = get_yf_data(ticker_symbol)

	merged_info = {}

	# 2. Map FMP data first (Primary source for fundamentals)
	if fmp_raw:
		profile = fmp_raw.get("profile", {})
		metrics = fmp_raw.get("key_metrics", {})
		ratios = fmp_raw.get("ratios", {})

		merged_info.update(
			{
				"symbol": ticker_symbol,
				"longName": profile.get("companyName"),
				"currentPrice": profile.get("price"),
				"marketCap": profile.get("mktCap"),
				"trailingPE": profile.get("pe"),
				"forwardPE": metrics.get("forwardPeRatio"),
				"pegRatio": metrics.get("pegRatio"),
				"priceToBook": metrics.get("pbRatio"),
				"returnOnEquity": ratios.get("returnOnEquity"),
				"profitMargins": ratios.get("netProfitMargin"),
				"debtToEquity": (
					ratios.get("debtEquityRatio") * 100
					if ratios.get("debtEquityRatio") is not None
					else None
				),
				"currentRatio": ratios.get("currentRatio"),
				"revenueGrowth": metrics.get("revenueGrowthRatio"),
				"dividendYield": metrics.get("dividendYield"),
				"sharesChange1Year": metrics.get(
					"netIncomeGrowth"
				),  # Placeholder growth
			}
		)

	# 3. Layer in Yahoo Finance (Secondary source / Fallback)
	# This fills in missing fields and adds specialized YF fields like sharesChange3Year
	for key, val in yf_raw.items():
		if merged_info.get(key) is None:
			merged_info[key] = val

	return merged_info
