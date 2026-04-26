from typing import Any, Dict

# Mapping for Yahoo Finance fields
YF_METRIC_MAP = {
	"trailingPE": "trailingPE",
	"forwardPE": "forwardPE",
	"pegRatio": "pegRatio",
	"priceToBook": "priceToBook",
	"returnOnEquity": "returnOnEquity",
	"profitMargins": "profitMargins",
	"debtToEquity": "debtToEquity",
	"currentRatio": "currentRatio",
	"revenueGrowth": "revenueGrowth",
	"heldPercentInsiders": "heldPercentInsiders",
	"heldPercentInstitutions": "heldPercentInstitutions",
	"dividendYield": "dividendYield",
	"netExpenseRatio": "netExpenseRatio",
	"beta3Year": "beta3Year",
	"recommendationMean": "recommendationMean",
	"recommendationKey": "recommendationKey",
	"sharesChange1Year": "sharesChange1Year",
	"sharesChange3Year": "sharesChange3Year",
	"shortPercentOfFloat": "shortPercentOfFloat",
	"shortRatio": "shortRatio",
	"sharesShort": "sharesShort",
	"enterpriseToEbitda": "enterpriseToEbitda",
	"ebitdaMargins": "ebitdaMargins",
}


def map_provider_data(
	raw_data: Dict[str, Any], mapping: Dict[str, str]
) -> Dict[str, Any]:
	"""
	General purpose mapper from raw provider data to internal metrics.
	"""
	metrics = {}
	for provider_key, internal_key in mapping.items():
		metrics[internal_key] = raw_data.get(provider_key)
	return metrics
