import json
from functools import lru_cache
from typing import Any, Dict, List

from config import BENCHMARKS_PATH

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
	Fetches Yahoo Finance data (cached 3h).
	"""
	return get_yf_data(ticker_symbol.upper())
