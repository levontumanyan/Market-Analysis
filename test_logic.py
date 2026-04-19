import pandas as pd
import yfinance as yf


def test_logic(ticker_symbol):
	ticker = yf.Ticker(ticker_symbol)
	info = ticker.info
	try:
		shares = ticker.get_shares_full()
		if shares is not None and not shares.empty:
			print("--- Shares Full Data ---")
			print(shares)
			print("------------------------")
			latest_shares = shares.iloc[-1]
			print(f"Latest shares: {latest_shares}")

			# 1 Year Change
			one_year_ago = shares.index[-1] - pd.DateOffset(years=1)
			shares_1y = shares.asof(one_year_ago)
			print(f"Shares 1y ago: {shares_1y}")
			if not pd.isna(shares_1y):
				info["sharesChange1Year"] = float(
					(latest_shares - shares_1y) / shares_1y
				)
				print(f"sharesChange1Year: {info['sharesChange1Year']}")

			# 3 Year Change
			three_years_ago = shares.index[-1] - pd.DateOffset(years=3)
			shares_3y = shares.asof(three_years_ago)
			print(f"Shares 3y ago: {shares_3y}")
			if not pd.isna(shares_3y):
				info["sharesChange3Year"] = float(
					(latest_shares - shares_3y) / shares_3y
				)
				print(f"sharesChange3Year: {info['sharesChange3Year']}")
		else:
			print(f"[DEBUG] No shares data for {ticker_symbol}")
	except Exception as e:
		print(f"[DEBUG] Error fetching shares for {ticker_symbol}: {e}")


if __name__ == "__main__":
	test_logic("AAPL")
