from typing import List

import pandas as pd
import yfinance as yf

from .constituents import get_constituents


def get_index_components(index_ticker: str) -> List[str]:
	"""
	Fetch components of an index or ETF.
	1. Checks if it's a major index (SP500, NASDAQ100, DOW) for full lists.
	2. Falls back to yfinance funds_data (Top 10) for other ETFs.
	Returns a list of ticker symbols.
	"""
	index_ticker = index_ticker.upper().strip()

	# 1. Try major index full constituent fetching
	mapping = {
		"SP500": "sp500",
		"S&P500": "sp500",
		"NASDAQ100": "nasdaq100",
		"NDX100": "nasdaq100",
		"DOW": "dow",
		"DJIA": "dow",
	}

	if index_ticker in mapping:
		full_list = get_constituents(mapping[index_ticker])
		if full_list:
			return full_list

	# 2. Fallback to yfinance top holdings for ETFs
	try:
		ticker = yf.Ticker(index_ticker)
		funds_data = ticker.funds_data

		if funds_data is not None:
			top_holdings = funds_data.top_holdings
			if isinstance(top_holdings, pd.DataFrame) and not top_holdings.empty:
				symbols = top_holdings.index.tolist()
				valid_symbols = [
					str(s).upper() for s in symbols if s and isinstance(s, str)
				]
				if valid_symbols:
					return valid_symbols

		# Fallback to the ticker itself if no holdings are found
		return [index_ticker]
	except Exception:
		return [index_ticker]
