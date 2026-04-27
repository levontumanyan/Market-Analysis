import json
from functools import lru_cache
from typing import Any, Dict, List, Optional

from core.database.repository import DatabaseRepository

from .providers.openbb_provider import OpenBBProvider
from .schema import AssetData


def load_benchmarks(
	path: str, sector: Optional[str] = None, repo: Optional[DatabaseRepository] = None
) -> List[Dict[str, Any]]:
	"""
	Load benchmarks from a specific path and optionally apply sector overrides from the DB.
	"""
	try:
		with open(path, "r") as f:
			global_benchmarks = json.load(f)

		if not sector or not repo:
			return global_benchmarks

		# Apply Sector Overrides from the database
		db_overrides = repo.get_sector_benchmarks(sector)
		if not db_overrides:
			return global_benchmarks

		# Convert DB format back to the dictionary format expected by the merge logic
		# DB rows: {'metric_key': 'pe_ratio', 'benchmark_type': 'best_worst', 'value_a': 25.0, 'value_b': 60.0}
		overrides = {}
		for row in db_overrides:
			m_key = row["metric_key"]
			b_type = row["benchmark_type"]
			if b_type == "best_worst":
				overrides[m_key] = {"best": row["value_a"], "worst": row["value_b"]}
			elif b_type == "target_width":
				overrides[m_key] = {"target": row["value_a"], "width": row["value_b"]}

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
