from typing import Optional

from core.schema import AssetData, AssetType
from core.yf_client import get_yf_data

from .base import BaseProvider


class YFinanceProvider(BaseProvider):
	def get_data(self, symbol: str) -> Optional[AssetData]:
		raw_info = get_yf_data(symbol)
		if not raw_info or "symbol" not in raw_info:
			return None

		# Map Asset Type
		quote_type = raw_info.get("quoteType", "EQUITY").upper()
		asset_type = AssetType.UNKNOWN
		if quote_type == "EQUITY":
			asset_type = AssetType.STOCK
		elif quote_type == "ETF":
			asset_type = AssetType.ETF
		elif quote_type == "INDEX":
			asset_type = AssetType.INDEX

		# Map Metrics (using original keys for now to avoid breaking evaluation)
		# In a more advanced version, we'd map 'trailingPE' -> 'pe_ratio'
		# But since evaluation.py uses the keys from benchmarks.json,
		# we keep them as-is in the metrics dict.
		metrics = {
			"trailingPE": raw_info.get("trailingPE"),
			"forwardPE": raw_info.get("forwardPE"),
			"pegRatio": raw_info.get("pegRatio"),
			"priceToBook": raw_info.get("priceToBook"),
			"returnOnEquity": raw_info.get("returnOnEquity"),
			"profitMargins": raw_info.get("profitMargins"),
			"debtToEquity": raw_info.get("debtToEquity"),
			"currentRatio": raw_info.get("currentRatio"),
			"revenueGrowth": raw_info.get("revenueGrowth"),
			"heldPercentInsiders": raw_info.get("heldPercentInsiders"),
			"heldPercentInstitutions": raw_info.get("heldPercentInstitutions"),
			"dividendYield": raw_info.get("dividendYield"),
			"netExpenseRatio": raw_info.get("netExpenseRatio"),
			"beta3Year": raw_info.get("beta3Year"),
			"recommendationMean": raw_info.get("recommendationMean"),
			"recommendationKey": raw_info.get("recommendationKey"),
			"sharesChange1Year": raw_info.get("sharesChange1Year"),
			"sharesChange3Year": raw_info.get("sharesChange3Year"),
		}

		return AssetData(
			symbol=raw_info.get("symbol", symbol),
			asset_type=asset_type,
			name=raw_info.get("longName", raw_info.get("shortName")),
			metrics=metrics,
			raw_data=raw_info,
		)
