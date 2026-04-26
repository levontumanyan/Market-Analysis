import json
from functools import lru_cache
from typing import Any, Dict, List, Optional

from config import BENCHMARKS_PATH

from .providers.yf_provider import YFinanceProvider
from .schema import AssetData


def load_benchmarks(path: str = BENCHMARKS_PATH) -> List[Dict[str, Any]]:
	"""Load benchmarks from JSON file."""
	try:
		with open(path, "r") as f:
			data = json.load(f)
			return data.get("benchmarks", [])
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
