import json
from functools import lru_cache
from typing import Any, Dict, List, Optional

from config import SECTORS_PATH

from .providers.openbb_provider import OpenBBProvider
from .schema import AssetData


def load_benchmarks(path: str, sector: Optional[str] = None) -> List[Dict[str, Any]]:
	"""
	Load benchmarks from a specific path and optionally apply sector overrides.
	"""
	try:
		with open(path, "r") as f:
			global_benchmarks = json.load(f)

		if not sector:
			return global_benchmarks

		# Apply Sector Overrides from the dedicated sectors file
		try:
			with open(SECTORS_PATH, "r") as f:
				all_overrides = json.load(f)
				overrides = all_overrides.get(sector, {})
		except (FileNotFoundError, json.JSONDecodeError):
			overrides = {}

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
		print(f"[ERROR] Failed to load benchmarks from {path}: {e}")
		return []


@lru_cache(maxsize=100)
def get_stock_data(ticker_symbol: str) -> Optional[AssetData]:
	"""
	Master function:
	Fetches data using the configured providers and returns normalized AssetData.
	"""
	provider = OpenBBProvider()
	return provider.get_data(ticker_symbol.upper())
