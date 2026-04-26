import csv
import os
from typing import List

import yfinance as yf


def parse_ticker_file(file_path: str) -> List[str]:
	"""Parse a .txt or .csv file for ticker symbols."""
	tickers = []
	if not os.path.exists(file_path):
		return []

	ext = os.path.splitext(file_path)[1].lower()
	with open(file_path, "r") as f:
		if ext == ".csv":
			reader = csv.reader(f)
			for row in reader:
				if row:
					tickers.append(row[0].strip().upper())
		else:
			for line in f:
				ticker = line.strip().upper()
				if ticker and not ticker.startswith("#"):
					tickers.append(ticker)
	return tickers


def get_index_components(index_ticker: str) -> List[str]:
	"""
	Fetch components of an index or ETF.
	Currently uses yfinance's basic info if available,
	otherwise returns just the ticker itself as a fallback.
	NOTE: yfinance doesn't easily provide full holdings for all ETFs.
	"""
	# Special handling for common indexes if needed
	# For now, we try to see if it's an ETF and has holdings
	try:
		_ = yf.Ticker(index_ticker)
		# This is a bit of a hack as yf doesn't always expose holdings directly in .info
		# In a real scenario, we might scrape a list or use FMP/other source.
		# For this implementation, we'll return a placeholder or the ticker.
		# If it's '^GSPC' (S&P 500), we could have a hardcoded list or use a library.
		return [index_ticker]
	except Exception:
		return [index_ticker]
