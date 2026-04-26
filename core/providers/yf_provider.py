from typing import Optional

from core.schema import AssetData, AssetType
from core.yf_client import get_yf_data

from .base import BaseProvider
from .mappings import YF_METRIC_MAP, map_provider_data


class YFinanceProvider(BaseProvider):
	def get_data(self, symbol: str) -> Optional[AssetData]:
		raw_info = get_yf_data(symbol)
		if not raw_info or "symbol" not in raw_info:
			return None

		# Map Asset Type
		quote_type = raw_info.get("quoteType", "EQUITY").upper()
		asset_type = self._map_asset_type(quote_type)

		# Map Metrics using the external mapping configuration
		metrics = map_provider_data(raw_info, YF_METRIC_MAP)

		return AssetData(
			symbol=raw_info.get("symbol", symbol),
			asset_type=asset_type,
			name=raw_info.get("longName", raw_info.get("shortName")),
			metrics=metrics,
			raw_data=raw_info,
		)

	def _map_asset_type(self, quote_type: str) -> AssetType:
		if quote_type == "EQUITY":
			return AssetType.STOCK
		elif quote_type == "ETF":
			return AssetType.ETF
		elif quote_type == "INDEX":
			return AssetType.INDEX
		return AssetType.UNKNOWN
