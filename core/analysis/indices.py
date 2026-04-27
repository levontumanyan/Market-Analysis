from typing import List

import pandas as pd
import yfinance as yf  # Keep as fallback for free ETF holdings until OpenBB supports it keyless


def get_index_components(index_ticker: str) -> List[str]:
	"""
	Fetch components of an index or ETF.
	Currently uses yfinance directly as a fallback because OpenBB
	requires API keys (FMP/Intrinio) for holdings data.
	"""
	index_ticker = index_ticker.upper()
	try:
		ticker = yf.Ticker(index_ticker)
		funds_data = ticker.funds_data

		if funds_data is not None:
			top_holdings = funds_data.top_holdings
			if isinstance(top_holdings, pd.DataFrame) and not top_holdings.empty:
				# The symbols are stored in the DataFrame index
				symbols = top_holdings.index.tolist()
				# Ensure we only return valid non-empty strings
				valid_symbols = [s for s in symbols if s and isinstance(s, str)]
				if valid_symbols:
					return valid_symbols

		# Fallback to the ticker itself if no holdings are found
		return [index_ticker]
	except Exception:
		# Fallback to the ticker itself if any error occurs (e.g., indices like ^GSPC)
		return [index_ticker]
