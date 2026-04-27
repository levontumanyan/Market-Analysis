from typing import Optional

from core.openbb_client import get_openbb_data
from core.schema import AssetData, AssetType

from .base import BaseProvider


class OpenBBProvider(BaseProvider):
	def get_data(self, symbol: str) -> Optional[AssetData]:
		raw_data = get_openbb_data(symbol)
		if not raw_data or "symbol" not in raw_data:
			return None

		# Determine Asset Type
		# OpenBB 'issue_type' for stocks is often 'cs' (common stock)
		# For ETFs, we can check if it has 'fund_family' or if 'issue_type' is empty
		# But a better way is to see which endpoint returned the data
		# In our combined_data, we can add a 'source_type' flag in get_openbb_data

		# For now, a heuristic:
		asset_type = AssetType.STOCK
		if "fund_family" in raw_data or "nav_price" in raw_data:
			asset_type = AssetType.ETF
		elif raw_data.get("issue_type") == "etf":
			asset_type = AssetType.ETF

		# Mapping Metrics
		# We'll adopt OpenBB standardized keys directly in the benchmarks.
		# So 'metrics' here will just be the raw_data.
		# AssetData.get will handle looking into metrics.

		return AssetData(
			symbol=raw_data.get("symbol", symbol),
			asset_type=asset_type,
			name=raw_data.get("name") or raw_data.get("long_name"),
			sector=raw_data.get("sector"),
			industry=raw_data.get("industry_category"),
			metrics=raw_data,
			raw_data=raw_data,
		)
