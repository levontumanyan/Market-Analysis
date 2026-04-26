import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf


def convert_keys_to_string(data):
	"""Recursively convert dictionary keys to strings, especially for Timestamps."""
	if isinstance(data, dict):
		return {str(k): convert_keys_to_string(v) for k, v in data.items()}
	elif isinstance(data, list):
		return [convert_keys_to_string(i) for i in data]
	return data


def dump_everything(symbol):
	print(f"Fetching everything for {symbol}...")
	ticker = yf.Ticker(symbol)

	data = {}

	# 1. Basic Info
	try:
		data["info"] = ticker.info
	except Exception as e:
		print(f"Error fetching info for {symbol}: {e}")
		data["info"] = {}

	# Helper for DataFrames
	def df_to_dict(df):
		if df is not None and not df.empty:
			return df.to_dict()
		return {}

	# 2. Financials
	print(f"Fetching financials for {symbol}...")
	data["income_stmt"] = df_to_dict(ticker.income_stmt)
	data["balance_sheet"] = df_to_dict(ticker.balance_sheet)
	data["cashflow"] = df_to_dict(ticker.cashflow)

	# 3. Quarterly Financials
	data["quarterly_income_stmt"] = df_to_dict(ticker.quarterly_income_stmt)
	data["quarterly_balance_sheet"] = df_to_dict(ticker.quarterly_balance_sheet)
	data["quarterly_cashflow"] = df_to_dict(ticker.quarterly_cashflow)

	# 4. Holders
	data["major_holders"] = df_to_dict(ticker.major_holders)
	data["institutional_holders"] = df_to_dict(ticker.institutional_holders)

	# 5. Recommendations
	data["recommendations"] = df_to_dict(ticker.recommendations)

	# 6. Analysts & Growth
	data["earnings_estimate"] = df_to_dict(ticker.earnings_estimate)
	data["revenue_estimate"] = df_to_dict(ticker.revenue_estimate)
	data["growth_estimates"] = df_to_dict(ticker.growth_estimates)

	# 7. Sustainability (ESG)
	try:
		data["sustainability"] = df_to_dict(ticker.sustainability)
	except Exception:
		data["sustainability"] = {}

	# 8. Calendar & News
	data["calendar"] = ticker.calendar if ticker.calendar else {}
	data["news"] = ticker.news

	# Clean up keys for JSON (Pandas uses Timestamps as keys)
	print(f"Converting keys for {symbol}...")
	clean_data = convert_keys_to_string(data)

	# Save to file
	output_file = Path(f"dump_{symbol}.json")

	def serializer(obj):
		if isinstance(obj, (pd.Timestamp, datetime)):
			return obj.isoformat()
		return str(obj)

	output_file.write_text(json.dumps(clean_data, indent=2, default=serializer))
	print(f"Done! Check {output_file}")


if __name__ == "__main__":
	dump_everything("AAPL")
	dump_everything("O")
