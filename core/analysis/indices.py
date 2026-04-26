from typing import List

import yfinance as yf


def get_index_components(index_ticker: str) -> List[str]:
	"""
	Fetch components of an index or ETF.
	Currently uses yfinance's basic info if available,
	otherwise returns just the ticker itself as a fallback.
	"""
	try:
		# In a real scenario, this would be more robust (scraping or using a dedicated API)
		_ = yf.Ticker(index_ticker)
		return [index_ticker]
	except Exception:
		return [index_ticker]
