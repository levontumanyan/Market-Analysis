import csv
import os
from typing import List


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
