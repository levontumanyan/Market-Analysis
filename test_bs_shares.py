import yfinance as yf


def test_other_shares(symbol):
	ticker = yf.Ticker(symbol)
	print(f"--- {symbol} ---")
	print("\nticker.balance_sheet['Ordinary Shares Number']:")
	try:
		bs = ticker.balance_sheet
		if "Ordinary Shares Number" in bs.index:
			print(bs.loc["Ordinary Shares Number"])
		else:
			print("Ordinary Shares Number not found in balance sheet")
			print("Available index:")
			print(bs.index)
	except Exception as e:
		print(f"Error fetching balance sheet: {e}")


if __name__ == "__main__":
	test_other_shares("AAPL")
