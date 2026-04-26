import json
from functools import lru_cache
from typing import Any, Dict, List, Optional

from config import BENCHMARKS_PATH

from .providers.yf_provider import YFinanceProvider
from .schema import AssetData


def load_benchmarks(
	path: str = BENCHMARKS_PATH, sector: Optional[str] = None
) -> List[Dict[str, Any]]:
	"""
	Load benchmarks from JSON file.
	Supports both legacy flat list and new sector-aware nested structure.
	"""
	try:
		with open(path, "r") as f:
			data = json.load(f)

		# 1. Determine base benchmarks
		if "benchmarks" in data and isinstance(data["benchmarks"], list):
			# Legacy format
			global_benchmarks = data["benchmarks"]
		else:
			# New sector-aware format
			global_benchmarks = data.get("global", [])

		if not sector:
			return global_benchmarks

		# 2. Apply Sector Overrides if available
		overrides = data.get("sector_overrides", {}).get(sector, {})
		if not overrides:
			return global_benchmarks

		# Apply overrides to global defaults
		final_benchmarks = []
		for b in global_benchmarks:
			metric_key = b.get("metric")
			if metric_key in overrides:
				# Merge the global benchmark with sector-specific overrides
				merged = {**b, **overrides[metric_key]}
				final_benchmarks.append(merged)
			else:
				final_benchmarks.append(b)

		return final_benchmarks

	except Exception as e:
		print(f"[ERROR] Failed to load {path}: {e}")
		return []


@lru_cache(maxsize=100)
def get_stock_data(ticker_symbol: str) -> Optional[AssetData]:
	"""
	Master function:
	Fetches data using the configured providers and returns normalized AssetData.
	"""
	provider = YFinanceProvider()
	return provider.get_data(ticker_symbol.upper())
