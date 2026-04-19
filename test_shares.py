import pandas as pd
import yfinance as yf


def test_shares(symbol):
	ticker = yf.Ticker(symbol)
	print(f"--- {symbol} ---")
	shares = ticker.get_shares_full()
	if shares is not None and not shares.empty:
		print(shares.tail())
		# Calculate 1 year change if possible
		latest = shares.iloc[-1]
		# find value from approx 1 year ago
		one_year_ago = shares.index[-1] - pd.DateOffset(years=1)
		# get the value closest to one year ago
		shares_one_year_ago = shares.asof(one_year_ago)
		if pd.isna(shares_one_year_ago):
			# if asof fails, just try to find the earliest in that year or something
			shares_one_year_ago = shares.iloc[0]  # fallback

		change = (latest - shares_one_year_ago) / shares_one_year_ago
		print(f"1 Year Change: {change:.2%}")
	else:
		print("No historical shares data found.")


if __name__ == "__main__":
	test_shares("AAPL")
	test_shares("TSLA")
	test_shares("NVDA")
